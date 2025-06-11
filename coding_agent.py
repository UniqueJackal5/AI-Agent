# coding_agent.py
import argparse
import os
from gemini_core import call_gemini # <-- Importing our function from the other file!

# --- 1. The Agent's Persona: The System Prompt ---
# This is one of the most important parts. It gives the AI its instructions and rules.
# A good system prompt dramatically improves the quality of the output.
SYSTEM_PROMPT = """
You are an expert pair-programming assistant named 'CodeAgent'.
Your sole purpose is to help a user modify a code file.
You will be given the full content of a code file and a user request for a change.
You must follow these rules strictly:
1.  Analyze the user's request and the provided file content carefully.
2.  Generate ONLY the new or modified code block (function, class, etc.).
3.  Do NOT output the entire file's content again. Only provide the changed section.
4.  Do NOT include any explanations, conversational text, apologies, or introductions like "Here is the code:".
5.  Do NOT wrap the code in markdown backticks like ```python. Output only the raw code.
6.  If the user asks to add a new function, generate only that new function.
7.  If the user asks to modify an existing function, generate the complete, modified version of that function.
"""

# --- 2. Helper Functions ---
def read_file_content(file_path: str) -> str | None:
    """A safe way to read the content of a file."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def construct_final_prompt(user_request: str, file_content: str) -> str:
    """Assembles the system prompt, user request, and file context into one large prompt."""
    # This structure helps the model clearly distinguish its instructions, the context, and the task.
    return f"""{SYSTEM_PROMPT}

--- START OF FILE CONTENT ---
{file_content}
--- END OF FILE CONTENT ---

--- USER REQUEST ---
{user_request}
--- END OF USER REQUEST ---

Based on the file content and the user request, generate the required code block now:
"""

# --- 3. Main Execution Block ---
def main():
    # Set up command-line argument parsing to make our tool user-friendly
    parser = argparse.ArgumentParser(description="A simple AI coding agent powered by Gemini.")
    parser.add_argument("file", help="The path to the code file you want to modify.")
    parser.add_argument("prompt", help="Your instructions for the agent (e.g., 'add a docstring to the greet function').")
    
    # We pass the project ID as an argument to make the tool flexible
    parser.add_argument("--project-id", required=True, help="Your Google Cloud Project ID.")
    parser.add_argument("--location", default="us-central1", help="The Google Cloud location for Vertex AI.")
    
    args = parser.parse_args()

    # --- 4. The Agent's Workflow ---
    print(f"▶️  Agent starting...")
    print(f"▶️  Reading file: {args.file}")
    
    # Step A: Gather context
    file_content = read_file_content(args.file)
    if file_content is None:
        return # Exit if file reading failed

    print(f"▶️  User request: '{args.prompt}'")
    
    # Step B: Construct the final prompt
    final_prompt = construct_final_prompt(args.prompt, file_content)

    print("\n[INFO] Sending request to Gemini. Please wait...")
    
    # Step C: Call the Gemini model via our core function
    suggested_code = call_gemini(
        project_id=args.project_id,
        location=args.location,
        prompt=final_prompt
    )
    
    # Step D: Present the result
    print("\n✅ --- Gemini's Suggested Code ---")
    print(suggested_code)
    print("---------------------------------\n")
    print("Agent finished. You can now copy the code above and place it in your file.")

if __name__ == '__main__':
    main()