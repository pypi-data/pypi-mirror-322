from bs4 import BeautifulSoup
import re
import unicodedata
from typing import Callable
from herotools.texttools import name_fix

# Define the type for the content and link fetching functions
LinkFetcher = Callable[[str, str, str, str], str]
ContentFetcher = Callable[[str, str, str, str], str]


# Sample get_link and get_content functions with language, site_name, page, and name
def get_link(language: str, site_name: str, pagename: str, name: str) -> str:
    language = name_fix(language)
    site_name = name_fix(site_name)
    pagename = name_fix(pagename)
    name = name_fix(name)
    # Replace this with your logic to get the actual link
    return f"https://example.com/{language}/{site_name}/{pagename}/{name}.jpg"

def get_content(language: str, site_name: str, pagename: str, name: str) -> str:
    language = name_fix(language)
    site_name = name_fix(site_name)
    pagename = name_fix(pagename)
    name = name_fix(name)
    # Replace this with your logic to get the actual content
    return f"Replaced text for {name} on page {pagename} in {language} language on {site_name} site"

# Function to process HTML and replace content
def process_html(language: str, site_name: str, pagename: str, html_content: str) -> str:
    language = name_fix(language)
    site_name = name_fix(site_name)
    pagename = name_fix(pagename)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements with class names starting with !!img: or !!txt:
    for element in soup.find_all(class_=re.compile(r'!!(img|txt):(.+)')):
        for cls in element['class']:
            if cls.startswith('!!img:'):
                name = cls.split(':')[1]
                name = name_fix(name)
                # Get the link to replace the src attribute in !!img: elements
                link = get_link(language, site_name, pagename, name)
                if element.name == 'img':
                    element['src'] = link
                elif 'src' in element.attrs:
                    element['src'] = link  # In case the element is not an img but has a src attribute
            elif cls.startswith('!!txt:'):
                name = cls.split(':')[1]
                name = name_fix(name)
                # Get the content to replace the text in !!txt: elements
                content = get_content(language, site_name, pagename, name)
                element.string = content

    # Output the modified HTML
    return str(soup)

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
    language = "en"
    site_name = "ExampleSite"
    pagename = "HomePage"
    processed_html = process_html(language, site_name, pagename, html_content)

    # Print the modified HTML
    print(processed_html)
