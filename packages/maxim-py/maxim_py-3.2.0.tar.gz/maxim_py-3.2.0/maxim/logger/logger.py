# Assuming similar components exist in Python with the same functionality
import logging
from typing import Any, Dict, List, Optional

from typing_extensions import deprecated

from ..logger import (
    Feedback,
    Generation,
    GenerationConfig,
    GenerationError,
    Retrieval,
    RetrievalConfig,
    Session,
    SessionConfig,
    Span,
    SpanConfig,
    ToolCall,
    ToolCallConfig,
    ToolCallError,
    Trace,
    TraceConfig,
)
from ..logger.components.types import Entity
from .writer import LogWriter, LogWriterConfig


class LoggerConfig:
    def __init__(self, id, auto_flush=True, flush_interval=10):
        self.id = id
        self.auto_flush = auto_flush
        self.flush_interval = flush_interval


logger = logging.getLogger("MaximSDK")


class Logger:

    def __init__(
        self,
        config: LoggerConfig,
        api_key,
        base_url,
        is_debug=False,
        raise_exceptions=False,
    ):
        """
        Initializes the logger with the given configuration.

        Args:
            config (LoggerConfig): The configuration for the logger.
            api_key (str): The API key for the logger.
            base_url (str): The base URL for the logger.
            is_debug (bool, optional): Whether to enable debug logging. Defaults to False.
            raise_exceptions (bool, optional): Whether to raise exceptions. Defaults to False.
        """
        logger.setLevel(logging.DEBUG if is_debug else logging.INFO)
        if not config.id:
            raise ValueError("Logger must be initialized with id of the logger")
        self._id = config.id
        self.raise_exceptions = raise_exceptions
        self.is_debug = is_debug
        writer_config = LogWriterConfig(
            auto_flush=config.auto_flush,
            flush_interval=config.flush_interval,
            base_url=base_url,
            api_key=api_key,
            is_debug=is_debug,
            repository_id=config.id,
        )
        self.writer = LogWriter(writer_config)
        logger.debug("Logger initialized")

    def session(self, config: SessionConfig) -> Session:
        """
        Creates a new session with the given configuration.

        Args:
            config (SessionConfig): The configuration for the new session.

        Returns:
            Session: The newly created session.
        """
        return Session(config, self.writer)

    def trace(self, config: TraceConfig) -> Trace:
        """
        Creates a new trace with the given configuration.

        Args:
            config (TraceConfig): The configuration for the new trace.

        Returns:
            Trace: The newly created trace.
        """
        return Trace(config, self.writer)

    # Session methods
    def session_add_tag(self, session_id: str, key: str, value: str):
        """
        Adds a tag to the session.

        Args:
            session_id (str): The ID of the session.
            key (str): The key of the tag.
            value (str): The value of the tag.
        """
        Session.add_tag_(self.writer, session_id, key, value)

    def session_end(self, session_id: str):
        """
        Ends the session.

        Args:
            session_id (str): The ID of the session.
        """
        Session.end_(self.writer, session_id)

    def session_event(self, session_id: str, event_id: str, event: str, data: Any):
        """
        Adds an event to the session.

        Args:
            session_id (str): The ID of the session.
            event_id (str): The ID of the event.
            event (str): The name of the event.
            data (Any): The data associated with the event.
        """
        Session.event_(self.writer, session_id, event_id, event, data)

    def session_feedback(self, session_id: str, feedback: Feedback):
        """
        Adds a feedback to the session.

        Args:
            session_id (str): The ID of the session.
            feedback (Feedback): The feedback to add.
        """
        Session.feedback_(self.writer, session_id, feedback)

    def session_trace(self, session_id: str, config: TraceConfig) -> Trace:
        """
        Adds a trace to the session.

        Args:
            session_id (str): The ID of the session.
            config (TraceConfig): The configuration for the trace.

        Returns:
            Trace: The newly created trace.
        """
        return Session.trace_(self.writer, session_id, config)

    # Trace methods
    @deprecated(
        "This method will be removed in a future version. Use trace_add_generation instead."
    )
    def trace_generation(self, trace_id: str, config: GenerationConfig) -> Generation:
        return Trace.generation_(self.writer, trace_id, config)

    def trace_add_generation(
        self, trace_id: str, config: GenerationConfig
    ) -> Generation:
        """
        Adds a generation to the trace.

        Args:
            trace_id (str): The ID of the trace.
            config (GenerationConfig): The configuration for the generation.

        Returns:
            Generation: The newly created generation.
        """
        return Trace.generation_(self.writer, trace_id, config)

    @deprecated(
        "This method will be removed in a future version. Use trace_add_retrieval instead."
    )
    def trace_retrieval(self, trace_id: str, config: RetrievalConfig) -> Retrieval:
        return Trace.retrieval_(self.writer, trace_id, config)

    def trace_add_retrieval(self, trace_id: str, config: RetrievalConfig) -> Retrieval:
        """
        Adds a retrieval to the trace.

        Args:
            trace_id (str): The ID of the trace.
            config (RetrievalConfig): The configuration for the retrieval.

        Returns:
            Retrieval: The newly created retrieval.
        """
        return Trace.retrieval_(self.writer, trace_id, config)

    @deprecated(
        "This method will be removed in a future version. Use trace_add_span instead."
    )
    def trace_span(self, trace_id: str, config: SpanConfig) -> Span:
        return Trace.span_(self.writer, trace_id, config)

    def trace_add_span(self, trace_id: str, config: SpanConfig) -> Span:
        """
        Adds a span to the trace.

        Args:
            trace_id (str): The ID of the trace.
            config (SpanConfig): The configuration for the span.

        Returns:
            Span: The newly created span.
        """
        return Trace.span_(self.writer, trace_id, config)

    def trace_add_tag(self, trace_id: str, key: str, value: str):
        """
        Adds a tag to the trace.

        Args:
            trace_id (str): The ID of the trace.
            key (str): The key of the tag.
            value (str): The value of the tag.
        """
        Trace.add_tag_(self.writer, trace_id, key, value)

    def trace_add_tool_call(self, trace_id: str, config: ToolCallConfig) -> ToolCall:
        """
        Adds a tool call to the trace.

        Args:
            trace_id (str): The ID of the trace.
            config (ToolCallConfig): The configuration for the tool call.

        Returns:
            ToolCall: The newly created tool call.
        """
        return Trace.tool_call_(self.writer, trace_id, config)

    def trace_attach_evaluators(self, trace_id: str, evaluators: List[str]):
        Trace._attach_evaluators_(self.writer, Entity.TRACE, trace_id, evaluators)

    def trace_with_variables(
        self, trace_id: str, for_evaluators: List[str], variables: Dict[str, str]
    ):
        Trace._with_variables_(
            self.writer, Entity.TRACE, trace_id, for_evaluators, variables
        )

    def trace_event(
        self,
        trace_id: str,
        event_id: str,
        event: str,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        Adds an event to the trace.

        Args:
            trace_id (str): The ID of the trace.
            event_id (str): The ID of the event.
            event (str): The name of the event.
            tags (Optional[Dict[str, str]]): The tags associated with the event.
        """
        Trace.event_(self.writer, trace_id, event_id, event, tags)

    def trace_set_input(self, trace_id: str, input: str):
        """
        Sets the input for the trace.

        Args:
            trace_id (str): The ID of the trace.
            input (str): The input for the trace.
        """
        Trace.set_input_(self.writer, trace_id, input)

    def trace_set_output(self, trace_id: str, output: str):
        """
        Sets the output for the trace.

        Args:
            trace_id (str): The ID of the trace.
            output (str): The output for the trace.
        """
        Trace.set_output_(self.writer, trace_id, output)

    def trace_feedback(self, trace_id: str, feedback: Feedback):
        """
        Adds a feedback to the trace.

        Args:
            trace_id (str): The ID of the trace.
            feedback (Feedback): The feedback to add.
        """
        Trace.feedback_(self.writer, trace_id, feedback)

    def trace_end(self, trace_id: str):
        """
        Ends the trace.

        Args:
            trace_id (str): The ID of the trace.
        """
        Trace.end_(self.writer, trace_id)

    # Generation methods
    def generation_set_model(self, generation_id: str, model: str):
        """
        Sets the model for the generation.

        Args:
            generation_id (str): The ID of the generation.
            model (str): The model for the generation.
        """
        Generation.set_model_(self.writer, generation_id, model)

    def generation_add_message(self, generation_id: str, message: Any):
        """
        Adds a message to the generation.

        Args:
            generation_id (str): The ID of the generation.
            message (Any): The OpenAI chat message to add.
        """
        Generation.add_message_(self.writer, generation_id, message)

    def generation_set_model_parameters(
        self, generation_id: str, model_parameters: dict
    ):
        """
        Sets the model parameters for the generation.

        Args:
            generation_id (str): The ID of the generation.
            model_parameters (dict): The model parameters for the generation.
        """
        Generation.set_model_parameters_(self.writer, generation_id, model_parameters)

    def generation_result(self, generation_id: str, result: Any):
        """
        Sets the result for the generation.

        Args:
            generation_id (str): The ID of the generation.
            result (Any): The result for the generation.
        """
        Generation.result_(self.writer, generation_id, result)

    def generation_end(self, generation_id: str):
        """
        Ends the generation.

        Args:
            generation_id (str): The ID of the generation.
        """
        Generation.end_(self.writer, generation_id)

    def generation_error(self, generation_id: str, error: GenerationError):
        Generation.error_(self.writer, generation_id, error)

    def generation_attach_evaluators(self, generation_id: str, evaluators: List[str]):
        Generation._attach_evaluators_(
            self.writer, Entity.GENERATION, generation_id, evaluators
        )

    def generation_with_variables(
        self, generation_id: str, for_evaluators: List[str], variables: Dict[str, str]
    ):
        Generation._with_variables_(
            self.writer, Entity.GENERATION, generation_id, for_evaluators, variables
        )

    # Span methods
    @deprecated(
        "This method will be removed in a future version. Use span_add_generation instead."
    )
    def span_generation(self, span_id: str, config: GenerationConfig) -> Generation:
        return Span.generation_(self.writer, span_id, config)

    def span_add_generation(self, span_id: str, config: GenerationConfig) -> Generation:
        """
        Adds a generation to the span.

        Args:
            span_id (str): The ID of the span.
            config (GenerationConfig): The configuration for the generation.

        Returns:
            Generation: The newly created generation.
        """
        return Span.generation_(self.writer, span_id, config)

    @deprecated(
        "This method will be removed in a future version. Use span_add_retrieval instead."
    )
    def span_retrieval(self, span_id: str, config: RetrievalConfig):
        return Span.retrieval_(self.writer, span_id, config)

    def span_add_retrieval(self, span_id: str, config: RetrievalConfig):
        """
        Adds a retrieval to the span.

        Args:
            span_id (str): The ID of the span.
            config (RetrievalConfig): The configuration for the retrieval.

        Returns:
            Retrieval: The newly created retrieval.
        """
        return Span.retrieval_(self.writer, span_id, config)

    def span_add_tool_call(self, span_id: str, config: ToolCallConfig) -> ToolCall:
        """
        Adds a tool call to the span.

        Args:
            span_id (str): The ID of the span.
            config (ToolCallConfig): The configuration for the tool call.

        Returns:
            ToolCall: The newly created tool call.
        """
        return Span.tool_call_(self.writer, span_id, config)

    def span_end(self, span_id: str):
        """
        Ends the span.

        Args:
            span_id (str): The ID of the span.
        """
        Span.end_(self.writer, span_id)

    def span_add_tag(self, span_id: str, key: str, value: str):
        """
        Adds a tag to the span.

        Args:
            span_id (str): The ID of the span.
            key (str): The key of the tag.
            value (str): The value of the tag.
        """
        Span.add_tag_(self.writer, span_id, key, value)

    def span_event(
        self,
        span_id: str,
        event_id: str,
        name: str,
        tags: Optional[Dict[str, str]] = None,
    ):
        """
        Adds an event to the span.

        Args:
            span_id (str): The ID of the span.
            event_id (str): The ID of the event.
            name (str): The name of the event.
            tags (Optional[Dict[str, str]]): The tags associated with the event.
        """
        Span.event_(self.writer, span_id, event_id, name, tags)

    @deprecated(
        "This method will be removed in a future version. Use span_add_sub_span instead."
    )
    def span_span(self, span_id: str, config: SpanConfig):
        return Span.span_(self.writer, span_id, config)

    def span_add_sub_span(self, span_id: str, config: SpanConfig):
        """
        Adds a sub-span to the span.

        Args:
            span_id (str): The ID of the span.
            config (SpanConfig): The configuration for the sub-span.

        Returns:
            Span: The newly created sub-span.
        """
        return Span.span_(self.writer, span_id, config)

    def span_attach_evaluators(self, span_id: str, evaluators: List[str]):
        Span._attach_evaluators_(self.writer, Entity.SPAN, span_id, evaluators)

    def span_with_variables(
        self, span_id: str, for_evaluators: List[str], variables: Dict[str, str]
    ):
        Span._with_variables_(
            self.writer, Entity.SPAN, span_id, for_evaluators, variables
        )

    # Retrieval methods
    def retrieval_end(self, retrieval_id: str):
        """
        Ends the retrieval.

        Args:
            retrieval_id (str): The ID of the retrieval.
        """
        Retrieval.end_(self.writer, retrieval_id)

    def retrieval_input(self, retrieval_id: str, query: Any):
        """
        Sets the input for the retrieval.

        Args:
            retrieval_id (str): The ID of the retrieval.
            query (Any): The input for the retrieval.
        """
        Retrieval.input_(self.writer, retrieval_id, query)

    def retrieval_output(self, retrieval_id: str, docs: Any):
        """
        Sets the output for the retrieval.

        Args:
            retrieval_id (str): The ID of the retrieval.
            docs (Any): The output for the retrieval.
        """
        Retrieval.output_(self.writer, retrieval_id, docs)

    def retrieval_add_tag(self, retrieval_id: str, key: str, value: str):
        Retrieval.add_tag_(self.writer, retrieval_id, key, value)

    def retrieval_attach_evaluators(self, retrieval_id: str, evaluators: List[str]):
        Retrieval._attach_evaluators_(
            self.writer, Entity.RETRIEVAL, retrieval_id, evaluators
        )

    def retrieval_with_variables(
        self, retrieval_id: str, for_evaluators: List[str], variables: Dict[str, str]
    ):
        Retrieval._with_variables_(
            self.writer, Entity.RETRIEVAL, retrieval_id, for_evaluators, variables
        )

    # Tool call methods

    def tool_call_result(self, tool_call_id: str, result: Any):
        """
        Sets the result for the tool call.

        Args:
            tool_call_id (str): The ID of the tool call.
            result (Any): The result for the tool call.
        """
        ToolCall.result_(self.writer, tool_call_id, result)

    def tool_call_error(self, tool_call_id: str, error: ToolCallError):
        """
        Sets the error for the tool call.

        Args:
            tool_call_id (str): The ID of the tool call.
            error (ToolCallError): The error for the tool call.
        """
        ToolCall.error_(self.writer, tool_call_id, error)

    @property
    def id(self):
        """
        Returns the ID of the logger.
        """
        return self._id

    def flush(self):
        """
        Flushes the writer.
        """
        self.writer.flush()

    def cleanup(self):
        """
        Cleans up the writer.
        """
        self.writer.cleanup()
