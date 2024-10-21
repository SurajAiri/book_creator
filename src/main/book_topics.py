from langchain.prompts import  PromptTemplate
from main.prompt_template import STRUCTURE_PROMPT_TEMPLATE


# Function to generate book structure
def generate_book_structure(llm,context,genre):
    # Define a prompt template to generate the book structure in JSON
    structure_prompt_template = STRUCTURE_PROMPT_TEMPLATE

    prompt = PromptTemplate(input_variables=["context","genre"], template=structure_prompt_template).format(context=context, genre=genre)
    structure_response = llm(prompt)
    return structure_response
