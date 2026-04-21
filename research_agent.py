from crewai import Agent, Task, Crew

research_agent = Agent(
    role="Cybersecurity Research Analyst",
    goal="Analyze network threats and explain their behavior clearly",
    backstory="Expert in intrusion detection and network attack analysis.",
    llm="gpt-4",
    verbose=False
)

def run_research_agent(detection_output, analysis_output):

    task = Task(
        description=f"""
        Detection Output:
        {detection_output}

        Analysis Output:
        {analysis_output}

        Explain:
        - Attack type
        - Why it's dangerous
        - Key indicators
        - Severity
        """,
        expected_output="A concise explanation of the attack, its risks, indicators, and severity level.",
        agent=research_agent
    )

    crew = Crew(
        agents=[research_agent],
        tasks=[task],
        verbose=False
    )

    return str(crew.kickoff())