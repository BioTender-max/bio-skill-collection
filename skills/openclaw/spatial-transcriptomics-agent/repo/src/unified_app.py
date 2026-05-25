# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

import base64
import json
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, BaseMessage, SystemMessage
from graph import invoke_our_graph as invoke_gpt_graph
from graph_anthropic import invoke_our_graph as invoke_anthropic_graph
from util import display_message as display_message_gpt, render_conversation_history as render_conversation_history_gpt, get_conversation_summary as get_conversation_summary_gpt
from util_anthropic import display_message as display_message_anthropic, render_conversation_history as render_conversation_history_anthropic, get_conversation_summary as get_conversation_summary_anthropic
from speech_to_text import input_from_mic, convert_text_to_speech
from datetime import datetime
from prompt import system_prompt

# Load environment variables
load_dotenv()

# Initialize session state if not present
if "page" not in st.session_state:
    st.session_state["page"] = "OpenAI"

if "final_state" not in st.session_state:
    st.session_state["final_state"] = {
        "messages": [SystemMessage(content=system_prompt)]
    }
if "audio_transcription" not in st.session_state:
    st.session_state["audio_transcription"] = None

# Add custom CSS with theme-aware styling
st.markdown("""
<style>
    /* Custom styling for the main title */
    .main-title {
        text-align: center;
        color: #FF5722;
        padding: 1rem 0;
        border-bottom: 2px solid #FF5722;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Provider selection styling */
    .provider-section {
        background-color: var(--secondary-background-color);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 25px;
        background-color: #FF5722;
        color: white;
        font-weight: 600;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .new-chat-button > button {
        background-color: #2196F3 !important;
        margin: 1rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0px 0px;
        padding: 8px 16px;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.75rem;
        border-radius: 12px;
        margin: 1.25rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .user-message {
        background-color: #FBE9E7;
        border-left: 4px solid #FF5722;
    }
    
    .ai-message {
        background-color: #E8F5E9;
        border-left: 4px solid #2196F3;
    }
    
    /* Form styling */
    .stForm {
        background-color: var(--background-color);
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    
    /* Image upload area styling */
    [data-testid="stFileUploader"] {
        background-color: var(--background-color);
        padding: 1.25rem;
        border-radius: 12px;
        border: 2px dashed #FF5722;
    }
    
    /* Dark mode styles */
    @media (prefers-color-scheme: dark) {
        .main-title {
            color: #FFAB91;
            border-bottom-color: #FFAB91;
        }
        
        .provider-section {
            background-color: #1E1E1E;
        }
        
        .user-message {
            background-color: #3E2723;
            border-left: 4px solid #FFAB91;
        }
        
        .ai-message {
            background-color: #1A237E;
            border-left: 4px solid #90CAF9;
        }
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding: 12px 24px;
        border: 2px solid #FF5722;
        font-size: 16px;
    }
    
    /* Submit button hover effect */
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        background-color: #E64A19;
    }
    
    /* Tab hover effect */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FBE9E7;
        transition: background-color 0.3s ease;
    }

    /* API key setup styling */
    .api-key-setup {
        background-color: var(--secondary-background-color);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.25rem 0;
        border: 1px solid #FF5722;
    }

    /* Audio instructions styling */
    .audio-instructions {
        background-color: var(--secondary-background-color);
        padding: 14px;
        border-radius: 10px;
        margin-bottom: 14px;
        border: 1px solid #FF5722;
    }
    
    /* Main chat interface title styling */
    .chat-title {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 18px;
        background: linear-gradient(90deg, #FBE9E7, transparent);
        border-radius: 12px;
        margin-bottom: 24px;
    }
    
    .robot-icon {
        font-size: 28px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .provider-name {
        color: #FF5722;
        font-weight: bold;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

# Set up Streamlit layout
st.markdown('<h1 class="main-title">🤖 Spatial Transcriptomics Agent</h1>', unsafe_allow_html=True)

# Navigation in sidebar with improved styling
st.sidebar.markdown('<div class="provider-section">', unsafe_allow_html=True)
st.sidebar.title("🎯 Navigation")

PROVIDER_CONFIGS = {
    "Anthropic": {
        "icon": "🟣(Recommended)",
        "color": "#FF5722",
        "hover_color": "#E64A19"
    },
    "OpenAI": {
        "icon": "🟢",
        "color": "#2196F3",
        "hover_color": "#1976D2"
    }
}

# Then update the provider selection
provider_options = [f"{PROVIDER_CONFIGS[p]['icon']} {p}" for p in ["Anthropic", "OpenAI"]]
selected = st.sidebar.radio("Select LLM Provider Family", provider_options)
page = selected.split(" ")[1]  # Extract provider name without emoji
st.session_state["page"] = page

# Set provider-specific functions and variables
if page == "OpenAI":
    HISTORY_DIR = "conversation_histories_gpt"
    invoke_graph = invoke_gpt_graph
    display_message = display_message_gpt
    render_conversation_history = render_conversation_history_gpt
    get_conversation_summary = get_conversation_summary_gpt
    available_models = ["gpt-4o"]
else:  # Anthropic
    HISTORY_DIR = "conversation_histories_anthropic"
    invoke_graph = invoke_anthropic_graph
    display_message = display_message_anthropic
    render_conversation_history = render_conversation_history_anthropic
    get_conversation_summary = get_conversation_summary_anthropic
    available_models = [
        "claude_3_7_sonnet_20250219",
        "claude_3_5_sonnet_20241022"
    ]

# Add model selection with improved styling
selected_model = st.sidebar.selectbox(f"🔧 Select {page} Model:", available_models, index=0)

# Add New Chat button with custom styling
st.sidebar.markdown('<div class="new-chat-button">', unsafe_allow_html=True)
if st.sidebar.button("🔄 Start New Chat"):
    st.session_state["final_state"] = {
        "messages": [SystemMessage(content=system_prompt)]
    }
    st.session_state["last_summary_point"] = 0
    st.session_state["last_summary_title"] = "Default Title"
    st.session_state["last_summary_summary"] = "This is the default summary for short conversations."
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Set up environment for API keys
if page == "OpenAI" and not os.getenv('OPENAI_API_KEY'):
    st.sidebar.markdown("""
        <div class="api-key-setup">
            <h3>🔑 OpenAI API Key Setup</h3>
        </div>
    """, unsafe_allow_html=True)
    api_key = st.sidebar.text_input(label="OpenAI API Key", type="password", label_visibility="collapsed")
    os.environ["OPENAI_API_KEY"] = api_key
    if not api_key:
        st.info("Please enter your OpenAI API Key in the sidebar.")
        st.stop()
elif page == "Anthropic" and not os.getenv('ANTHROPIC_API_KEY'):
    st.sidebar.header("Anthropic API Key Setup")
    api_key = st.sidebar.text_input(label="Anthropic API Key", type="password", label_visibility="collapsed")
    os.environ["ANTHROPIC_API_KEY"] = api_key
    if not api_key:
        st.info("Please enter your Anthropic API Key in the sidebar.")
        st.stop()

os.makedirs(HISTORY_DIR, exist_ok=True)

# Helper Functions for Conversation Management
def save_history(title: str, summary: str):
    """Save the current conversation history to a file with title and summary."""
    history_data = {
        "title": title,
        "summary": summary,
        "timestamp": datetime.now().isoformat(),
        "messages": messages_to_dicts(st.session_state["final_state"]["messages"])
    }
    filename = f"{HISTORY_DIR}/{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(history_data, f)
    st.rerun()

def load_all_histories():
    """Load all saved conversation histories as a list of metadata for display."""
    histories = []
    for file in os.listdir(HISTORY_DIR):
        if file.endswith(".json"):
            with open(os.path.join(HISTORY_DIR, file), "r") as f:
                history = json.load(f)
                histories.append({
                    "title": history["title"],
                    "summary": history["summary"],
                    "timestamp": history["timestamp"],
                    "filename": file
                })
    return sorted(histories, key=lambda x: x["timestamp"], reverse=True)

def load_history(filename: str):
    """Load a specific conversation history file into session state."""
    try:
        with open(os.path.join(HISTORY_DIR, filename), "r") as f:
            history_data = json.load(f)
            st.session_state["final_state"]["messages"] = dicts_to_messages(history_data["messages"])
        st.sidebar.success(f"Conversation '{history_data['title']}' loaded successfully")
    except FileNotFoundError:
        st.sidebar.error("Conversation history not found.")

def delete_history(filename: str):
    """Delete a specific conversation history file."""
    os.remove(os.path.join(HISTORY_DIR, filename))
    st.sidebar.success("Conversation history deleted.")
    st.rerun()

# Convert messages to serializable dictionaries and vice versa
def messages_to_dicts(messages):
    return [msg.dict() for msg in messages]

def dicts_to_messages(dicts):
    reconstructed_messages = []
    for d in dicts:
        if d["type"] == "ai":
            reconstructed_messages.append(AIMessage(**d))
        elif d["type"] == "human":
            reconstructed_messages.append(HumanMessage(**d))
        elif d["type"] == "tool":
            reconstructed_messages.append(ToolMessage(**d))
    return reconstructed_messages

# Organize Sidebar with Tabs and improved styling
st.sidebar.title("⚙️ Settings")
tab1, tab2, tab3 = st.sidebar.tabs(["💬 Conversation", "🎤 Voice", "🖼️ Image"])

# Initialize session state variables
if "last_summary_point" not in st.session_state:
    st.session_state["last_summary_point"] = 0
if "last_summary_title" not in st.session_state:
    st.session_state["last_summary_title"] = "Default Title"
if "last_summary_summary" not in st.session_state:
    st.session_state["last_summary_summary"] = "This is the default summary for short conversations."

# Tab 1: Conversation Management
with tab1:
    st.subheader("History")
    histories = load_all_histories()
    if histories:
        st.markdown("### Saved Histories")
        for history in histories:
            with st.expander(f"{history['title']} ({history['timestamp'][:10]})"):
                st.write(history["summary"])
                if st.button("Load", key=f"load_{history['filename']}"):
                    load_history(history["filename"])
                if st.button("Delete", key=f"delete_{history['filename']}"):
                    delete_history(history["filename"])

    # Determine title and summary based on message count and last summary point
    message_count = len(st.session_state["final_state"]["messages"])
    if message_count > 5 and (message_count - 5) % 10 == 0 and message_count != st.session_state["last_summary_point"]:
        #generated_title, generated_summary = get_conversation_summary(st.session_state["final_state"]["messages"])
        #st.session_state["last_summary_title"] = generated_title
        st.session_state["last_summary_title"] = "Default Title"
        #st.session_state["last_summary_summary"] = generated_summary
        st.session_state["last_summary_summary"] = "This is the default summary for short conversations."
        st.session_state["last_summary_point"] = message_count
    elif message_count <= 5:
        st.session_state["last_summary_title"] = "Default Title"
        st.session_state["last_summary_summary"] = "This is the default summary for short conversations."

    title = st.text_input("Conversation Title", value=st.session_state["last_summary_title"])
    summary = st.text_area("Conversation Summary", value=st.session_state["last_summary_summary"])

    if st.button("Save Conversation"):
        save_history(title, summary)
        st.sidebar.success(f"Conversation saved as '{title}'")

# Tab 2: Voice Options
with tab2:
    st.subheader("Audio Options")
    use_audio_input = st.checkbox("Enable Voice Input", value=False)
    if use_audio_input:
        with st.form("audio_input_form", clear_on_submit=True):
            st.markdown("""
                <div class="audio-instructions">
                    <strong>Instructions for Recording Audio:</strong>
                    <ol style="padding-left: 20px; line-height: 1.5;">
                        <li>Click <strong>Submit Audio</strong> below to activate the audio recorder.</li>
                        <li>Once activated, click <strong>Start Recording</strong> to begin capturing audio.</li>
                        <li>When finished, click <strong>Stop</strong> to end the recording.</li>
                        <li>Finally, click <strong>Submit Audio</strong> again to use the recorded audio.</li>
                    </ol>
                </div>
            """, unsafe_allow_html=True)
            submitted_audio = st.form_submit_button("Submit Audio")
            if submitted_audio:
                audio_transcript = input_from_mic()
                if audio_transcript:
                    st.session_state["audio_transcription"] = audio_transcript
                    prompt = st.session_state["audio_transcription"]
                else:
                    st.session_state["audio_transcription"] = None

    use_voice_response = st.checkbox("Enable Voice Response", value=False)
    if use_voice_response:
        st.write("If the voice response is too long, a summarized version will generate.")

# Tab 3: Image Upload
with tab3:
    st.subheader("Image")
    with st.form("image_upload_form", clear_on_submit=True):
        uploaded_images = st.file_uploader("Upload one or more images (optional)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        submitted = st.form_submit_button("Submit Images")
        if submitted:
            if uploaded_images:
                st.session_state["uploaded_images_data"] = [
                    base64.b64encode(image.read()).decode("utf-8") for image in uploaded_images
                ]
            else:
                st.session_state["uploaded_images_data"] = []

# Initialize prompt variable
prompt = st.session_state.get("audio_transcription")

# Main chat interface
st.markdown(f"""
    <div class="chat-title">
        <span class="robot-icon">🤖</span>
        <span>Chat with Spatial Transcriptomics Agent</span>
    </div>
""", unsafe_allow_html=True)

render_conversation_history(st.session_state["final_state"]["messages"][0:])

# Capture text input if no audio input
if prompt is None:
    prompt = st.chat_input()

# Process new user input if available
if prompt:
    content_list = [{"type": "text", "text": prompt}]
    if "uploaded_images_data" in st.session_state and st.session_state["uploaded_images_data"]:
        content_list.extend([
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}}
            for img_data in st.session_state["uploaded_images_data"]
        ])
        st.session_state["uploaded_images_data"] = []
    
    user_message = HumanMessage(content=content_list)
    st.session_state["final_state"]["messages"].append(user_message)
    render_conversation_history([user_message])

    with st.spinner(f"Agent is thinking..."):
        previous_message_count = len(st.session_state["final_state"]["messages"])
        updated_state = invoke_graph(st.session_state["final_state"]["messages"], selected_model)
    
    st.session_state["final_state"] = updated_state
    new_messages = st.session_state["final_state"]["messages"][previous_message_count:]
    
    if st.session_state.get("render_last_message", True):
        render_conversation_history([st.session_state["final_state"]["messages"][-1]])
    
    if use_voice_response:
        audio_file = convert_text_to_speech(new_messages[-1].content)
        if audio_file:
            st.audio(audio_file)
    
    st.session_state["audio_transcription"] = None 




__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
