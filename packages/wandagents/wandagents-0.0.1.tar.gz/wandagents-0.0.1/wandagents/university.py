from autogen.agentchat.contrib.agent_builder import AgentBuilder
import json


class University:
    def __init__(self, llm_config, builder_agent_model, agent_model):
        self.agents = []
        self.llm_config = llm_config
        self.builder_agent_model = builder_agent_model
        self.agent_model = agent_model

    def add_agent(self, agent):
        self.agents.append(agent)

    def list_agents(self):
        for agent in self.agents:
            print(f"University Agent: {agent.name}")

    def build_agents(self, message, ):
        config_path = 'agent_config.json'
        config_list = self.llm_config['config_list']

        with open(config_path, 'w') as f:
            json.dump(config_list, f)

        builder = AgentBuilder(
            config_file_or_env=config_path,
            builder_model=self.builder_agent_model,
            agent_model=self.agent_model
        )

        # Define the building task for investment agents
        # TODO change the hard code here
        building_task = """Create specialized agents for investment analysis and execution:
                1. A planner to coordinate the overall investment strategy and approve plans
                2. A data analyst to analyze market data and provide investment recommendations
                3. An investment executor to implement approved investment plans using provided tools
                The agents should work together to analyze stock data, create investment plans, and execute trades."""

        # Build the agents using AgentBuilder
        agent_list, _ = builder.build(building_task, self.llm_config, coding=True)

        return agent_list
