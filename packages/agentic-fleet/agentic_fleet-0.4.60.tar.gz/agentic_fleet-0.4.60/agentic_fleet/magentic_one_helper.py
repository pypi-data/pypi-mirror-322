import asyncio
import logging
import os
import tempfile
from typing import Any, AsyncGenerator, Dict, List, Optional

from autogen_agentchat.agents import CodeExecutorAgent
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_core import AgentId, AgentProxy, DefaultTopicId, SingleThreadedAgentRuntime
from autogen_ext.agents.file_surfer import FileSurfer
from autogen_ext.agents.magentic_one import MagenticOneCoderAgent
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.code_executors.azure import ACADynamicSessionsCodeExecutor
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from promptflow.tracing import start_trace

load_dotenv()



azure_credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    azure_credential, "https://cognitiveservices.azure.com/.default"
)

#You can view the traces in http://127.0.0.1:23333/v1.0/ui/traces/
start_trace()


class MagenticOneHelper:
    def __init__(self, logs_dir: str = True, save_screenshots: bool = True, run_locally: bool = False) -> None:
        """
        A helper class to interact with the MagenticOne system.
        Initialize MagenticOne instance.

        Args:
            logs_dir: Directory to store logs and downloads
            save_screenshots: Whether to save screenshots of web pages
        """
        self.logs_dir = logs_dir or os.getcwd()
        self.runtime: Optional[SingleThreadedAgentRuntime] = None
        # self.log_handler: Optional[LogHandler] = None
        self.save_screenshots = save_screenshots
        self.run_locally = run_locally

        self.max_rounds = 50
        self.max_time = 25 * 60
        self.max_stalls_before_replan = 5
        self.return_final_answer = True
        self.start_page = "https://www.bing.com"

        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    async def initialize(self, agents) -> None:
        """
        Initialize the MagenticOne system, setting up agents and runtime.
        """
        # Create the runtime
        self.runtime = SingleThreadedAgentRuntime()

        self.client = AzureOpenAIChatCompletionClient(
            model="gpt-4o-2024-11-20",
            azure_deployment="gpt-4o-fleet",
            api_version="2024-08-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_ad_token_provider=token_provider,
            model_info={
                "vision": True,
                "function_calling": True,
                "json_output": True,
            }
        )

        # Set up agents
        self.agents = await self.setup_agents(agents, self.client, self.logs_dir) 

        print("Agents setup complete!")

    async def setup_agents(self, agents, client, logs_dir):
        agent_list = []
        for agent in agents:
            # This is default MagenticOne agent - Coder
            if (agent["type"] == "MagenticOne" and agent["name"] == "Coder"):
                coder = MagenticOneCoderAgent("Coder", model_client=client)
                agent_list.append(coder)
                print("Coder added!")

            # This is default MagenticOne agent - Executor
            elif (agent["type"] == "MagenticOne" and agent["name"] == "Executor"):
                # hangle local = local docker execution
                if self.run_locally:
                    #docker
                    code_executor = DockerCommandLineCodeExecutor(work_dir=logs_dir)
                    await code_executor.start()

                    executor = CodeExecutorAgent("Executor", code_executor=code_executor)

                # or remote = Azure ACA Dynamic Sessions execution
                else:
                    pool_endpoint=os.getenv("POOL_MANAGEMENT_ENDPOINT")
                    assert pool_endpoint, "POOL_MANAGEMENT_ENDPOINT environment variable is not set"
                    with tempfile.TemporaryDirectory() as temp_dir:
                        executor = CodeExecutorAgent("Executor", code_executor=ACADynamicSessionsCodeExecutor(pool_management_endpoint=pool_endpoint, credential=azure_credential, work_dir=temp_dir))


                agent_list.append(executor)
                print("Executor added!")

            # This is default MagenticOne agent - WebSurfer
            elif (agent["type"] == "MagenticOne" and agent["name"] == "WebSurfer"):
                web_surfer = MultimodalWebSurfer("WebSurfer", model_client=client)
                agent_list.append(web_surfer)
                print("WebSurfer added!")

            # This is default MagenticOne agent - FileSurfer
            elif (agent["type"] == "MagenticOne" and agent["name"] == "FileSurfer"):
                file_surfer = FileSurfer("FileSurfer", model_client=client)
                agent_list.append(file_surfer)
                print("FileSurfer added!")


        return agent_list

    def main(self, task):
        team = MagenticOneGroupChat(
            participants=self.agents,
            model_client=self.client,
            max_turns=self.max_rounds,
            max_stalls=self.max_stalls_before_replan,

        )
        stream = team.run_stream(task=task)
        return stream