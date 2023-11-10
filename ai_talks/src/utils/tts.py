from openai import OpenAI
from io import BytesIO
import streamlit as st

def show_audio_player(ai_content: str, voice, API_O) -> None:
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key= API_O,
    )


    # Create a BytesIO object to hold the audio data
    sound_file = BytesIO()

    try:
        # Call OpenAI's text-to-speech model
        response = client.audio.speech.create(
            model="tts-1",
            # model="tts-1-hd"
            voice=voice,
            input=ai_content
        )

        # Write the binary content of the response to the BytesIO object
        sound_file.write(response.content)
        sound_file.seek(0)  # Rewind the BytesIO object to the beginning

        # Display placeholder text (if needed)
        st.write(st.session_state.locale.stt_placeholder)

        # Use Streamlit's audio widget to display the audio player
        st.audio(sound_file)
    except Exception as err:
        st.error(f"An error occurred: {err}")
