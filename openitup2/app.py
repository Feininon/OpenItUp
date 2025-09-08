import requests
import json
import ast
from flask import Flask, render_template, request

# --- App Setup ---
app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gpt-oss:20b" # Or any other model you have downloaded

# --- Helper Function to Call Ollama ---
# This avoids repeating the same request logic everywhere
def call_ollama(prompt: str):
    """Sends a prompt to the Ollama API and returns the response."""
    try:
        payload = {
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=3000)
        response.raise_for_status()
        return response.json().get("response", "Error: No response from model.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"

# --- Homepage Route ---
@app.route('/')
def index():
    return render_template('index.html')

# --- 1. StoryCode Feature ---
# (Your original feature, now in its own endpoint)
class CodeAnalyzer(ast.NodeVisitor): # AST parser from our previous example
    def __init__(self):
        self.elements = {"functions": [], "loops": [], "conditions": [], "variables": set()}
    def visit_FunctionDef(self, node): self.elements["functions"].append(node.name); self.generic_visit(node)
    def visit_For(self, node): self.elements["loops"].append("for loop"); self.generic_visit(node)
    def visit_While(self, node): self.elements["loops"].append("while loop"); self.generic_visit(node)
    def visit_If(self, node): self.elements["conditions"].append("if/else statement"); self.generic_visit(node)
    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Store, ast.Param)): self.elements["variables"].add(node.id)
        self.generic_visit(node)

@app.route('/storycode', methods=['GET', 'POST'])
def storycode():
    result = ""
    if request.method == 'POST':
        code = request.form['code']
        prompt = f"You are StoryCode, a master storyteller. Turn the following code structure into a whimsical, short fairy tale under 150 words: {code}"
        result = call_ollama(prompt)
    return render_template('storycode.html', result=result)


# --- 2. Mental Health Chatbot for Coders ---
@app.route('/mental-health', methods=['GET', 'POST'])
def mental_health():
    result = ""
    if request.method == 'POST':
        issue = request.form['issue']
        prompt = f"""
        You are a caring, empathetic, and supportive mental health companion AI named 'Cody'.
        Your user is a software developer who is feeling stressed.
        Their issue is: '{issue}'.
        Your task is to:
        1. Validate their feelings.
        2. Offer a comforting and constructive perspective.
        3. Provide one simple, actionable piece of advice (like taking a short walk, practicing the 5-4-3-2-1 grounding technique, or timeboxing a problem).
        Keep your response warm, friendly, and under 200 words. Do not give medical advice.
        """
        result = call_ollama(prompt)
    return render_template('mental_health.html', result=result)

# --- 3. Generative Art from Programming Challenges ---
# This is a clever trick: we ask the LLM to generate SVG code (which is just text).
@app.route('/art-generator', methods=['GET', 'POST'])
def art_generator():
    art_svg = ""
    if request.method == 'POST':
        challenge = request.form['challenge']
        prompt = f"""
        You are an abstract digital artist who creates SVG code.
        Based on the programming theme '{challenge}', generate a complete, valid, and visually interesting SVG image.
        The SVG should be 400x400 pixels. Use a dark background and vibrant colors.
        Your output must be ONLY the SVG code, starting with `<svg` and ending with `</svg>`. No explanations.
        """
        art_svg = call_ollama(prompt)
    # The |safe filter in the HTML is crucial to render the SVG
    return render_template('art_generator.html', art_svg=art_svg)


# --- 4. Code Bug Joke Generator ---
@app.route('/joke-generator', methods=['GET', 'POST'])
def joke_generator():
    result = None
    if request.method == 'POST':
        bug = request.form['bug']
        prompt = f"""
        You are a programmer comedian. Your task is to analyze a code bug, create a funny, one-line joke about it, and then provide a simple explanation of the bug.
        The bug is: '{bug}'.
        Respond in a valid JSON format with two keys: "joke" and "explanation".
        Example:
        {{
            "joke": "Why did the recursive function get a loan? Because it was expecting a big return!",
            "explanation": "A recursive function calls itself. If it doesn't have a 'base case' to stop, it can lead to a 'stack overflow' error, like a debt that never gets paid off."
        }}
        """
        response_text = call_ollama(prompt)
        try:
            # Clean the response to ensure it's valid JSON
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response_text[start:end]
                result = json.loads(json_str)
            else:
                result = {"joke": "The model told a joke I couldn't parse!", "explanation": "The AI's response was not in the expected JSON format. This is like an API returning XML when you're expecting JSON – a classic mix-up!"}
        except json.JSONDecodeError:
            result = {"joke": "The AI's JSON was malformed!", "explanation": f"The response from the model was not valid JSON, which caused a parsing error. Response was: {response_text}"}

    return render_template('joke_generator.html', result=result)


# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)