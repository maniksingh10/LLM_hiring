# TalentScout AI Hiring Assistant

## Project Overview

The TalentScout AI Hiring Assistant is a Streamlit chatbot designed to automate initial candidate screening. It gathers essential information, performs intelligent input validation (including AI-driven semantic checks), and generates dynamic technical interview questions using Google's Gemini Flash model and LangChain.

## Key Features

* **Guided Information Collection:** Collects candidate details like name, email, phone, experience, desired role, location, and tech stack.
* **Intelligent Input Validation:** Combines regex/range checks with AI-powered semantic validation for fields like tech stack, desired position, and location, ensuring data quality.
* **Dynamic Technical Questions:** Generates 3-4 relevant technical questions based on the candidate's specified tech stack.
* **Contextual Conversation:** Uses `ConversationSummaryBufferMemory` to maintain chat context efficiently.
* **Professional AI Persona:** Maintains a strict and professional tone for effective screening.
* **Information Summary:** Provides a clear summary of all collected candidate data.

## Setup & Run

1.  **Prerequisites:** Python 3.8+, `pip`, Google Cloud Project with Generative Language API enabled, and a Google API Key.
2.  **Save Files:** Place the provided `app.py` and `prompt_templates.py` in a new project directory.
3.  **Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    .\venv\Scripts\activate   # Windows
    ```
4.  **Install Dependencies:** Create `requirements.txt` with `streamlit`, `langchain-google-genai`, `langchain`, `python-dotenv`.
    ```bash
    pip install -r requirements.txt
    ```
5.  **Google API Key:** Create a `.env` file in the project root with `GOOGLE_API_KEY="YOUR_API_KEY"`.
6.  **Run Application:**
    ```bash
    streamlit run app.py
    ```
    (Opens in your browser at `http://localhost:8501`)

## Usage

* The assistant will greet you and guide you through a series of questions.
* Enter your responses in the chat input at the bottom and press `Enter`.
* The assistant will validate your inputs and prompt for corrections if needed (e.g., invalid email, non-existent tech stack).
* Once information is collected, technical questions will be generated.
* Type `exit`, `quit`, `bye`, `goodbye`, or `close` to end the chat.
* View collected information in the "View Candidate Information" expander.

## Technical Highlights

* **Frontend:** Streamlit (`st.chat_input`, `st.chat_message`, `st.session_state`).
* **LLM:** Google Gemini 2.0 Flash (`gemini-2.0-flash-001`) via `langchain-google-genai`.
* **Orchestration:** LangChain (for `PromptTemplate`, `ConversationSummaryBufferMemory`).
* **Modular Prompts:** All LLM prompts are externalized in `prompt_templates.py` for clarity and maintainability.
* **Validation:** Custom Python regex for basic checks, and LLM-based validation (using dedicated prompts) for semantic checks on tech stack, position, and location.

## Prompt Design

Prompts are critical for guiding the LLM:
* **`chat_prompt_for_llm`:** Establishes the professional hiring assistant persona and context management.
* **`question_prompt`:** Directs the LLM to act as a technical interviewer and generate structured questions.
* **`validate_tech_stack_prompt`, `validate_position_prompt`, `validate_location_prompt`:** These are specialized prompts that instruct the LLM to act as a strict validator, responding with "YES" or "NO" (plus a concise explanation for "NO") to ensure the quality of user-provided data.

## Challenges & Solutions

* **Robust Validation:** Addressed by combining traditional regex/range checks with AI-powered semantic validation using specialized LLM prompts.
* **Context Management:** Solved using LangChain's `ConversationSummaryBufferMemory` to maintain coherent long conversations efficiently.
* **Structured Flow:** Managed through `st.session_state` flags and a predefined `FIELDS` list to guide users through sequential information gathering with proper error handling and re-prompts.