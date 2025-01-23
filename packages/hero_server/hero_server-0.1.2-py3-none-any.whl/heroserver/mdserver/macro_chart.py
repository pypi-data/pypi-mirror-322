import re
from typing import TYPE_CHECKING
from mdcollections.base_types import MDPage

def js_to_python(js_str):
    """Convert JavaScript object notation to Python dictionary syntax."""
    # Remove any 'option =' prefix and trailing semicolon
    js_str = re.sub(r'^option\s*=\s*', '', js_str)
    js_str = re.sub(r';(\s*)$', '', js_str)
    
    # Convert JavaScript property names to Python dictionary keys
    js_str = re.sub(r'(\b\w+):', r'"\1":', js_str)
    
    # Convert single quotes to double quotes for string values
    # First, replace escaped single quotes with a placeholder
    js_str = js_str.replace("\\'", "___ESCAPED_QUOTE___")
    # Then replace regular single quotes with double quotes
    js_str = js_str.replace("'", '"')
    # Finally, restore escaped single quotes
    js_str = js_str.replace("___ESCAPED_QUOTE___", "\\'")
    
    # Handle trailing commas
    js_str = re.sub(r',(\s*[}\]])', r'\1', js_str)
    
    # Handle special JavaScript values
    js_str = js_str.replace('true', 'True').replace('false', 'False').replace('null', 'None')
    
    # Remove any comments
    js_str = re.sub(r'//.*?\n|/\*.*?\*/', '', js_str, flags=re.DOTALL)
    
    return js_str.strip()

def process_markdown_echarts(page: MDPage) -> MDPage:
    """Convert ```echarts blocks to ```py sl blocks that use st_echarts."""
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")

    def replace_echarts_block(match):
        echarts_code = match.group(1).strip()
        python_code = js_to_python(echarts_code)
        
        # Create the streamlit code block
        streamlit_code = f"""```py sl
from streamlit_echarts import st_echarts
option = {python_code}
st_echarts(options=option, height="400px")
```"""
        return streamlit_code

    # Process all echarts code blocks
    processed_content = re.sub(r"```echarts\n(.*?)\n```", replace_echarts_block, page.content, flags=re.DOTALL)
    
    page.content_ = processed_content
    
    return page
