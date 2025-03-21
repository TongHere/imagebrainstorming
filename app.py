import random
import streamlit as st
import streamlit.components.v1 as components
import uuid
import requests  # For making API calls
import os
import yaml
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Access API key from Streamlit Secrets
API_KEY = st.secrets["api_key"]

# Predefined brainstorming prompts
prompts = [
    "A futuristic cityscape with neon lights",
    "A cyberpunk robot with glowing eyes",
    "A surreal dream-like forest with floating islands",
    "An ancient temple hidden deep in the jungle",
    "A cozy cottage in a magical winter wonderland",
    "A sci-fi spaceship exploring an alien planet",
    "A medieval knight battling a fire-breathing dragon",
    "A cybernetic humanoid in a digital world",
    "A peaceful sunset over an endless ocean",
    "A fantasy steampunk airship flying through the clouds"
]

# Function to shuffle and select a new prompt
def shuffle_prompt():
    return random.choice(prompts)

# Function to generate images using an API
def generate_image(prompt, medium):
    # Replace this with the actual API call
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": f"{prompt}, {medium} art style",
        "n": 4,  # Number of images to generate
        "size": "300x300"  # Image size
    }
    response = requests.post("https://api.example.com/generate", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["images"]  # Assuming the API returns a list of image URLs
    else:
        st.error("Failed to generate images. Please try again.")
        return []

# Streamlit UI
st.set_page_config(page_title="AI Brainstorming & Image Generation", layout="wide")
st.title("🎨 AI Brainstorming & Image Generation")

# Initialize session state
if "selected_prompt" not in st.session_state:
    st.session_state["selected_prompt"] = shuffle_prompt()
if "generated_images" not in st.session_state:
    st.session_state["generated_images"] = []

col1, col2 = st.columns([1, 2])

# Left panel for prompt and settings
with col1:
    st.subheader("Image Description")
    prompt = st.text_input("Enter your prompt:", st.session_state["selected_prompt"])
    
    if st.button("Shuffle Prompt"):
        st.session_state["selected_prompt"] = shuffle_prompt()
    
    st.subheader("Art Medium")
    medium_options = ["Any", "Pencil sketch", "Crayon", "Ink", "Charcoal", "Linocut", "Color Pencil", "Oil Painting"]
    selected_medium = st.radio("Select an art medium:", medium_options)
    
    if st.button("Generate Image 🎨"):
        st.session_state["generated_images"] = generate_image(prompt, selected_medium)

# Right panel for displaying and dragging images
with col2:
    st.subheader("Generated Images")
    if st.session_state["generated_images"]:
        draggable_container = """
        <script>
        function allowDrop(ev) {
          ev.preventDefault();
        }
        function drag(ev) {
          ev.dataTransfer.setData("text", ev.target.id);
        }
        function drop(ev) {
          ev.preventDefault();
          var data = ev.dataTransfer.getData("text");
          ev.target.appendChild(document.getElementById(data));
        }
        </script>
        <style>
        .drag-container { display: flex; flex-wrap: wrap; gap: 10px; }
        .drop-zone { width: 150px; height: 150px; border: 2px dashed #ccc; display: inline-block; text-align: center; }
        </style>
        <div class='drag-container'>
        """
        for idx, image in enumerate(st.session_state["generated_images"]):
            draggable_container += f"""
            <div class='drop-zone' ondrop='drop(event)' ondragover='allowDrop(event)'>
                <img id='img{idx}' src='{image}' draggable='true' ondragstart='drag(event)' width='150' height='150'>
            </div>
            """
        draggable_container += "</div>"
        components.html(draggable_container, height=400)