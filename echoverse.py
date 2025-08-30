# echoverse_app.py

import streamlit as st
import PyPDF2
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# --- Configuration Section ---
# Replace with your IBM Watson Text to Speech credentials
API_KEY = "aFAYTNJ3sSZOCPLU3Y-dr9edxKIq3q0MIWdgLE8vCX1F"
SERVICE_URL = "https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/2b4962e9-6680-4b09-9ac1-436ff10639d9"

# Initialize the IBM Watson Text to Speech service
try:
    authenticator = IAMAuthenticator(API_KEY)
    text_to_speech = TextToSpeechV1(authenticator=authenticator)
    text_to_speech.set_service_url(SERVICE_URL)
except Exception as e:
    st.error(f"Failed to connect to IBM Watson: {e}")
    text_to_speech = None

# --- Streamlit Front-End ---
st.title("EchoVerse: AI-Powered Audiobook Creator 📚🎧")
st.markdown("Easily convert your documents into high-quality audiobooks.")


st.subheader("1. Upload Your Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    # --- File Processing and Text Extraction ---
    st.subheader("2. Extract and Review Text")
    full_text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            full_text += page.extract_text()
        
        text_area_placeholder = st.text_area("Review Extracted Text", full_text, height=300)

        # --- Audiobook Generation Options ---
        st.subheader("3. Customize and Generate Audiobook")
        voice_options = {
            "Male (US)": "en-US_KevinV3Voice",
            "Female (US)": "en-US_LisaV3Voice",
            # Add more voices as needed
        }
        selected_voice_name = st.selectbox("Select a Voice", list(voice_options.keys()))
        selected_voice_id = voice_options[selected_voice_name]

        if st.button("Create Audiobook"):
            if text_to_speech:
                with st.spinner("Generating audiobook... this may take a moment."):
                    try:
                        audio_stream = text_to_speech.synthesize(
                            text=text_area_placeholder,
                            accept='audio/mp3',
                            voice=selected_voice_id
                        ).get_result().content

                        st.audio(audio_stream, format='audio/mp3')
                        st.download_button(
                            label="Download Audiobook as MP3",
                            data=audio_stream,
                            file_name="audiobook.mp3",
                            mime="audio/mp3"
                        )
                        st.success("Audiobook created successfully! You can listen or download it above.")
                    except Exception as e:
                        st.error(f"An error occurred during audio synthesis: {e}")
            else:
                st.warning("Text-to-speech service not initialized. Please check your credentials.")
    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
else:
    st.info("Please upload a PDF file to begin.")