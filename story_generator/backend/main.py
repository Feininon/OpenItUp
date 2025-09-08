import ast
import requests
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- 1. FastAPI App Setup ---
app = FastAPI()

# Allow requests from our React frontend (running on http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Pydantic Models for API data validation ---
class CodeRequest(BaseModel):
    code: str
    style: str = "a whimsical fairy tale" # Default story style

class StoryResponse(BaseModel):
    story: str

# --- 3. Code Parser using Python's AST ---
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.elements = {
            "functions": [],
            "loops": [],
            "conditions": [],
            "variables": set(),
        }

    def visit_FunctionDef(self, node):
        self.elements["functions"].append(node.name)
        self.generic_visit(node)

    def visit_For(self, node):
        self.elements["loops"].append("for loop")
        self.generic_visit(node)

    def visit_While(self, node):
        self.elements["loops"].append("while loop")
        self.generic_visit(node)

    def visit_If(self, node):
        self.elements["conditions"].append("if/else statement")
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Param)):
            self.elements["variables"].add(node.id)
        self.generic_visit(node)

def analyze_code(code: str) -> dict:
    try:
        tree = ast.parse(code)
        analyzer = CodeAnalyzer()
        analyzer.visit(tree)
        # Convert set to list for JSON serialization
        analyzer.elements["variables"] = list(analyzer.elements["variables"])
        return analyzer.elements
    except SyntaxError:
        return {"error": "Invalid Python code"}

# --- 4. Prompt Builder and Ollama Integration ---
OLLAMA_URL = "http://localhost:11434/api/generate"

def build_prompt(analysis: dict, style: str) -> str:
    # Create a summary of the code's structure
    summary = []
    if analysis.get("functions"):
        summary.append(f"a main character (a function) named '{', '.join(analysis['functions'])}'")
    if analysis.get("variables"):
        summary.append(f"with companions (variables) like '{', '.join(analysis['variables'])}'")
    if analysis.get("loops"):
        summary.append(f"who goes on a repetitive journey or quest (a {' and '.join(analysis['loops'])})")
    if analysis.get("conditions"):
        summary.append(f"and faces {len(analysis['conditions'])} forks in the road or moral dilemmas (if/else statements)")

    code_structure_summary = ", ".join(summary) + "."

    # The "Meta-Prompt" that instructs the LLM
    prompt = f"""
    You are StoryCode, a master storyteller who translates computer code into engaging narratives.
    Your task is to transform a summary of a program's structure into {style}.

    **Rules:**
    1.  The story must metaphorically represent the code's logic. A function is a character, a loop is a journey, a condition is a choice or conflict.
    2.  Use the actual names of functions and variables as characters or items in the story.
    3.  Keep the story short, concise, and under 200 words.
    4.  Be creative, humorous, and entertaining. Do NOT just describe what the code does line-by-line.

    **Code Structure Summary:**
    {code_structure_summary}

    Now, write the story.
    """
    return prompt

# --- 5. API Endpoint ---
@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: CodeRequest):
    analysis = analyze_code(request.code)
    if "error" in analysis:
        return StoryResponse(story=f"Error parsing code: {analysis['error']}")

    prompt = build_prompt(analysis, request.style)

    payload = {
        "model": "gpt-oss:20b",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120000)
        response.raise_for_status()
        story = response.json().get("response", "Failed to get a story from the model.")
        return StoryResponse(story=story.strip())
    except requests.exceptions.RequestException as e:
        return StoryResponse(story=f"Error connecting to Ollama: {e}")

# To run the server: uvicorn main:app --reload