

import asyncio
from abc import ABC, abstractmethod
from exlog import ExLog
from collections import defaultdict, deque
from .tasks import AgentTask, AsyncAgentTask, TaskState, TaskStateTransitionError
import traceback
class Agent:
    def __init__(self, name, group='main', message_callback=None, send_callback=None, logger=None):
        """
        Initialize an Agent.
        :param name: The agent's name.
        :param group: The group name the agent belongs to.
        :param message_callback: A callback function triggered when the agent receives a message.
        :param send_callback: A callback function triggered after sending a message.
        """
        self.name = name
        self.task = None
        self.swarm = None
        # self.groups = ['main'] if group == 'main' else ['main', group]
        self.logger = logger or ExLog(log_level=1) # You can change this within the instantiation for your own scripts to be silent just set logger=ExLog(log_level=0)
        self.message_callback = message_callback  # Function called on receive
        self.send_callback = send_callback  # Function called after sending
        self.local_task_queue = deque()
        
        # --- Multi-group logic ---
        if isinstance(group, list):
            # If the user passes a list of groups, ensure 'main' is included
            group_set = set(group)
            group_set.add('main')
            self.groups = list(group_set)
        else:
            # If the user passes a single string
            if group == 'main':
                self.groups = ['main']
            else:
                self.groups = ['main', group]        
    def prioritize_tasks(self):
        """Reorder the agent's local task queue based on priority."""
        self.local_task_queue = deque(sorted(self.local_task_queue, key=lambda t: t.priority, reverse=True))
    
    def set_swarm(self, swarm):
        """Assign the agent to a swarm."""
        self.swarm = swarm


    def is_available(self):
        """Check if the agent is available to take on a task."""
        return self.task is None

    # Task Assignment (Sync + Async)
    def assign_task(self, task, print_full_result=True):
        """Assign a task and execute it synchronously or asynchronously."""
        if self.task is not None:
            self.logger.dprint(f"Agent '{self.name}' already has an active task '{self.task.task_name}'. Skipping assignment.", level="warning")
            return
        self.task = task
        self.task.set_state(TaskState.QUEUED)  # Transition to QUEUED
        self.logger.dprint(f"---Task '{task.task_name}' assigned to agent '{self.name}' and queued.", level="info")

        # Check the type of task and execute accordingly
        if isinstance(task, AsyncAgentTask):
            asyncio.create_task(self.schedule_async_task(print_full_result=print_full_result))
            print(f"%%%%%%%%%Scheduling async stuf {task}")
        else:
            print(f"##########Scheduling sync stuf {task}")
            self.schedule_sync_task(print_full_result=print_full_result)
    
    async def async_assign_task(self, task, print_full_result=True):
        """Assign a task asynchronously and schedule it immediately."""
        
        if self.task is not None:
            self.logger.dprint(f"Agent '{self.name}' already has an active task '{self.task.task_name}'. Skipping assignment.", level="warning")
            return

        self.task = task
        self.task.set_state(TaskState.QUEUED)  # Transition to QUEUED
        self.logger.dprint(f"Async Task '{task.task_name}' assigned to agent '{self.name}' and queued.", level="info")

        # Schedule the task asynchronously
        asyncio.create_task(self.schedule_async_task(print_full_result=print_full_result))

    
    async def schedule_async_task(self, print_full_result=True):
        
        """Schedule and manage an asynchronous task."""
        if self.task is None or self.task.state != TaskState.QUEUED:
            self.logger.dprint(f"No valid task to schedule for agent '{self.name}'.", level="warning")
            return

        try:
            self.task.set_state(TaskState.SCHEDULED)  # Transition to SCHEDULED
            self.logger.dprint(f"Async task '{self.task.task_name}' scheduled for execution by agent '{self.name}'.", level="info")
            await self.manage_async_task(print_full_result=print_full_result)
        except TaskStateTransitionError as e:
            self.logger.dprint(f"Failed to schedule async task '{self.task.task_name}': {e}", level="error")


    def schedule_sync_task(self, print_full_result=True):
        """
        Schedule a task for an agent.
        Currently a placeholder method that can be expounded upon.
        Right now it just marks the task as scheduled from queued.
        """
        if self.task is None or self.task.state != TaskState.QUEUED:
            self.logger.dprint(f"No valid task to schedule for agent '{self.name}'.", level="warning")
            return

        try:
            self.task.set_state(TaskState.SCHEDULED)  # Transition to SCHEDULED
            self.logger.dprint(f"Sync task '{self.task.task_name}' scheduled for execution by agent '{self.name}'.", level="info")
            self.manage_sync_task(print_full_result=print_full_result)
        except TaskStateTransitionError as e:
            self.logger.dprint(f"Failed to schedule sync task '{self.task.task_name}': {e}", level="error")
    
    def manage_sync_task(self, print_full_result=True):
        """Manage a synchronous task."""
        if self.task is None or self.task.state != TaskState.SCHEDULED:
            self.logger.dprint(f"Invalid sync task state for agent '{self.name}'.", level="error")
            return

        try:
            self.task.set_state(TaskState.RUNNING)  # Transition to RUNNING
            self.task.run_task()  # Run the sync task
            self.task.set_state(TaskState.COMPLETED)  # Transition to COMPLETED

            # Log task completion with appropriate detail
            if print_full_result:
                self.logger.dprint(f"Sync task '{self.task.task_name}' completed by '{self.name}'. Result: {self.task.get_result()}", level="info")
            else:
                self.logger.dprint(f"Sync task '{self.task.task_name}' completed successfully by '{self.name}'.", level="info")
        except Exception as e:
            self.task.set_state(TaskState.FAILED)
            self.logger.dprint(f"Sync task '{self.task.task_name}' failed with error: {e}", level="error")
        finally:
            self.swarm.notify_task_completed(self, result=self.task.get_result())
            self.task = None
            

    async def manage_async_task(self, print_full_result=True):
        """Manage an asynchronous task."""
        current_task = self.task  # Create a reference to the current task
        if current_task is None or current_task.state != TaskState.SCHEDULED:
            self.logger.dprint(f"Invalid async task state for agent '{self.name}'.", level="error")
            return

        try:
            current_task.set_state(TaskState.RUNNING)  # Transition to RUNNING
            result = await current_task.run_task()  # Execute the async task and capture the result
            current_task.set_state(TaskState.COMPLETED)  # Transition to COMPLETED

            if print_full_result:
                self.logger.dprint(f"Async task '{current_task.task_name}' completed by agent '{self.name}'. Result: {result}", level="info")
            else:
                self.logger.dprint(f"Async task '{current_task.task_name}' completed successfully by agent '{self.name}'.", level="info")
        except Exception as e:
            current_task.set_state(TaskState.FAILED)  # Transition to FAILED
            self.logger.dprint(f"Async task '{current_task.task_name}' failed with error: {e}", level="error")
            result = f"Task failed with error: {e}"
        finally:
            self.swarm.notify_task_completed(self, result=result)  # Pass the result to the swarm
            self.task = None  # Reset the agent's task





    async def manage_task(self, print_full_result=True):
        """
        Manage the assigned task.

        Parameters:
        - print_full_result (bool): If True, prints the full result; if False, prints a success message without the full result.
        """
        ##### - Traceback for pesky bugs
        ###
        ##
        stack = traceback.extract_stack()
        if len(stack) > 2:
            # Get the second-to-last stack frame (the caller)
            caller_frame = stack[-3]
            file_name = caller_frame.filename
            line_number = caller_frame.lineno
            caller_name = caller_frame.name
            caller_info = f"[Called from {caller_name} in {file_name}, line {line_number}]"
        else:
            caller_info = "[Caller information not available]"
        ##
        ###
        ##### - End Traceback info build
        if self.task is None:
            self.logger.dprint(f"No task assigned to agent '{self.name}'.", level="critical")
            return "No task to execute."

        try:
            # Validate state and transition to RUNNING
            if self.task.state != TaskState.SCHEDULED:
                self.logger.dprint(f"Task '{self.task.task_name}' in invalid state '{self.task.state}' for execution.", level="error")
                return "Invalid task state for execution."

            self.task.set_state(TaskState.RUNNING)  # Transition to RUNNING

            # Execute the task
            if isinstance(self.task, AsyncAgentTask):
                await self.task.run_task()  # Asynchronous execution
            else:
                self.task.run_task()  # Synchronous execution

            # Transition to COMPLETED after successful execution
            self.task.set_state(TaskState.COMPLETED)

            # Notify the swarm of completion
            result = self.task.get_result()
            self.swarm.notify_task_completed(self, result, print_full_result=print_full_result)

        except Exception as e:
            # Transition to FAILED state on error
            self.task.set_state(TaskState.FAILED)
            self.logger.dprint(f"Task '{self.task.task_name}' failed with error: {e}", level="error")
            raise
       
        
        ##### - Old ProtoCode
        ###
        ##
  
        # if isinstance(self.task, AsyncAgentTask):
        #     await self.task.run_task()  # Asynchronous task
        # else:
        #     self.task.run_task()  # Synchronous task
        # if self.task is None:
        #     self.logger.dprint(f"Task execute task recieved None-Type Object caller: {caller_info}", level="critical")
        #     return "Task was returned as none."

        # result = self.task.get_result()  # Retrieve the result after task completion

        # if print_full_result:
        #     self.logger.dprint(f"Task '{self.task.task_name}' completed by '{self.name}'. Result: {result}", level="info")
        # else:
        #     self.logger.dprint(f"Task '{self.task.task_name}' completed successfully by '{self.name}'", level="info")

        # self.swarm.notify_task_completed(self, result, print_full_result=print_full_result)
  
        ##
        ###
        ##### - End Old ProtoCode

    # Sending Messages (Sync + Async)
    def send_message(self, message, recipient_name=None, group_name=None):
        """Send a message synchronously."""
        self.logger.dprint(f"Agent '{self.name}' sending message: '{message}'", level="info")
        self.swarm.communicate(message, self, recipient_name, group_name)

        # Call the send callback if defined
        if self.send_callback:
            self.send_callback(self.name, message, recipient_name, group_name)

    async def async_send_message(self, message, recipient_name=None, group_name=None):
        """Send a message asynchronously."""
        self.logger.dprint(f"[ASYNC] Agent '{self.name}' sending message: '{message}'", level="info")
        await self.swarm.async_communicate(message, self, recipient_name, group_name)

        # Call the async send callback if defined
        if self.send_callback:
            await self.send_callback(self.name, message, recipient_name, group_name)

    # Receiving Messages (Sync + Async)
    def receive_message(self, message, sender, from_groups=None, to_group=None):
        """Synchronously receive a message."""
        if from_groups is None:
            from_groups = []
        self.logger.dprint(f"Agent '{self.name}' received message from '{sender}' (groups={from_groups}, to_group={to_group}): '{message}'", level="info")

        # Trigger the external receive callback if provided
        if self.message_callback:
            self.message_callback(self.name, message, sender, from_groups, to_group)

    async def async_receive_message(self, message, sender, from_groups=None, to_group=None):
        """Asynchronously receive a message."""
        if from_groups is None:
            from_groups = []
        self.logger.dprint(f"[ASYNC] Agent '{self.name}' received message from '{sender}' (groups={from_groups}, to_group={to_group}): '{message}'", level="info")
        await asyncio.sleep(0)  # Yield control

        if self.message_callback:
            await self.message_callback(self.name, message, sender, from_groups, to_group)
