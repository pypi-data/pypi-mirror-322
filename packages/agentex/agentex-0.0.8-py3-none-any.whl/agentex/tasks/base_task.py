from abc import ABC, abstractmethod
from exlog import ExLog
from ..logging.logger import LoggerWrapper
import traceback
class BaseTask(ABC):
    """
    Base class for shared attributes and logging.
    """
    def __init__(self, name, description, priority=0, logger=None, silent=False):
        """
        :param task_name: Name of the task.
        :param description: Description of the task.
        :param logger: Logger instance (ExLog or standard logger).
        :param silent: Whether to suppress logging only within this task's `.log` method.
        """
        self.task_name = name
        self.description = description
        self.state = TaskState.PENDING
        self.logger = logger or LoggerWrapper(log_level=1)
        self.result = None
        self.silent = silent  # Add silent mode specific to the `BaseTask.log()`
        self.priority = priority

    def set_state(self, new_state):
        TaskState.validate_transition(self.state, new_state)
        # self.logger.dprint(f"Task '{self.task_name}' transitioning from {self.state} to {new_state}", level="info", custom_tag="STATE")
        self.state = new_state

    def log(self, message, level="info"):
        """
        Log a message if `silent` is False.
        """
        # stack = traceback.extract_stack()
        # if len(stack) > 2:
        #     # Get the second-to-last stack frame (the caller)
        #     caller_frame = stack[-3]
        #     file_name = caller_frame.filename
        #     line_number = caller_frame.lineno
        #     caller_name = caller_frame.name
        #     caller_info = f"[Called from {caller_name} in {file_name}, line {line_number}]"
        # else:
        #     caller_info = "[Caller information not available]"

        # Log the message with the caller info

        if self.silent:  # Check if this specific task should suppress logs
            return  # Do nothing if silent mode is enabled

        if self.logger:
            log_method = getattr(self.logger, level, self.logger.info)
            log_method(f"log() {self.task_name}: {message}")

class TaskStateTransitionError(Exception):
    pass

class TaskState:
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    PAUSED = "PAUSED"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"
    TIMED_OUT = "TIMED_OUT"
    ABORTED = "ABORTED"
    WAITING = "WAITING"
    SKIPPED = "SKIPPED"
    
    VALID_TRANSITIONS = {
        PENDING: [QUEUED, CANCELLED],
        QUEUED: [SCHEDULED, CANCELLED],
        SCHEDULED: [RUNNING, WAITING, CANCELLED, BLOCKED],
        RUNNING: [COMPLETED, FAILED, PAUSED, CANCELLED, TIMED_OUT, WAITING],
        COMPLETED: [],
        FAILED: [RETRYING, CANCELLED],
        RETRYING: [RUNNING, FAILED, CANCELLED],
        PAUSED: [RUNNING, CANCELLED],
        CANCELLED: [],
        BLOCKED: [WAITING, CANCELLED],
        TIMED_OUT: [RETRYING, CANCELLED],
        ABORTED: [],
        WAITING: [RUNNING, CANCELLED],  # Tasks leave WAITING to RUNNING or CANCELLED
        SKIPPED: [],
    }

    @classmethod
    def validate_transition(cls, current_state, new_state):
        if new_state not in cls.VALID_TRANSITIONS.get(current_state, []):
            raise TaskStateTransitionError(
                f"Invalid transition from {current_state} to {new_state}"
            )