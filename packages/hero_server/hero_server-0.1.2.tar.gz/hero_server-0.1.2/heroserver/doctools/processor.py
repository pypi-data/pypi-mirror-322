import os
import re
from typing import Callable

from herotools.logger import logger
from herotools.md5 import file_md5
from herotools.texttools import name_fix


def _example_set_file(site_name: str, path: str, md5: str) -> None:
    # Placeholder for actual implementation
    logger.debug(f"set_file     : site_name={site_name[:20]:<20} {path}")


def _example_set_img(site_name: str, path: str, md5: str) -> None:
    # Placeholder for actual implementation
    logger.debug(f"set_img      : site_name={site_name[:20]:<20} {path}")


def _example_set_markdown(
    site_name: str, path: str, md5: str, content: str
) -> None:
    # Placeholder for actual implementation
    logger.debug(f"set_markdown : site_name={site_name[:20]:<20} {path}")


def _example_set_site(site_name: str, path: str) -> None:
    # Placeholder for actual implementation
    logger.info(f"set_site : site_name={site_name[:20]:<20} {path}")


def _site_process_action(
    site_name: str,
    site_path: str,
    set_file: Callable[[str, str, str], None],
    set_img: Callable[[str, str, str], None],
    set_markdown: Callable[[str, str, str, str], None],
) -> None:
    logger.debug(f"site process: {site_path[:60]:<60} -> {site_name}")
    for root, _, files in os.walk(site_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_path_rel = os.path.relpath(file_path, site_path)
            file_name = os.path.basename(file)
            # print(file_name)
            mymd5 = file_md5(file_path)
            if file.lower().endswith(".md"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                set_markdown(site_name, file_path_rel, mymd5, content)
            elif file_name in [".collection", ".site", ".done"]:
                continue
            elif re.search(
                r"\.(jpg|jpeg|png|gif|bmp|tiff|webp)$", file, re.IGNORECASE
            ):
                set_img(site_name, file_path_rel, mymd5)
            else:
                set_file(site_name, file_path_rel, mymd5)


def process(
    path: str,
    set_site: Callable[[str, str], None],
    set_file: Callable[[str, str, str], None],
    set_img: Callable[[str, str, str], None],
    set_markdown: Callable[[str, str, str, str], None],
) -> None:
    """
    walk over directory and apply set_file(), set_img() and set_markdown()
    """
    path = os.path.abspath(os.path.expanduser(path))
    logger.info(f"sites process: {path}")
    for root, dirs, files in os.walk(path):
        if ".site" in files or ".collection" in files:
            site_name = name_fix(os.path.basename(root))
            set_site(site_name, root)
            _site_process_action(
                site_name, root, set_file, set_img, set_markdown
            )
            # Prevent the os.walk from going deeper into subdirectories
            dirs[:] = []


if __name__ == "__main__":
    mypath = "~/code/git.ourworld.tf/projectmycelium/info_projectmycelium/collections"

    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    process(
        mypath,
        _example_set_site,
        _example_set_file,
        _example_set_img,
        _example_set_markdown,
    )
