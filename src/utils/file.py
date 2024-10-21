import pypandoc
import subprocess
import tempfile
import os
import json
from docx import Document

# Function to convert markdown to a .docx file
def __markdown_to_docx__(markdown_content, output_file):
    print("trying to create docx file")
    try:
        # Attempt to convert the markdown content to docx and save it
        output = pypandoc.convert_text(markdown_content, 'docx', format='md', outputfile=output_file)
        
        # The output is 0 if successful
        if output == 0 or output == "":
            print(f"File '{output_file}' created successfully!")
        else:
            print(f"Failed to create file '{output_file}'. Output: {output}")
    except OSError as e:
        # Print the error if pandoc isn't found or the conversion fails
        print(f"Conversion failed. Error: {e}")


def __append_markdown_to_docx__(large_docx_path, markdown_content, output_docx_path):
    # Step 1: Create a temporary markdown file from in-memory content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as temp_md_file:
        temp_md_file.write(markdown_content.encode('utf-8'))
        temp_md_file.flush()  # Make sure the content is written to disk
        temp_md_file_path = temp_md_file.name
    
    # Step 2: Convert the temporary markdown file to a temporary docx file using Pandoc
    temp_docx_file_path = tempfile.mktemp(suffix=".docx")
    subprocess.run(['pandoc', temp_md_file_path, '-o', temp_docx_file_path])
    
    # Step 3: Append the converted docx to the large docx file
    subprocess.run(['pandoc', large_docx_path, temp_docx_file_path, '-o', output_docx_path])

    # Step 4: Clean up the temporary files
    os.remove(temp_md_file_path)
    os.remove(temp_docx_file_path)

def save_docx(file_path,content):
    if os.path.exists(file_path):
        # print("appending to existing file")
        __append_markdown_to_docx__(file_path, content, file_path)
    else:
        # print("creating new file")
        __markdown_to_docx__(content, file_path)


def add_page_break(file_path):
    # Open the existing .docx file
    doc = Document(file_path)
    # Add a page break at the end
    doc.add_page_break()
    # Save the modified document
    doc.save(file_path)
    print("Page break added successfully!")

## json file operations
# save json in file
def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Data saved in {file_path}")

# load json from file
def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data