from main.book_topics import generate_book_structure
from main.content import *
from langchain.llms import Ollama
from utils.parser import parse_json
from utils.file import *
import os

BOOK_CONTEXT = "A book about various techniques used in NLP and their applications for beginner."
BOOK_GENRE = "Educational"
DIRECTORY_PATH = "../output/"
BOOK_NAME = "NLP Techniques1"
BOOK_PATH = DIRECTORY_PATH+BOOK_NAME+".docx"
BOOK_STRUCTURE_PATH = DIRECTORY_PATH+BOOK_NAME+".json"
BOOK_PROGRESS_PATH = DIRECTORY_PATH+BOOK_NAME+"_progress.json"

# create a dictionary if doesn't exist
if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)

# initialize the Ollama model
ollama = Ollama(model='phi3',temperature=0.7)

# Generate the book structure
if not os.path.exists(BOOK_STRUCTURE_PATH):
    book_structure = generate_book_structure(ollama, BOOK_CONTEXT, BOOK_GENRE)
    # parse json
    data = parse_json(book_structure)
    save_json(BOOK_STRUCTURE_PATH, data)
else: 
    data = load_json(BOOK_STRUCTURE_PATH)


# brief information about the book in md format
book_intro = generate_book_introduction(ollama, BOOK_CONTEXT, BOOK_GENRE, data)
# save the book introduction in docx file
save_docx(BOOK_PATH, book_intro.strip())
add_page_break(BOOK_PATH)


# for each chapter
#     generate chapter introduction
#     for each heading
#         generate heading content
#         for each subheading
#             generate subheading content
#     end
# store above all content in md format to docx file

for chapter in data['chapters']:
    chapter_title = chapter['chapter_title']
    chapter_headings = chapter['headings']
    print("Generating content for chapter: ", chapter_title)
    chapter_intro = generate_book_chapter(ollama, BOOK_CONTEXT, BOOK_GENRE, chapter_title, chapter_headings)
    save_docx(BOOK_PATH, chapter_intro.strip())
    print("Successfully saved chapter intro")
    for heading in chapter_headings:
        heading_title = heading['heading']
        heading_index = heading['index']
        sub_headings = heading['subheadings']
        print("Generating content for heading: ", heading_title)

        heading_content = generate_book_heading(ollama, BOOK_CONTEXT, BOOK_GENRE, chapter_title, heading_title, heading_index, sub_headings)
        save_docx(BOOK_PATH, heading_content.strip())

        print("Successfully saved heading content: ", heading_title)
        for sub_heading in sub_headings:
            print("Generating content for subheading: ", sub_heading)
            
            sub_heading_content = generate_book_subheading(ollama, BOOK_CONTEXT, BOOK_GENRE, chapter_title, heading_title, heading_index, sub_heading)
            save_docx(BOOK_PATH, sub_heading_content.strip())
            
            print("Successfully saved subheading content: ", sub_heading)

    add_page_break(BOOK_PATH)






