import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.messages import AnyMessage, HumanMessage,AIMessage
from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
from typing import Annotated
import os
import re
from dotenv import load_dotenv
import prompt_templates as pt

# Load environment variables
load_dotenv()

# Check API key
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Missing GOOGLE_API_KEY")
    st.stop()
# tools implement
jobs_search = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
tools =[jobs_search]

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.8)
llm_with_tools = llm.bind_tools(tools)

# Langgraph Implement
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def tools_call_llm(state):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("tools_call_llm", tools_call_llm)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "tools_call_llm")
builder.add_conditional_edges("tools_call_llm",tools_condition)
builder.add_edge("tools","tools_call_llm")
graph = builder.compile()

# Streamlit page config
st.set_page_config(page_title="Hiring Assistant")
st.title("Hiring Assistant for TalentScout")

# Exit commands
EXIT_KEYWORDS = {"exit", "quit", "bye", "goodbye", "close"}

# Fields to collect
FIELDS = [
    ("full_name", "Please provide your full name."),
    ("email", "Please enter your email address."),
    ("phone", "Please enter your phone number."),
    ("years", "How many years of experience do you have?"),
    ("desired_position", "What position(s) are you interested in?"),
    ("location", "Where are you currently located?"),
    ("tech_stack", "At last, list your tech stack."),
]

# Initialize session state on first load
if "initialized" not in st.session_state:
    st.session_state.memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=1000,
        return_messages=True,
    )
    st.session_state.current_field = 0
    st.session_state.candidate_info = {}
    st.session_state.collecting_info = True
    st.session_state.chat_active = True
    st.session_state.initialized = True

    greet_user = (
        "Welcome to TalentScout Hiring Assistant.\n\n"
        "Before we start, please provide the following details. You can type 'exit' anytime to end the chat.\n\n"
        f"{FIELDS[0][1]}"
    )
    st.session_state.memory.chat_memory.add_ai_message(greet_user)
    st.rerun()


# Validate input for email, phone, and years
def validate_input(field_key, user_text):
    if field_key == "email":
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_text):
            return False, "Please enter a valid email."
    elif field_key == "phone":
        if not re.match(r"^\+?\d{10,13}$", user_text):
            return False, "Please enter a valid phone number."
    elif field_key == "years":
        try:
            val = int(user_text)
            if val < 0 or val > 60:
                raise ValueError
        except ValueError:
            return False, "Please enter valid years of experience."
    return True, ""

# Store candidate field and advance
def handle_candidate_field(field_key, user_text):
    if field_key == "years":
        user_text = str(int(user_text))
    st.session_state.candidate_info[field_key] = user_text
    st.session_state.current_field += 1

# Generate tech questions
def generate_tech_questions(tech_stack):
    question_prompt_text = pt.question_prompt.format(tech_stack=tech_stack)
    with st.spinner("Generating technical questions..."):
        # Access the content attribute here
        return llm.invoke(question_prompt_text).content

# Build candidate summary
def generate_candidate_summary():
    if not st.session_state.candidate_info:
        return "No candidate information collected yet."
    summary = "**✅ Candidate Information:**\n\n"
    for key, _ in FIELDS:
        value = st.session_state.candidate_info.get(key, "_")
        label = key.replace("_", " ").title()
        summary += f"- **{label}:** {value}\n"
    return summary


# Generic validator function
def validate_with_prompt(prompt_template, value):
    prompt_text = prompt_template.format(value=value)
    result = llm.invoke(prompt_text)
    # Access the content attribute here
    return result and result.content.strip().upper() == "YES"

# Handle user input
def process_input(user_text):
    
    user_text = user_text.strip()
    if not user_text:
        return
    
    memory = st.session_state.memory.chat_memory

    if user_text.lower() in EXIT_KEYWORDS:
        st.session_state.chat_active = False
        memory.add_user_message(user_text)
        memory.add_ai_message("Thank you for chatting with me. Best Wishes for your career.")
        return

    memory.add_user_message(user_text)

    if st.session_state.collecting_info:
        field_key, _ = FIELDS[st.session_state.current_field]
        is_valid, error_msg = validate_input(field_key, user_text)
        if not is_valid:
            memory.add_ai_message(error_msg)
            return

        # Special AI validation
        if field_key == "tech_stack":
            if not validate_with_prompt(pt.validate_tech_stack_prompt, user_text):
                memory.add_ai_message(
                    "❗ This does not appear to be a valid tech stack. Please list technologies, frameworks, or tools you use."
                )
                return
        elif field_key == "desired_position":
            if not validate_with_prompt(pt.validate_position_prompt, user_text):
                memory.add_ai_message(
                    "❗ This does not appear to be a valid job title. Please enter a correct role (e.g., Software Engineer, Data Analyst)."
                )
                return
        elif field_key == "location":
            if not validate_with_prompt(pt.validate_location_prompt, user_text):
                memory.add_ai_message(
                    "❗ This does not appear to be a valid location. Please enter a city, region, or country."
                )
                return

        handle_candidate_field(field_key, user_text)

        if st.session_state.current_field < len(FIELDS):
            next_question = FIELDS[st.session_state.current_field][1]
            memory.add_ai_message(next_question)
        else:
            st.session_state.collecting_info = False
            tech_stack_text = st.session_state.candidate_info.get("tech_stack", "").strip()
            if tech_stack_text:
                questions_response_content = generate_tech_questions(tech_stack_text) # Get the content directly
                if questions_response_content and questions_response_content.strip():
                    message = f"🔍 **Here are some technical questions to assess your skills:**\n\n{questions_response_content.strip()}"
                else:
                    message = "⚠️ Sorry, I could not generate questions at this time."
                memory.add_ai_message(message)

    elif st.session_state.chat_active:
        initial_messages = st.session_state.memory.chat_memory.messages + [HumanMessage(content=user_text)]

        with st.spinner("Thinking..."):
            response_state = graph.invoke({"messages": initial_messages})
        
        if response_state and response_state["messages"]:
            ai_response_message = response_state["messages"][-1]

            st.session_state.memory.chat_memory.add_ai_message(ai_response_message)
        else:
            st.session_state.memory.chat_memory.add_ai_message("Sorry, I couldn't generate a response.")


# Display chat messages
for msg in st.session_state.memory.chat_memory.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(
            f"> {msg.content.strip()}"
        )

# Show candidate summary
with st.expander("View Candidate Information"):
    st.markdown(generate_candidate_summary())



# Chat input
if st.session_state.chat_active:
    prompt = st.chat_input("Your message")
    if prompt:
        process_input(prompt)
        st.rerun()
else:
    if st.button("🔄 Start New Conversation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()