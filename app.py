import streamlit as st
from transformers import pipeline
import google.generativeai as genai
from apikey import gemini_api_key
genai.coonfigure(api_key=gemini_api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)


# Load the story generation pipeline
#generator = pipeline('text-generation', model='gpt-2')
st.set_page_config(layout="wide")
# Streamlit app title and description
st.title("🌟 Interactive Storytelling Assistant")
st.subheader("Create your own adventure by choosing different story paths!")

with st.sidebar:
    st.title("Preferences:")
    st.subheader("Customize the story with your own preferences.") 
    story_title = st.text_input("Title")
    keywords = st.text_input("Keywords(Comma separated)")
    story_description = st.text_area("Description")
    num_words = st.slider("Number of words", 50, 500, 100)
    num_images = st.number_input("Number of images", 1, 10, 3)
    if st.button("Generate Story"):
        st.write("Generating story...")

    
# Session state to track story progress
if 'story' not in st.session_state:
    st.session_state.story = "Once upon a time in a distant land, there was a brave adventurer."

# Display current story
st.write(st.session_state.story)

# Provide options for the next part of the story
st.write("### What happens next?")
option1 = st.button("The adventurer encounters a mysterious stranger.")
option2 = st.button("The adventurer finds a hidden treasure map.")
option3 = st.button("The adventurer hears a strange noise from the forest.")

# Function to generate next part of the story
def generate_next_part(prompt):
    result = generator(prompt, max_length=100, num_return_sequences=1)
    return result[0]['generated_text']

# Update story based on user choice
if option1:
    new_story = generate_next_part(st.session_state.story + " The adventurer encounters a mysterious stranger.")
    st.session_state.story = new_story
    st.experimental_rerun()

if option2:
    new_story = generate_next_part(st.session_state.story + " The adventurer finds a hidden treasure map.")
    st.session_state.story = new_story
    st.experimental_rerun()

if option3:
    new_story = generate_next_part(st.session_state.story + " The adventurer hears a strange noise from the forest.")
    st.session_state.story = new_story
    st.experimental_rerun()

# Option to reset the story
if st.button("Restart Story"):
    st.session_state.story = "Once upon a time in a distant land, there was a brave adventurer."
    st.experimental_rerun()
