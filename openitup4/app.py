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

@app.route('/commit-poet', methods=['GET', 'POST'])
def commit_poet():
    result = ""
    # Use .get() to avoid errors on first page load
    code_before = request.form.get('code_before', '')
    code_after = request.form.get('code_after', '')
    commit_style = request.form.get('style', 'Conventional')

    if request.method == 'POST':
        if not code_before and not code_after:
            result = "Please provide the code before and after your changes."
        else:
            prompt = f"""
            You are a Git expert who writes commit messages. Analyze the following code change and write a commit message in the '{commit_style}' style.
            Generate a concise, one-line subject followed by a blank line and a brief, bulleted description of the main changes.

            Code Before:
            ```{code_before}```

            Code After:
            ```{code_after}```
            """
            result = call_ollama(prompt)
            
    return render_template('commit_poet.html', result=result, code_before=code_before, code_after=code_after, style=commit_style)

@app.route('/regex-wizard', methods=['GET', 'POST'])
def regex_wizard():
    result = ""
    form_submitted = ""
    # Use .get() to repopulate forms
    description = request.form.get('description', '')
    regex_pattern = request.form.get('regex_pattern', '')

    if request.method == 'POST':
        # Check which form was submitted
        if 'generate_regex' in request.form:
            form_submitted = "generate"
            prompt = f"""
            You are a regular expression expert. Your task is to generate a regex pattern that precisely matches the following description.
            Provide ONLY the regex pattern and nothing else.

            Description: '{description}'
            """
            result = call_ollama(prompt)
        elif 'explain_regex' in request.form:
            form_submitted = "explain"
            prompt = f"""
            You are a regular expression expert. Your task is to break down the following regex pattern and explain each part of it in simple, bulleted points.

            Regex Pattern: `{regex_pattern}`
            """
            result = call_ollama(prompt)

    return render_template('regex_wizard.html', result=result, form_submitted=form_submitted, description=description, regex_pattern=regex_pattern)

@app.route('/error-sleuth', methods=['GET', 'POST'])
def error_sleuth():
    result = ""
    error_message = request.form.get('error_message', '')

    if request.method == 'POST':
        if not error_message.strip():
            result = "Please paste an error message or stack trace to analyze."
        else:
            prompt = f"""
            You are an expert developer and debugger called 'The Sleuth'. A user has provided an error message. Your task is to:
            1. **Explain the Error:** In simple terms, what does this error mean?
            2. **List Likely Causes:** In a bulleted list, what are the most common reasons for this error?
            3. **Suggest Solutions:** In a numbered list, what concrete steps can the user take to fix it?

            Error Message:
            ```{error_message}```
            """
            result = call_ollama(prompt)
            
    return render_template('error_sleuth.html', result=result, error_message=error_message)

@app.route('/api-mockup', methods=['GET', 'POST'])
def api_mockup():
    result = ""
    description = request.form.get('description', '')

    if request.method == 'POST':
        if not description.strip():
            result = "Please describe the data model you want to mock."
        else:
            prompt = f"""
            You are a backend API design expert who generates sample data.
            A user will describe a data model. Your task is to generate a realistic, sample JSON response for a GET request that would return a list of these objects.
            Generate a valid JSON array containing 3 sample objects based on the description.
            Provide ONLY the JSON code and nothing else.

            Description: '{description}'
            """
            result = call_ollama(prompt)

    return render_template('api_mockup.html', result=result, description=description)

@app.route('/doc-writer', methods=['GET', 'POST'])
def doc_writer():
    result = ""
    function_code = request.form.get('function_code', '')
    doc_style = request.form.get('style', 'Google')

    if request.method == 'POST':
        if not function_code.strip():
            result = "Please paste a Python function to document."
        else:
            prompt = f"""
            You are an expert Python developer who writes excellent documentation.
            Analyze the following Python function and write a complete {doc_style}-style docstring for it.
            The docstring should include a one-line summary, a longer description (if necessary), and sections for arguments (Args) and what it returns (Returns).
            Provide back the entire function with the new docstring inserted.

            Function:
            ```{function_code}```
            """
            result = call_ollama(prompt)

    return render_template('doc_writer.html', result=result, function_code=function_code, style=doc_style)

@app.route('/code-visualizer', methods=['GET', 'POST'])
def code_visualizer():
    result = ""
    code_to_visualize = request.form.get('code_to_visualize', '')

    if request.method == 'POST':
        if not code_to_visualize.strip():
            result = "flowchart TD\nA[Start] --> B[Please paste a function to visualize.] --> C[End]"
        else:
            prompt = f"""
            You are an expert software analyst. Your task is to analyze the following Python code and generate a Mermaid.js flowchart diagram that visually represents its logic.
            - Use flowchart TD (top down).
            - Use diamond shapes for conditions (if/else).
            - Use clear, concise labels for each step.
            - Provide ONLY the Mermaid syntax, starting with 'flowchart TD'. Do not include markdown fences like ```.

            Python Code:
            ```{code_to_visualize}```
            """
            raw_result = call_ollama(prompt)

            try:
                # Find the start of the flowchart code
                start_index = raw_result.find("flowchart")
                if start_index != -1:
                    # Extract the potential mermaid block
                    mermaid_block = raw_result[start_index:].strip()
                    
                    # --- NEW CLEANUP LOGIC ---
                    # The model sometimes duplicates the 'flowchart TD' line. This code cleans it up.
                    lines = mermaid_block.split('\n')
                    cleaned_lines = []
                    found_declaration = False
                    for line in lines:
                        trimmed_line = line.strip()
                        if trimmed_line.lower().startswith("flowchart"):
                            # Only add the flowchart declaration once
                            if not found_declaration:
                                cleaned_lines.append(trimmed_line)
                                found_declaration = True
                            # Otherwise, we skip the duplicate line
                        elif trimmed_line: # Add any other non-empty lines
                            cleaned_lines.append(trimmed_line)
                    
                    # Rejoin the cleaned lines into the final result
                    result = "\n".join(cleaned_lines)

                else:
                    # If 'flowchart' isn't found, the model failed.
                    result = "flowchart TD\nA[Error] --> B[Model did not return valid Mermaid syntax.]"
            except Exception:
                result = "flowchart TD\nA[Error] --> B[An error occurred while parsing the model response.]"
            
    return render_template('code_visualizer.html', result=result, code_to_visualize=code_to_visualize)

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    