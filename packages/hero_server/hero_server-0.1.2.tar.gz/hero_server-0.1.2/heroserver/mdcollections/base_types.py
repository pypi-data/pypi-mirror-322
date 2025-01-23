from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from .tools import name_fix

import os

class MDItem:
    """Base class for items in a collection."""
    def __init__(self, collection: "MDCollection", rel_path: Path):
        if not isinstance(rel_path, Path):
            raise TypeError("rel_path must be a Path instance")
        self.collection = collection
        self.rel_path = rel_path
        self.content_ = ""
        self.processed = bool

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.rel_path}"

    @property
    def full_path(self) -> Path:
        """Returns the full path to the item."""
        return self.collection.path / self.rel_path

    @property
    def path(self) -> str:
        """Returns the fixed name of the item without extension."""
        return str(self.full_path.resolve())

    @property
    def name(self) -> str:
        """Returns the fixed name of the item."""
        return name_fix(os.path.basename(self.rel_path))

class MDPage(MDItem):
    """Represents a markdown file in the collection."""
    pass

    @property
    def content(self) -> str:
        if not self.content_:
            if os.path.exists(self.path):
                try:
                    with open(self.path, 'r', encoding='utf-8') as f:
                        self.content_ = f.read()
                except OSError as e:
                    raise Exception(f"Error reading file {self.path}: {e}")
            else:
                raise FileNotFoundError(f"Cannot find markdown file: {self.path}")
        return self.content_
    
        

class MDImage(MDItem):
    """Represents an image file in the collection."""
    pass



@dataclass
class MDCollection:
    """Represents a collection of markdown files and images."""
    path: Path
    name: str
    items: List[MDItem]

    def page_get(self, name: str) -> MDPage:
        """
        Get a markdown page by name.
        
        Args:
            name: Name of the page to find (will be normalized)
            
        Returns:
            MDPage object
            
        Raises:
            ValueError: If page not found
        """
        # Remove .md extension if present
        if "__" in name:
            raise ValueError("there should be no __ in name of page_get")
        
        if name.endswith('.md'):
            name=name[:-3]
        normalized_name = name_fix(name)
        for item in self.items:
            if isinstance(item, MDPage):
                item_name = name_fix(item.rel_path.stem)
                if item_name == normalized_name:
                    return item
        raise ValueError(f"Page not found: {name}")

    def image_get(self, name: str) -> MDImage:
        """
        Get an image by name.
        
        Args:
            name: Name of the image to find (will be normalized)
            
        Returns:
            MDImage object
            
        Raises:
            ValueError: If image not found
        """
        normalized_name = name_fix(name)
        for item in self.items:
            if isinstance(item, MDImage):
                # For images, compare with extension
                item_name = name_fix(os.path.basename(item.rel_path))
                if item_name == normalized_name:
                    return item
        raise ValueError(f"Image not found: {name}")

    def __str__(self) -> str:
        """Returns a tree-like string representation of the collection."""
        result = [f"Collection: {self.name} ({self.path})"]
        
        # Group items by type
        pages = [item for item in self.items if isinstance(item, MDPage)]
        images = [item for item in self.items if isinstance(item, MDImage)]
        
        # Add pages
        if pages:
            result.append("  Pages:")
            for page in sorted(pages, key=lambda x: str(x.rel_path)):
                result.append(f"    └─ {page.name}")
        
        # Add images
        if images:
            result.append("  Images:")
            for image in sorted(images, key=lambda x: str(x.rel_path)):
                result.append(f"    └─ {image.name}")
        
        return "\n".join(result)

    def index_page(self) -> MDPage:
        """Generate a dynamic index of all markdown files in the collection."""
        # Get all markdown pages and sort them by relative path
        pages = sorted(
            [item for item in self.items if isinstance(item, MDPage)],
            key=lambda x: str(x.rel_path)
        )
        
        # Group pages by directory
        page_groups: Dict[str, List[MDPage]] = {}
        for page in pages:
            dir_path = str(page.rel_path.parent)
            if dir_path == '.':
                dir_path = 'Root'
            if dir_path not in page_groups:
                page_groups[dir_path] = []
            page_groups[dir_path].append(page)
        
        # Generate markdown content
        content = ["# Collection Index\n"]
        
        for dir_path in sorted(page_groups.keys()):
            # Add directory header
            if dir_path != 'Root':
                content.append(f"\n## {dir_path}\n")
            elif len(page_groups) > 1:  # Only show Root header if there are other directories
                content.append("\n## Root Directory\n")
            
            # Add pages in current directory
            for page in sorted(page_groups[dir_path], key=lambda x: x.name):
                # Create display name by removing extension and formatting
                display_name = page.rel_path.stem.replace('_', ' ').replace('-', ' ').title()
                # Create link using relative path
                link_path = str(page.rel_path)
                content.append(f'- [{display_name}]({self.name}__{link_path})')
        
        mdp=MDPage(self,Path("index.md"))
        mdp.content_ = "\n".join(content)
        return mdp
