import argparse
from langchain_community.llms import Ollama
from base import BookCreator

# Function to handle progress updates
def progress_listener(message, progress=None):
    print(message)

def main(book_context,model_name, book_genre, book_name, output_dir, temperature):
    # Initialize the Ollama model with the specified temperature
    model = Ollama(model=model_name, temperature=temperature)
    
    # Initialize the BookCreator with the given model and output directory
    book_creator = BookCreator(model, output_dir=output_dir)

    # Call the create_book method with the provided arguments
    book_creator.create_book(
        book_context=book_context,
        book_genre=book_genre,
        book_name=book_name,
        progress_listener=progress_listener
    )

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Generate a book using NLP techniques.")

    # Define the arguments
    parser.add_argument('-c','--book_context', type=str, required=True, help='*Context or theme of the book')
    parser.add_argument('-g','--book_genre', type=str, required=True, help='*Genre of the book')
    parser.add_argument('-n','--book_name', type=str, required=True, help='*Title of the book')
    parser.add_argument('-m','--model-name',type=str,default='phi3',help='Name of the model to use (default: phi3)')
    parser.add_argument('-o','--output_dir', type=str, default="output/", help='Directory to save the generated book (default: output/)')
    parser.add_argument('-t','--temperature', type=float, default=0.7, help='Temperature setting for the model (default: 0.7)')

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(
        book_context=args.book_context,
        model_name=args.model_name,
        book_genre=args.book_genre,
        book_name=args.book_name,
        output_dir=args.output_dir,
        temperature=args.temperature
    )
