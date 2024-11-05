import streamlit as st
from langchain_ollama import ChatOllama
from base import BookCreator
from lib.prompt_template import *
import subprocess

# Function to reset prompts to default
def reset_prompts(book_creator):
    book_creator.update_prompt(
        structure_prompt=None, 
        intro_prompt=None, 
        chapter_prompt=None, 
        heading_prompt=None, 
        subheading_prompt=None
    )

# Function to get the installed Ollama models using subprocess
def get_ollama_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        model_names = []
        for line in lines[1:]:
            parts = line.split()
            if parts:
                model_name_with_version = parts[0]
                model_name = model_name_with_version.split(':')[0]
                model_names.append(model_name)
        return model_names
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return []

# List of installed Ollama models
installed_models = get_ollama_models()

# Streamlit GUI
st.title("Book Generator using Ollama")

# Model selection
selected_model = st.selectbox("Select Ollama Model", installed_models)

# Input for book details
book_context = st.text_input("Book Context", "A book about various techniques used in NLP and their applications for beginners.")
book_genre = st.text_input("Book Genre", "Educational")
book_name = st.text_input("Book Name", "NLP Techniques")
output_dir = st.text_input("Output Directory", "../output/")

# Initialize the model and book creator
model = ChatOllama(model=selected_model, temperature=0.7)
book_creator = BookCreator(model, output_dir=output_dir)  

# Initialize default prompt values
current_prompts = {
    "structure_prompt": STRUCTURE_PROMPT_TEMPLATE,
    "intro_prompt": BOOK_INTRODUCTION_TEMPLATE,
    "chapter_prompt": CHAPTER_BRIEF_TEMPLATE,
    "heading_prompt": HEADING_BRIEF_TEMPLATE,
    "subheading_prompt": SUBHEADING_BRIEF_TEMPLATE
}

# Section to update prompts or use default
st.subheader("Customize Prompts (Optional)")
use_custom_prompt = st.checkbox("Use Custom Prompts")

if use_custom_prompt:
    # Show the latest prompts, allowing users to modify them
    structure_prompt = st.text_area("Structure Prompt", current_prompts["structure_prompt"])
    intro_prompt = st.text_area("Intro Prompt", current_prompts["intro_prompt"])
    chapter_prompt = st.text_area("Chapter Prompt", current_prompts["chapter_prompt"])
    heading_prompt = st.text_area("Heading Prompt", current_prompts["heading_prompt"])
    subheading_prompt = st.text_area("Subheading Prompt", current_prompts["subheading_prompt"])
    
    if st.button("Update Prompts"):
        # Update the prompts in the BookCreator and the current prompts dictionary
        book_creator.update_prompt(
            structure_prompt=structure_prompt,
            intro_prompt=intro_prompt,
            chapter_prompt=chapter_prompt,
            heading_prompt=heading_prompt,
            subheading_prompt=subheading_prompt
        )
        # Update the current prompt dictionary
        current_prompts.update({
            "structure_prompt": structure_prompt,
            "intro_prompt": intro_prompt,
            "chapter_prompt": chapter_prompt,
            "heading_prompt": heading_prompt,
            "subheading_prompt": subheading_prompt
        })
        st.success("Prompts updated successfully!")

if st.button("Reset Prompts to Default"):
    reset_prompts(book_creator)
    # Reset the current prompts to default values
    current_prompts = {
        "structure_prompt": STRUCTURE_PROMPT_TEMPLATE,
        "intro_prompt": BOOK_INTRODUCTION_TEMPLATE,
        "chapter_prompt": CHAPTER_BRIEF_TEMPLATE,
        "heading_prompt": HEADING_BRIEF_TEMPLATE,
        "subheading_prompt": SUBHEADING_BRIEF_TEMPLATE
    }
    st.success("Prompts reset to default.")

# Progress status as a scrollable list view
progress_text = st.empty()  # Placeholder for the scrollable progress

# Button to create the book
if st.button("Generate Book"):
    progress_messages = []  # To accumulate progress messages
    with st.spinner("Generating your book..."):
        def progress_listener(message, progress=None):
            # progress_messages.append(message)
            # add message at first
            progress_messages.insert(0,message)
            # Update the scrollable list of progress messages
            progress_text.text_area("Progress", "\n".join(progress_messages), height=150)
            # if progress:
            #     st.progress(progress.get("percentage", 0))

        book_creator.create_book(
            book_context=book_context,
            book_genre=book_genre,
            book_name=book_name,
            progress_listener=progress_listener
        )
    st.success(f"Book '{book_name}' generated successfully!")
