from crewai import Agent, Task, Crew

response_agent = Agent(
    role="Cybersecurity Response Agent",
    goal="Decide the best response to detected threats",
    backstory="Expert in incident response and network defense.",
    llm="gpt-4",
    verbose=False
)

def run_response_agent(detection_output, analysis_output):

    task = Task(
        description=f"""
        Detection Output:
        {detection_output}

        Analysis Output:
        {analysis_output}

        Decide:
        - Action (block / alert / monitor / ignore)
        - Reason
        - Response plan
        """,
        expected_output="A structured response including action, reasoning, and response plan.",
        agent=response_agent
    )

    crew = Crew(
        agents=[response_agent],
        tasks=[task],
        verbose=False
    )

    return str(crew.kickoff())