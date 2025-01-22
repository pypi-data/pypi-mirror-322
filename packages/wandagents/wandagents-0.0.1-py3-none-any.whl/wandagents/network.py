import autogen

##Need to downgrade autogen to 0.7.0 and install autogen[autobuild] / ag2[autobuild]

##so pip install autogen[autobuild]==0.7.0
class Network:
    def __init__(self, llm_config):
        self.agents = []
        self.llm_config = llm_config
        self.tool_agent = None

        # Initialize base agents
        self.planner = autogen.AssistantAgent(
            name="Planner",
            system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin, until admin approval.
        The plan may involve an engineer who can write code and a scientist who doesn't write code.
        Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
        """,
            llm_config=llm_config,
        )

        self.executor = autogen.UserProxyAgent(
            name="Executor", 
            system_message="Executor. Execute the code written by the engineer and report the result.",
            human_input_mode="NEVER",
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "executor",
                "use_docker": False,
            },
        )

        self.engineer = autogen.AssistantAgent(
            name="Engineer",
            llm_config=llm_config,
            system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. 
            Wrap the code in a code block that specifies the script type. The user can't modify your code. 
            So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
            Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. 
            Check the execution result returned by the executor.
            If the result indicates there is an error, fix the error and output the code again. 
            Suggest the full code instead of partial code or code changes. 
            If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        """,
        )

    def add_agent(self, agent):
        self.agents.append(agent)

    def list_agents(self):
        for agent in self.agents:
            print(f"Network Agent: {agent.name}")

    def add_tool_provider(self, agent):
        self.tool_agent = agent

    def run_initial_task(self, user_prompt):
        user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
            code_execution_config=False,
        )

        groupchat = autogen.GroupChat(
            agents=[user_proxy, self.engineer, self.tool_agent, self.planner, self.executor], messages=[], max_round=50
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        user_proxy.initiate_chat(
            manager,
            message=user_prompt,
        )

    def first_round_investment(self, tool_agent, agent_list, sys_message):
        user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin, Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
            code_execution_config=False,
        )

        # Combine built agents with existing ones
        agents = [user_proxy, self.engineer, tool_agent, self.executor] + agent_list

        groupchat = autogen.GroupChat(agents=agents, messages=[], max_round=50)
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        result = user_proxy.initiate_chat(
            manager,
            message=sys_message,
        )

        return result



