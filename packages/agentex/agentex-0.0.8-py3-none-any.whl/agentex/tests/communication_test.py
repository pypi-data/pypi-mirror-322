# main.py

import asyncio
import random
import time

# These imports assume you've structured your updated AgentEx code
# within a package named "agentex" that exposes CentralHub, etc.
from agentex import CentralHub
from agentex import Swarm
from exlog import ExLog

import asyncio

# Adjust these imports to match your project structure
from agentex.central_hub import CentralHub
from agentex.swarm import Swarm
from agentex.agent import Agent

def run_sync_demo():
    """
    Demonstrate synchronous usage of the updated messaging logic.
    """
    print("\n[SYNC DEMO]")
    def my_message_handler(agent_name, msg, sender, from_groups, to_group):
        print(f"{agent_name} got message '{msg}' from {sender} in groups {from_groups}.")
        # Here you can parse 'msg', create tasks, or do custom logic:
        if "urgent" in msg.lower():
            print(f"{agent_name} is handling an URGENT message!")
        # 1. Create a logger if needed; otherwise None
    logger = ExLog(1)
    
    # 2. Create a central hub with your updated send_message() methods
    hub = CentralHub(logger=logger)

    # 3. Create two swarms for demonstration
    #    Notice Swarm automatically does `central_hub.register_swarm(self)`
    swarm1 = Swarm(name="Swarm1", central_hub=hub, logger=logger)
    swarm2 = Swarm(name="Swarm2", central_hub=hub, logger=logger)

    # 4. Add Agents to each swarm
    #    The group membership is how Swarm's 'groups' dict is populated
    agent1 = Agent(name="Agent1", group=["GroupAlpha"], logger=logger, message_callback=my_message_handler)
    agent2 = Agent(name="Agent2", group=["GroupBeta"], logger=logger, message_callback=my_message_handler)
    swarm1.add_agent(agent1)
    swarm1.add_agent(agent2)

    agent3 = Agent(name="Agent3", group=["GroupAlpha"], logger=logger, message_callback=my_message_handler)
    agent4 = Agent(name="Agent4", group=["GroupGamma"], logger=logger, message_callback=my_message_handler)
    swarm2.add_agent(agent3)
    swarm2.add_agent(agent4)

    # --- Demonstrate 4 messaging cases (A, B, C, D) ---

    # Case A: Swarm + Group
    print("\n--- Case A: Swarm + Group ---")
    hub.send_message(
        message="Hello GroupAlpha in Swarm2!",
        sender_swarm_name="Swarm1",
        recipient_swarm_name="Swarm2",
        group_name="GroupAlpha"
    )

    # Case B: Swarm Only (no group)
    print("\n--- Case B: Swarm-Only ---")
    hub.send_message(
        message="Hello entire Swarm2!",
        sender_swarm_name="Swarm1",
        recipient_swarm_name="Swarm2"
    )

    # Case C: Group Only (broadcast to all swarms that have this group)
    print("\n--- Case C: Group-Only (GroupAlpha in ANY Swarm) ---")
    hub.send_message(
        message="Hey to GroupAlpha across all swarms!",
        sender_swarm_name="Swarm1",
        group_name="GroupAlpha"
    )

    # Case D: Full broadcast (no swarm, no group)
    print("\n--- Case D: Full Broadcast (no swarm, no group) ---")
    hub.send_message(
        message="Global broadcast to all swarms and all groups!",
        sender_swarm_name="Swarm1"
    )

    print("\n[SYNC DEMO COMPLETE]\n")


async def run_async_demo():
    """
    Demonstrate asynchronous usage of the updated async_send_message() logic.
    """
    print("\n[ASYNC DEMO]")
    async def my_message_handler(agent_name, msg, sender, from_groups, to_group):
        print(f"{agent_name} got message '{msg}' from {sender} in groups {from_groups}.")
        # Here you can parse 'msg', create tasks, or do custom logic:
        if "urgent" in msg.lower():
            print(f"{agent_name} is handling an URGENT message!")
    # or schedule a new task, etc.

    # 1. Create a logger if needed; otherwise None
    logger = ExLog(1)
    
    # 2. Create a central hub with the updated async_send_message() methods
    hub = CentralHub(logger=logger)

    # 3. Create two swarms
    swarm1 = Swarm(name="SwarmA", central_hub=hub, logger=logger)
    swarm2 = Swarm(name="SwarmB", central_hub=hub, logger=logger)

    # 4. Add Agents
    agentA1 = Agent(name="AgentA1", group=["Group1"], logger=logger, message_callback=my_message_handler)
    agentA2 = Agent(name="AgentA2", group=["Group2"], logger=logger, message_callback=my_message_handler)
    swarm1.add_agent(agentA1)
    swarm1.add_agent(agentA2)

    agentB1 = Agent(name="AgentB1", group=["Group1"], logger=logger, message_callback=my_message_handler)
    agentB2 = Agent(name="AgentB2", group=["GroupXYZ"], logger=logger, message_callback=my_message_handler)
    swarm2.add_agent(agentB1)
    swarm2.add_agent(agentB2)

    # --- Demonstrate 4 messaging cases (A, B, C, D) asynchronously ---

    # Case A: Swarm + Group
    print("\n--- Case A: Async Swarm + Group ---")
    await hub.async_send_message(
        message="[ASYNC] Hello Group1 in SwarmB!",
        sender_swarm_name="SwarmA",
        recipient_swarm_name="SwarmB",
        group_name="Group1"
    )

    # Case B: Swarm Only
    print("\n--- Case B: Async Swarm-Only ---")
    await hub.async_send_message(
        message="[ASYNC] Hello entire SwarmB!",
        sender_swarm_name="SwarmA",
        recipient_swarm_name="SwarmB"
    )

    # Case C: Group Only
    print("\n--- Case C: Async Group-Only (Group1 anywhere) ---")
    await hub.async_send_message(
        message="[ASYNC] Hey Group1 in ANY swarm!",
        sender_swarm_name="SwarmA",
        group_name="Group1"
    )

    # Case D: Full broadcast
    print("\n--- Case D: Async Full Broadcast (no swarm, no group) ---")
    await hub.async_send_message(
        message="[ASYNC] Global broadcast to all swarms!",
        sender_swarm_name="SwarmA"
    )

    print("\n[ASYNC DEMO COMPLETE]\n")


def main():
    """Run the sync demo and then the async demo."""
    run_sync_demo()
    asyncio.run(run_async_demo())


if __name__ == "__main__":
    main()
