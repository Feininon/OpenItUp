# Code Creativity Suite 🎨✨

The Code Creativity Suite is a collection of AI-powered web tools for software developers, designed to assist with creative, practical, and sometimes tedious parts of the coding lifecycle. Powered by a local Large Language Model (LLM) via Ollama and a Flask backend, this suite provides a range of utilities from generating stories from your code to debugging complex errors.

## ✨ Features

This suite includes a growing number of tools, each on its own dedicated page:

  * **StoryCode:** Transforms Python code into a short, whimsical, character-driven narrative. A fun way to visualize your logic.
  * **Coder's Companion:** A supportive mental health chatbot trained to help developers deal with common stressors like imposter syndrome and burnout.
  * **Art Generator:** Creates abstract SVG art based on a programming concept or theme.
  * **Joke Generator:** Tells a programming joke about a specific bug or concept and then explains it.
  * **Commit Poet:** Generates well-formatted Git commit messages by analyzing the 'before' and 'after' states of your code.
  * **Regex Wizard:** A two-way tool that can generate a regular expression from a plain English description or explain a complex regex pattern in simple terms.
  * **Error Sleuth:** A debugging assistant that takes a stack trace or error message and provides a simple explanation, a list of likely causes, and suggested solutions.
  * **API Mockup:** Generates realistic JSON mock data from a simple description of a data model, perfect for frontend development.
  * **DocString Writer:** Automatically writes professional docstrings for your Python functions in various styles (Google, NumPy, etc.).
  * **Code Visualizer:** Analyzes a function's logic and generates a Mermaid.js flowchart diagram for easy visualization.

-----

## 🛠️ Tech Stack

This project is built with a focus on simplicity and local-first AI, using open-source tools.

  * **Backend:** **Python** with the **Flask** web framework.
  * **AI Model:** Any Ollama-compatible model(gpt-oss:20b). The connection is made via simple HTTP requests.
  * **Frontend:** Standard **HTML5**, **CSS3**, and minimal vanilla **JavaScript**.
  * **Templating:** **Jinja2** (comes with Flask).
  * **Diagrams:** **Mermaid.js** for rendering flowcharts in the Code Visualizer.

-----

## 🚀 Getting Started

Follow these instructions to get the Code Creativity Suite running on your local machine.

### Prerequisites

1.  **Python 3.8+**: Make sure you have a modern version of Python installed.
2.  **Ollama**: You must have [Ollama](https://ollama.com/) installed and running.
3.  **An LLM Model**: Pull a model to use with the application. We recommend a versatile model gpt-oss:20b.
    ```bash
    ollama pull gpt-oss:20b
    ```

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd code-creativity-suite
    ```

2.  **Create and activate a Python virtual environment:**

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
    or use conda env ig
    
    ```bash
    conda create --name [env_name] python=3.12
    conda activate [env_name]
    ```

4.  **Install the required Python packages:**

    ```bash
    pip install Flask requests
    ```

5.  **Configure the Model (Optional):**
    Open the `app.py` file and change the `MODEL` variable to the name of the model you have downloaded with Ollama.

    ```python
    # in app.py
    MODEL = "gpt-oss:20b" # Change this to your model
    ```

### Running the Application

1.  **Ensure Ollama is running:** Make sure the Ollama application is active on your machine.
2.  **Start the Flask server:** Run the following command from the project's root directory:
    ```bash
    python app.py
    ```
3.  **Open your browser:** Navigate to `http://127.0.0.1:5000`. You should see the homepage of the Code Creativity Suite\!

-----

## 📂 Project Structure

The project is organized in a standard Flask application structure:

```
code-creativity-suite/
├── app.py              # The main Flask application with all routes and logic.
├── templates/            # Contains all the HTML files for each tool.
│   ├── layout.html     # The base template with the navigation bar.
│   └── ...             # HTML files for each feature.
├── static/
│   └── style.css       # The single stylesheet for the entire application.
└── README.md           # This file.
```

## CONTRIBUTING

This is our project the 
