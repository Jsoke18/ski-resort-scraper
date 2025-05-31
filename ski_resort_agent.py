import os
from dotenv import load_dotenv
import litellm

# === Load environment variables ===
load_dotenv()

# === Setup environment ===
os.environ["LANGCHAIN_VERBOSE"] = "true"
litellm.set_verbose = True
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY") or "77a5c2cf36eac1a2f5ad36b7d21437ae3df1bf96"

from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from api_tools import GetResortsTool, GetAllSkiPassesTool, AssignSkiPassToResortTool

# === Setup LLM with Ollama ===
ollama_llm = LLM(
    model="ollama/gemma3:lastest",
    base_url="http://localhost:11434"
)

# === Tool Setup ===
search_tool = SerperDevTool()
get_resorts_tool = GetResortsTool()
get_all_ski_passes_tool = GetAllSkiPassesTool()
assign_ski_pass_tool = AssignSkiPassToResortTool()

# === Agent ===
ski_pass_manager_agent = Agent(
    role='Ski Pass Database Manager',
    goal=(
        "For a given ski resort (or resorts in a country), identify its major ski passes (e.g., Ikon, Epic) using online research, "
        "then find the corresponding skiPassId from our system's API, and finally assign these passes to the resort(s) in our database via API."
    ),
    backstory=(
        "You are an automated system for keeping the ski resort database up-to-date with the latest ski pass affiliations. "
        "Your process is: 1. Receive a resort name or country. 2. If a country, use GetResortsTool to list resorts. "
        "3. For each target resort, use Serper to research its ski passes. "
        "4. Use GetAllSkiPassesTool to get all ski passes from our system. "
        "5. Match researched pass names to system pass names to get skiPassIds. "
        "6. Use AssignSkiPassToResortTool to link the resort with its passes. "
        "You are precise and ensure all IDs are correctly matched before updating."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool, get_resorts_tool, get_all_ski_passes_tool, assign_ski_pass_tool],
    llm=ollama_llm
)

# === Task ===
# Example: Update passes for a specific resort. You can change this input.
# For a country, you might say: "Update ski pass information for all resorts in Canada listed in our system."
# input_resort_name = "Whistler Blackcomb" # Example input - this would ideally come from your API or a user
# input_resort_id = "your_whistler_resort_id_here" # Example - agent should get this if not provided
input_country = "Canada" # Specifically setting the agent to work on Canadian resorts

# Construct the task description based on available input
if input_country:
    task_description = f"Identify all ski resorts in {input_country} using the GetResortsTool. For each of these resorts, research its major ski passes (like Ikon, Epic) using Serper. Then, use the GetAllSkiPassesTool to fetch all ski passes from our system. Match the researched pass names to the system's pass names to find their skiPassIds. Finally, for each resort and its identified skiPassIds, use the AssignSkiPassToResortTool to update the database. Confirm successful updates for each resort."
    expected_task_output = f"A confirmation summary of all ski pass updates made for resorts in {input_country}. For each resort, list the passes assigned and the outcome of the API call."
elif input_resort_name and input_resort_id:
    task_description = f"For the ski resort named '{input_resort_name}' (ID: {input_resort_id}), research its major ski passes (like Ikon, Epic) using Serper. Then, use the GetAllSkiPassesTool to fetch all ski passes from our system. Match the researched pass names to the system's pass names to find their skiPassIds. Finally, use the AssignSkiPassToResortTool to link the resort with its identified skiPassIds. Confirm the successful update."
    expected_task_output = f"A confirmation message stating whether the ski passes for '{input_resort_name}' (ID: {input_resort_id}) were successfully updated in the database, listing the passes assigned."
else:
    task_description = "The task is not properly configured. Please provide a resort name and ID, or a country."
    expected_task_output = "An error message indicating the task could not be run due to missing input."

update_pass_task = Task(
    description=task_description,
    expected_output=expected_task_output,
    agent=ski_pass_manager_agent,
    # output_file can be added if you want a separate report for this task too
)

# === Crew ===
ski_pass_crew = Crew(
    agents=[ski_pass_manager_agent],
    tasks=[update_pass_task],
    process=Process.sequential,
    verbose=True
)

# === Execute ===
if __name__ == "__main__":
    print("Starting the ski pass update crew...")
    print("Ensure Ollama is running (http://localhost:11434) with the model pulled.")
    print(f"Using Ollama model: {ollama_llm.model}")
    if not os.getenv("YOUR_API_BASE_URL_IN_API_TOOLS_PY"): # A reminder to set it in api_tools.py
        print("IMPORTANT: Remember to set YOUR_API_BASE_URL in api_tools.py before running!")
    if not os.getenv("SERPER_API_KEY"):
        print("Error: SERPER_API_KEY not found. Please set it in your .env or environment.")
        # exit(1) # You might want to exit if essential keys are missing

    if "task is not properly configured" in task_description:
        print(f"Error: {task_description}")
    else:
        try:
            result = ski_pass_crew.kickoff()
            print("\n\n########################")
            print("## Ski Pass Update Crew Results")
            print("########################\n")
            print(result)
        except Exception as e:
            print(f"❌ Error running the crew: {e}")
