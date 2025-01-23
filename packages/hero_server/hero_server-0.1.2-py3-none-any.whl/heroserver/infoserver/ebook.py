import os
import re

from infoserver.texttools import name_fix


class Page:
    def __init__(
        self,
        indentation: int,
        title: str,
        collection: str,
        pagename: str,
        isbold: bool,
        isitalic: bool,
    ):
        self.indentation = indentation
        self.title = title
        self.collection = collection
        self.pagename = pagename
        self.isbold = isbold
        self.isitalic = isitalic

    def __repr__(self) -> str:
        return f"Page(indentation={self.indentation}, title='{self.title}', collection='{self.collection}', pagename='{self.pagename}', isbold={self.isbold}, isitalic={self.isitalic})"


class EBook:
    def __init__(self):
        self.pages = []
        self.path: str = ''

    def parse(self, summary: str) -> None:
        lines = summary.strip().split('\n')

        for line in lines:
            indentation = (len(line) - len(line.lstrip())) // 2

            # Extract title
            title_match = re.search(r'\[([^\]]+)\]', line)
            if title_match:
                title = title_match.group(1)
            else:
                continue  # Skip lines without a title

            # Clean title from markdown markup
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)  # Remove bold
            title = re.sub(r'_(.*?)_', r'\1', title)  # Remove italic

            # Extract collection and pagename
            path_match = re.search(r'\((.*?)\)', line)
            if path_match:
                path = path_match.group(1)
                collection, pagename = (
                    path.split('/', 1) if '/' in path else (path, '')
                )
            else:
                collection, pagename = '', ''

            # Check if bold or italic
            isbold = '**' in line
            isitalic = '*' in line and not isbold

            page = Page(
                int(indentation / 2),
                title,
                name_fix(collection),
                name_fix(pagename),
                isbold,
                isitalic,
            )
            self.pages.append(page)

    def page_get(self, collection: str, name: str) -> str:
        name = name_fix(name)
        collection = name_fix(collection)
        file_path = os.path.join(self.path, collection, name)

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content

        raise ValueError(
            f"Page with name '{name}' not found in collection '{collection}'"
        )

    def image_get(self, collection: str, name: str) -> str:
        name = name_fix(name)
        collection = name_fix(collection)
        file_path = os.path.join(self.path, collection, name)

        if os.path.isfile(file_path):
            return f'/static/collections/{collection}/{name}'

        raise ValueError(
            f"Image with name '{name}' not found in collection '{collection}'"
        )

    def __str__(self) -> str:
        result = []
        for page in self.pages:
            indent = '  ' * (page.indentation * 2)
            title = page.title
            if page.isbold:
                title = f'**{title}**'
            elif page.isitalic:
                title = f'*{title}*'
            result.append(
                f'{indent}- [{title}]({page.collection}/{page.pagename})'
            )
        return '\n'.join(result)


if __name__ == '__main__':
    summary = """
- [Introduction](projectinca/intro.md)
- [Tokenomics](projectinca/tokens.md)
    - [Liquidity Pool](projectinca/liquidity_pool.md)
    - [Liquidity](projectinca/liquidity.md)
- [Decentralization](projectinca/decentralization.md)
    - [Decentralization 3.x](projectinca/decentralization3.md)
    - [Decentralization 4.x](projectinca/decentralization4.md)
    - [TF Validators 4.x](projectinca/TFValidatorCluster.md)
    - [All Trust](tfgrid4/alltrust.md)
- [Blockchain](projectinca/blockchain.md)
        - [Blockchain 2](projectinca/ourworld_blockchain.md)
    - [Generator Tokens](projectinca/generator_token.md)
    - [Minting Contract](projectinca/minting_contract.md)
    - [Oracle Contract](projectinca/oracle_contract.md)
    - [Code Contract](projectinca/code_contract.md)
    - [Bridging Contract](projectinca/bridging_contract.md)
    - [Liquidity Pool](projectinca/liquidity_pool_contract.md)
- [**Technology**](projectinca/technology.md)
"""

    summary_parser = EBook()
    summary_parser.parse(summary)

    # Print the parsed pages
    for page in summary_parser.pages:
        print(page)

    print(summary_parser)
