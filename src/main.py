from lib.book_topics import generate_book_structure
from lib.content import *
from langchain.llms import Ollama
from utils.parser import parse_json
from utils.file import *
import os

BOOK_CONTEXT = "A book about various techniques used in NLP and their applications for beginners."
BOOK_GENRE = "Educational"
DIRECTORY_PATH = "../output/"
BOOK_NAME = "NLP Techniques6"
BOOK_PATH = DIRECTORY_PATH + BOOK_NAME + ".docx"
BOOK_STRUCTURE_PATH = DIRECTORY_PATH + BOOK_NAME + ".json"
BOOK_PROGRESS_PATH = DIRECTORY_PATH + "."+BOOK_NAME + "_progress.json"


def update_progress(**kargs):
    global progress_data
    progress_data.update(kargs)
    save_json(BOOK_PROGRESS_PATH, progress_data)

# Create directory if it doesn't exist
if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)

# If the book file exists and the progress file does not, assume the book is fully generated
if os.path.exists(BOOK_PATH) and not os.path.exists(BOOK_PROGRESS_PATH):
    print(f"Book '{BOOK_NAME}' already exists. No further processing is required.")
    exit()

# Initialize the Ollama model
ollama = Ollama(model='phi3', temperature=0.7)

# Load book structure
if not os.path.exists(BOOK_STRUCTURE_PATH):
    book_structure = generate_book_structure(ollama, BOOK_CONTEXT, BOOK_GENRE)
    # Parse json
    data = parse_json(book_structure)
    save_json(BOOK_STRUCTURE_PATH, data)
else:
    data = load_json(BOOK_STRUCTURE_PATH)

# Load progress if it exists, otherwise initialize progress
if os.path.exists(BOOK_PROGRESS_PATH):
    progress_data = load_json(BOOK_PROGRESS_PATH)
else:
    progress_data = {
        "intro_generated": False,
        "chapter_index": 0,
        "heading_index": -1,
        "subheading_index": -1
    }

# Generate the book introduction only if it hasn't been generated yet
if not progress_data["intro_generated"]:
    book_intro = generate_book_introduction(ollama, BOOK_CONTEXT, BOOK_GENRE, data)
    save_docx(BOOK_PATH, book_intro.strip())
    add_page_break(BOOK_PATH)
    update_progress(intro_generated=True)
    print("Successfully saved book introduction.")

# Loop through chapters, headings, and subheadings, saving progress after each step
for chapter_index in range(progress_data['chapter_index'], len(data['chapters'])):
    chapter = data['chapters'][chapter_index]
    chapter_title = chapter['chapter_title']
    chapter_headings = chapter['headings']
    print(f"Generating content for chapter: {chapter_title}")
    
    # Generate chapter introduction only if resuming from a new chapter
    if progress_data['heading_index'] == -1:
        chapter_intro = generate_book_chapter(ollama, BOOK_CONTEXT, BOOK_GENRE, chapter_title,chapter_index + 1, chapter_headings)
        save_docx(BOOK_PATH, chapter_intro.strip())
        print(f"Successfully saved chapter intro: {chapter_title}")

        # Save progress after chapter intro generation
        update_progress(chapter_index=chapter_index,heading_index=0)

    # Loop through headings
    for heading_index in range(progress_data['heading_index'], len(chapter_headings)):
        heading = chapter_headings[heading_index]
        heading_title = heading['heading']
        sub_headings = heading['subheadings']
        print(f"Generating content for heading: {heading_title}")
        
        if progress_data['subheading_index'] == -1:
            heading_content = generate_book_heading(ollama, BOOK_CONTEXT, BOOK_GENRE, chapter_title, heading_title, heading_index + 1, sub_headings)
            save_docx(BOOK_PATH, heading_content.strip())
            print(f"Successfully saved heading content: {heading_title}")
        
            # Save progress after heading generation
            update_progress(chapter_index=chapter_index,heading_index=heading_index,subheading_index=0)

        # Loop through subheadings
        for subheading_index in range(progress_data['subheading_index'], len(sub_headings)):
            sub_heading = sub_headings[subheading_index]
            print(f"Generating content for subheading: {sub_heading}")
            
            sub_heading_content = generate_book_subheading(ollama, BOOK_CONTEXT, BOOK_GENRE, chapter_title, heading_title, heading_index, sub_heading)
            save_docx(BOOK_PATH, sub_heading_content.strip())
            print(f"Successfully saved subheading content: {sub_heading}")
            
            # # Update progress after subheading generation
            update_progress(chapter_index=chapter_index,heading_index=heading_index,subheading_index=subheading_index + 1)
        
        # Reset subheading index for the next heading
        # progress_data['subheading_index'] = 0
        update_progress(subheading_index=-1)

    # Add a page break after each chapter
    add_page_break(BOOK_PATH)

    # Reset heading index for the next chapter
    # progress_data['heading_index'] = 0
    update_progress(heading_index=-1)


# Clean up progress file after successful completion
if os.path.exists(BOOK_PROGRESS_PATH):
    os.remove(BOOK_PROGRESS_PATH)