from .base_task import BaseTask, TaskState
from abc import ABC, abstractmethod

import traceback
class AsyncAgentTask(BaseTask):
    
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass


# Example modification in run_task in async_task.py
    async def run_task(self, *args, **kwargs):
        try:
            if self.agent is None:
                self.log("[CRITICAL - NEW] Agent is None for the current task.", level="critical")
                raise ValueError("Agent not assigned to the task.")

            if self.agent.task is None:
                self.log("[ERROR - NEW] Task is None for the current agent during execution.", level="error")
                raise ValueError("Task reference is None during execution.")

            return await self.execute()
        except Exception as e:
            # Capture and log traceback
            tb = traceback.format_exc()
            self.log(f"[CRITICAL - NEW] Error during task execution: {str(e)}\n{tb}", level="critical")
            raise


    def get_result(self):
        """
        Retrieve the result for async tasks.
        """
        if self.result is None:
            return "Nothing was returned."
        self.log(f"Result: {self.result}", level="debug")

        return self.result

