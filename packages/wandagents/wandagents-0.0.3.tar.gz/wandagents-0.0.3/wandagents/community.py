from wandagents.network import Network
from wandagents.university import  University
from wandagents.gov import Government
from wandagents.eco import Economy
# write a class to group eco, gov, network, univeristy together


class Community:
    def __init__(self, name):
        self.name = name
        self.university = None
        self.economy = None
        self.network = None
        self.government = None
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def list_members(self):
        for member in self.members:
            print(f"Community Member: {member.name}")

    def build_community(self, llm_config):
        network = Network(llm_config, True)
        government = Government(llm_config)
        university = University(llm_config)
        economy = Economy(llm_config)

        self.set_component('economy', economy)
        self.set_component('government', government)
        self.set_component('network', network)
        self.set_component('university', university)

        self.add_member(network)
        self.add_member(government)
        self.add_member(university)
        self.add_member(economy)

    def set_component(self, component_name, component_instance):
        """
        Sets a component (economy, government, network, university) dynamically.
        Args:
            component_name (str): Name of the component to set.
            component_instance: Instance of the component.
        """
        if hasattr(self, component_name):
            setattr(self, component_name, component_instance)
        else:
            raise AttributeError(f"Invalid component name: {component_name}")

    def execute_user_prompt(self, prompt):
        # get the Agent List from University
        agent_list = self.university.build_agents(prompt)

        # get the Agent List from Eco
        tool_agents = self.economy.build_agents(prompt)

        # get the Agent List from Gov
        government_agent = self.government.build_agents(prompt)

        # TODO: Add the government agent to the network

        # network to run the agents talking to each other
        result = self.network.run_group_chat(tool_agents, agent_list, prompt)

        return result

    def summary_of_result(self):
        summary = ""
        return summary
