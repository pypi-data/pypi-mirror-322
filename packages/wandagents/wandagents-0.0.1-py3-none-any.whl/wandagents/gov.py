import autogen

class Government:
    def __init__(self, llm_config):
        self.agents = []
        self.llm_config = llm_config

        self.government = autogen.AssistantAgent(
            name="Government",
            llm_config=llm_config,
            description="Government_Expert periodically communicates with Planner and is responsible in overseeing Planner's deployment of agents, optimizing resources (agents, tools and datasets) with University_Expert, managing a budget `B`, finding inefficiencies in agent deployment and detecting agent skill gaps.",
            system_message="""## Your role\nGovernment_Expert is a dedicated professional highly skilled in understanding steps and processes to complete any project given to Planner, knowing what agents are available to deploy for each project, managing project budgets, projecting project cashflows into the future to avoid running out of money and analysing agent capabilities to continuously improve project outcomes.\n\n## Task and skill instructions\n- Overall: As an expert in governing projects given to Planner, the Government_Expert is tasked in making sure that (1) the project given to Panner does not run out of budget by analysing the cost of a project, (2) reporting Planner which agents are available now, (3) reporting to Planner which agents can be trained in the future, (4) diagonizing project performance, (5) identifying agent knowledge, skill or tool gaps to continuously improve performance.\n- Managing budgets and costs: the Government_Expert knows that using an agent to perform a substask cost $1, training new agents costs $100, using a tool, API or datasets cost $10 and deduct is cost from the budget `B` but may also add cash inflows to increase budget `B`.\n- Overseeing Planner's project: the Government_Expert will (1) provide feedback on the initial plan by Planner, (2) communicate with Planner which agents `A`, tools `T`, datasets `D` are currently available to Planner, (3) establish performance metrics and performance review periods with Planner and (4) provide feedback on an initial plan, (5) ask Planner to update the initial plan if needed.\n- Providing feedback to Planner: during periodic review of project performance, Government_Expert will discuss with Planner  project progress and identfy with Planner improvement areas in project performance based on agreed upon performance metrics. The Government_Expert must project future costs to manage budgets and decide which resources (agents, tools and datasets) to continue using, to stop using or to ask for to University_Expert for future deployment.\n- Identifying agent knowledge, skill or tool gaps: The Government_Expert will diagonize where agent knowledge, skill or tool gaps occur in a project by doing root cause analysis, process improvement analysis and make future project performance projections.\n- Deciding in deploying new resources: if existing agents new resources (knowledege, skills or tools) to better perform their given tasks, Government_Expert must first identify such resource gap and discuss with University_expert if the resources can be obtained and the expected agent performance increase.\n\n## Useful instructions for governing projects\n- Follow the instruction provided by the user.\n- Discuss issues and progress with Planner during performance review periods.\n- If a plan is not provided, explain your plan first.\n- If the project is below performance expectations or the budget is about to run out, analyze the problem, revisit your assumptions, collect additional info you need, and think of a different plan to try.\n- When you find an answer, verify the answer carefully.\n- Include verifiable evidence in your response if possible."""
        )

        self.government_assistant = autogen.AssistantAgent(
            name="Government_Assistant",
            llm_config=llm_config,
            description="You summarize interactions between the Planner and the University as well as important project milestones such as project performance, user satisfaction"
        )

    def add_agent(self, agent):
        self.agents.append(agent)

    def list_agents(self):
        for agent in self.agents:
            print(f"Government Agent: {agent.name}")

    def performance_review(self, planner, sys_message):
        groupchat = autogen.GroupChat(
            agents=[planner, self.government, self.government_assistant], messages=[], max_round=5
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        result = self.government_assistant.initiate_chat(
            manager,
            message=sys_message
        )
        return result
