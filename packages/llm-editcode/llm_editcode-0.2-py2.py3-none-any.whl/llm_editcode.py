import re
import click
import llm

SYSTEM_PROMPT = """
Take requests for changes to the supplied code.

Always reply to the user in the same language they are using.

You MUST:

1. Propose *SEARCH/REPLACE* edits for the code provided in the chat.

2. Think step-by-step and explain the needed changes in a few short sentences.

3. Describe each change with a *SEARCH/REPLACE block* per the examples below.

All changes to files must use this *SEARCH/REPLACE block* format.
ONLY EVER RETURN CODE IN A *SEARCH/REPLACE BLOCK*!

# Example conversations:

## USER: Change get_factorial() to use math.factorial

## ASSISTANT: To make this change we need to make the following changes:

1. Import the math package.
2. Remove the existing factorial() function.
3. Update get_factorial() to call math.factorial instead.

Here are the *SEARCH/REPLACE* blocks:

<SEARCH>
from flask import Flask
</SEARCH>
<REPLACE>
import math
from flask import Flask
</REPLACE>

<SEARCH>
def factorial(n):
    "compute factorial"

    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

</SEARCH>
<REPLACE>
</REPLACE>

<SEARCH>
    return str(factorial(n))
</SEARCH>
<REPLACE>
    return str(math.factorial(n))
</REPLACE>

# *SEARCH/REPLACE block* Rules:

Every *SEARCH/REPLACE block* must use this format:

1. The start of search block: <SEARCH>
2. A contiguous chunk of lines to search for in the existing source code
3. The end of the search block: </SEARCH>
4. The start of replace block: <REPLACE>
5. The lines to replace into the source code
6. The end of the replace block: </REPLACE>
7. Please *DO NOT* put *SEARCH/REPLACE block* inside three backticks: {%raw%}```{%endraw%}

Every *SEARCH* section must *EXACTLY MATCH* the existing file content, character for character, including all comments, docstrings, etc.
If the input contains code or other data wrapped/escaped in json/xml/quotes or other containers, you need to propose edits to the literal contents of the file, including the container markup.

*SEARCH/REPLACE* blocks will replace *all* matching occurrences.
Include enough lines to make the SEARCH blocks uniquely match the lines to change.

*DO NOT* include three backticks: {%raw%}```{%endraw%} in your response!
Keep *SEARCH/REPLACE* blocks concise.
Break large *SEARCH/REPLACE* blocks into a series of smaller blocks that each change a small portion of the file.
Include just the changing lines, and a few surrounding lines if needed for uniqueness.
Do not include long runs of unchanging lines in *SEARCH/REPLACE* blocks.

To move code within a file, use 2 *SEARCH/REPLACE* blocks: 1 to delete it from its current location, 1 to insert it in the new location.

ONLY EVER RETURN CODE IN A *SEARCH/REPLACE BLOCK*!
""".strip()

@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.argument("args", nargs=-1)
    @click.option("-f", "--file", required=True, help="File to edit")
    @click.option("-m", "--model", default=None, help="Specify the model to use")
    @click.option("-s", "--system", help="Custom system prompt")
    @click.option("--key", help="API key to use")
    def editcode(args, file, model, system, key):
        """Edit code files in place"""
        from llm.cli import get_default_model
        model_id = model or get_default_model()
        model_obj = llm.get_model(model_id)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)
        # prompt the llm
        prompt = []
        with open(file, "r") as f:
            code = f.read()
            prompt.append(f"=== File: {file} ===")
            prompt.append(code)
            prompt.append("====")
        prompt.append(" ".join(args))
        result = model_obj.prompt("\n".join(prompt), system=system or SYSTEM_PROMPT)
        for chunk in result:
            print(chunk, end='')
        # edit the file contents
        edits = extract(str(result))
        if not edits:
            print("No edits found in response")
            return
        code = apply(code, edits)
        # Write back to file
        with open(file, "w") as f:
            f.write(code)
        print(f"Applied {len(edits)} edit(s) to {file}")


class Edit:
    def __init__(self, search, replace):
        self.search = search
        self.replace = replace

    def __str__(self):
        return f"<SEARCH>\n{self.search}\n</SEARCH>\n<REPLACE>\n{self.replace}\n</REPLACE>\n"

    def __repr__(self):
        return str(self)

def extract(s):
    """
    Extracts code edits from a string containing <SEARCH> and <REPLACE> tags.

    Args:
        s (str): The input string containing the edits.

    Returns:
        list[Edit]: A list of Edit objects with search and replace fields.
    """
    edits = []
    pattern = re.compile(r"<SEARCH>(.*?)</SEARCH>\s*<REPLACE>(.*?)</REPLACE>", re.DOTALL)
    matches = pattern.findall(s)
    for search, replace in matches:
        search = search.strip('\n')
        replace = replace.strip('\n')
        edits.append(Edit(search, replace))
    return edits

def apply(s, edits):
    """
    Applies a series of edits to the input string.

    Args:
        s (str): The input text to modify.
        edits (list[Edit]): The edits to apply.

    Returns:
        str: The modified text.
    """
    lines = s.splitlines()
    for edit in edits:
        search_lines = edit.search.splitlines()
        replace_lines = edit.replace.splitlines()
        index = find_sublist_index(lines, search_lines)
        if index != -1:
            lines = lines[:index] + replace_lines + lines[index + len(search_lines):]
    
    # Preserve original trailing newline if it exists
    if s.endswith('\n'):
        return '\n'.join(lines) + '\n'
    return '\n'.join(lines)

def find_sublist_index(lines, search_lines):
    """
    Finds the start index of a sublist in a list of lines.

    Args:
        lines (list[str]): The main list of lines.
        search_lines (list[str]): The sublist to find.

    Returns:
        int: The starting index of the sublist, or -1 if not found.
    """
    for i in range(len(lines) - len(search_lines) + 1):
        if lines[i:i + len(search_lines)] == search_lines:
            return i
    return -1
