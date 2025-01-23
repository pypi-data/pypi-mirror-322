"""
This module provides a custom LangChain callback handler for Maxim logging.

It includes functionality for tracing and logging various events in LangChain
workflows, such as LLM calls, tool usage, and agent actions. The module
integrates with the Maxim logging system to provide detailed insights and
observability for LangChain-based applications.
"""

import json
import logging
import threading
from threading import Lock
from time import sleep, time
from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID, uuid4

# Use LangChain features
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.outputs import LLMResult

from ...expiring_key_value_store import ExpiringKeyValueStore
from ...logger import (
    GenerationConfig,
    Logger,
    RetrievalConfig,
    Span,
    SpanConfig,
    ToolCallConfig,
    TraceConfig,
)
from .utils import (
    parse_langchain_llm_error,
    parse_langchain_llm_result,
    parse_langchain_messages,
    parse_langchain_model_and_provider,
    parse_langchain_model_parameters,
    parse_langchain_provider,
)

logger = logging.getLogger("MaximSDK")


# 20 minutes
DEFAULT_TIMEOUT = 60 * 20


class Graph:
    """
    A class representing a hierarchical graph structure with time-based expiration.

    This class maintains parent-child relationships between entities identified by unique IDs.
    It supports adding relationships, retrieving parents, and automatically cleaning up expired relationships.

    Attributes:
        parent_map (dict): A dictionary storing child_id -> (parent_id, timestamp) mappings.
        ttl_seconds (int): Time-to-live in seconds for each relationship before it expires.
        lock (threading.Lock): A lock for ensuring thread-safe operations.
        cleanup_thread (threading.Thread): A background thread for periodic cleanup of expired relationships.

    Methods:
        add_relationship(child_id, parent_id): Adds a parent-child relationship to the graph.
        get_parent(child_id): Retrieves the parent ID for a given child ID.
        _cleanup_loop(): Internal method for periodically removing expired relationships.
        stop(): Stops the cleanup thread and terminates the graph's operations.
    """

    def __init__(self, ttl_seconds=600):  # 600 seconds = 10 minutes
        self.parent_map = {}  # stores child_id -> (parent_id, timestamp) mapping
        self.ttl_seconds = ttl_seconds
        self.lock = Lock()  # For thread-safe operations
        self._running = True  # Flag to control cleanup thread

        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()

    def remove_node(self, node_id: str):
        """Remove a node and all its descendants from the hierarchy"""
        with self.lock:
            descendants = [node_id]
            to_check = [node_id]

            while to_check:
                current = to_check.pop()
                children = [
                    child
                    for child, (parent, _, _) in self.parent_map.items()
                    if parent == current
                ]
                descendants.extend(children)
                to_check.extend(children)

            for descendant in descendants:
                self.parent_map.pop(descendant, None)

    def add_relationship(self, parent_id:str , child_id:str, metadata=None):
        """Add a parent-child relationship to the hierarchy with optional metadata"""
        with self.lock:
            self.parent_map[child_id] = (parent_id, metadata or {}, time())

    def get_node_data(self, node_id:str) -> Optional[Dict[str, Any]]:
        """Get the data associated with a given node ID"""
        with self.lock:
            parent_data = self.parent_map.get(node_id)
            if parent_data is None:
                return None
            return parent_data

    def get_parent(self, child_id:str):
        """Get the parent ID for a given child ID"""
        with self.lock:
            if child_id not in self.parent_map:
                return None

            parent_data = self.parent_map[child_id]
            if time() - parent_data[2] > self.ttl_seconds:
                del self.parent_map[child_id]
                return None

            return parent_data[0]

    def get_ancestry(self, child_id:str):
        """Get the full ancestry chain from child to root"""
        ancestry = []
        current_id = child_id

        with self.lock:
            while current_id in self.parent_map:
                parent_data = self.parent_map[current_id]

                # Check if entry has expired
                if time() - parent_data[2] > self.ttl_seconds:
                    del self.parent_map[current_id]
                    break

                parent_id = parent_data[0]
                ancestry.append(parent_id)
                current_id = parent_id

        return ancestry

    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = time()
        with self.lock:
            expired = [
                child_id
                for child_id, (_, _, timestamp) in self.parent_map.items()
                if current_time - timestamp > self.ttl_seconds
            ]
            for child_id in expired:
                del self.parent_map[child_id]

    def _cleanup_loop(self):
        """Periodically clean up expired entries"""
        while self._running:
            self._cleanup_expired()
            sleep(60)  # Run cleanup every minute

    def __del__(self):
        """Cleanup when object is destroyed"""
        self._running = False
        self._cleanup_expired()


