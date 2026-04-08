"""automated persona generation pipeline"""

import os
import json
from groq import Groq

#LLM PREP AND JSON READING:
#Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#Load cleaned dataset
reviews = []
with open("../data/reviews_clean.jsonl", "r") as f:
    for line in f:
        reviews.append(json.loads(line))

#Load prompt auto
with open("../prompts/prompt_auto.json", "r") as f:
    promptAuto = json.load(f)["prompt"]

#Take a subset because of limits
reviewsSubset = reviews[:600]

#Format reviews for prompt
formattedReviews = ""
for r in reviewsSubset:
    formattedReviews += f"{r['reviewId']}: {r['content']}\n"

#Full prompt to send to LLM
fullPrompt = promptAuto.replace("{reviews}", formattedReviews)

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

#4.1 GENERATE GROUPS:
llmOutput = get_completion(fullPrompt)

#Parse JSON output from LLM
groups = json.loads(llmOutput)

#Write groups
with open("../data/review_groups_auto.json", "w") as f:
    json.dump(groups, f, indent=2)

#------------------------------------------------------------------

#4.2 PERSONA GENERATION:
#Load review groups from previous step
with open("../data/review_groups_auto.json", "r") as f:
    reviewGroups = json.load(f)["groups"]

#Prompt for persona generation
promptAuto = """
You are generating a user persona based on mental wellbeing app reviews that have been put into a group by similarity for you.

Given the following group:
{group}

Generate ONE persona in JSON format for the group with the following structure (Output ONLY valid JSON in the following format):

{
  "id": "P#",
  "name": "",
  "description": "",
  "derived_from_group": "",
  "goals": [],
  "pain_points": [],
  "context": [],
  "constraints": [],
  "evidence_reviews": []
}

Rules:
- id should be in format P1, P2, etc.
- derived_from_group must match the group_id
- evidence_reviews must be taken from the group's review_ids
- goals, pain_points, context, constraints should each have 2-4 items
- Keep descriptions concise but meaningful
- Please output the persona as JSON only, do NOT include ```json or any markdown formatting. The JSON must start with { and be valid.
"""

#GENERATE PERSONAS:
allPersonas = []
personaCounter = 1

#Pass each group individually
for group in reviewGroups:

    #group structure
    groupInfo = f"""
    Group ID: {group['group_id']}
    Theme: {group['theme']}
    Review IDs: {group['review_ids']}
    Example Reviews: {group['example_reviews']}
    """

    #pass the current group into the prompt
    fullPrompt = promptAuto.replace("{group}", groupInfo)
    llmOutput = get_completion(fullPrompt)

    #Ensure id is correct for each persona and appends to the full personas list
    persona = json.loads(llmOutput)
    persona["id"] = f"P_auto_{personaCounter}"
    personaCounter += 1
    allPersonas.append(persona)

#Write personas
with open("../personas/personas_auto.json", "w") as f:
    json.dump({"personas": allPersonas}, f, indent=2)