from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..parsers.tags_parser import parse_tags
from ..writer import LogWriter
from .types import CommitLog, Entity


class ContainerLister:
    def on_end(self):
        pass


BaseConfig = Dict[str, Any]


class Evaluators:
    """
    A class to manage evaluators for a specific entity.

    This class provides functionality to initialize and manage a set of evaluators
    associated with a particular entity and writer.

    Attributes:
        entity (Entity): The entity associated with these evaluators.
        writer (LogWriter): The log writer used for committing evaluator actions.
        evaluators (List[str]): A list of evaluator identifiers.
        id (str): A unique identifier for this set of evaluators.

    Methods:
        with_variables: Allows adding variables to be used by the evaluators.
    """

    def __init__(
        self, id: str, entity: Entity, writer: LogWriter, evaluators: List[str]
    ) -> None:
        self.entity = entity
        self.writer = writer
        self.evaluators = evaluators
        self.id = id

    def with_variables(self, variables: Dict[str, str]):
        self.writer.commit(
            CommitLog(
                self.entity,
                self.id,
                "with-variables",
                {
                    "evaluators": self.evaluators,
                    "variables": variables,
                    "timestamp": datetime.now(timezone.utc),
                },
            )
        )


class BaseContainer:

    def __init__(self, entity: Entity, config: BaseConfig, writer: LogWriter):
        self.entity = entity
        self._id = config["id"]
        self._name = config.get("name")
        self.span_id = config.get("span_id")
        self.start_timestamp = datetime.now(timezone.utc)
        self.end_timestamp = None
        self.tags = parse_tags(config.get("tags", {}))
        self.writer = writer

    @property
    def id(self) -> str:
        return self._id

    def attach_evaluators(
        self,
        *evaluators: str,
    ) -> Evaluators:
        """
        Attach evaluators to this container.

        Args:
            *evaluators (str): Variable number of evaluator names to attach.

        Returns:
            Evaluators: An Evaluators object if evaluators are provided, None otherwise.

        Note:
            This method commits an 'attach-evaluators' action with the provided evaluators
            and creates an Evaluators object with unique evaluator names.
        """
        if len(evaluators) == 0:
            return
        self._commit(
            "attach-evaluators",
            {
                "evaluators": list(set(evaluators)),
                "timestamp": datetime.now(timezone.utc),
            },
        )
        return Evaluators(self._id, self.entity, self.writer, list(set(evaluators)))

    def with_variables(self, for_evaluators: List[str], variables: Dict[str, str]):
        """
        Associate variables with specific evaluators for this container.

        Args:
            for_evaluators (List[str]): List of evaluator names to associate the variables with.
            variables (Dict[str, str]): Dictionary of variables to be associated.

        Note:
            This method commits a 'with-variables' action, associating the provided
            variables with the specified evaluators and recording the current timestamp.
        """
        self._commit(
            "with-variables",
            {
                "evaluators": for_evaluators,
                "variables": variables,
                "timestamp": datetime.now(timezone.utc),
            },
        )

    @staticmethod
    def _attach_evaluators_(
        writer: LogWriter, entity: Entity, id: str, evaluators: List[str]
    ):
        writer.commit(
            CommitLog(entity, id, "attach-evaluators", {"evaluators": evaluators})
        )

    @staticmethod
    def _with_variables_(
        writer: LogWriter,
        entity: Entity,
        id: str,
        for_evaluators: List[str],
        variables: Dict[str, str],
    ):
        writer.commit(
            CommitLog(
                entity,
                id,
                "with-variables",
                {"evaluators": for_evaluators, "variables": variables},
            )
        )

    def add_tag(self, key: str, value: str):
        if self.tags == None:
            self.tags = {}
        if not isinstance(value, str):
            raise ValueError("Tag value must be a string")
        # Validate if value is str and not None
        if not value:
            raise ValueError("Tag value must not be empty")
        self.tags[key] = value
        self.tags = parse_tags(self.tags)
        self._commit("update", {"tags": {key: value}})

    @staticmethod
    def _add_tag_(writer: LogWriter, entity: Entity, id: str, key: str, value: str):
        writer.commit(CommitLog(entity, id, "update", {"tags": {key: value}}))

    def end(self):
        self.end_timestamp = datetime.now(timezone.utc)
        self._commit("end", {"endTimestamp": self.end_timestamp})

    @staticmethod
    def _end_(
        writer: LogWriter,
        entity: Entity,
        id: str,
        data: Optional[Dict[str, Any]] = None,
    ):
        if data is None:
            data = {}
        data = {k: v for k, v in data.items() if v is not None}
        writer.commit(CommitLog(entity, id, "end", data))

    def data(self) -> Dict[str, Any]:
        data = {
            "name": self._name,
            "spanId": self.span_id,
            "tags": self.tags,
            "startTimestamp": self.start_timestamp,
            "endTimestamp": self.end_timestamp,
        }
        # removing none values
        data = {k: v for k, v in data.items() if v is not None}
        return data

    @staticmethod
    def _commit_(
        writer: LogWriter,
        entity: Entity,
        id: str,
        action: str,
        data: Optional[Dict[str, Any]] = None,
    ):
        # Removing all null values from data dict
        if data is not None:
            data = {k: v for k, v in data.items() if v is not None}
        writer.commit(CommitLog(entity, id, action, data))

    def _commit(self, action: str, data: Optional[Dict[str, Any]] = None):
        if data is None:
            data = self.data()
        # Removing all null values from data dict
        data = {k: v for k, v in data.items() if v is not None}
        self.writer.commit(CommitLog(self.entity, self._id, action, data))


class EventEmittingBaseContainer(BaseContainer):

    @staticmethod
    def _event_(
        writer: LogWriter,
        entity: Entity,
        entity_id: str,
        id: str,
        name: str,
        tags: Optional[Dict[str, str]] = None,
    ):
        BaseContainer._commit_(
            writer,
            entity,
            entity_id,
            "add-event",
            {
                "id": id,
                "name": name,
                "timestamp": datetime.now(timezone.utc),
                "tags": tags,
            },
        )

    def event(self, id: str, name: str, tags: Optional[Dict[str, str]] = None):
        self._commit(
            "add-event",
            {
                "id": id,
                "name": name,
                "timestamp": datetime.now(timezone.utc),
                "tags": tags,
            },
        )
