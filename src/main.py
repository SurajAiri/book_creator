
from langchain_community.llms import Ollama
from base import BookCreator


book_creator = BookCreator()

# Initialize the Ollama model
model = Ollama(model='phi3', temperature=0.7)
book_creator.create_book(
    model,
    book_context="A book about various techniques used in NLP and their applications for beginners.",
    book_genre="Educational",
    directory_path="../output/",
    book_name="NLP Techniques"
)
