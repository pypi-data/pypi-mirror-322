from fastapi_agents import FastAPIAgents
from fastapi_agents.crewai import CrewAIAgent
from crewai import Agent, Crew, Task, LLM
from crewai.process import Process
import os

# LiteLLM (used by CrewAI) requires the old OpenAI environment variable 
os.environ['OPENAI_API_BASE'] = os.environ['OPENAI_BASE_URL']

# Define the agent
poet = Agent(
    role="Poet",
    goal="Write beautiful poetry.",
    backstory="Experienced poetry, author of 60 poems.",
    verbose=True,
    llm=LLM('openai/gpt-4o')
)

# Define the task
writing_task = Task(
    description="Write a beautiful poem.",
    expected_output="A poem with 3 stanzas.",
    agent=poet
)

# Create a crew with the agent and task
ai_crew = Crew(
    agents=[poet],
    tasks=[writing_task],
    process=Process.sequential,  # Tasks will be executed sequentially
    verbose=True
)

app = FastAPIAgents.as_app(mode='openai')
app.register("crew", CrewAIAgent(ai_crew))
