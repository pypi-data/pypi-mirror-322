import re
from typing import TYPE_CHECKING
from mdcollections.base_types import MDPage


def process_markdown_mermaid(page: MDPage) -> MDPage:
    """Convert ```mermaid blocks to ```py sl blocks that use st_mermaid."""
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")

    def replace_mermaid_block(match):
        mermaid_code = match.group(1).strip()
        
        # Create the streamlit code block
        # Note: The mermaid code needs to be properly escaped as a string
        mermaid_code = mermaid_code.replace('"', '\\"')  # Escape double quotes
        streamlit_code = f'''```py sl
from streamlit_mermaid import st_mermaid
st_mermaid("""
{mermaid_code}
""")
```'''
        return streamlit_code

    # Process all mermaid code blocks
    processed_content = re.sub(r"```mermaid\n(.*?)\n```", replace_mermaid_block, page.content, flags=re.DOTALL)
    page.content_ = processed_content
    
    return page
