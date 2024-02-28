import streamlit as st
from openai import OpenAI
import os

st.set_page_config(
    page_title="Text -> Voice",
    page_icon="🔊",
)
st.title('🔊 Text -> Voice')
st.caption('Enter some text and turn it into a voice!') 


open_api_key = st.sidebar.text_input(
    "Enter Your OpenAI API Key 🗝️",
    value=st.session_state.get('open_api_key', ''),
    help="Get your API key from https://openai.com/",
    type='password'
)
os.environ["OPENAI_API_KEY"] = open_api_key
st.session_state['open_api_key'] = open_api_key

with st.sidebar.expander("⚙️ Settings"):
    voice = st.selectbox(
        "Voice Options 🗣️",
        [
            "nova",
            "alloy",
            "echo",
            "fable",
            "onyx",
            "shimmer"
        ],
        help="Choose the voice you want to use. Test out the voices here: https://platform.openai.com/docs/guides/text-to-speech"
    )

    model = st.selectbox(
        "Model Options 🤖",
        ["tts-1", "tts-1-hd"],
        help="Choose the model you want to use for the voice. Compare prices here: https://openai.com/pricing"
    )

with st.form(key='text_form'):
    text_input = st.text_area("Enter Text", "My name is Arya Stark. I want you to know that. The last thing you're ever going to see is a Stark smiling down at you as you die.")
    submit_button = st.form_submit_button(label='Generate Audio 🎵', type="primary")

if submit_button is not None:
    if open_api_key == '' or open_api_key is None:
        st.error("⚠️ Please enter your API key in the sidebar")
    else:
        client = OpenAI(
            api_key=open_api_key
        )
        with st.spinner('Generating audio...'):
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=text_input
            )
            response.write_to_file("output.mp3")
        with open("output.mp3", "rb") as audio_file:
            st.audio(audio_file, format='audio/mp3')