class MaximLangchainTracer(BaseCallbackHandler):
    """
    A callback handler that logs langchain outputs to Maxim logger

    Args:
        logger: Logger: Maxim Logger instance to log outputs
    """

    def __init__(self, logger: Logger, metadata: Optional[Dict[str, Any]]) -> None:
        """Initializes the Langchain Tracer
        Args:
            logger: Logger: Maxim Logger instance to log outputs
        """
        super().__init__()
        self.run_inline = True
        self.logger = logger
        self.chains = Graph()
        self.containers = ExpiringKeyValueStore()
        self.tool_calls = ExpiringKeyValueStore()
        self.generations = ExpiringKeyValueStore()
        self.retrievals = ExpiringKeyValueStore()
        self.metadata_store = ExpiringKeyValueStore()
        self.metadata = None
        if metadata is not None:
            self._validate_maxim_metadata(metadata)
            self.metadata = metadata

    def _validate_maxim_metadata(self, metadata: Dict[str, Any]):
        if metadata is None:
            return
        id_keys = ["session_id", "trace_id", "span_id"]
        present_keys = [key for key in id_keys if key in metadata]
        if len(present_keys) > 1:
            raise ValueError(
                f"Multiple keys found in metadata: {present_keys}. You can pass only one of these."
            )
        valid_keys = [
            "session_id",
            "trace_id",
            "span_id",
            "generation_tags",
            "retrieval_tags",
            "trace_tags",
            "retrieval_name",
            "trace_name",
            "generation_name",
            "chain_tags",
            "chain_name",
        ]
        invalid_keys = [key for key in metadata if key not in valid_keys]
        if len(invalid_keys) > 0:
            raise ValueError(
                f"Invalid keys found in metadata: {invalid_keys}. Valid keys are {valid_keys}"
            )

    def _get_container(self, run_id: UUID):
        # Now we will checking in containers
        if self.containers.get(str(run_id)) is not None:
            container = self.containers.get(str(run_id))
            if ":" in container:
                return container.split(":", 1)
        return None, None

    def _get_nearest_container(self, run_id: UUID) -> (Optional[str], Optional[str]):
        current_id = str(run_id)
        component, component_id = self._get_container(current_id)
        while component is None:
            current_id = self.chains.get_parent(current_id)
            if current_id is None:
                return None, None
            component, component_id = self._get_container(current_id)
        return component, component_id

    def _get_container_from_metadata(self, run_id: UUID):
        maxim_metadata = self.metadata_store.get(str(run_id))
        if maxim_metadata is not None:
            span_id = maxim_metadata.get("span_id", None)
            if span_id is not None:
                return "span", span_id
            session_id = maxim_metadata.get("session_id", None)
            if session_id is not None:
                return "session", session_id
            trace_id = maxim_metadata.get("trace_id", None)
            if trace_id is not None:
                return "trace", trace_id
        return "local_trace", str(run_id)

    # LLM callbacks

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug("[MaximSDK: Langchain] on_llm_start called")
        model, model_parameters = parse_langchain_model_parameters(**kwargs)
        provider = parse_langchain_provider(serialized)
        model, provider = parse_langchain_model_and_provider(model, provider)
        messages = parse_langchain_messages(prompts)
        generation_id = str(uuid4())
        generation_name = None
        generation_tags = None
        trace_tags = None

        if metadata is not None and metadata.get("maxim", None) is not None:
            self._validate_maxim_metadata(metadata.get("maxim", None))
            self.metadata_store.set(
                str(run_id), metadata.get("maxim", None), DEFAULT_TIMEOUT
            )
            trace_tags = metadata.get("maxim", {}).get("trace_tags", None)
            generation_name = metadata.get("maxim", {}).get("generation_name", None)
            generation_tags = metadata.get("maxim", {}).get("generation_tags", None)
        elif self.metadata is not None:
            self.metadata_store.set(str(run_id), self.metadata, DEFAULT_TIMEOUT)
            trace_name = self.metadata.get("trace_name", None)
            trace_tags = self.metadata.get("trace_tags", None)
            generation_name = self.metadata.get("generation_name", None)
            generation_tags = self.metadata.get("generation_tags", None)

        generation_config = GenerationConfig(
            id=generation_id,
            name=generation_name,
            provider=provider,
            model=model,
            messages=messages,
            model_parameters=model_parameters,
            tags=generation_tags,
        )

        self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)

        container, container_id = self._get_container_from_metadata(run_id)

        if container == "span":
            self.logger.span_add_generation(container_id, generation_config)
        elif container == "trace":
            self.logger.trace_add_generation(container_id, generation_config)
        elif container == "session":
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.session_trace(
                container_id,
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags),
            )
            trace.generation(generation_config)
        else:
            trace_name = None
            if metadata is not None:
                trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace = self.logger.trace(
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags)
            )
            trace.generation(generation_config)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        logger.debug("[MaximSDK: Langchain] on_llm_end called")
        run_id = kwargs.get("run_id", None)
        if run_id is not None:
            result = parse_langchain_llm_result(response)
            generation_id = self.generations.get(str(run_id))
            if generation_id is not None:
                container, container_id = self._get_container_from_metadata(run_id)
                self.logger.generation_result(generation_id, result)
                if container == "local_trace":
                    self.logger.trace_end(container_id)

    # Retrieval callbacks

    def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Run when Retriever starts running.
        """
        logger.debug("[Langchain] on_retriever_start called")
        container, container_id = self._get_container_from_metadata(run_id)
        retrieval_id = str(uuid4())
        retrieval_config = RetrievalConfig(id=retrieval_id)
        if container == "span":
            retrieval = self.logger.span_add_retrieval(
                container_id, config=retrieval_config
            )
            retrieval.input(query)
        elif container == "trace":
            retrieval = self.logger.trace_add_retrieval(
                container_id, config=retrieval_config
            )
            retrieval.input(query)
        elif container == "session":
            trace = self.logger.session_trace(container_id, TraceConfig(id=str(run_id)))
            retrieval = trace.retrieval(retrieval_config)
            retrieval.input(query)
        else:
            retrieval = self.logger.trace_add_retrieval(
                str(run_id), config=retrieval_config
            )
            retrieval.input(query)

    def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug("[Langchain] on_retriever_end called")
        trace_id = str(run_id)
        retrieval_id = self.retrievals.get(trace_id)
        if retrieval_id is not None:
            self.logger.retrieval_output(retrieval_id, documents)

    # ChatModel callbacks

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        logger.debug("[Langchain] on_chat_model_start called")
        run_id = kwargs.get("run_id", None)
        model, model_parameters = parse_langchain_model_parameters(**kwargs)
        provider = parse_langchain_provider(serialized)
        model, provider = parse_langchain_model_and_provider(model, provider)
        maxim_messages = parse_langchain_messages(messages)
        generation_id = str(uuid4())
        # Checking if generation id already present for this run_id
        if self.generations.get(str(run_id)) is not None:
            generation_id = self.generations.get(str(run_id))
        generation_name = None
        generation_tags = None
        trace_tags = None
        trace_name = None

        if metadata is not None and metadata.get("maxim", None) is not None:
            self._validate_maxim_metadata(metadata.get("maxim", None))
            self.metadata_store.set(
                str(run_id), metadata.get("maxim", None), DEFAULT_TIMEOUT
            )
            trace_name = metadata.get("maxim", {}).get("trace_name", None)
            trace_tags = metadata.get("maxim", {}).get("trace_tags", None)
            generation_name = metadata.get("maxim", {}).get("generation_name", None)
            generation_tags = metadata.get("maxim", {}).get("generation_tags", None)
        elif self.metadata is not None:
            self.metadata_store.set(str(run_id), self.metadata, DEFAULT_TIMEOUT)
            trace_name = self.metadata.get("trace_name", None)
            trace_tags = self.metadata.get("trace_tags", None)
            generation_name = self.metadata.get("generation_name", None)
            generation_tags = self.metadata.get("generation_tags", None)

        generation_config = GenerationConfig(
            id=generation_id,
            name=generation_name,
            provider=provider,
            model=model,
            messages=maxim_messages,
            model_parameters=model_parameters,
            tags=generation_tags,
        )
        self.generations.set(str(run_id), generation_id, DEFAULT_TIMEOUT)

        container, container_id = self._get_container_from_metadata(run_id)

        if container == "span":
            self.logger.span_add_generation(container_id, generation_config)
        elif container == "trace":
            self.logger.trace_add_generation(container_id, generation_config)
        elif container == "session":
            trace = self.logger.session_trace(
                container_id,
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags),
            )
            trace.generation(generation_config)
        else:
            trace = self.logger.trace(
                TraceConfig(id=str(run_id), name=trace_name, tags=trace_tags)
            )
            trace.generation(generation_config)

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        logger.debug("[Langchain] on_llm_error called")
        run_id = kwargs.get("run_id", None)
        if run_id is not None:
            generation_id = self.generations.get(str(run_id))
            if generation_id is not None:
                container, container_id = self._get_container_from_metadata(run_id)
                generation_error = parse_langchain_llm_error(error)
                self.logger.generation_error(generation_id, generation_error)
                if container == "local_trace":
                    self.logger.trace_end(container_id)

    # Chain callbacks

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        try:
            parent_run_id = (
                str(kwargs.get("parent_run_id", None))
                if kwargs.get("parent_run_id", None) is not None
                else None
            )
            run_id = (
                str(kwargs.get("run_id", None))
                if kwargs.get("run_id", None) is not None
                else None
            )
            if parent_run_id is not None:
                chain_data = {}
                self.chains.add_relationship(parent_run_id, run_id, chain_data)
            name = kwargs.get("name", None)
            span: Optional[Span] = None
            span_id = str(uuid4())
            tags: Dict[str, str] = {}
            if self.metadata.get("chain_tags") is not None:
                # its a dict
                for key, value in self.metadata["chain_tags"].items():
                    tags[key] = str(value)
            tags["run_id"] = run_id
            if parent_run_id is not None:
                tags["parent_run_id"] = parent_run_id
            if kwargs.get("tags", None) is not None:
                for tag in kwargs["tags"]:
                    key, value = tag.split(":", 1)
                    tags[key.strip()] = value.strip()
            metadata = kwargs.get("metadata", None)
            if metadata is not None:
                for key, value in kwargs["metadata"].items():
                    tags[key.strip()] = str(value)

            # We hide the hidden chains
            if "langsmith:hidden" in kwargs.get("tags", []):
                # Here we can complete the chain
                # here we are checking if we have to end anything
                # we fire events here
                container, container_id = self._get_container(parent_run_id)
                event_id = str(uuid4())
                if container == "span":
                    self.logger.span_event(container_id, event_id, name, tags)
                elif container == "trace":
                    self.logger.trace_event(container_id, event_id, name, tags)
                return

            # Checking if this is a generation
            messages = inputs["messages"] if "messages" in inputs else []

            # Checking
            if parent_run_id is None:
                # This is the start of new chain
                # We create a new span - create a start event inside it
                span_name = self.metadata.get("chain_name") or name
                span_config = SpanConfig(id=span_id, name=span_name, tags=tags)
                span: Optional[Span] = None
                event_id = str(uuid4())
                container, container_id = self._get_container_from_metadata(run_id)
                if container == "span":
                    span = self.logger.span_add_sub_span(container_id, span_config)
                elif container == "trace":
                    span = self.logger.trace(container_id, span_config)
                else:
                    # Checking if I have current trace
                    if self.metadata is not None:
                        trace_id = self.metadata["trace_id"]
                        if trace_id is not None:
                            span = self.logger.trace_add_span(trace_id, span_config)
                    else:
                        # Creating trace locally
                        trace_name = None
                        trace = self.logger.trace(
                            TraceConfig(id=str(run_id), name=trace_name)
                        )
                        span = trace.span(span_config)
                if span is not None:
                    # Getting existing metadata
                    new_meta = {"span_id": span.id}
                    run_meta = self.metadata_store.get(run_id)
                    if run_meta is not None:
                        new_meta.update(run_meta)
                    # Here we will set the container for the given run_id
                    self.containers.set(run_id, f"span:{span.id}", DEFAULT_TIMEOUT)
                    self.metadata_store.set(run_id, new_meta, DEFAULT_TIMEOUT)
                return
            # Adding to graph
            # Lets get hold of the top level container
            container, container_id = self._get_container(parent_run_id)
            if container == "span":
                message = messages[-1]
                if isinstance(message, (HumanMessage, ToolMessage)):
                    # This is the new round
                    generation_id = str(uuid4())
                    parsed_messages = parse_langchain_messages([[message]])
                    generation_name = name
                    # Here 100% container is a span
                    self.logger.span_add_generation(
                        container_id,
                        GenerationConfig(
                            id=generation_id,
                            name=generation_name,
                            provider="unknown",
                            model="unknown",
                            messages=parsed_messages,
                            tags=tags,
                        ),
                    )
                    # Adding entity for this run_id
                    self.containers.set(
                        run_id, f"generation:{generation_id}", DEFAULT_TIMEOUT
                    )
                if isinstance(message, AIMessage):
                    # This is a new turn
                    # We check if there was a tool call
                    # But before that we will fire an event in the main span as this is a node switch
                    message = messages[-1]
                    tool_calls = message.tool_calls or []
                    if len(tool_calls) > 0:
                        # Here we will create the tool_call
                        # Creating a tool_call using same run_id
                        # So even if it gets into
                        for tool_call in tool_calls:
                            tool_call_id = str(uuid4())
                            name = tool_call.get("name")
                            description = ""
                            args = json.dumps(tool_call.get("args"))
                            config = ToolCallConfig(
                                id=tool_call_id,
                                name=name,
                                description=description,
                                args=args,
                            )
                            tool_call = self.logger.span_add_tool_call(
                                container_id, config
                            )
                            self.containers.set(
                                run_id, f"tool_call:{tool_call_id}", DEFAULT_TIMEOUT
                            )                            

            if container is None:
                # This is the case where container is none
                # Here we pick the parent container and add an event to it
                container, container_id = self._get_nearest_container(parent_run_id)
                if container == "span":
                    event_id = str(uuid4())
                    self.logger.span_event(container_id, event_id, name, tags)
                elif container == "trace":
                    event_id = str(uuid4())
                    self.logger.trace_event(container_id, event_id, name, tags)
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse chain-start: {e}")

    def on_chain_end(self, outputs: Union[str, Dict[str, Any]], **kwargs: Any) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            parent_run_id = kwargs.get("parent_run_id", None)
            # We hide the hidden chains
            tags = {
                tag.split(":")[0]: tag.split(":")[1]
                for tag in kwargs.get("tags", [])
                if ":" in tag
            }
            container, container_id = self._get_container(parent_run_id)
            if container == "generation":
                # make sure that the outputs has messages and it has at-least one entry
                if isinstance(outputs, dict) and "messages" in outputs:
                    message = outputs["messages"][-1]
                    model, model_parameters = parse_langchain_model_parameters(**kwargs)
                    model = message.response_metadata.get(
                        "model_name"
                    ) or message.response_metadata.get("model", "unknown")

                    self.logger.generation_set_model(container_id, model)
                    self.logger.generation_result(
                        generation_id=container_id, result=message
                    )
                    # deleting the container
                    self.containers.delete(str(parent_run_id))
                    return
                print("generation ended")
            elif container == "tool_call":
                # ending tool call here
                # This is a new turn
                # We check if there was a tool call
                # But before that we will fire an event in the main span as this is a node switch
                if isinstance(outputs, dict) and "messages" in outputs:
                    output = outputs["messages"][-1]
                    tool_call_id = container_id
                    if isinstance(output, ToolMessage):
                        if output.status == "success":
                            self.logger.tool_call_result(tool_call_id, output.content)
                        elif output.status == "error":
                            self.logger.tool_call_error(tool_call_id, output.content)
                    self.containers.delete(str(parent_run_id))
                    return
            elif container == "span" and isinstance(outputs, str):
                event_id = str(uuid4())
                self.logger.span_event(container_id, event_id, str(outputs), tags)
                print(f"container: {container}, container_id: {container_id}")

            # This is the case where container is none
            # Here we pick the parent container and add an event to it
            if isinstance(outputs, str):
                container, container_id = self._get_nearest_container(parent_run_id)
                if container == "span":
                    event_id = str(uuid4())
                    self.logger.span_event(container_id, event_id, str(outputs), tags)
                elif container == "trace":
                    event_id = str(uuid4())
                    self.logger.trace_event(container_id, event_id, str(outputs), tags)
            # Deleting the chain node
            self.chains.remove_node(str(run_id))
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse chain-end: {e}")

    def on_chain_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        print("chain-error", error, kwargs)

    def on_custom_event(
        self,
        name: str,
        data: Any,
        *,
        run_id: UUID,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        print("on-custom-event", name, data, run_id, tags, metadata, kwargs)

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        print("on-agent-action", action, run_id, parent_run_id, kwargs)

    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        print("on-agent-finish", finish, run_id, parent_run_id, kwargs)

    # Tool callbacks

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            parent_run_id = kwargs.get("parent_run_id", None)
            name = serialized.get("name", None)
            description = serialized.get("description", None)
            container, container_id = self._get_container(str(parent_run_id))
            if container is None:
                container, container_id = self._get_container_from_metadata(
                    parent_run_id
                )
            if container == "tool_call":
                tool_call_id = container_id
                self.logger.tool_call_update(tool_call_id, {"name": name, "description": description, "args": input_str})
                self.tool_calls.set(str(run_id), tool_call_id, DEFAULT_TIMEOUT)
            elif container == "span":
                tool_call_id = str(uuid4())
                config = ToolCallConfig(
                    id=str(tool_call_id),
                    name=name,
                    description=description,
                    args=input_str,
                )
                tool_call = self.logger.span_add_tool_call(container_id, config)
                self.tool_calls.set(str(run_id), tool_call.id, DEFAULT_TIMEOUT)
            elif container == "trace":
                tool_call_id = str(uuid4())
                config = ToolCallConfig(
                    id=str(tool_call_id),
                    name=name,
                    description=description,
                    args=input_str,
                )
                tool_call = self.logger.trace_add_tool_call(container_id, config)
                self.tool_calls.set(str(run_id), tool_call.id, DEFAULT_TIMEOUT)
            else:
                logger.error(
                    "[MaximSDK] No container found for tool call. This is invalid state."
                )                

        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse tool-start: {e}")

    def on_tool_end(self, output: Any, **kwargs: Any) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            tool_call_id = self.tool_calls.get(str(run_id))
            if tool_call_id is None:
                logger.error(
                    "[MaximSDK] No tool call id found for tool end. This is invalid state."
                )
                return
            if isinstance(output, ToolMessage):
                if output.status == "success":
                    self.logger.tool_call_result(tool_call_id, output.content)
                elif output.status == "error":
                    self.logger.tool_call_error(tool_call_id, output.content)
            else:
                logger.error(
                    f"[MaximSDK] Invalid output type {type(output)}. This is invalid state."
                )
            self.tool_calls.delete(str(run_id))
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse tool-end: {e}")

    def on_tool_error(
        self, error: Union[Exception, BaseException, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        try:
            run_id = kwargs.get("run_id", None)
            tool_call_id = self.tool_calls.get(str(run_id))
            if tool_call_id is None:
                logger.error(
                    "[MaximSDK] No tool call id found for tool end. This is invalid state."
                )
                return
            self.logger.tool_call_error(tool_call_id, str(error))
        except Exception as e:
            logger.error(f"[MaximSDK] Failed to parse tool-end: {e}")

    def on_text(self, text: str, **kwargs: Any) -> Any:
        print("on-text", text, kwargs)
