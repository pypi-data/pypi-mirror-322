import os
import re
import streamlit as st
from PIL import Image  # Pillow package provides PIL
from typing import Optional, List, Tuple, TYPE_CHECKING
from mdcollections.base_types import MDImage, MDPage
from mdcollections.mdcollections import MDCollections
from .tools import debug


def process_image(myimage: MDImage, alt_text: Optional[str] = None) -> str:
    """
    Process an image and return HTML img tag for proper rendering in markdown.
    
    Args:
        myimage: The MDImage object to process
        alt_text: Optional alternative text for the image
        
    Returns:
        str: HTML img tag with proper styling
    """
    if not isinstance(myimage, MDImage):
        raise TypeError("myimage must be a MDImage")
    try:
        # Verify image can be opened
        Image.open(myimage.path)
        
        # Construct static URL using collection name and relative path
        static_url = f"/app/static/{myimage.collection.name}/{myimage.rel_path}"
        
        # Create HTML img tag with proper styling
        return f'<img src="{static_url}" alt="{alt_text or ""}" style="max-width: 100%; height: auto; display: inline-block; margin: 0.5em 0;">'
    except Exception as e:
        debug(f"Error processing image {myimage.path}: {str(e)}")
        return f"Error loading image: {myimage.path}"


def process_images(page: MDPage, collections: MDCollections) -> MDPage:
    """
    Process images in the markdown content while preserving text structure.
    
    Args:
        page: The MDPage object containing markdown content
        collections: The MDCollections object containing image references
        
    Returns:
        MDPage: The processed page with images displayed
    """
    if not isinstance(page, MDPage):
        raise TypeError("page must be a MDPage")
    if not isinstance(collections, MDCollections):
        raise TypeError("collections must be a MDCollections")

    debug(f"Processing images for page: {page.name}")
    debug(f"Content length before processing: {len(page.content)} characters")

    # Match markdown image syntax: ![alt text](path)
    link_pattern = r'!\[(.*?)\]\((.*?)\)'

    def replace_link(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # Split path into collection and image name
        try:
            parts = image_path.split("__", 1)
            if len(parts) != 2:
                debug(f"Invalid image path format (missing __): {image_path}")
                return f"Invalid image path format: {image_path}"
                
            image_name, collection_name = parts
            debug(f"Found image link, will now check - Alt text: {alt_text}, Image: '{image_name}', Collection: '{collection_name}'")
            
            # Get the image from collections using the path            
            myimage = collections.image_get(image_name, collection_name)
            return process_image(myimage, alt_text if alt_text else None)
        except ValueError as e:
            debug(f"Image not found in collection: {image_path}.\n{e}")
            return f"Image not found: {image_path}"
        except Exception as e:
            debug(f"Error processing image {image_path}: {str(e)}")
            return f"Error processing image: {image_path}"
    
    # Process all image links while preserving surrounding text
    page.content_ = re.sub(link_pattern, replace_link, page.content)
    
    debug("Image processing complete")
    
    return page
