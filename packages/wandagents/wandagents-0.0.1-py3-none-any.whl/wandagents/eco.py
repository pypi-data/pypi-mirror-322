import autogen

class Economy:
    def __init__(self, llm_config):
        self.agents = []
        self.llm_config = llm_config

    def add_agent(self, agent):
        self.agents.append(agent)

    def list_agents(self):
        for agent in self.agents:
            print(f"Economy Agent: {agent.name}")


    def provide_tool_agent(self):

        ## TODO Hard code here
        tool_agent = autogen.AssistantAgent(
            name="Tool_provider",
            llm_config=self.llm_config,
            system_message="""Tool_provider. You are expert in Python and related python package, 
            if one engineer need the Yahoo finance data, you provide python function from yahoo-finance package for him, and need engineer to install the yahoo-financ package at first.
            You don't write code.""",
        )

        return tool_agent