from langchain.prompts import  PromptTemplate
from main.prompt_template import *


def generate_book_introduction(llm,context, genre, data):
    book_introduction_template = BOOK_INTRODUCTION_TEMPLATE

    book_introduction_prompt = PromptTemplate(input_variables=["context","genre","data"], template=book_introduction_template)

    t = book_introduction_prompt.format(context=context, genre=genre, data=data)
    return llm(t)

def generate_book_chapter(llm,context,genre,chapter,chapter_index,headings):
    chapter_brief_template = CHAPTER_BRIEF_TEMPLATE

    chapter_prompt = PromptTemplate(input_variables=["context","index","genre","chapter","headings"], template=chapter_brief_template)

    t = chapter_prompt.format(context=context, genre=genre, chapter=chapter,index=chapter_index, headings=headings,)
    return llm(t)


def generate_book_heading(llm, context, genre, chapter, heading, index, sub_headings):
    heading_brief_template = HEADING_BRIEF_TEMPLATE

    heading_prompt = PromptTemplate(input_variables=["context","genre","chapter","heading","index","sub_headings"], template=heading_brief_template)

    t = heading_prompt.format(context=context, genre=genre, chapter=chapter, heading=heading, index=index, sub_headings=sub_headings)
    return llm(t)


def generate_book_subheading(llm, context, genre, chapter, heading, index, sub_heading):
    subheading_brief_template = SUBHEADING_BRIEF_TEMPLATE

    subheading_prompt = PromptTemplate(input_variables=["context","genre","chapter","heading","index","sub_heading"], template=subheading_brief_template)

    t = subheading_prompt.format(context=context, genre=genre, chapter=chapter, heading=heading, index=index, sub_heading=sub_heading)
    return llm(t)