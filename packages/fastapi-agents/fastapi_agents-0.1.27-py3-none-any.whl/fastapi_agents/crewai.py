from crewai import Crew
from fastapi_agents.models import RequestPayload, BaseAgent
from fastapi_agents.logs import logger

class CrewAIAgent(BaseAgent):
    """
    Adapter class for the CrewAI library for use with FastAPIAgents.
    
    Parameters:
        agent (Crew): The CrewAI crew instance.
    
    Example:
    
        from fastapi_agents.crewai import CrewaiAgent
        from crewai import Crew, Agent, Task
        from crewai.process import Process
        poet = Agent(...)
        write_poem = Task(...)
        crew = Crew(
            agents=[poet],
            tasks=[write_poem],
            process=Process.sequential
        )
        agents.register("poet", CrewAIAgent(crew))
    
    Raises:
        ValueError: If any messages are supplied.
    
    Returns:
        CrewAIAgent: A CrewAI agent.
    """
    def __init__(self, agent: Crew):
        if type(agent) is not Crew:
            raise TypeError('agent must be of type Crew')
        self.agent = agent

    async def run(self, payload: RequestPayload) -> dict:
        validated_payload = RequestPayload(**payload.dict())
        logger.info(f"Validated payload: {validated_payload}")

        # Ensure only one user message is allowed
        if len(validated_payload.messages) > 0:
            raise ValueError("Message inputs are not yet supported for CrewAI. Please set \"messages\":[] in the request body.")

        result = self.agent.kickoff()

        return str(result)

__all__ = ["CrewAIAgent"]
