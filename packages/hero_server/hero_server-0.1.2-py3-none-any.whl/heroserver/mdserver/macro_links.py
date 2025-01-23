import os
import re
import streamlit as st
from PIL import Image  # Pillow package provides PIL
from typing import Optional, List, Tuple, TYPE_CHECKING
from mdcollections.tools import name_fix, is_image
from mdcollections.base_types import MDPage
from mdcollections.mdcollections import MDCollections
from .process_images import process_image
from .tools import debug

def link_process(link: str, page: MDPage, collections: MDCollections, is_image_link: bool, debug_enabled: bool = False) -> str:
    """Process link path and verify existence in collection."""
    
    if not isinstance(link, str):
        raise TypeError("link  must be strings")
    
    if not isinstance(collections, MDCollections):
        raise TypeError("collection  must be MDCollection")

    if not isinstance(page, MDPage):
        raise TypeError("page  must be MDPage")

    debug(f"\nProcessing link: {link}")
    debug(f"Is image link: {is_image_link}")
    
    # Remove './' if present
    if link.startswith("./"):
        link = link[2:]
        debug("Removed './' prefix from link")
    
    # Get just the filename without directories
    link = os.path.basename(link)
    debug(f"Extracted basename: {link}")
    

    # Process link format
    if not '__' in link:
        if ":" in link:
            link = link.replace(':', '__')
            
    # Create full link if needed
    if not "__" in link:
        link = f"{page.collection.name}__{link}"    
        debug(f"Created full link: {link}")
        
    if link.count("__")>1:
        raise RuntimeError(f"cannot have 2x __ in ${link}")
        
    collection_name, item_name = link.split('__', 1)
            
    # Convert to lowercase and replace spaces with underscores
    item_name = name_fix(item_name)
    collection_name = name_fix(collection_name)
    debug(f"Normalized: '{collection_name}__{item_name}'")        
    
    # Ensure .md extension for pages
    if is_image_link:
        try:
            md_i = collections.image_get(collection_name=collection_name,image_name=item_name)
            debug("Successfully verified image exists")
            # process_image(md_i)
            # return ""
            return f"{collection_name}__{item_name}"
        except ValueError:
            debug(f"Error - image not found: {link}")
            return f'<span style="color: red;">ERROR: Image not found: {link}</span>'        
    else:
        if not item_name.endswith('.md'):
            item_name = f"{item_name}.md"
            debug(f"Added .md extension: {item_name}")
        try:
            collections.page_get(collection_name, item_name)
            debug("Successfully verified page exists")
        except ValueError:
            debug(f"Error - page not found: {link}")
            return f'<span style="color: red;">ERROR: Page not found: {link}</span>'
    
    return f"?page={collection_name}__{item_name}.md"

def process_links(page: MDPage, collections: MDCollections) -> MDPage:
    """Process links in the markdown content."""
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")
    if not isinstance(collections, MDCollections):
        raise TypeError("collections must be a MDCollections")

    debug(f"Processing links for page: {page.name}")
    debug(f"Content length before processing: {len(page.content)} characters")

    link_pattern = r'(!?)\[(.*?)\]\((.*?)\)'

    def replace_link(match):
        is_image_link = match.group(1) == '!'
        link_text = match.group(2)
        link_path = match.group(3)
        
        debug(f"Found link - Text: {link_text}, Path: {link_path}")
        debug(f"Is image link: {is_image_link}")
        
        processed_link = link_process(link_path, page, collections, is_image_link)
        
        if "ERROR:" in processed_link:
            debug(f"Link processing error: {processed_link}")
            return processed_link #this forwards the error, is html in red
            
        if is_image_link: 
            debug(f"Returning processed image link: ![{link_text}]({processed_link})")
            return f'![{link_text}]({processed_link})'
        else:
            debug(f"Returning processed text link: [{link_text}]({processed_link})")
            return f'[{link_text}]({processed_link})'
    
    page.content_ = re.sub(link_pattern, replace_link, page.content)
    
    debug(f"Content length after processing: {len(page.content)} characters")
    debug("Link processing complete")
    
    return page
