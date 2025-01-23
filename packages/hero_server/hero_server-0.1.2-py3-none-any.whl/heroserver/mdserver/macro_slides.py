import re
import streamlit as st
from PIL import Image
from typing import TYPE_CHECKING, List
from mdcollections.base_types import MDPage, MDImage

# if TYPE_CHECKING:
#     from .markdown_server import MDServer

def create_slider_component(images: List[str]) -> None:
    """Create a Streamlit component for image slides."""
    st.markdown("""
        <style>
        .stImage {
            cursor: pointer;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("⬅️ Previous"):
            st.session_state.current_slide = (st.session_state.current_slide - 1) % len(images)
            
    with col3:
        if st.button("Next ➡️"):
            st.session_state.current_slide = (st.session_state.current_slide + 1) % len(images)
    
    # Display current image
    current_image_spec = images[st.session_state.current_slide]
    if not hasattr(st.session_state, 'md_server') or not st.session_state.md_server.collections_manager:
        st.error("Collections manager not initialized")
        return

    try:
        image_item = st.session_state.md_server.collections_manager.image_get(current_image_spec)
        image = Image.open(image_item.path)
        st.image(image, use_column_width=True)
    except Exception as e:
        st.error(f"Could not load image: {current_image_spec}. Error: {str(e)}")
    
    # Display slide counter
    st.caption(f"Slide {st.session_state.current_slide + 1} of {len(images)}")

def process_markdown_slides(page: MDPage) -> MDPage:
    """Convert ```slides blocks to ```py sl blocks that use the slider component."""
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")
    # if not hasattr(md_server, 'collections_manager'):
    #     raise TypeError("md_server must be an instance of MDServer")

    # # Store md_server in session state for use by create_slider_component
    # st.session_state.md_server = md_server

    def replace_slides_block(match):
        slides_content = match.group(1).strip()
        image_paths = [line.strip() for line in slides_content.split('\n') if line.strip()]
        
        # Create the streamlit code block
        image_paths_str = repr(image_paths)
        streamlit_code = f'''```py sl
from .macro_slides import create_slider_component
create_slider_component({image_paths_str})
```'''
        return streamlit_code

    # Process all slides code blocks
    page.content_ = re.sub(r"```slides\n(.*?)\n```", replace_slides_block, page.content, flags=re.DOTALL)
    
    return page
