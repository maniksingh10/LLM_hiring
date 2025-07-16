
# TalentScout AI Hiring Assistant

The TalentScout AI Hiring Assistant is a Streamlit-based chatbot designed to automate candidate screening and assist job seekers. It collects essential candidate information, performs intelligent validation (including AI-driven semantic checks), generates technical interview questions, and searches live job postings using LangGraph and Google Jobs.


## ✨ Key Features

- Guided Information Collection 📝
  Collects candidate details like name, email, phone, experience, desired role, location, and tech stack in a structured flow.

- Intelligent Input Validation ✅
  Combines regex/range checks with LLM-powered semantic validation for fields like tech stack, desired position, and location to ensure high-quality data.

- Dynamic Technical Questions 🧠
  Generates relevant technical questions based on the candidate’s specified tech stack using Gemini Flash.

- Contextual Conversation 🗣️
  Maintains coherent multi-turn conversations with ConversationSummaryBufferMemory.

- Live Job Search Integration 💼
  Allows candidates to search for real-time job postings through the Google Jobs API via LangGraph agent workflows.

- Agentic Workflows 🤖
  Automatically decides whether to answer queries conversationally or trigger job search tools using LangGraph’s conditional routing.

- Professional AI Persona 🤵
  Maintains a structured, polite, and professional tone for effective candidate engagement.

- Information Summary 📋
  Presents a clean summary of collected candidate details.




## 💡 Usage

Information Collection Mode
- The assistant will greet you and guide you through a series of questions.
- Enter responses in the chat input and press Enter.
- Validation is applied, with error messages for incorrect inputs.

Technical Question Generation
- Once all details are collected, you’ll receive 3–4 relevant technical questions.

Job Search Mode
- After completing the initial flow, you can ask:
  - "Find software engineer jobs in New York."
  - "Show data analyst openings in Bangalore."
- The assistant will query Google Jobs live and return results.

Ending the Chat
- Type exit, quit, bye, goodbye, or close to end.
- Use the "View Candidate Information" expander to review collected details.


## 🛠️ Technical Highlights

- Frontend: Streamlit (st.chat_input, st.chat_message, st.session_state)
- LLM: Google Gemini 2.0 Flash (gemini-2.0-flash-001) via langchain-google-genai
- Orchestration:
  - LangChain: Prompt templates, memory management
  - LangGraph: Agentic workflows, dynamic tool invocation, conditional routing
- Tools: Google Jobs API integration via GoogleJobsQueryRun and GoogleJobsAPIWrapper
- Validation: Regex and LLM-powered checks
- State Management: Modular control flow using FIELDS and st.session_state flags



## 🎨 Prompt Design

Prompts are modular and stored in prompt_templates.py:
- chat_prompt_for_llm: Defines the professional assistant persona.
- question_prompt: Generates structured technical interview questions.
- validate_tech_stack_prompt, validate_position_prompt, validate_location_prompt: Specialized validation prompts returning YES/NO with explanations.


## 🚧 Challenges & Solutions

Dynamic Tool Invocation
- Solved with: LangGraph’s ToolNode and conditional edges to switch between conversation and job search seamlessly.

Context Management
- Managed with: ConversationSummaryBufferMemory to maintain summaries of long exchanges.

Robust Validation
- Combined: Traditional regex checks with semantic LLM prompts to ensure accuracy and relevance.

