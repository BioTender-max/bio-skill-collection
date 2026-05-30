# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

# speech_to_text.py

import base64
import os
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import streamlit as st
from dotenv import load_dotenv
from typing import Optional
from st_audiorec import st_audiorec
# Load environment variables for API credentials
load_dotenv()

# Function to convert audio bytes to text using OpenAI's Whisper model
def convert_audio_to_text(audio_bytes: bytes) -> Optional[str]:
    """
    Convert audio bytes to text using OpenAI's Whisper model.
    
    Parameters:
    - audio_bytes (bytes): The audio data to convert to text.
    
    Returns:
    - str: Transcribed text if successful, None otherwise.
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(
            api_key=os.getenv("WHISPER_API_KEY")
        )
        
        # Create a temporary file to store the audio bytes
        temp_filename = "temp_audio.wav"
        with open(temp_filename, "wb") as f:
            f.write(audio_bytes)
        
        # Open the temporary file and transcribe using Whisper
        with open(temp_filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.remove(temp_filename)
        
        return transcription.text
    
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}", icon="🚨")
        return None

# Function to record audio and get transcription
def input_from_mic() -> Optional[str]:
    """
    Record audio from the microphone in the Audio Options tab and convert it to text.
    """
    # Use st_audiorec within the Audio Options tab
    with st.spinner("Recording..."):
        st.session_state["audio_bytes"] = st_audiorec()

    # Check if audio was captured and proceed with transcription
    if st.session_state.get("audio_bytes"):
        with st.spinner("Transcribing..."):
            transcribed_text = convert_audio_to_text(st.session_state["audio_bytes"])

        # Display the transcribed text in the sidebar Audio Options tab
        st.write("**Transcribed Text:**")
        st.write(transcribed_text)
        
        # Clear audio bytes after processing to avoid reuse
        st.session_state["audio_bytes"] = None
        return transcribed_text
    else:
        st.write("No audio recorded.")  # Inform the user if no audio was captured
        return None

    
def convert_text_to_speech(text: str, filename: str = "response.wav") -> Optional[str]:
    """
    Convert text to speech using OpenAI's GPT-4o audio model and save as a WAV file.
    
    Parameters:
    - text (str): The text to convert to speech.
    - filename (str): The name of the file to save the audio output. Default is "response.wav".
    
    Returns:
    - str: Path to the saved audio file if successful, None otherwise.
    """
    prompt_text = f'''Please convert the text between <<< and >>> into speech. 
    Please be consistent with the user's input language. you are a multi-lingual assistant.
    If the text is too long to convert fully, create a summarized version. 
    Start a summarized response with: "The original response is too long; here is a summary."
    Remember: the speech output should NOT exceed 1 minute.  
    Text to convert: <<< {text} >>>'''

    try:
        # Initialize OpenAI client
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Show spinner while processing
        with st.spinner("Generating voice response..."):
            # Prepare the API call
            completion = client.chat.completions.create(
                model="gpt-4o-audio-preview",
                modalities=["text", "audio"],
                audio={"voice": "alloy", "format": "wav"},
                messages=[
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ]
            )
        
            # Decode and save the audio file
            wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
            with open(filename, "wb") as f:
                f.write(wav_bytes)
        
        return filename
    
    except Exception as e:
        st.sidebar.error(f"An error occurred: {e}", icon="🚨")
        return None


__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
