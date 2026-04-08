"""generates structured specs from personas"""

import os
import json
from groq import Groq

#LLM PREP AND JSON READING:
#Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Function to call LLM (prompt eng lab)
def get_completion(prompt, model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.0):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Load personas
with open("../personas/personas_auto.json", "r") as f:
    personas = json.load(f)["personas"]

#Prompt for requirements generation
promptAuto = """
You are generating a structured software requirement from a user persona for a mental wellbeing app.

Given the following persona:
{persona}

Generate ONE requirement in the following EXACT format (no extra text):

# Requirement ID: {req_id}
- Description: [The system shall ...]
- Source Persona: [{persona_name}]
- Traceability: [Derived from review group {group_id}]
- Acceptance Criteria: [Given ..., When ..., Then ...]

Rules:
- Description must start with "The system shall" and describe one concrete, testable behavior
- Base the requirement on the persona's goals and pain points
- Acceptance Criteria must follow the Given/When/Then format exactly
- Keep each field to 1-2 sentences
- Output ONLY the requirement block above, no markdown fences, no extra commentary
"""

#GENERATE SPECIFICATIONS:
allRequirements = []
reqCounter = 1

#Pass each persona individually
for persona in personas:

    #Persona structure
    personaInfo = f"""
    Persona ID: {persona['id']}
    Name: {persona['name']}
    Description: {persona['description']}
    Derived From Group: {persona['derived_from_group']}
    Goals: {persona['goals']}
    Pain Points: {persona['pain_points']}
    Context: {persona['context']}
    Constraints: {persona['constraints']}
    """

    #Imbedded loop to create two requirements per persona to reach 10 requirements
    for _ in range(2):

        reqId = f"FR_auto_{reqCounter}"
        personaSpecific = f"{persona['name']} - {persona['id']}"

        #Specifically replace key information in prompt for better output
        fullPrompt = (
            promptAuto
            .replace("{persona}", personaInfo)
            .replace("{req_id}", reqId)
            .replace("{persona_name}", personaSpecific)
            .replace("{group_id}", persona['derived_from_group'])
        )

        llmOutput = get_completion(fullPrompt)
        reqCounter += 1
        allRequirements.append(llmOutput.strip())

#Write specs
with open("../spec/spec_auto.md", "w") as f:
    f.write("# Auto Requirements Specification\n")
    f.write("\n")
    f.write("\n\n".join(allRequirements))