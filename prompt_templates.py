from langchain.prompts import PromptTemplate

# Prompt template for the general chat phase (after collecting initial info)
chat_prompt_for_llm = PromptTemplate(
    input_variables=["history", "user_input"],
    template="""
You are a strict and professional hiring assistant helping candidates through an initial screening chat.
Use the previous conversation to maintain context and respond appropriately.

=== Conversation History ===
{history}

=== User's Latest Message ===
{user_input}

=== Your Response ===
"""
)

# Prompt template for generating technical questions
question_prompt = PromptTemplate(
    input_variables=["tech_stack"],
    template="""
You are an expert technical interviewer.

Generate 3 concise, clear technical interview questions to assess a candidate's proficiency in the following technologies:

{tech_stack}

Format them as a numbered list.
"""
)

# Prompt for validating tech stack
validate_tech_stack_prompt = PromptTemplate(
    input_variables=["value"],
    template="""
You are an AI assistant validating a list of technologies.
Review the following text: "{value}"

Is this a valid and recognizable list of technical skills or technologies?
Be strict and ensure it refers to actual technologies (e.g., programming languages, frameworks, databases, tools).

If it is a valid list, respond ONLY with the word "YES".
If it is NOT a valid list (e.g., just random words, a general statement not about tech, or gibberish), respond ONLY with "NO" and a brief, concise explanation why.

Examples:
Input: Python, JavaScript, React, SQL, AWS
Output: YES

Input: I like to code.
Output: NO - Not a list of technologies.

Input: running jumping coding
Output: NO - Not recognizable technologies.
"""
)

# Prompt for validating desired position
validate_position_prompt = PromptTemplate(
    input_variables=["value"],
    template="""
You are an AI assistant validating a job position title.
Review the following text: "{value}"

Is this a valid and recognizable job position or role that typically exists in the tech industry?
Be strict.

If it is a valid position, respond ONLY with the word "YES".
If it is NOT a valid position (e.g., gibberish, too general, or clearly not a job title), respond ONLY with "NO" and a brief, concise explanation why.

Examples:
Input: Software Engineer
Output: YES

Input: Senior Data Scientist
Output: YES

Input: Coding person
Output: NO - Too informal for a job title.

Input: XYZ Developer
Output: NO - "XYZ" is not a recognized technology or domain.
"""
)

# Prompt for validating location
validate_location_prompt = PromptTemplate(
    input_variables=["value"],
    template="""
You are an AI assistant validating a geographical location.
Review the following text: "{value}"

Is this a valid and recognizable real-world geographical location (city, state/region, country, or a well-known area)?
Be strict.

If it is a valid location, respond ONLY with the word "YES".
If it is NOT a valid location (e.g., gibberish, a fictional place, or not a geographical term), respond ONLY with "NO" and a brief, concise explanation why.

Examples:
Input: New York
Output: YES

Input: London, UK
Output: YES

Input: Delhi, India
Output: YES

Input: Narnia
Output: NO - Fictional place.

Input: asdfgh
Output: NO - Not a recognizable location.
"""
)