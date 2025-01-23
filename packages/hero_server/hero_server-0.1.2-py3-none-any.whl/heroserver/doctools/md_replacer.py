import sys
import os

# Add the parent directory of herotools to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from herotools.logger import logger
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode
import re
from enum import Enum
from herotools.texttools import name_fix
from mdformat.renderer import MDRenderer
from urllib.parse import urlparse

class ImageType(Enum):
    JPEG = 'jpeg'
    PNG = 'png'
    GIF = 'gif'
    OTHER = 'other'


def get_link_page(prefix:str, linkname:str, sitename: str, name: str) -> str:
    """
    Generates a page link based on sitename and name.
    
    Args:
        sitename (str): The name of the site.
        name (str): The name of the page.
    
    Returns:
        str: The generated link.
    """
    logger.debug(f"get_link_page: {prefix[:60]:<60} {linkname} {sitename}:{name}")
    return f"[{linkname}]({prefix}/{sitename}/{name})"

def get_link_image(prefix:str, sitename: str, name: str, image_type: ImageType) -> str:
    """
    Generates an image link based on the URL and image type.
    
    Args:
        url (str): The original URL of the image.
        image_type (ImageType): The type of the image.
    
    Returns:
        str: The generated link.
    """
    logger.debug(f"get_link_image: {prefix[:60]:<60} {sitename}:{name}")
    return f"![]({prefix}/{sitename}/{name})"

def get_include(sitename: str, name: str) -> str:
    """
    Generates an include directive link based on sitename and name.
    
    Args:
        sitename (str): The name of the site.
        name (str): The name of the page to include.
    
    Returns:
        str: The generated include directive.
    """
    logger.debug(f"get_include: {sitename}:{name}")
    return f"include: {sitename}/{name}"

def replace(prefix:str, markdown: str) -> str:
    """
    Finds all image links, markdown page links, and custom include directives in the provided markdown text
    and replaces them using the appropriate functions.
    
    Args:
        markdown (str): The markdown content.
    
    Returns:
        str: The modified markdown content with updated links.
    """
    # Initialize the Markdown parser
    md = MarkdownIt()
    tokens = md.parse(markdown)
    ast = SyntaxTreeNode(tokens)

    print(ast.pretty(indent=2, show_text=True))

    def process_node(node: SyntaxTreeNode):
        # from IPython import embed; embed()

        def get_new_url(url: str):
            logger.debug(f"url: {url}")

            parsed_url = urlparse(url)
            # site_name = parsed_url.netloc
            image_path = parsed_url.path
            logger.debug(f"parsed_url: {parsed_url}")  

            # prefix = prefix.rstrip('/')
            # image_path = image_path.strip('/')

            new_url = f"{prefix.rstrip('/')}/{image_path.strip('/')}"
            logger.debug(f"new_url: {new_url}")

            return new_url

        if node.type == 'image':
            # Process image link
            url = node.attrs.get('src', '')
            new_url = get_new_url(url)
            node.attrs['src'] = new_url

        elif node.type == 'link':
            # Process markdown page link
            url = node.attrs.get('href', '')
            new_url = get_new_url(url)
            node.attrs['href'] = new_url

        # Recursively process child nodes
        for child in node.children or []:
            process_node(child)
            
    def replace_include_directives(match: re.Match) -> str:
        """
        Replaces custom include directives with appropriate links.
        
        Args:
            match (re.Match): The match object containing the found include directive.
        
        Returns:
            str: The generated link for the include directive.
        """
        url = match.group(1)
        if ':' in url:
            site_name, page = url.split(':', 1)
            page_name = page.split('/')[-1]
        else:
            site_name = ""
            page_name = url        
        if not page.endswith('.md'):
            page += '.md'
        return get_include(prefix, site_name, page_name)
            

    # Process the root node
    process_node(ast)

    # Convert the AST back to markdown
    renderer = MDRenderer()
    options = {}
    env = {}
    rendered_markdown = renderer.render(tokens, options, env)

    # include_pattern = re.compile(r"!!include page:'(.*?)'")
    # rendered_markdown = include_pattern.sub(replace_include_directives, rendered_markdown) 

    return rendered_markdown



if __name__ == "__main__":

    text = """
![Image description](https://example.com/image.png)
[Page link](sitename:some/path/to/page.md)
!!include page:'mypage'
!!include page:'mypage.md'
!!include page:'mysite:mypage
!!include page:'mysite:mypage'
!!include page:'mysite:mypage.md'
    """

    print(text)
    text2=replace("http://localhost:8080/pre/", text)
    print(text2)
    
    