import re
import streamlit as st

def strip_ansi_codes(text):
    """Remove ANSI escape codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)



def debug(message: str):
    """Display debug messages in a compact code block format.
    
    Args:
        message: The debug message to display
    """
    debug_enabled=st.session_state.debug_mode
    if debug_enabled:
        #st.code(message, language="text")
        print(strip_ansi_codes(message))


def rewrite_summary_links(text:str) -> str:
    import re
    
    def replace_first_slash(match):
        # Get the matched text
        link = match.group(1)
        # Replace the first slash with double underscore
        new_link = link.replace('/', '__', 1)
        return f'({new_link})'
    
    # Use a regular expression to find links in the format (path/to/resource)
    pattern = r'\(([^)]+)\)'
    
    # Process each line and apply the substitution
    rewritten_lines = []
    for line in text.splitlines():
        rewritten_line = re.sub(pattern, replace_first_slash, line)
        rewritten_lines.append(rewritten_line)
    
    # Join the rewritten lines back together
    return '\n'.join(rewritten_lines)
