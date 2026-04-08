"""generates tests from specs"""

import os
import json
from groq import Groq

#LLM PREP:
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Function to call LLM
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

#Load requirements (markdown file
with open("../spec/spec_auto.md", "r") as f:
    specText = f.read()

#Extract requirement IDs
lines = specText.split("\n")
requirementIDs = []

for line in lines:
    if line.startswith("# Requirement ID:"):
        reqId = line.replace("# Requirement ID:", "").strip()
        requirementIDs.append(reqId)

#Prompt for test generation
promptAuto = """
You are generating a validation test scenario for a software requirement in a mental wellbeing app.

Given the following requirement ID:
{req_id}

Generate ONE test scenario in JSON format for the requirement with the following structure (Output ONLY valid JSON in the following format):

{
  "test_id": "T_auto_#",
  "requirement_id": "{req_id}",
  "scenario": "",
  "steps": [
  "step one",
  "step two",
  "step three",
  etc
  ],
  "expected_result": ""
}

Rules:
- test_id must be T_auto_1, T_auto_2, etc.
- scenario should briefly describe what is being tested
- steps must be clear, sequential, and 2-4 steps long, and MUST FOLLOW the exact format exactly for EVERY test outlined above
- expected_result must clearly validate the requirement
- Please output the test as JSON only, do NOT include ```json or any markdown formatting. The JSON must start with { and be valid.
"""

#GENERATE TESTS:
allTests = []
testCounter = 1

#pass each requirement indivdually
for reqId in requirementIDs:

    fullPrompt = promptAuto.replace("{req_id}", reqId)

    llmOutput = get_completion(fullPrompt)

    #ensure test id is correct    
    test = json.loads(llmOutput)
    test["test_id"] = f"T_auto_{testCounter}"
    testCounter += 1
    allTests.append(test)
    
#Write tests
with open("../tests/tests_auto.json", "w") as f:
    json.dump({"tests": allTests}, f, indent=2)