from herotools.logger import logger
from bs4 import BeautifulSoup
import re
from typing import Callable
from herotools.texttools import name_fix

# Define the type for the content and link fetching functions
LinkFetcher = Callable[[str, str, str, str, str], str]
ContentFetcher = Callable[[str, str, str, str], str]

# Private functions to be used internally

def _get_link(language: str, prefix: str, site_name: str, pagename: str, name: str) -> str:
    # Replace this with your logic to get the actual link
    logger.debug(f"_get_link: {language[:10]:<10} {site_name}:{pagename}:{name}")
    return f"{prefix}{language}/{site_name}/{pagename}/{name}.jpg"

def _get_content(language: str, site_name: str, pagename: str, name: str) -> str:
    # Replace this with your logic to get the actual content
    logger.debug(f"_get_content: {language[:10]:<10} {site_name}:{pagename}:{name}")
    return f"Replaced text for {name} on page {pagename} in {language} language on {site_name} site"

def _process_html(language: str, prefix: str, site_name: str, pagename: str, html_content: str) -> str:
    """
    Function to process HTML and replace content based on tags.
    This allows us to work with templates and get content based on language to replace in HTML.
    """
    language = name_fix(language)
    site_name = name_fix(site_name)
    pagename = name_fix(pagename)
    prefix = prefix.strip()
    if not prefix.endswith('/'):
        prefix += '/'

    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class names starting with !!img: or !!txt:
    for element in soup.find_all(class_=re.compile(r'!!(img|txt):(.+)')):
        for cls in element['class']:
            if cls.startswith('!!img:'):
                name = cls.split(':')[1]
                name = name_fix(name)
                # Get the link to replace the src attribute in !!img: elements
                link = _get_link(language=language, prefix=prefix, site_name=site_name, pagename=pagename, name=name)
                if element.name == 'img':
                    element['src'] = link
                elif 'src' in element.attrs:
                    element['src'] = link  # In case the element is not an img but has a src attribute
            elif cls.startswith('!!txt:'):
                name = cls.split(':')[1]
                name = name_fix(name)
                # Get the content to replace the text in !!txt: elements
                content = _get_content(language=language, site_name=site_name, pagename=pagename, name=name)
                element.string = content

    # Output the modified HTML
    return str(soup)

# Public function to process the HTML content
def process(language: str, prefix: str, site_name: str, pagename: str, html_content: str) -> str:
    """
    Public function to process HTML and replace content based on tags.
    This function wraps the internal _process_html function.
    """
    return _process_html(language=language, prefix=prefix, site_name=site_name, pagename=pagename, html_content=html_content)

# Sample usage with a given language, site name, page name, and HTML content
if __name__ == "__main__":
    # Example HTML content
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sample Page</title>
    </head>
    <body>
        <h2 class="mb-6 is-size-1 is-size-3-mobile has-text-weight-bold !!txt:title1">Take care of your performance every day.</h2>
        <img class="responsive !!img:logo" src="old-link.jpg" alt="Company Logo">
        <p class="content !!txt:description">This is a sample description text.</p>
    </body>
    </html>
    '''

    # Process the HTML content for a specific language, site name, and page
    language: str = "en"
    site_name: str = "ExampleSite"
    pagename: str = "HomePage"
    prefix: str = "http://localhost/images/"
    processed_html: str = process(language=language, prefix=prefix, site_name=site_name, pagename=pagename, html_content=html_content)

    # Print the modified HTML
    print(processed_html)
