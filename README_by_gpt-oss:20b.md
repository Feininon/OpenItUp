# 🌟 StoryCode & Code‑Mate: A Multi‑Purpose Flask API
> **An all‑in‑one toolkit that turns code into stories, art, jokes, and much more**
> Powered by an Ollama LLM (default: `gpt‑oss:20b`)

---

## Table of Contents

| Section | Link |
|---------|------|
| 🎯 Overview | #overview |
| 🚀 Quick Start | #quick-start |
| 📦 Installation | #installation |
| ⚙️ Configuration | #configuration |
| 📖 Endpoints & Features | #endpoints |
| 🧪 Testing | #testing |
| 📝 Documentation | #documentation |
| 🛠️ Contributing | #contributing |
| 📄 License | #license |
| 🙏 Acknowledgements | #acknowledgements |

---

## 🎯 Overview

This Flask app bundles **nine distinct creative‑coding helpers** in a single web service:

| Feature | What it does |
|---------|--------------|
| **StoryCode** | Turns Python code snippets into whimsical fairy‑tales |
| **Mental‑Health Chatbot** | Empathetic support for stressed developers |
| **Art‑Generator** | Generates SVG art from a programming challenge |
| **Joke‑Generator** | One‑liner code‑bug jokes + explanation |
| **Commit‑Poet** | Write Git commit messages in a chosen style |
| **Regex‑Wizard** | Generate or explain regex patterns |
| **Error‑Sleuth** | Debug error messages & stack traces |
| **API‑Mockup** | Produce realistic JSON mock‑data for a data model |
| **Doc‑Writer** | Generate Google‑style docstrings for a Python function |
| **Code‑Visualizer** | Mermaid.js flowchart from Python code |

All routes are **REST‑style** and render simple, self‑contained HTML pages.
Behind the scenes they all call the Ollama LLM (via the `/api/generate` endpoint) with a carefully crafted prompt.

> **Why use Ollama?**
> - Runs locally, no API key required.
> - Free & fast.
> - Works with any model you have downloaded (`gpt‑oss:20b` is shipped with the repo as a sane default).

---

## 🚀 Quick Start

> **Prerequisites** – Python 3.10+, `pip`, and a running Ollama server.

```bash
# 1️⃣ Clone
git clone https://github.com/your-username/storycode.git
cd storycode

# 2️⃣ (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Download the default LLM (once)
ollama pull gpt-oss:20b

# 5️⃣ Start the app
python app.py

# 6️⃣ Open your browser
http://127.0.0.1:5000
```

You should see the home page with links to every feature.

---

## 📦 Installation

### Clone the repo

```bash
git clone https://github.com/your-username/storycode.git
cd storycode
```

### Install dependencies

```bash
pip install -r requirements.txt
```

> `requirements.txt` contains:
> - Flask
> - requests
> - (Optional) jinja2‑excel if you want to export tables

### Set up Ollama

```bash
# Download and install the Ollama client if you haven’t already
# https://ollama.ai/download

# Pull the default model (20 GB, may take a while)
ollama pull gpt-oss:20b
```

> **Tip**: If you want a smaller model, replace `MODEL` in `app.py` with e.g. `mistral:7b`.

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Base URL for your Ollama server |
| `MODEL` | `gpt-oss:20b` | The LLM you want to use |
| `DEBUG` | `True` (in `app.run`) | Flask debug mode |

If you prefer environment variables:

```bash
export OLLAMA_URL="http://localhost:11434/api/generate"
export MODEL="mistral:7b"
```

The app will pick them up automatically via `os.getenv()` (extend `app.py` accordingly).

---

## 📖 Endpoints & Features

Below is a quick reference to each route, the form fields it expects, and the prompt logic it uses.

| Route | Method | Form Fields | Example Request | What you’ll see |
|-------|--------|-------------|-----------------|-----------------|
| `/` | GET | – | Home page (link menu) | Links to every feature |
| `/storycode` | GET/POST | `code_snippet` | Submit a snippet → fairy‑tale |
| `/mental-health` | GET/POST | `message` | Ask for support → empathetic response |
| `/art-generator` | GET/POST | `challenge` | Submit a programming challenge → SVG art |
| `/joke-generator` | GET/POST | `bug_description` | Generate joke & explanation (JSON) |
| `/commit-poet` | GET/POST | `commit_message`, `style` | Choose a style (e.g. Conventional, Gitmoji,
Conventional) |
| `/regex-wizard` | GET/POST | `regex_type` (`generate`/`explain`), `pattern` | Generate or explain a regex |
| `/error-sleuth` | GET/POST | `error_message` | Analyse and explain an error |
| `/api-mockup` | GET/POST | `description` | Sample JSON array of 3 objects |
| `/doc-writer` | GET/POST | `function_code`, `style` | Generate Google‑style docstring |
| `/code-visualizer` | GET/POST | `code_to_visualize` | Mermaid flowchart (cleaned) |

All pages are **user‑friendly** – simply paste your snippet / description into the text area, press *Submit*, and
the result appears right below.

> **Mermaid diagrams** are returned *without* code fences. The app cleans up duplicate `flowchart TD` declarations
for you.
> **Joke responses** come wrapped in a JSON object so you can consume them programmatically if you need to.

---

## 🧪 Testing

### Unit tests

We provide a small test suite that mocks the Ollama call and verifies that each endpoint renders the expected
sections.

```bash
pip install pytest
pytest
```

> **If you run into “timeout” errors** – make sure the `OLLAMA_URL` is reachable.
> Adjust `timeout` in `call_ollama()` (currently set to 120 s).

### Manual testing

1. Use Postman / curl to hit each endpoint directly.
   ```bash
   curl -X POST http://127.0.0.1:5000/storycode \
        -d "code_snippet=def hello():\n    print('Hello!')"
   ```

2. Inspect the raw LLM output in the debug console to fine‑tune prompts.

---

## 📝 Documentation

The HTML templates live in `templates/` – they’re intentionally minimal, but you can add styling or copy‑paste
features as you wish.

**Prompt helpers**
All LLM calls are routed through the `call_ollama()` function:

```python
def call_ollama(prompt: str) -> str:
    payload = {"model": MODEL, "prompt": prompt}
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["response"]
```

Feel free to tweak the prompts in `app.py` if you want different output styles.

---

## 🛠️ Contributing

We’d love contributions! Please follow these steps:

1. **Fork** and **branch**
   ```bash
   git checkout -b feature/awesome-new-feature
   ```

2. **Create tests** for any new functionality.
3. **Follow PEP‑8** guidelines – `black` and `flake8` are pre‑configured.
4. Submit a **Pull Request** – include a concise description of the change.

> **Note**: When adding a new endpoint, remember to update the README so the community knows how to use it.

---

## 📄 License

MIT © 2024 **Your Name**
See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

| Resource | Purpose |
|----------|---------|
| **Ollama** – https://ollama.ai | Local LLM inference |
| **Flask** – https://flask.palletsprojects.com/ | Lightweight web framework |
| **Mermaid.js** – https://mermaid-js.github.io/mermaid/ | Flowchart rendering |
| **OpenAI Cookbook** – inspiration for prompt design | https://github.com/openai/openai-cookbook |
| **Google Docstring Style** – for `doc-writer` | https://google.github.io/styleguide/pyguide.html |

Feel free to give us a star ⭐ if you found this helpful!

---
