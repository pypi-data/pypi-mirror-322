from dataclasses import dataclass, field, asdict
from typing import List, Optional
from stellar_sdk import Keypair, Server, StrKey
import json
import redis

@dataclass
class StellarAsset:
    type: str
    balance: float
    issuer: str = ""

    def format_balance(self):
        balance_float = float(self.balance)
        formatted_balance = f"{balance_float:,.2f}"
        if '.' in formatted_balance:
            formatted_balance = formatted_balance.rstrip('0').rstrip('.')
        return formatted_balance

    def md(self):
        formatted_balance = self.format_balance()
        return f"- **{self.type}**: {formatted_balance}"

@dataclass
class StellarAccount:
    owner: str
    priv_key: str = ""
    public_key: str = ""
    assets: List[StellarAsset] = field(default_factory=list)
    name: str = ""
    description: str = ""
    comments: List[str] = field(default_factory=list)
    cat: str = ""
    question: str = ""

    def md(self):
        result = [
            f"# Stellar Account: {self.name or 'Unnamed'}","",
            f"**Public Key**: {self.public_key}",
            f"**Cat**: {self.cat}",
            f"**Description**: {self.description[:60]}..." if self.description else "**Description**: None",
            f"**Question**: {self.question}" if self.question else "**Question**: None",
            "",
            "## Assets:",""
        ]

        for asset in self.assets:
            result.append(asset.md())

        if len(self.assets) == 0:
            result.append("- No assets")

        result.append("")

        if self.comments:
            result.append("## Comments:")
            for comment in self.comments:
                if '\n' in comment:
                    multiline_comment = "\n    ".join(comment.split('\n'))
                    result.append(f"- {multiline_comment}")
                else:
                    result.append(f"- {comment}")

        return "\n".join(result)

    def balance_str(self) -> str:
        out=[]
        for asset in self.assets:
            out.append(f"{asset.type}:{float(asset.balance):,.0f}")
        return " ".join(out)
