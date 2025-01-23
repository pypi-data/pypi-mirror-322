import hashlib
import os
import shutil
from urllib.parse import urlparse

import redis
import requests
from bs4 import BeautifulSoup

# from typing import Dict
from colorama import Fore

# from herotools.extensions import check_and_add_extension
from web.deduper import Deduper

image_movie_extensions = (
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.webp',
    '.mp3',
    '.mp4',
    '.avi',
    '.mov',
    '.wmv',
    '.flv',
    '.webm',
)


# import pudb; pudb.set_trace()


class HTMLTemplateConverter:
    def __init__(
        self,
        src_dir: str,
        dest_dir: str,
        static_dir: str = '',
        reset: bool = False,
    ):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

        if reset and os.path.exists(self.dest_dir):
            print(' - reset')
            shutil.rmtree(self.dest_dir)

        if static_dir == '':
            static_dir = f'{dest_dir}/static'

        self.static_dir = static_dir

        os.makedirs(self.dest_dir, exist_ok=True)
        os.makedirs(self.static_dir, exist_ok=True)

        # Create a relative symlink called 'static' in dest_dir pointing to self.static_dir
        static_link_path = os.path.join(self.dest_dir, 'static')
        if not os.path.exists(static_link_path):
            os.symlink(self.static_dir, static_link_path)

        self.deduper_static = Deduper(static_dir)

        if reset:
            self.deduper_static.load_assets()

        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.cache_expiration = 3600  # 1 hour

    def download_file(self, myurl: str, remove: bool = False) -> str:
        # Check if the file is already in Redis cache
        key = f'web.download.{myurl}'
        cached_path = self.redis_client.get(key)
        if cached_path:
            print(f' - download cached {myurl}')
            temp_path = cached_path.decode('utf-8')
        else:
            print(f' - download {myurl}')
            response = requests.get(myurl)
            if response.status_code == 200:
                if '?' in myurl:
                    local_filename = hashlib.md5(
                        myurl.encode('utf-8')
                    ).hexdigest()
                else:
                    url_path = urlparse(myurl).path
                    base_name, extension = os.path.splitext(
                        os.path.basename(url_path)
                    )
                    local_filename = base_name + extension

                # Download to temporary directory
                temp_dir = os.path.join('/tmp/files')
                os.makedirs(temp_dir, exist_ok=True)
                temp_path = os.path.join(temp_dir, local_filename)

                with open(temp_path, 'wb') as f:
                    f.write(response.content)

                # Update Redis cache
                self.redis_client.setex(key, self.cache_expiration, temp_path)
            else:
                raise Exception(f'ERROR: failed to download {myurl}')
        if remove:
            os.remove(temp_path)
            self.redis_client.delete(key)
        return temp_path

    def add_to_static(self, file_path: str, dest_dir_rel: str = '') -> str:
        """
        add path to the static directory
        returns the path as need to be used in the template for the file link
        """
        # Check if the file path exists
        if not os.path.exists(file_path):
            file_path2 = f'{self.src_dir}/{file_path}'
            if not os.path.exists(file_path2):
                print(
                    f"{Fore.RED}ERROR: File '{file_path}' or '{file_path2}' does not exist.{Fore.RESET}"
                )
                # raise FileNotFoundError(f"File '{file_path}' and {file_path2} does not exist.")
                return f'error/{file_path2}'
            else:
                file_path = file_path2

        # Calculate hash for the file to be added
        file_dedupe_location = self.deduper_static.path_check(file_path)
        if file_dedupe_location:
            return file_dedupe_location
        return self.deduper_static.add(
            source_path=file_path, dest_dir_rel=dest_dir_rel
        )

    def add_file(
        self,
        src_file_path: str,
        file_path: str,
        remove: bool = False,
        dest_dir_rel: str = '',
    ) -> str:
        print(
            f' - addfile {file_path} for dest_dir_rel:{dest_dir_rel}\n    from out of file: {src_file_path}'
        )

        if 'fonts.googleapis.com' in file_path:
            return file_path

        if file_path.startswith('http://') or file_path.startswith('https://'):
            try:
                temp_path = self.download_file(file_path)
            except Exception:
                print(
                    f"{Fore.RED}ERROR DOWNLOAD: File '{file_path}'.{Fore.RESET}"
                )
                return f'/error/download/{file_path}'

            # import pudb; pudb.set_trace()
            # from IPython import embed;embed()
            # s

            src_file_path = ''
            r = self.add_file(
                src_file_path, temp_path, remove=True, dest_dir_rel=dest_dir_rel
            )
            return f'{r}'

        else:
            if not os.path.exists(file_path):
                # now we need to go relative in relation to the src_file_path
                file_path2 = os.path.abspath(
                    os.path.join(os.path.dirname(src_file_path), file_path)
                )
                if os.path.exists(file_path2):
                    file_path = file_path2
                else:
                    print(
                        f"{Fore.RED}ERROR: File '{file_path}' or `{file_path2}` does not exist.{Fore.RESET}"
                    )
                    return f'/error/{file_path}'
                    # raise FileNotFoundError(f"File '{file_path}' or `{file_path2}` does not exist.")

            # Check if file exists inself.deduper
            existing_path = self.deduper_static.path_check(file_path)
            if existing_path:
                return f'/static/{existing_path}'

            return self.add_to_static(file_path, dest_dir_rel=dest_dir_rel)

    def convert(self) -> None:
        os.makedirs(self.dest_dir, exist_ok=True)

        for root, _, files in os.walk(self.src_dir):
            for file in files:
                if file.endswith('.html'):
                    src_file_path = os.path.abspath(os.path.join(root, file))
                    rel_path = os.path.relpath(src_file_path, self.src_dir)

                    dest_file_path = os.path.join(self.dest_dir, rel_path)
                    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                    with open(
                        src_file_path, 'r', encoding='utf-8'
                    ) as html_file:
                        html_content = html_file.read()

                    soup = BeautifulSoup(html_content, 'html.parser')

                    svg_elements = soup.find_all('svg')

                    for i, svg in enumerate(svg_elements, start=1):
                        svg_file_path = '/tmp/my.svg'
                        with open(
                            svg_file_path, 'w', encoding='utf-8'
                        ) as svg_file:
                            svg_file.write(str(svg))

                        svg_path = self.add_file(
                            src_file_path,
                            file_path=svg_file_path,
                            dest_dir_rel='svg',
                        )

                        svg_file_path_in_out = os.path.join(
                            'static', 'svg', os.path.basename(svg_path)
                        )

                        svg.replace_with(
                            f"{{% include '{svg_file_path_in_out}' %}}"
                        )

                        os.remove(svg_file_path)

                    for link in soup.find_all('link', href=True):
                        href = link['href']
                        base_href = href.split('?')[0] if '?' in href else href
                        if base_href.endswith('.css'):
                            new_href = self.add_file(
                                src_file_path, base_href, dest_dir_rel='css'
                            )
                            link['href'] = new_href
                        else:
                            # Check if base_href is an image or movie file
                            if base_href.lower().endswith(
                                image_movie_extensions
                            ):
                                new_src = self.add_file(
                                    src_file_path, base_href, dest_dir_rel='img'
                                )
                                # Assuming the original attribute was 'src' for images/movies
                            else:
                                # Handle other types of files or links here if needed
                                if href.startswith(
                                    'http://'
                                ) or href.startswith('https://'):
                                    new_src = self.add_file(src_file_path, href)
                                else:
                                    new_src = self.add_file(
                                        src_file_path, base_href
                                    )
                                # from IPython import embed;embed()
                                # s
                            if link.has_key('src'):
                                link['src'] = new_src
                            elif link.has_key('href'):
                                link['href'] = new_src
                            # if "pro-tailwind.min" in href:
                            #     from IPython import embed;embed()
                            #     w

                    for script in soup.find_all('script', src=True):
                        src = script['src']
                        src_href = src.split('?')[0] if '?' in src else src
                        if src_href.endswith('.js'):
                            new_src = self.add_file(
                                src_file_path, src_href, dest_dir_rel='js'
                            )
                            script['src'] = new_src

                    for img in soup.find_all('img', src=True):
                        src = img['src']
                        new_src = self.add_file(
                            src_file_path, src, dest_dir_rel='img'
                        )
                        img['src'] = new_src

                    jinja_template = str(soup.prettify())

                    with open(
                        dest_file_path, 'w', encoding='utf-8'
                    ) as dest_file:
                        dest_file.write(jinja_template)


# Example usage
#
# converter = HTMLTemplateConverter("source_directory", "destination_directory")
# converter.convert_html_to_jinja()


def new(
    src_dir: str, dest_dir: str, static_dir: str = '', reset: bool = False
) -> HTMLTemplateConverter:
    f = HTMLTemplateConverter(
        src_dir, dest_dir, static_dir=static_dir, reset=reset
    )
    f.convert()
    return f
