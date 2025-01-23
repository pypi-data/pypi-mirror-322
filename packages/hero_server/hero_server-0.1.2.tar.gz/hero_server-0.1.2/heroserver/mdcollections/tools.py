from pathlib import Path
from typing import Union
import os
import re

def should_skip_path(path: Union[str, Path]) -> bool:
    """
    Check if a path should be skipped based on its basename.
    Skips paths that start with . or _
    
    Args:
        path: Path to check (can be file or directory)
        
    Returns:
        True if path should be skipped, False otherwise
    """
    path = Path(path)
    return path.name.startswith(('.', '_'))


def strip_ansi_codes(text):
    """Remove ANSI escape codes from text."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)



def name_fix(path: str) -> str:
    """
    Normalize only the final part (stem) of a path by:
    - Converting spaces to underscores
    - Making lowercase
    Preserves the directory structure and only modifies the final name.
    
    Args:
        path: Path to normalize
        
    Returns:
        Path with normalized stem but unchanged structure
    """
    if not isinstance(path, str):
        raise TypeError("Input must be a string")
    
    if '/' in path:
        raise ValueError("Path should not contain forward slashes - use for filenames only")
    
    path = strip_ansi_codes(path).strip()
    name, ext = os.path.splitext(path)
    
    if not is_image(path) and ext.lower() == '.md':
        ext = ""
    
    # Convert to lowercase and replace spaces and other characters
    name = name.lower().replace(' ', '_').replace('-', '_').replace(',', '')
    name = name.replace('__', '_').rstrip(' ')

    # Only strip trailing underscores for image files
    if is_image(name):
        name = name.rstrip('_')
    
    return f"{name}{ext}"


def path_fix(path: Union[str, Path]) -> Path:
    """
    Normalize only the final part (stem) of a path by:
    - Converting spaces to underscores
    - Making lowercase
    Preserves the directory structure and only modifies the final name.
    
    Args:
        path: Path to normalize
        
    Returns:
        Path with normalized stem but unchanged structure
    """
    if not isinstance(path, (str, Path)):
        path = str(path)
    path = Path(path)
    # Keep directory structure unchanged, only normalize the filename
    parent = path.parent
    filename = name_fix(path.name)
    # Recombine with original parent path
    return parent / filename


def is_image(basename):
    # Define a set of valid image extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    
    # Get the file extension from the basename
    _, extension = os.path.splitext(basename)
    extension = extension.strip()
    
    #print(f" ----- {basename} '{extension.lower()}' {extension.lower() in image_extensions}")
    
    # Check if the extension is in the set of image extensions
    return extension.lower() in image_extensions

