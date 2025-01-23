import os
import re
import streamlit as st
from PIL import Image  # Pillow package provides PIL
from typing import Optional, List, Tuple, TYPE_CHECKING
from .macro_sl import process_streamlit_blocks
from .macro_chart import process_markdown_echarts
from .macro_mermaid import process_markdown_mermaid
from .macro_slides import process_markdown_slides
from .macro_sl import process_streamlit_blocks
from .macro_links import process_links
from .process_images import process_images
from mdcollections.tools import name_fix, is_image
from mdcollections.base_types import MDPage, MDCollection
from mdcollections.mdcollections import MDCollections
from .tools import debug,rewrite_summary_links


def summary_load(collection:MDCollection) -> MDPage:
    """Load the summary.md file if it exists, otherwise it creates an index"""
    if not isinstance(collection, MDCollection):
        raise TypeError("collection must be a MDCollection")
    try:
        mypage = collection.page_get("summary.md")
        mypage.content_=rewrite_summary_links(mypage.content_) #need to rewrite the first part of path as collection, might change in future
        return mypage
    except ValueError:
        return collection.index_page()

def process_markdown(page: MDPage, collections: MDCollections) -> MDPage:
    """Process markdown content and handle images, links, and streamlit code blocks.
    
    Args:
        page: The MDPage object to process
        collections: The MDCollections object containing all collections
    """
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")
    if not isinstance(collections, MDCollections):
        raise TypeError("collections must be a MDCollections")
    
    debug(f"Processing markdown for page: {page.name} in collection: {page.collection.name}\nInitial content length: {len(page.content)} characters")
    
    if page.processed:
        RuntimeError(f"double processing of page {page.name}")

    # Process special blocks with page and md_server arguments
    #debug("Processing echarts blocks...")
    page = process_markdown_echarts(page)
    
    #debug("Processing mermaid blocks...")
    page = process_markdown_mermaid(page)
    
    #debug("Processing slides blocks...")
    page = process_markdown_slides(page)
    
    #debug("Processing streamlit blocks...")
    page = process_streamlit_blocks(page)
    
    #debug("Processing links...")
    # Pass the debug flag to process_links
    page = process_links(page=page, collections=collections)
    
    page = process_images(page=page, collections=collections  )
    
    # Process remaining content
    if page.content.strip():
        debug(f"Rendering final markdown content (length: {len(page.content)} characters)")
        st.markdown(page.content, unsafe_allow_html=True)
    else:
        debug("No content to render after processing")
        
    return page

def parse_page_parameter(page_param: str) -> Tuple[Optional[str], str]:
    """Parse the page parameter to extract collection and file name."""
    if '__' in page_param:
        collection, filename = page_param.split('__', 1)
        return collection, filename
    return None, page_param
