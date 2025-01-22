import logging
import warnings
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    TypedDict,
)

import requests
from urllib3.util import retry

from databricks import version
from databricks.agents.utils.mlflow_utils import get_workspace_url
from databricks.rag_eval import entities, env_vars, schemas, session
from databricks.rag_eval.clients import databricks_api_client
from databricks.rag_eval.monitoring import rest_entities
from databricks.rag_eval.utils import (
    NO_CHANGE,
    collection_utils,
    input_output_utils,
    request_utils,
)

SESSION_ID_HEADER = "managed-evals-session-id"
CLIENT_VERSION_HEADER = "managed-evals-client-version"
SYNTHETIC_GENERATION_NUM_DOCS_HEADER = "managed-evals-synthetic-generation-num-docs"
SYNTHETIC_GENERATION_NUM_EVALS_HEADER = "managed-evals-synthetic-generation-num-evals"
USE_NOTEBOOK_CLUSTER_ID = False
# When using batch endpoints, limit batches to this size, in bytes
# Technically 1MB = 1048576 bytes, but we leave 48kB for overhead of HTTP headers/other json fluff.
_BATCH_SIZE_LIMIT = 1_000_000
# When using batch endpoints, limit batches to this number of rows.
# The service has a hard limit at 2K nodes updated per request; sometimes 1 row is more than 1 node.
_BATCH_QUANTITY_LIMIT = 100

TagType = TypedDict("TagType", {"tag_name": str, "tag_id": str})

_logger = logging.getLogger(__name__)


def get_default_retry_config():
    return retry.Retry(
        total=env_vars.AGENT_EVAL_GENERATE_EVALS_MAX_RETRIES.get(),
        backoff_factor=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_FACTOR.get(),
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_jitter=env_vars.AGENT_EVAL_GENERATE_EVALS_BACKOFF_JITTER.get(),
        allowed_methods=frozenset(
            ["GET", "POST"]
        ),  # by default, it doesn't retry on POST
    )


def get_batch_edit_retry_config():
    return retry.Retry(
        total=3,
        backoff_factor=10,  # Retry after 0, 10, 20, 40... seconds.
        status_forcelist=[
            429
        ],  # Adding lots of evals in a row can result in rate limiting errors
        allowed_methods=["POST"],  # POST not retried by default
    )


def _raise_for_status(resp: requests.Response) -> None:
    """
    Raise an Exception if the response is an error.
    Custom error message is extracted from the response JSON.
    """
    if resp.status_code == requests.codes.ok:
        return
    http_error_msg = ""
    if 400 <= resp.status_code < 500:
        http_error_msg = (
            f"{resp.status_code} Client Error: {resp.reason}\n{resp.text}. "
        )
    elif 500 <= resp.status_code < 600:
        http_error_msg = (
            f"{resp.status_code} Server Error: {resp.reason}\n{resp.text}. "
        )
    raise requests.HTTPError(http_error_msg, response=resp)


def _get_default_headers() -> Dict[str, str]:
    """
    Constructs the default request headers.
    """
    headers = {
        CLIENT_VERSION_HEADER: version.VERSION,
    }

    return request_utils.add_traffic_id_header(headers)


def _get_synthesis_headers() -> Dict[str, str]:
    """
    Constructs the request headers for synthetic generation.
    """
    eval_session = session.current_session()
    if eval_session is None:
        return {}
    return request_utils.add_traffic_id_header(
        {
            CLIENT_VERSION_HEADER: version.VERSION,
            SESSION_ID_HEADER: eval_session.session_id,
            SYNTHETIC_GENERATION_NUM_DOCS_HEADER: str(
                eval_session.synthetic_generation_num_docs
            ),
            SYNTHETIC_GENERATION_NUM_EVALS_HEADER: str(
                eval_session.synthetic_generation_num_evals
            ),
        }
    )


