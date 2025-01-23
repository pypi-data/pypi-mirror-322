import re
import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import sys
from typing import TYPE_CHECKING
from mdcollections.base_types import MDPage

# if TYPE_CHECKING:
#     from .markdown_server import MDServer

def execute_streamlit_code(code_block):
    """
    Execute a streamlit code block and capture its output.
    The code block should be valid Python code that uses streamlit.
    """
    # Create string buffer to capture any print outputs
    old_stdout = sys.stdout
    redirected_output = StringIO()
    sys.stdout = redirected_output

    try:
        # Execute the code block
        # The code block can use st, pd, np which are already imported
        exec(code_block, {
            'st': st,
            'pd': pd,
            'np': np
        })
        
        # Get any printed output
        printed_output = redirected_output.getvalue()
        return True, printed_output
    except Exception as e:
        return False, f"Error: {str(e)}\n\nFailed code:\n{code_block}"
    finally:
        # Restore stdout
        sys.stdout = old_stdout


def process_streamlit_blocks(page: MDPage) -> MDPage:
    """
    Find and process ```py sl code blocks in markdown content.
    Returns the modified content with executed streamlit code blocks replaced by their output.
    """
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")
    # if not hasattr(md_server, 'collections_manager'):
    #     raise TypeError("md_server must be an instance of MDServer")

    def replace_code_block(match):
        code = match.group(1).strip()
        success, result = execute_streamlit_code(code)
        
        if not success:
            # If execution failed, return the error message
            return f"```\n{result}\n```"
        
        # If successful, return empty string - the streamlit components 
        # will be rendered but the code block itself won't be shown
        return ""

    # Process the code block
    processed_content = re.sub(r"```py\s+sl\n(.*?)\n```", replace_code_block, page.content, flags=re.DOTALL)

    page.content_ = processed_content
    
    return page
