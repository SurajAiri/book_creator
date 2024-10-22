from lib.book_topics import generate_book_structure
from lib.content import *
from langchain_community.llms import Ollama
from utils.parser import parse_json
from utils.file import *
import os

class BookCreator:
    BOOK_STRUCTURE_RETRY_LIMIT = 3

    def update_progress(self, progress_path, progress_data, **kargs):
        progress_data.update(kargs)
        save_json(progress_path, progress_data)

    # Recursive retries as LLM sometimes returns invalid json
    def create_book_structure(self,model,book_context,book_genre,book_structure_path,retry=0):
        try:
            book_structure = generate_book_structure(model, book_context, book_genre)
            # Parse json
            data = parse_json(book_structure)
            save_json(book_structure_path, data)
        except Exception as e:
            print("Invalid Json Received from LLM\n{e}")
            if retry < self.BOOK_STRUCTURE_RETRY_LIMIT:
                retry += 1
                print("Retrying to create book structure. \nRetry Count: ",retry)
                self.create_book_structure(model,book_context,book_genre, book_structure_path,retry)
            else:
                print("Failed to create book structure. Exiting.")
                print("Please try again later with valid input or another LLM model or try changing prompt to get valid json response.")
                exit()


            

    def create_book(self,model, book_context, book_genre, directory_path, book_name):
        # Set paths based on inputs
        book_path = directory_path + book_name + ".docx"
        book_structure_path = directory_path + book_name + ".json"
        book_progress_path = directory_path + "." + book_name + "_progress.json"

        # Create directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        # If the book file exists and the progress file does not, assume the book is fully generated
        if os.path.exists(book_path) and not os.path.exists(book_progress_path):
            print(f"Book '{book_name}' already exists. No further processing is required.")
            exit()

        # Load book structure
        if not os.path.exists(book_structure_path):
            self.create_book_structure(model,book_context,book_genre,book_structure_path)
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
            book_intro = generate_book_introduction(model, book_context, book_genre, data)
            save_docx(book_path, book_intro.strip())
            add_page_break(book_path)
            self.update_progress(book_progress_path, progress_data, intro_generated=True)
            print("Successfully saved book introduction.")

        # Loop through chapters, headings, and subheadings, saving progress after each step
        for chapter_index in range(progress_data['chapter_index'], len(data['chapters'])):
            chapter = data['chapters'][chapter_index]
            chapter_title = chapter['chapter_title']
            chapter_headings = chapter['headings']
            print(f"Generating content for chapter: {chapter_title}")

            # Generate chapter introduction only if resuming from a new chapter
            if progress_data['heading_index'] == -1:
                chapter_intro = generate_book_chapter(model, book_context, book_genre, chapter_title, chapter_index + 1, chapter_headings)
                save_docx(book_path, chapter_intro.strip())
                print(f"Successfully saved chapter intro: {chapter_title}")

                # Save progress after chapter intro generation
                self.update_progress(book_progress_path, progress_data, chapter_index=chapter_index, heading_index=0)

            # Loop through headings
            for heading_index in range(progress_data['heading_index'], len(chapter_headings)):
                heading = chapter_headings[heading_index]
                heading_title = heading['heading']
                sub_headings = heading['subheadings']
                print(f"Generating content for heading: {heading_title}")

                if progress_data['subheading_index'] == -1:
                    heading_content = generate_book_heading(model, book_context, book_genre, chapter_title, heading_title, heading_index + 1, sub_headings)
                    save_docx(book_path, heading_content.strip())
                    print(f"Successfully saved heading content: {heading_title}")

                    # Save progress after heading generation
                    self.update_progress(book_progress_path, progress_data, chapter_index=chapter_index, heading_index=heading_index, subheading_index=0)

                # Loop through subheadings
                for subheading_index in range(progress_data['subheading_index'], len(sub_headings)):
                    sub_heading = sub_headings[subheading_index]
                    print(f"Generating content for subheading: {sub_heading}")

                    sub_heading_content = generate_book_subheading(model, book_context, book_genre, chapter_title, heading_title, heading_index, sub_heading)
                    save_docx(book_path, sub_heading_content.strip())
                    print(f"Successfully saved subheading content: {sub_heading}")

                    # Update progress after subheading generation
                    self.update_progress(book_progress_path, progress_data, chapter_index=chapter_index, heading_index=heading_index, subheading_index=subheading_index + 1)

                # Reset subheading index for the next heading
                self.update_progress(book_progress_path, progress_data, subheading_index=-1)

            # Add a page break after each chapter
            add_page_break(book_path)

            # Reset heading index for the next chapter
            self.update_progress(book_progress_path, progress_data, heading_index=-1)

        # Clean up progress file after successful completion
        if os.path.exists(book_progress_path):
            os.remove(book_progress_path)

