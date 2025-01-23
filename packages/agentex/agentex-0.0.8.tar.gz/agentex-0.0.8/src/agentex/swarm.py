import asyncio
from collections import defaultdict, deque
from exlog import ExLog
from .central_hub import CentralHub
from .agent import Agent
from .tasks import AgentTask, AsyncAgentTask, TaskState, TaskStateTransitionError


class Swarm:
    def __init__(self, name, central_hub, logger=None):
        self.name = name
        self.central_hub = central_hub
        self.agents = []  # List of agents in the swarm
        self.groups = defaultdict(list)  # Dictionary for agent groups
        self.task_queue = deque()  # Task queue for the swarm
        self.agent_queue = deque()  # Queue of available agents
        self.logger = logger or ExLog(log_level=1) # You can change this within the instantiation for your own scripts to be silent just set logger=ExLog(log_level=0)
        central_hub.register_swarm(self)  # Register the swarm with the central hub
    
    def has_group(self, group_name):
        return group_name in self.groups  # Adjust if you store groups differently

    def schedule_task(self, task, agent):
        """
        Schedule a task for an agent.
        Currently a placeholder method that can be expounded upon.
        Right now it just marks the task as scheduled from queued.
        """
        if task.state != TaskState.QUEUED:
            self.logger.dprint(f"Task '{task.task_name}' not in QUEUED state. Cannot schedule.", level="warning")
            return

        try:
            task.set_state(TaskState.SCHEDULED)  # Transition to SCHEDULED
            self.logger.dprint(f"Task '{task.task_name}' scheduled for agent '{agent.name}'.", level="info")
            agent.assign_task(task)  # Hand over the task to the agent
        except TaskStateTransitionError as e:
            self.logger.dprint(f"Failed to schedule task '{task.task_name}' for agent '{agent.name}': {e}", level="error")
            self.task_queue.append(task)  # Requeue the task

    def prioritize_tasks(self):
        """Reorder the global task queue based on priority number."""
        self.task_queue = deque(sorted(self.task_queue, key=lambda t: t.priority, reverse=True))

    def add_agent(self, agent):
        """Add an agent to the swarm."""
        self.agents.append(agent)
        for grp in agent.groups:
            self.groups[grp].append(agent)
        agent.set_swarm(self)
        self.agent_queue.append(agent)
        self.logger.dprint(f"Agent '{agent.name}' added to Swarm '{self.name}'.", level="info")

    # --- Synchronous Communication ---
    def communicate(self, message, sender, recipient_name=None, group_name=None):
        """Synchronously send message to agents within the swarm."""
        self.logger.dprint(f"Swarm '{self.name}' sending message: '{message}'", level="info")
        self._handle_message(message, sender, recipient_name, group_name)

    async def async_communicate(self, message, sender, recipient_name=None, group_name=None):
        """Asynchronously send message to agents within the swarm."""
        self.logger.dprint(f"[ASYNC] Swarm '{self.name}' sending message: '{message}'", level="info")
        await self._async_handle_message(message, sender, recipient_name, group_name)

    def _handle_message(self, message, sender, recipient_name=None, group_name=None):
        """Internal helper to handle synchronous message communication."""
        sender_name, sender_groups = self._get_sender_info(sender)

        if recipient_name:
            for agent in self.agents:
                if agent.name == recipient_name:
                    agent.receive_message(message, sender_name, sender_groups, recipient_name)
                    return

        elif group_name:
            if group_name not in self.groups:
                self.logger.dprint(f"Group '{group_name}' not found in Swarm '{self.name}', broadcasting to all.", level="warning")
                self.broadcast_entire_swarm(message, sender_name, sender_groups)
            else:
                for agent in self.groups[group_name]:
                    if agent.name != sender_name:
                        agent.receive_message(message, sender_name, sender_groups, group_name)
        else:
            self.broadcast_entire_swarm(message, sender_name, sender_groups)

    async def _async_handle_message(self, message, sender, recipient_name=None, group_name=None):
        """Internal helper to handle asynchronous message communication."""
        sender_name, sender_groups = self._get_sender_info(sender)

        if recipient_name:
            for agent in self.agents:
                if agent.name == recipient_name:
                    await agent.async_receive_message(message, sender_name, sender_groups, recipient_name)
                    return

        elif group_name:
            if group_name not in self.groups:
                self.logger.dprint(f"[ASYNC] Group '{group_name}' not found in Swarm '{self.name}', broadcasting to all.", level="warning")
                await self.async_broadcast_entire_swarm(message, sender_name, sender_groups)
            else:
                for agent in self.groups[group_name]:
                    if agent.name != sender_name:
                        await agent.async_receive_message(message, sender_name, sender_groups, group_name)
        else:
            await self.async_broadcast_entire_swarm(message, sender_name, sender_groups)

    def receive_message_from_swarm(self, message, sender_swarm_name, recipient_name=None, group_name=None):
        """Receive a message from another swarm (synchronous)."""
        self.logger.dprint(f"Swarm '{self.name}' received message from Swarm '{sender_swarm_name}': '{message}'", level="info")
        self.communicate(message, sender_swarm_name, recipient_name, group_name)

    async def async_receive_message_from_swarm(self, message, sender_swarm_name, recipient_name=None, group_name=None):
        """Receive a message from another swarm (asynchronous)."""
        self.logger.dprint(f"[ASYNC] Swarm '{self.name}' received async message from Swarm '{sender_swarm_name}': '{message}'", level="info")
        await self.async_communicate(message, sender_swarm_name, recipient_name, group_name)

    def broadcast_entire_swarm(self, message, sender_name, sender_groups):
        """Synchronously broadcast a message to the entire swarm."""
        for agent in self.agents:
            if agent.name != sender_name:
                agent.receive_message(message, sender_name, sender_groups, None)
        self.logger.dprint(f"Broadcasted message '{message}' to all agents in Swarm '{self.name}'.", level="info")

    async def async_broadcast_entire_swarm(self, message, sender_name, sender_groups):
        """Asynchronously broadcast a message to the entire swarm."""
        for agent in self.agents:
            if agent.name != sender_name:
                await agent.async_receive_message(message, sender_name, sender_groups, None)
        self.logger.dprint(f"[ASYNC] Broadcasted message '{message}' to all agents in Swarm '{self.name}'.", level="info")

    def send_message_to_swarm(self, message, recipient_swarm_name, from_swarm_group_name=None, recipient_name=None, group_name=None):
        """Send message to another swarm synchronously."""
        if self.name == recipient_swarm_name:
            self.communicate(message, self.name, recipient_name, group_name)
        else:
            self.logger.dprint(f"Swarm '{self.name}' sending message to Swarm '{recipient_swarm_name}': '{message}'", level="info")
            self.central_hub.send_message(message, self.name, recipient_swarm_name, recipient_name, group_name)

    async def async_send_message_to_swarm(self, message, recipient_swarm_name, from_swarm_group_name=None, recipient_name=None, group_name=None):
        """Send message to another swarm asynchronously."""
        if self.name == recipient_swarm_name:
            await self.async_communicate(message, self.name, recipient_name, group_name)
        else:
            self.logger.dprint(f"[ASYNC] Swarm '{self.name}' sending message to Swarm '{recipient_swarm_name}': '{message}'", level="info")
            await self.central_hub.async_send_message(message, self.name, recipient_swarm_name, recipient_name, group_name)

    def add_task(self, task):
        """Add a task to the task queue and attempt to distribute tasks."""
        self.task_queue.append(task)
        self.logger.dprint(f"Task '{task.task_name}' added to Swarm '{self.name}'.", level="info")
        if isinstance(task, AsyncAgentTask):
            asyncio.create_task(self.async_distribute_tasks())  # Async distribution
        else:
            self.distribute_tasks()  # Sync distribution

    def distribute_tasks(self):
        """Synchronously distribute tasks to available agents."""
        while self.task_queue and self.agent_queue:
            print(f"in the task distribute func sync")

            # Check for valid task and agent
            if not self.task_queue or not self.agent_queue:
                self.logger.dprint("No tasks or agents available for distribution.", level="warning")
                break

            task = self.task_queue.popleft()
            agent = self.agent_queue.popleft()

            # Check if the dequeued object is a valid task
            if not isinstance(task, AgentTask):
                self.logger.dprint(f"Invalid task object: {task}. Requeuing agent '{agent.name}'.", level="error")
                self.agent_queue.append(agent)  # Requeue the agent
                continue

            # Ensure task is in QUEUED state
            if task.state != TaskState.QUEUED:
                self.logger.dprint(f"Skipping task '{task.task_name}' in invalid state '{task.state}'. Requeuing.", level="debug")
                self.task_queue.append(task)  # Requeue the task
                self.agent_queue.append(agent)  # Requeue the agent
                continue

            # Transition task to SCHEDULED
            try:
                task.set_state(TaskState.SCHEDULED)
            except TaskStateTransitionError as e:
                self.logger.dprint(f"Failed to schedule task '{task.task_name}': {e}", level="error")
                self.task_queue.append(task)  # Requeue the task
                self.agent_queue.append(agent)  # Requeue the agent
                continue

            # Assign task to agent
            agent.assign_task(task)
            self.logger.dprint(f"Assigned sync task '{task.task_name}' to agent '{agent.name}'.", level="info")



    async def async_distribute_tasks(self):
        """Asynchronously distribute tasks to available agents."""
        while self.task_queue and self.agent_queue:
            print(f"in the task distribute func async")

            # Check for valid task and agent
            if not self.task_queue or not self.agent_queue:
                self.logger.dprint("No tasks or agents available for distribution.", level="warning")
                break

            task = self.task_queue.popleft()
            agent = self.agent_queue.popleft()

            # Check if the dequeued object is a valid task
            if not isinstance(task, AsyncAgentTask):
                self.logger.dprint(f"Invalid async task object: {task}. Requeuing agent '{agent.name}'.", level="error")
                self.agent_queue.append(agent)  # Requeue the agent
                continue

            # Ensure task is in QUEUED state
            if task.state != TaskState.QUEUED:
                self.logger.dprint(f"Skipping async task '{task.task_name}' in invalid state '{task.state}'. Requeuing.", level="debug")
                self.task_queue.append(task)  # Requeue the task
                self.agent_queue.append(agent)  # Requeue the agent
                continue

            # Transition task to SCHEDULED
            try:
                task.set_state(TaskState.SCHEDULED)
            except TaskStateTransitionError as e:
                self.logger.dprint(f"Failed to schedule async task '{task.task_name}': {e}", level="error")
                self.task_queue.append(task)  # Requeue the task
                self.agent_queue.append(agent)  # Requeue the agent
                continue

            # Assign task to agent asynchronously
            await agent.async_assign_task(task)
            self.logger.dprint(f"[ASYNC] Assigned async task '{task.task_name}' to agent '{agent.name}'.", level="info")



    def notify_task_completed(self, agent, result, print_full_result=True):
        """Synchronously notify that a task is completed."""
        if print_full_result:
            self.logger.dprint(f"Agent '{agent.name}' completed sync task. Result: {result}", level="info")
        else:
            self.logger.dprint(f"Agent '{agent.name}' completed sync task.", level="info")
        
        if agent.task:
            agent.task = None

        self.agent_queue.append(agent)
        self.distribute_tasks()

    async def async_notify_task_completed(self, agent, result, print_full_result=True):
        """Asynchronously notify that an async task is completed."""
        if print_full_result:
            self.logger.dprint(f"Agent '{agent.name}' completed async task. Result: {result}", level="info")
        else:
            self.logger.dprint(f"Agent '{agent.name}' completed async task.", level="info")
        if agent.task:
            agent.task = None


        self.agent_queue.append(agent)
        await self.async_distribute_tasks()

    def _get_sender_info(self, sender):
        """Get sender's name and groups."""
        if isinstance(sender, Agent):
            return sender.name, sender.groups[:]
        return sender, []

