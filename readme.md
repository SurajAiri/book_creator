# Book Generator Using Local LLMs and LangChain

This project allows you to generate books from scratch by leveraging **LangChain** and a local Large Language Model (LLM). By providing the **book genre** and **book context**, the model will generate the entire book. This project is ideal for those looking to create educational content, stories, or research-based books without manual writing effort.

## Key Features

- **Book Creation from Scratch:** Generate books by specifying just a few parameters like genre, context, and title.
- **Local LLMs:** Uses local models, such as `phi3` from **Ollama**, ensuring fast and secure book generation without relying on external APIs.
- **Customizable Parameters:** Control the creative output by adjusting parameters like `temperature` to influence the creativity of the generated content.

## Requirements

This project uses **Poetry** for dependency management. Make sure you have Poetry installed. You can install Poetry by following the [Poetry installation guide](https://python-poetry.org/docs/#installation).

- Python 3.7+
- [LangChain](https://python.langchain.com/docs/introduction/)
- [Ollama](https://ollama.com/)
- Other dependencies managed by Poetry.

### Installing Dependencies

**Note:** There can be various ways to run python program but I have used poetry with mini-conda environment. So Here is a follow up step for how would i run this project. Feel free to run as you wish.

0. Install [anaconda](https://www.anaconda.com/download?utm_source=anacondadocs) or [miniconda](https://docs.anaconda.com/miniconda/miniconda-install/) and activate environment

```bash
conda create -n testEnv python==3.11
conda activate testEnv
```

1. Clone the repository:

   ```bash
   git clone https://github.com/SurajAiri/book_creator.git
   cd book-creator
   ```

2. Install the dependencies using Poetry:

   ```bash
   pip install poetry
   poetry install
   ```

3. Make sure you have Ollama installed to use local models. For more details, visit [Ollama's official site](https://ollama.com/).

```bash
ollama serve
```

4.1. Run program (GUI)

```bash
streamlit run src/app.py
```

4.2. Run program (CLI)

```bash
python src/main.py -c <book-context> -g <book-genre> -n <book-name>
```

## How to Run

You can generate a book from the terminal by specifying the **book context**, **book genre**, **book name**, and **output directory**. An optional parameter `temperature` allows you to control the creativity of the content.
You can get access manual for CLI using.

```bash
python src/main.py -h
```

### Usage Example

```bash
python src/main.py --book_context "A book about various techniques used in NLP and their applications for beginners." --book_genre "Educational" --book_name "Basic NLP Techniques" --output_dir "./output/" --temperature 0.7
```
