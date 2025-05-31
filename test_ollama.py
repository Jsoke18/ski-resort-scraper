from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process

# Step 1: Set up the Ollama LLM
ollama_llm = Ollama(model="ollama/deepseek-r1:latest")  # You can replace with any model you have like 'mistral', 'codellama', etc.

# Step 2: Create an agent
agent = Agent(
    role='Fun Fact Generator',
    goal='Generate interesting random facts for users',
    backstory='You are a trivia enthusiast who loves surprising people with amazing knowledge.',
    verbose=True,
    llm=ollama_llm,  # 🔥 Here we use Ollama
    allow_delegation=False,
)

# Step 3: Create a task
task = Task(
    description='Generate 5 fun facts about space exploration.',
    expected_output='A bullet point list of 5 fun facts about space.',
    agent=agent,
)

# Step 4: Create the crew
crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential
)

# Step 5: Run it
result = crew.kickoff()
print(result)
