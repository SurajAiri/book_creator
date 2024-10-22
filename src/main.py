
from langchain_community.llms import Ollama
from base import BookCreator

def progress_listener(message, progress=None):
    print(message)

# Initialize the Ollama model
model = Ollama(model='phi3', temperature=0.7)

book_creator = BookCreator(model,output_dir="../output/")

book_creator.create_book(
    book_context="A book about various techniques used in NLP and their applications for beginners.",
    book_genre="Educational",
    book_name="Basic NLP Techniques",
    progress_listener=progress_listener
)
