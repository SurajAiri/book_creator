from lib.book_topics import generate_book_structure
from lib.content import *
from langchain_community.llms import Ollama
from utils.parser import parse_json
from utils.file import *
import os

class BookCreator:
    BOOK_STRUCTURE_RETRY_LIMIT = 3

    def __init__(self, model, output_dir):
        self.structure_prompt = STRUCTURE_PROMPT_TEMPLATE
        self.intro_prompt = BOOK_INTRODUCTION_TEMPLATE
        self.chapter_prompt = CHAPTER_BRIEF_TEMPLATE
        self.heading_prompt = HEADING_BRIEF_TEMPLATE
        self.subheading_prompt = SUBHEADING_BRIEF_TEMPLATE
        self.model = model
        self.output_dir = output_dir

    def update_prompt(self, structure_prompt=None, intro_prompt=None, chapter_prompt=None, heading_prompt=None, subheading_prompt=None):
        if structure_prompt:
            self.structure_prompt = structure_prompt
        if intro_prompt:
            self.intro_prompt = intro_prompt
        if chapter_prompt:
            self.chapter_prompt = chapter_prompt
        if heading_prompt:
            self.heading_prompt = heading_prompt
        if subheading_prompt:
            self.subheading_prompt = subheading_prompt
        

    def update_progress(self, progress_path, progress_data, **kargs):
        progress_data.update(kargs)
        save_json(progress_path, progress_data)

    # Recursive retries as LLM sometimes returns invalid json
    def create_book_structure(self, book_context, book_genre, book_structure_path, retry=0, progress_listener=None):
        try:
            if progress_listener:
                progress_listener("Book structure generation started.")
            
            book_structure = generate_book_structure(self.model, book_context, book_genre, self.structure_prompt)
            # Parse json
            data = parse_json(book_structure)
            save_json(book_structure_path, data)
            
            if progress_listener:
                progress_listener("Book structure generation completed.")
        
        except Exception as e:
            print(f"Invalid Json Received from LLM\n{e}")
            if retry < self.BOOK_STRUCTURE_RETRY_LIMIT:
                retry += 1
                if progress_listener:
                    progress_listener(f"Retrying book structure generation. Retry Count: {retry}")
                self.create_book_structure(self.model, book_context, book_genre, book_structure_path, retry, progress_listener)
            else:
                print("Failed to create book structure. Exiting.")
                if progress_listener:
                    progress_listener("Failed to create book structure after retries.")
                exit()

    def create_book(self, book_context, book_genre, book_name, progress_listener=None):
        """
        Generate a book based on the given context and genre.

        Args:
            book_context (str): The main theme or subject of the book.
            book_genre (str): The genre classification of the book.
            book_name (str): The desired name for the book.
            progress_listener (callable, optional): A callback function to receive progress updates. 
                It should accept two parameters: a message (str) and a progress dictionary (dict).
        """
        # Set paths based on inputs
        book_path = self.output_dir + book_name + ".docx"
        book_structure_path = self.output_dir + book_name + ".json"
        book_progress_path = self.output_dir + "." + book_name + "_progress.json"

        # Notify progress listener
        if progress_listener:
            progress_listener(f"Starting book creation: {book_name}")

        # Create directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # If the book file exists and the progress file does not, assume the book is fully generated
        if os.path.exists(book_path) and not os.path.exists(book_progress_path):
            if progress_listener:
                progress_listener(f"Book '{book_name}' already exists. No further processing is required.")
            exit()

        # Load book structure
        if not os.path.exists(book_structure_path):
            self.create_book_structure( book_context, book_genre, book_structure_path, progress_listener=progress_listener)
        else:
            data = load_json(book_structure_path)

        # Load progress if it exists, otherwise initialize progress
        if os.path.exists(book_progress_path):
            progress_data = load_json(book_progress_path)
        else:
            progress_data = {
                "intro_generated": False,
                "chapter_index": 0,
                "heading_index": -1,
                "subheading_index": -1
            }

        # Generate the book introduction only if it hasn't been generated yet
        if not progress_data["intro_generated"]:
            if progress_listener:
                progress_listener("Generating book introduction.",progress_data)
            
            book_intro = generate_book_introduction(self.model, book_context, book_genre, data, self.intro_prompt)
            save_docx(book_path, book_intro.strip())
            add_page_break(book_path)
            self.update_progress(book_progress_path, progress_data, intro_generated=True)
            
            if progress_listener:
                progress_listener("Successfully saved book introduction.",progress_data)

        # Loop through chapters, headings, and subheadings, saving progress after each step
        for chapter_index in range(progress_data['chapter_index'], len(data['chapters'])):
            chapter = data['chapters'][chapter_index]
            chapter_title = chapter['chapter_title']
            chapter_headings = chapter['headings']
            if progress_listener:
                progress_listener(f"Generating content for chapter: {chapter_title}",progress_data)

            # Generate chapter introduction only if resuming from a new chapter
            if progress_data['heading_index'] == -1:
                chapter_intro = generate_book_chapter(self.model, book_context, book_genre, chapter_title, chapter_index + 1, chapter_headings, self.chapter_prompt)
                save_docx(book_path, chapter_intro.strip())

                # Save progress after chapter intro generation
                self.update_progress(book_progress_path, progress_data, chapter_index=chapter_index, heading_index=0)
                
                if progress_listener:
                    progress_listener(f"Successfully saved chapter intro: {chapter_title}",progress_data)

            # Loop through headings
            for heading_index in range(progress_data['heading_index'], len(chapter_headings)):
                heading = chapter_headings[heading_index]
                heading_title = heading['heading']
                sub_headings = heading['subheadings']
                if progress_listener:
                    progress_listener(f"Generating content for heading: {heading_title}",progress_data)

                if progress_data['subheading_index'] == -1:
                    heading_content = generate_book_heading(self.model, book_context, book_genre, chapter_title, heading_title, heading_index + 1, sub_headings, self.heading_prompt)
                    save_docx(book_path, heading_content.strip())

                    # Save progress after heading generation
                    self.update_progress(book_progress_path, progress_data, chapter_index=chapter_index, heading_index=heading_index, subheading_index=0)

                    if progress_listener:
                        progress_listener(f"Successfully saved heading content: {heading_title}",progress_data)
                # Loop through subheadings
                for subheading_index in range(progress_data['subheading_index'], len(sub_headings)):
                    sub_heading = sub_headings[subheading_index]
                    if progress_listener:
                        progress_listener(f"Generating content for subheading: {sub_heading}",progress_data)

                    sub_heading_content = generate_book_subheading(self.model, book_context, book_genre, chapter_title, heading_title, heading_index, sub_heading, self.subheading_prompt)
                    save_docx(book_path, sub_heading_content.strip())

                    # Update progress after subheading generation
                    self.update_progress(book_progress_path, progress_data, chapter_index=chapter_index, heading_index=heading_index, subheading_index=subheading_index + 1)
                    
                    if progress_listener:
                        progress_listener(f"Successfully saved subheading content: {sub_heading}",progress_data)

                # Reset subheading index for the next heading
                self.update_progress(book_progress_path, progress_data, subheading_index=-1)

            # Add a page break after each chapter
            add_page_break(book_path)

            # Reset heading index for the next chapter
            self.update_progress(book_progress_path, progress_data, heading_index=-1)

        # Clean up progress file after successful completion
        if os.path.exists(book_progress_path):
            os.remove(book_progress_path)
        if progress_listener:
            progress_listener("Book creation process completed.\nBook saved at: " + book_path)