class ManagedEvalsClient(databricks_api_client.DatabricksAPIClient):
    """
    Client to interact with the managed-evals service.
    """

    def __init__(self):
        super().__init__(version="2.0")

    # override from DatabricksAPIClient
    def get_default_request_session(self, *args, **kwargs):
        session = super().get_default_request_session(*args, **kwargs)
        if USE_NOTEBOOK_CLUSTER_ID:
            from pyspark.sql import SparkSession

            spark = SparkSession.builder.getOrCreate()
            cluster_id = spark.conf.get("spark.databricks.clusterUsageTags.clusterId")
            session.params = {"compute_cluster_id": cluster_id}
        return session

    def gracefully_batch_post(
        self,
        url: str,
        all_items: Sequence[Any],
        request_body_create: Callable[[Iterable[Any]], Any],
        response_body_read: Callable[[Any], Iterable[Any]],
    ):
        with self.get_default_request_session(
            headers=_get_default_headers(),
            retry_config=get_batch_edit_retry_config(),
        ) as session:
            return_values = []
            for batch in collection_utils.safe_batch(
                all_items,
                batch_byte_limit=_BATCH_SIZE_LIMIT,
                batch_quantity_limit=_BATCH_QUANTITY_LIMIT,
            ):
                request_body = request_body_create(batch)

                response = session.post(url=url, json=request_body)
                try:
                    _raise_for_status(response)
                except requests.HTTPError as e:
                    _logger.error(
                        f"Created {len(return_values)}/{len(all_items)} items before encountering an error.\n"
                        f"Returning successfully created items; please take care to avoid double-creating objects.\n{e}"
                    )
                    return return_values
                return_values.extend(response_body_read(response))
            return return_values

    def generate_questions(
        self,
        *,
        doc: entities.Document,
        num_questions: int,
        agent_description: Optional[str],
        question_guidelines: Optional[str],
    ) -> List[entities.SyntheticQuestion]:
        """
        Generate synthetic questions for the given document.
        """
        request_json = {
            "doc_content": doc.content,
            "num_questions": num_questions,
            "agent_description": agent_description,
            "question_guidelines": question_guidelines,
        }
        with self.get_default_request_session(
            get_default_retry_config(),
            headers=_get_synthesis_headers(),
        ) as session:
            resp = session.post(
                url=self.get_method_url("/managed-evals/generate-questions"),
                json=request_json,
            )

        _raise_for_status(resp)

        response_json = resp.json()
        if "questions_with_context" not in response_json or "error" in response_json:
            raise ValueError(f"Invalid response: {response_json}")
        return [
            entities.SyntheticQuestion(
                question=question_with_context["question"],
                source_doc_uri=doc.doc_uri,
                source_context=question_with_context["context"],
            )
            for question_with_context in response_json["questions_with_context"]
        ]

    def generate_answer(
        self,
        *,
        question: entities.SyntheticQuestion,
        answer_types: Collection[entities.SyntheticAnswerType],
    ) -> entities.SyntheticAnswer:
        """
        Generate synthetic answer for the given question.
        """
        request_json = {
            "question": question.question,
            "context": question.source_context,
            "answer_types": [str(answer_type) for answer_type in answer_types],
        }

        with self.get_default_request_session(
            get_default_retry_config(),
            headers=_get_synthesis_headers(),
        ) as session:
            resp = session.post(
                url=self.get_method_url("/managed-evals/generate-answer"),
                json=request_json,
            )

        _raise_for_status(resp)

        response_json = resp.json()
        return entities.SyntheticAnswer(
            question=question,
            synthetic_ground_truth=response_json.get("synthetic_ground_truth"),
            synthetic_grading_notes=response_json.get("synthetic_grading_notes"),
            synthetic_minimal_facts=response_json.get("synthetic_minimal_facts"),
        )

    def create_managed_evals_instance(
        self,
        *,
        instance_id: str,
        agent_name: Optional[str] = None,
        agent_serving_endpoint: Optional[str] = None,
        experiment_ids: Optional[Iterable[str]] = None,
    ) -> entities.EvalsInstance:
        """
        Creates a new Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.
            agent_name: (optional) The name of the agent.
            agent_serving_endpoint: (optional) The name of the model serving endpoint that serves the agent.
            experiment_ids: (optional) The experiment IDs to associate with the instance.

        Returns:
            The created EvalsInstance.
        """
        evals_instance = entities.EvalsInstance(
            agent_name=agent_name,
            agent_serving_endpoint=agent_serving_endpoint,
            experiment_ids=experiment_ids if experiment_ids is not None else [],
        )
        request_body = {"instance": evals_instance.to_json()}
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(f"/managed-evals/instances/{instance_id}"),
                json=request_body,
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def delete_managed_evals_instance(self, instance_id: str) -> None:
        """
        Deletes a Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.
        """
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.delete(
                url=self.get_method_url(f"/managed-evals/instances/{instance_id}"),
            )
        _raise_for_status(response)

    def update_managed_evals_instance(
        self,
        *,
        instance_id: str,
        agent_name: Optional[str] = NO_CHANGE,
        agent_serving_endpoint: Optional[str] = NO_CHANGE,
        experiment_ids: List[str] = NO_CHANGE,
    ) -> entities.EvalsInstance:
        """
        Updates a Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.
            agent_name: (optional) The name of the agent.
            agent_serving_endpoint: (optional) The name of the model serving endpoint that serves the agent.
            experiment_ids: (optional) The experiment IDs to associate with the instance.

        Returns:
            The updated EvalsInstance.
        """
        evals_instance = entities.EvalsInstance(
            agent_name=agent_name,
            agent_serving_endpoint=agent_serving_endpoint,
            experiment_ids=experiment_ids,
        )
        request_body = {
            "instance": evals_instance.to_json(),
            "update_mask": evals_instance.get_update_mask(),
        }

        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.patch(
                url=self.get_method_url(f"/managed-evals/instances/{instance_id}"),
                json=request_body,
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def get_managed_evals_instance(self, instance_id: str) -> entities.EvalsInstance:
        """
        Gets a Managed Evals instance.

        Args:
            instance_id: Managed Evals instance ID.

        Returns:
            The EvalsInstance.
        """
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.get(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/configuration"
                ),
            )
        _raise_for_status(response)
        return entities.EvalsInstance.from_json(response.json())

    def sync_evals_to_uc(self, instance_id: str):
        """
        Syncs evals from the evals table to a user-visible UC table.

        Args:
            instance_id: Managed Evals instance ID.
        """
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/evals:sync"
                ),
            )
        _raise_for_status(response)

    def add_evals(
        self,
        *,
        instance_id: str,
        evals: List[Dict],
    ) -> List[str]:
        """
        Add evals to the evals table.

        Args:
            instance_id: The name of the evals table.
            evals: The evals to add to the evals table.

        Returns:
            The eval IDs of the created evals.
        """
        evals = [
            {
                "request_id": e.get(schemas.REQUEST_ID_COL),
                "source_type": e.get(schemas.SOURCE_TYPE_COL),
                "source_id": e.get(schemas.SOURCE_ID_COL),
                "agent_request": input_output_utils.to_chat_completion_request(
                    e.get(schemas.REQUEST_COL)
                ),
                "expected_response": e.get(schemas.EXPECTED_RESPONSE_COL),
                "expected_facts": [
                    {"fact": fact} for fact in e.get(schemas.EXPECTED_FACTS_COL, [])
                ],
                "expected_retrieved_context": e.get(
                    schemas.EXPECTED_RETRIEVED_CONTEXT_COL
                ),
                "tag_ids": e.get("tag_ids", []),
                "review_status": e.get("review_status"),
            }
            for e in evals
        ]
        return self.gracefully_batch_post(
            url=self.get_method_url(
                f"/managed-evals/instances/{instance_id}/evals:batchCreate"
            ),
            all_items=evals,
            request_body_create=lambda batch: {"evals": batch},
            response_body_read=lambda response: response.json().get("eval_ids", []),
        )

    def delete_evals(
        self,
        instance_id: str,
        *,
        eval_ids: List[str],
    ):
        """
        Delete evals from the evals table.
        """
        # Delete in a loop - this is inefficient but we don't have a batch delete endpoint yet.
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            for eval in eval_ids:
                response = session.delete(
                    url=self.get_method_url(
                        f"/managed-evals/instances/{instance_id}/evals/{eval}"
                    ),
                )
                _raise_for_status(response)

    def list_tags(
        self,
        instance_id: str,
    ) -> List[TagType]:
        """
        List all tags in the evals table.

        Args:
            instance_id: The name of the evals table.

        Returns:
            A list of tags.
        """
        tags = []
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            next_page_token = None
            for _ in range(100):
                response = session.get(
                    url=self.get_method_url(
                        f"/managed-evals/instances/{instance_id}/tags"
                        + (
                            ("?next_page_token=" + next_page_token)
                            if next_page_token
                            else ""
                        )
                    )
                )
                _raise_for_status(response)
                json_response = response.json()
                tags.extend(json_response.get("tags", []))
                if not (next_page_token := json_response.get("next_page_token")):
                    break
            else:
                warnings.warn(
                    "Giving up fetching tags after 100 pages of tags; potential internal error."
                )
        return tags

    def batch_create_tags(
        self,
        *,
        instance_id: str,
        tag_names: Collection[str],
    ) -> List[str]:
        """
        Call the batchCreate endpoint to create tags.

        Args:
            instance_id: The name of the evals table.
            tag_names: The tag names to create.

        Returns:
            The tag IDs of the created tags.
        """
        tag_bodies = [{"tag_name": tag} for tag in tag_names]
        return self.gracefully_batch_post(
            url=self.get_method_url(
                f"/managed-evals/instances/{instance_id}/tags:batchCreate"
            ),
            all_items=tag_bodies,
            request_body_create=lambda batch: {"tags": batch},
            response_body_read=lambda response: response.json().get("tag_ids", []),
        )

    def batch_create_eval_tags(
        self,
        instance_id: str,
        *,
        eval_tags: List[entities.EvalTag],
    ):
        """
        Batch tag evals.

        Args:
            instance_id: The name of the evals table.
            eval_tags: A list of eval-tags; each item of the list is one tag on an eval.
        """
        eval_tag_bodies = [et.to_json() for et in eval_tags]
        return self.gracefully_batch_post(
            url=self.get_method_url(
                f"/managed-evals/instances/{instance_id}/eval_tags:batchCreate"
            ),
            all_items=eval_tag_bodies,
            request_body_create=lambda batch: {"eval_tags": batch},
            response_body_read=lambda response: response.json().get("eval_tags", []),
        )

    def batch_delete_eval_tags(
        self,
        instance_id: str,
        *,
        eval_tags: List[entities.EvalTag],
    ):
        """
        Batch untag evals.

        Args:
            instance_id: The name of the evals table.
            eval_tags: A list of eval-tags; each item of the list is one tag on an eval.
        """
        eval_tag_bodies = [et.to_json() for et in eval_tags]
        return self.gracefully_batch_post(
            url=self.get_method_url(
                f"/managed-evals/instances/{instance_id}/eval_tags:batchDelete"
            ),
            all_items=eval_tag_bodies,
            request_body_create=lambda batch: {"eval_tags": batch},
            response_body_read=lambda response: response.json().get("eval_tags", []),
        )

    def update_eval_permissions(
        self,
        instance_id: str,
        *,
        add_emails: Optional[List[str]] = None,
        remove_emails: Optional[List[str]] = None,
    ):
        """Add or remove user permissions to edit an eval instance.

        Args:
            instance_id: The name of the evals table.
            add_emails: The emails to add to the permissions list.
            remove_emails: The emails to remove from the permissions list.
        """
        request_body = {"permission_change": {}}
        if add_emails:
            request_body["permission_change"]["add"] = [
                {
                    "user_email": email,
                    "permissions": ["WRITE"],
                }
                for email in add_emails
            ]
        if remove_emails:
            request_body["permission_change"]["remove"] = [
                {
                    "user_email": email,
                    "permissions": ["WRITE"],
                }
                for email in remove_emails
            ]

        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/instances/{instance_id}/permissions"
                ),
                json=request_body,
            )
        _raise_for_status(response)

    def create_monitor(
        self,
        *,
        endpoint_name: str,
        monitoring_config: entities.MonitoringConfig,
        experiment_id: str,
        workspace_path: str,
    ) -> entities.Monitor:
        pause_status: Optional[str] = None
        if monitoring_config.paused is not None:
            pause_status = (
                entities.SchedulePauseStatus.PAUSED
                if monitoring_config.paused
                else entities.SchedulePauseStatus.UNPAUSED
            ).value

        monitor_rest = rest_entities.Monitor(
            experiment_id=experiment_id,
            workspace_path=workspace_path,
            evaluation_config=rest_entities.EvaluationConfig(
                metrics=[
                    rest_entities.AssessmentConfig(name=metric)
                    for metric in monitoring_config.metrics or []
                ]
            ),
            sampling=rest_entities.SamplingConfig(
                sampling_rate=monitoring_config.sample
            ),
            schedule=rest_entities.ScheduleConfig(
                frequency_interval=monitoring_config.periodic.interval,
                frequency_unit=monitoring_config.periodic.unit,
                pause_status=pause_status,
            ),
        )
        request_body = {"monitor_config": monitor_rest.to_dict()}

        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.post(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        monitor_info_rest = rest_entities.MonitorInfo.from_dict(response.json())
        monitor = monitor_info_rest.to_monitor(endpoint_name)

        monitoring_page_url = f"{get_workspace_url()}/ml/experiments/{experiment_id}/evaluation-monitoring"
        user_message = f"""Created monitor for endpoint "{endpoint_name}".

View monitoring page: {monitoring_page_url}"""
        print(user_message)

        return monitor

    def update_monitor(
        self,
        *,
        endpoint_name: str,
        monitoring_config: entities.MonitoringConfig,
    ) -> entities.Monitor:
        pause_status: Optional[str] = None
        if monitoring_config.paused is not None:
            pause_status = (
                entities.SchedulePauseStatus.PAUSED
                if monitoring_config.paused
                else entities.SchedulePauseStatus.UNPAUSED
            )

        evaluation_config: Optional[rest_entities.EvaluationConfig] = None
        if monitoring_config.metrics:
            evaluation_config = rest_entities.EvaluationConfig(
                metrics=[
                    rest_entities.AssessmentConfig(name=metric)
                    for metric in monitoring_config.metrics
                ]
            )

        sampling_config: Optional[rest_entities.SamplingConfig] = None
        if monitoring_config.sample:
            sampling_config = rest_entities.SamplingConfig(
                sampling_rate=monitoring_config.sample
            )

        schedule_config: Optional[rest_entities.ScheduleConfig] = None
        if monitoring_config.periodic:
            schedule_config = rest_entities.ScheduleConfig(
                frequency_interval=monitoring_config.periodic.interval,
                frequency_unit=monitoring_config.periodic.unit,
                pause_status=pause_status,
            )
        monitor_rest = rest_entities.Monitor(
            evaluation_config=evaluation_config,
            sampling=sampling_config,
            schedule=schedule_config,
        )

        request_body = {
            "monitor": monitor_rest.to_dict(),
            "update_mask": monitor_rest.get_update_mask(),
        }
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.patch(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        monitor_info_rest = rest_entities.MonitorInfo.from_dict(response.json())
        return monitor_info_rest.to_monitor(endpoint_name)

    def get_monitor(
        self,
        *,
        endpoint_name: str,
    ) -> entities.Monitor:
        request_body = {}
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.get(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)
        monitor_info_rest = rest_entities.MonitorInfo.from_dict(response.json())
        return monitor_info_rest.to_monitor(endpoint_name)

    def delete_monitor(self, endpoint_name: str) -> None:
        request_body = {}
        with self.get_default_request_session(
            headers=_get_default_headers()
        ) as session:
            response = session.delete(
                url=self.get_method_url(f"/managed-evals/monitors/{endpoint_name}"),
                json=request_body,
            )
        _raise_for_status(response)

    def monitoring_usage_events(
        self,
        *,
        endpoint_name: str,
        job_id: str,
        run_id: str,
        run_ended: bool,
        error_message: Optional[str] = None,
        additional_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        :param endpoint_name: Name of endpoint associated with monitor.
        :param job_id: ID of job.
        :param run_id: ID of job run.
        :param run_ended: Whether this usage event is triggered by the completion of a job run, either success or failure.
        :param error_message: Error message associated with failed run. May be empty.
        :param additional_headers: Additional headers to be passed when sending the request. May be empty.
        """

        job_start = None if run_ended else {}
        job_completion = (
            rest_entities.JobCompletionEvent(
                success=error_message is None,
                error_message=error_message,
            )
            if run_ended
            else None
        )

        monitoring_event = rest_entities.MonitoringEvent(
            job_start=job_start,
            job_completion=job_completion,
        )

        request_body = {
            "job_id": job_id,
            "run_id": run_id,
            "events": [monitoring_event.to_dict()],
        }

        default_headers = _get_default_headers()
        headers = {**default_headers, **(additional_headers or {})}

        with self.get_default_request_session(headers=headers) as session:
            response = session.post(
                url=self.get_method_url(
                    f"/managed-evals/monitors/{endpoint_name}/usage-logging"
                ),
                json=request_body,
            )
        _raise_for_status(response)
