from pathlib import Path
from typing import List, Sequence
from .base_types import MDItem, MDPage, MDImage, MDCollection

def scan_directory(path: Path) -> Sequence[MDItem]:
    """
    Scan a directory for markdown files and images.
    
    Args:
        path: Directory to scan
        
    Returns:
        List of MDItem objects (MDPage or MDImage)
    """
    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    
    items: List[MDItem] = []
    
    # Create a temporary collection for the items
    temp_collection = MDCollection(
        path=path,
        name=path.name,
        items=[]  # Will be populated later
    )
    
    # First scan for markdown files
    for md_path in path.rglob("*.md"):
        # Skip files in hidden directories (starting with .)
        if any(part.startswith('.') for part in md_path.parts):
            continue
        
        # Get path relative to collection root
        rel_path = md_path.relative_to(path)
        
        # Create MDPage
        page = MDPage(temp_collection, rel_path)
        items.append(page)
    
    # Then scan for images
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}
    for img_path in path.rglob("*"):
        # Skip files in hidden directories (starting with .)
        if any(part.startswith('.') for part in img_path.parts):
            continue
        
        # Check if file has image extension
        if img_path.suffix.lower() in image_extensions:
            # Get path relative to collection root
            rel_path = img_path.relative_to(path)
            
            # Create MDImage
            image = MDImage(temp_collection, rel_path)
            items.append(image)
    
    # Update the temporary collection's items
    temp_collection.items = items
    
    return items
