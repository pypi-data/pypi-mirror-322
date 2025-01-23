from exlog import ExLog
from collections import defaultdict

class CentralHub:
    def __init__(self, logger=None):
        self.swarms = {}
        self.logger = logger or ExLog(log_level=1) # You can change this within the instantiation for your own scripts to be silent just set logger=ExLog(log_level=0)

    def register_swarm(self, swarm):
        """Register a swarm."""
        self.swarms[swarm.name] = swarm
        self.logger.dprint(f"Swarm '{swarm.name}' registered.", level="info")

    # def send_message(self, message, sender_swarm_name, recipient_swarm_name, recipient_name=None, group_name=None):
    #     """Synchronously send a message."""
    #     if sender_swarm_name == recipient_swarm_name:
    #         self.logger.dprint("Warning: Cannot send to the same swarm. Ignoring.", level="warning")
    #         return

    #     if recipient_swarm_name in self.swarms:
    #         recipient_swarm = self.swarms[recipient_swarm_name]
    #         recipient_swarm.receive_message_from_swarm(message, sender_swarm_name, recipient_name, group_name)
    #     else:
    #         self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")
   
    def send_message(self, message, sender_swarm_name, recipient_swarm_name=None, group_name=None):
        """
        Synchronously send a message with flexible broadcast logic:

        Case A: (recipient_swarm_name, group_name) -> send to that swarm group
        Case B: (recipient_swarm_name only) -> send to the entire swarm
        Case C: (group_name only) -> broadcast to all swarms that have that group
        Case D: (no recipient_swarm_name, no group_name) -> broadcast to ALL swarms & groups
        """

        # -- Prevent sending to the same swarm if that's undesired. --
        if recipient_swarm_name and (sender_swarm_name == recipient_swarm_name):
            self.logger.dprint("Warning: sender and recipient swarm are the same. Ignoring.", level="warning")
            return

        # Case A: Swarm + Group
        if recipient_swarm_name and group_name:
            if recipient_swarm_name in self.swarms:
                swarm = self.swarms[recipient_swarm_name]
                # Up to the swarm to route internally to the correct group
                swarm.receive_message_from_swarm(
                    message,
                    sender_swarm_name,
                    recipient_name=None,
                    group_name=group_name
                )
            else:
                self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")
            return

        # Case B: Swarm Only
        if recipient_swarm_name and not group_name:
            if recipient_swarm_name in self.swarms:
                swarm = self.swarms[recipient_swarm_name]
                swarm.receive_message_from_swarm(
                    message,
                    sender_swarm_name,
                    recipient_name=None,
                    group_name=None
                )
            else:
                self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")
            return

        # Case C: Group Only (no swarm specified) -> broadcast to all swarms that have this group
        if group_name and not recipient_swarm_name:
            found_group = False
            for swarm_name, swarm_obj in self.swarms.items():
                # Optionally skip the sender swarm if you don't want "local" messages
                # if swarm_name == sender_swarm_name:
                #     continue

                if swarm_obj.has_group(group_name):
                    found_group = True
                    swarm_obj.receive_message_from_swarm(
                        message,
                        sender_swarm_name,
                        recipient_name=None,
                        group_name=group_name
                    )
            if not found_group:
                self.logger.dprint(f"Warning: No swarm found containing group '{group_name}'.", level="warning")
            return

        # Case D: No swarm, no group => broadcast to ALL swarms & ALL groups
        if not recipient_swarm_name and not group_name:
            for swarm_name, swarm_obj in self.swarms.items():
                # Optionally skip the sender swarm
                if swarm_name == sender_swarm_name:
                    continue

                # We pass group_name=None so the swarm can either route it to all groups
                # or handle it in a default/broadcast manner
                swarm_obj.receive_message_from_swarm(
                    message,
                    sender_swarm_name,
                    recipient_name=None,
                    group_name=None
                )
            return

        # If we somehow didn't hit a return above, it's an error in logic
        self.logger.dprint(
            "Error: Unhandled messaging scenario. No valid recipient specified.",
            level="error"
        )

    async def async_send_message(self, message, sender_swarm_name, recipient_swarm_name=None, group_name=None):
        """
        Asynchronously send a message with flexible broadcast logic:

        Case A: (recipient_swarm_name, group_name) -> send to that swarm group
        Case B: (recipient_swarm_name only) -> send to the entire swarm
        Case C: (group_name only) -> broadcast to all swarms that have that group
        Case D: (no recipient_swarm_name, no group_name) -> broadcast to ALL swarms & groups
        """

        # -- Prevent sending to the same swarm if that's undesired. --
        if recipient_swarm_name and (sender_swarm_name == recipient_swarm_name):
            self.logger.dprint("Warning: sender and recipient swarm are the same. Ignoring.", level="warning")
            return

        # Case A: Swarm + Group
        if recipient_swarm_name and group_name:
            if recipient_swarm_name in self.swarms:
                swarm = self.swarms[recipient_swarm_name]
                await swarm.async_receive_message_from_swarm(
                    message,
                    sender_swarm_name,
                    recipient_name=None,
                    group_name=group_name
                )
            else:
                self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")
            return

        # Case B: Swarm Only
        if recipient_swarm_name and not group_name:
            if recipient_swarm_name in self.swarms:
                swarm = self.swarms[recipient_swarm_name]
                await swarm.async_receive_message_from_swarm(
                    message,
                    sender_swarm_name,
                    recipient_name=None,
                    group_name=None
                )
            else:
                self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")
            return

        # Case C: Group Only (no swarm specified) -> broadcast to all swarms that have this group
        if group_name and not recipient_swarm_name:
            found_group = False
            for swarm_name, swarm_obj in self.swarms.items():
                # Optionally skip the sender swarm
                # if swarm_name == sender_swarm_name:
                #     continue

                if swarm_obj.has_group(group_name):
                    found_group = True
                    await swarm_obj.async_receive_message_from_swarm(
                        message,
                        sender_swarm_name,
                        recipient_name=None,
                        group_name=group_name
                    )
            if not found_group:
                self.logger.dprint(f"Warning: No swarm found containing group '{group_name}'.", level="warning")
            return

        # Case D: No swarm, no group => broadcast to ALL swarms & ALL groups
        if not recipient_swarm_name and not group_name:
            for swarm_name, swarm_obj in self.swarms.items():
                # Optionally skip the sender swarm
                if swarm_name == sender_swarm_name:
                    continue

                await swarm_obj.async_receive_message_from_swarm(
                    message,
                    sender_swarm_name,
                    recipient_name=None,
                    group_name=None
                )
            return

        # Unhandled scenario
        self.logger.dprint("Error: Unhandled messaging scenario. No valid recipient specified.", level="error")

    # async def async_send_message(self, message, sender_swarm_name, recipient_swarm_name, recipient_name=None, group_name=None):
    #     """Asynchronously send a message."""
    #     if sender_swarm_name == recipient_swarm_name:
    #         self.logger.dprint("Warning: Cannot send to the same swarm. Ignoring.", level="warning")
    #         return

    #     if recipient_swarm_name in self.swarms:
    #         recipient_swarm = self.swarms[recipient_swarm_name]
    #         await recipient_swarm.async_receive_message_from_swarm(message, sender_swarm_name, recipient_name, group_name)
    #     else:
    #         self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")

