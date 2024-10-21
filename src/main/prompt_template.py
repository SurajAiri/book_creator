STRUCTURE_PROMPT_TEMPLATE = """
    Book Context: {context}
    Book Genre: {genre}

    Based on the book context and above provided information, create a book structure in JSON format with the following details:
    1. Book title (at least 4 titles).
    2. Chapters, each with headings and subheadings.

    Return the structure in JSON format like this:
    {{
    "title": ["Book Title1", "Book Title2", ...],
    "chapters": [
        {{
        "chapter_title": "Chapter 1",
        "headings": [
            {{
            "heading": "Heading 1",
            "subheadings": ["Subheading 1", "Subheading 2"]
            }}
        ]
        }},
        ...
    ]
    }}

    don't return anything except the JSON structure.
    """


BOOK_INTRODUCTION_TEMPLATE = """
    Imagine you are an author crafting a book. You need to write a compelling introduction for the book, emphasizing its overall theme and significance. You have the following details:

    Book Context: {context}
    Book Genre: {genre}
    Book Structure: {data}

    Please provide a markdown-formatted introduction that outlines the main ideas and themes of the book. The introduction should capture the essence of what will be discussed, including relevant examples or a narrative. It should give readers an overview of the book's content and purpose in a concise and engaging manner, while avoiding any specific mention of the chapters or headings. Focus on setting the stage for the reader, highlighting the book's importance and intriguing aspects without breaking it down into bullet points, as those will be addressed later in detail. Return the content in markdown format.
    """


CHAPTER_BRIEF_TEMPLATE= """
    Imagine you are an author crafting a book. You need to write a compelling introduction for a specific chapter, emphasizing its overall theme and significance. You have the following details:
    
    Book Context: {context}
    Book Genre: {genre}
    
    Chapter Title: {chapter}
    Chapter Index: {index}
    Headings to be Covered: {headings}

    start with # Chapter <chapter index>: <Chapter Title>
    
    Please provide a markdown-formatted introduction that outlines the main ideas and themes of the chapter. The introduction should capture the essence of what will be discussed, including relevant examples or a narrative, while avoiding any specific mention of the headings or subheadings. Focus on setting the stage for the reader, highlighting the chapter's importance and intriguing aspects without breaking it down into bullet points, as those will be addressed later in detail.
    """

HEADING_BRIEF_TEMPLATE = """
    You are author crafting book. You have done chapter introduction and going to write about heading. You have following information:

    Book Context: {context}
    Book Genre: {genre}
    Chapter Title: {chapter}
    Heading: {heading}
    Heading Index: {index}
    Sub-Headings: {sub_headings}

    Return the content in markdown format for the heading {heading} in the chapter {chapter}. The content should provide a detailed overview of the heading, including key points, examples, and any relevant information that will help readers understand the topic. Avoid going into subheadings at this stage and focus on creating a comprehensive narrative for the heading.
    """

SUBHEADING_BRIEF_TEMPLATE = """
    You are author crafting book. You have done chapter introduction and heading. You are going to write about sub-heading. You have following information:

    Book Context: {context}
    Book Genre: {genre}
    Chapter Title: {chapter}
    Heading: {heading}
    Heading Index: {index}
    Sub-Heading: {sub_heading}

    Return the content in markdown format for the sub-heading {sub_heading} under the heading {heading} in the chapter {chapter}. The content should provide detailed information on the sub-topic, including examples, explanations, and any other relevant details that will help readers understand the concept. Focus on creating a clear and informative narrative that complements the heading content.
    """
