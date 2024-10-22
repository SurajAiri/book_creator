import streamlit as st
from langchain_community.llms import Ollama
from base import BookCreator
from lib.prompt_template import *

# Function to reset prompts to default
def reset_prompts(book_creator):
    book_creator.update_prompt(
        structure_prompt=None, 
        intro_prompt=None, 
        chapter_prompt=None, 
        heading_prompt=None, 
        subheading_prompt=None
    )

# List of installed Ollama models (You need to adjust it according to how models are retrieved in your system)
installed_models = ['phi3']  # Example models

# Streamlit GUI
st.title("Book Generator using Ollama")

# Model selection
selected_model = st.selectbox("Select Ollama Model", installed_models)

# Input for book details
book_context = st.text_input("Book Context", "A book about various techniques used in NLP and their applications for beginners.")
book_genre = st.text_input("Book Genre", "Educational")
book_name = st.text_input("Book Name", "NLP Techniques")

# Section to update prompts or use default
st.subheader("Customize Prompts (Optional)")
use_custom_prompt = st.checkbox("Use Custom Prompts")

model = Ollama(model=selected_model, temperature=0.7)
book_creator = BookCreator(model, output_dir="../output/")

if use_custom_prompt:
    structure_prompt = st.text_area("Structure Prompt", STRUCTURE_PROMPT_TEMPLATE)
    intro_prompt = st.text_area("Intro Prompt", BOOK_INTRODUCTION_TEMPLATE)
    chapter_prompt = st.text_area("Chapter Prompt", CHAPTER_BRIEF_TEMPLATE)
    heading_prompt = st.text_area("Heading Prompt", HEADING_BRIEF_TEMPLATE)
    subheading_prompt = st.text_area("Subheading Prompt", SUBHEADING_BRIEF_TEMPLATE)
    
    if st.button("Update Prompts"):
        book_creator.update_prompt(
            structure_prompt=structure_prompt,
            intro_prompt=intro_prompt,
            chapter_prompt=chapter_prompt,
            heading_prompt=heading_prompt,
            subheading_prompt=subheading_prompt
        )
        st.success("Prompts updated successfully!")

if st.button("Reset Prompts to Default"):
    reset_prompts(book_creator)
    st.success("Prompts reset to default.")

# Button to create the book
if st.button("Generate Book"):
    with st.spinner("Generating your book..."):
        def progress_listener(message, progress=None):
            st.text(f"{message}")
            if progress:
                st.progress(progress.get("percentage", 0))

        book_creator.create_book(
            book_context=book_context,
            book_genre=book_genre,
            book_name=book_name,
            progress_listener=progress_listener
        )
    st.success(f"Book '{book_name}' generated successfully!")
