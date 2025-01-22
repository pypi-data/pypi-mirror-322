import dataclasses
from typing import List, Optional, Sequence

from typing_extensions import Self

from databricks.rag_eval.utils import NO_CHANGE, error_utils, token_counting_utils
from databricks.rag_eval.utils.collection_utils import deep_getattr, deep_setattr
from databricks.rag_eval.utils.enum_utils import StrEnum

_FIELD_PATH = "FIELD_PATH"
_FIELD_IS_UPDATABLE = "FIELD_IS_UPDATABLE"
_FIELD_FROM_DICT = "FIELD_FROM_DICT"
_FIELD_TO_DICT = "FIELD_TO_DICT"


def _get_json_field_path(field: dataclasses.Field) -> Sequence[str]:
    """Get the JSON field path from the field metadata."""
    return field.metadata.get(_FIELD_PATH).split(".")


def _has_json_field_path(field: dataclasses.Field) -> bool:
    """Check if the field has a JSON field path."""
    return _FIELD_PATH in field.metadata


# noinspection PyTypeChecker,PyArgumentList
@dataclasses.dataclass
class JsonSerializable:
    def to_json(self) -> dict:
        """Convert the object to a JSON serializable dictionary."""
        json = {}
        for field in dataclasses.fields(self):
            if _has_json_field_path(field):
                value = getattr(self, field.name)
                if value is not None and value is not NO_CHANGE:
                    if _FIELD_TO_DICT in field.metadata:
                        to_dict_fn = field.metadata[_FIELD_TO_DICT]
                        value = to_dict_fn(value)
                    deep_setattr(json, _get_json_field_path(field), value)
        return json

    @classmethod
    def from_json(cls, json: dict) -> Self:
        """Create an instance from a JSON dictionary."""
        values = {}
        for field in dataclasses.fields(cls):
            if _has_json_field_path(field):
                raw_value = deep_getattr(json, _get_json_field_path(field))
                if raw_value is not None:
                    if _FIELD_FROM_DICT in field.metadata:
                        from_dict_fn = field.metadata[_FIELD_FROM_DICT]
                        value = from_dict_fn(raw_value)
                    else:
                        value = raw_value
                    values[field.name] = value
        return cls(**values)

    def get_update_mask(self) -> str:
        """Get the update mask for the fields that have changed."""
        return ",".join(
            field.metadata.get(_FIELD_PATH)
            for field in dataclasses.fields(self)
            if getattr(self, field.name) is not NO_CHANGE
            and field.metadata.get(_FIELD_IS_UPDATABLE, True)
        )


@dataclasses.dataclass
class UIPageConfig:
    name: str
    display_name: str
    path: str


@dataclasses.dataclass
class EvalsInstance(JsonSerializable):
    instance_id: Optional[str] = dataclasses.field(
        default=None, metadata={_FIELD_PATH: "instance_id", _FIELD_IS_UPDATABLE: False}
    )
    version: Optional[str] = dataclasses.field(
        default=None, metadata={_FIELD_PATH: "version", _FIELD_IS_UPDATABLE: False}
    )
    agent_name: Optional[str] = dataclasses.field(
        default=None, metadata={_FIELD_PATH: "agent_config.agent_name"}
    )
    agent_serving_endpoint: Optional[str] = dataclasses.field(
        default=None,
        metadata={
            _FIELD_PATH: "agent_config.model_serving_config.model_serving_endpoint_name"
        },
    )
    ui_page_configs: Optional[List[UIPageConfig]] = dataclasses.field(
        default=None,
        metadata={
            _FIELD_PATH: "ui_page_configs",
            _FIELD_IS_UPDATABLE: False,
            _FIELD_FROM_DICT: lambda value: [UIPageConfig(**page) for page in value],
            _FIELD_TO_DICT: lambda value: [dataclasses.asdict(page) for page in value],
        },
    )
    experiment_ids: List[str] = dataclasses.field(
        default_factory=list,
        metadata={
            _FIELD_PATH: "experiment_ids",
        },
    )


@dataclasses.dataclass
class EvalTag(JsonSerializable):
    """A tag on an eval row."""

    tag_id: str = dataclasses.field(metadata={_FIELD_PATH: "tag_id"})
    eval_id: str = dataclasses.field(metadata={_FIELD_PATH: "eval_id"})


@dataclasses.dataclass
class Document:
    """A document that holds the source data for an agent application."""

    content: str
    """The raw content of the document."""

    doc_uri: str
    """The URI of the document."""

    num_tokens: Optional[int] = None
    """The number of tokens in the document."""

    def __post_init__(self):
        if not self.content or not isinstance(self.content, str):
            raise error_utils.ValidationError(
                f"'content' of a document must be a non-empty string. Got: {self.content}"
            )

        if not self.doc_uri or not isinstance(self.doc_uri, str):
            raise error_utils.ValidationError(
                f"'doc_uri' of a document must be a non-empty string. Got: {self.doc_uri}"
            )

        if self.num_tokens is None:
            self.num_tokens = token_counting_utils.count_tokens(self.content)


@dataclasses.dataclass
class SyntheticQuestion:
    """A synthetic question generated by the synthetic API that can be used for evaluation."""

    question: str
    """The raw question text."""

    source_doc_uri: str
    """The URI of the document from which the question was generated."""

    source_context: str
    """
    The context from which the question was generated. 
    Could be a chunk of text from the source document or the whole document content.
    """


@dataclasses.dataclass
class SyntheticAnswer:
    """A synthetic answer generated by the synthetic API that can be used for evaluation."""

    question: SyntheticQuestion
    """The synthetic question to which the answer corresponds."""

    synthetic_ground_truth: Optional[str] = None
    """The synthetic ground truth answer for the question."""

    synthetic_grading_notes: Optional[str] = None
    """The synthetic grading notes to help judge the correctness of the question."""

    synthetic_minimal_facts: Optional[List[str]] = None
    """The synthetic minimum expected facts required to answer the question."""


class SyntheticAnswerType(StrEnum):
    GROUND_TRUTH = "GROUND_TRUTH"
    GRADING_NOTES = "GRADING_NOTES"
    MINIMAL_FACTS = "MINIMAL_FACTS"
