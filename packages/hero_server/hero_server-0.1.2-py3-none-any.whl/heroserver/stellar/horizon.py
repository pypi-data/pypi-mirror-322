from dataclasses import dataclass, field, asdict
from typing import List, Optional
from stellar_sdk import Keypair, Server, StrKey
import json
import redis
from stellar.model import StellarAsset, StellarAccount
import os
import csv
import toml
from herotools.texttools import description_fix



class HorizonServer:
    def __init__(self, instance: str = "default", network: str = "main", tomlfile: str = "", owner: str = ""):
        """
        Load a Stellar account's information using the Horizon server.
        The Horizon server is an API that allows interaction with the Stellar network. It provides endpoints to submit transactions, check account balances, and perform other operations on the Stellar ledger.
        All gets cached in redis
        """
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Adjust as needed
        self.instance = instance
        if network not in ['main', 'testnet']:
            raise ValueError("Invalid network value. Must be 'main' or 'testnet'.")
        self.network = network
        testnet = self.network == 'testnet'
        self.server = Server("https://horizon-testnet.stellar.org" if testnet else "https://horizon.stellar.org")
        self.tomlfile = os.path.expanduser(tomlfile)
        self.owner = owner
        if self.tomlfile:
            self.toml_load()

    def account_exists(self, pubkey: str) -> bool:
        """
        Check if an account exists in the Redis cache based on the public key.
        """
        redis_key = f"stellar:{self.instance}:accounts:{pubkey}"
        return self.redis_client.exists(redis_key) != None

    def account_get(self, key: str, reload: bool = False, name: str = "", description: str = "", cat: str = "") -> StellarAccount:
        """
        Load a Stellar account's information.

        Args:
            key (str): The private or public key of the Stellar account.
            reset (bool, optional): Whether to force a refresh of the cached data. Defaults to False.
            name (str, optional): Name for the account. Defaults to "".
            description (str, optional): Description for the account. Defaults to "".
            owner (str, optional): Owner of the account. Defaults to "".
            cat (str, optional): Category of the account. Defaults to "".

        Returns:
            StellarAccount: A struct containing the account's information.
        """

        if key == "" and name:
            for redis_key in self.redis_client.scan_iter(f"stellar:{self.instance}:accounts:*"):
                data = self.redis_client.get(redis_key)
                if data:
                    data = json.loads(str(data))
                    if data.get('name') == name and data.get('priv_key', data.get('public_key')):
                        key = data.get('priv_key', data.get('public_key'))
                        break

        if key == "":
            raise ValueError("No key provided")

        # Determine if the key is a public or private key
        if StrKey.is_valid_ed25519_public_key(key):
            public_key = key
            priv_key = ""
        elif StrKey.is_valid_ed25519_secret_seed(key):
            priv_key = key
            keypair = Keypair.from_secret(priv_key)
            public_key = keypair.public_key
        else:
            raise ValueError("Invalid Stellar key provided")

        redis_key = f"stellar:{self.instance}:accounts:{public_key}"

        data = self.redis_client.get(redis_key)
        changed = False
        if data:
            try:
                data = json.loads(str(data))
            except  Exception as e:
                print(data)
                raise e
            data['assets'] = [StellarAsset(**asset) for asset in data['assets']]
            account =  StellarAccount(**data)
            if description!="" and description!=account.description:
                account.description = description
                changed = True
            if name!="" and name!=account.name:
                account.name = name
                changed = True
            if self.owner!="" and self.owner!=account.owner:
                account.owner = self.owner
                changed = True
            if cat!="" and cat!=account.cat:
                account.cat = cat
                changed = True
        else:
            account =  StellarAccount(public_key=public_key, description=description, name=name, priv_key=priv_key, owner=self.owner, cat=cat)
            changed = True


        if reload or account.assets == []:
            changed = True
            if reload:
                account.assets = []
            account_data = self.server.accounts().account_id(public_key).call()
            account.assets.clear()  # Clear existing assets to avoid duplication
            for balance in account_data['balances']:
                asset_type = balance['asset_type']
                if asset_type == 'native':
                    account.assets.append(StellarAsset(type="XLM", balance=balance['balance']))
                else:
                    if 'asset_code' in balance:
                        account.assets.append(StellarAsset(
                            type=balance['asset_code'],
                            issuer=balance['asset_issuer'],
                            balance=balance['balance']
                        ))
            changed = True

        # Cache the result in Redis for 1 hour if there were changes
        if changed:
            self.account_save(account)

        return account

    def comment_add(self, pubkey: str, comment: str, ignore_non_exist: bool = False):
        """
        Add a comment to a Stellar account based on the public key.

        Args:
            pubkey (str): The public key of the Stellar account.
            comment (str): The comment to add to the account.
        """
        comment = description_fix(comment)
        if not self.account_exists(pubkey):
            if ignore_non_exist:
                return
            raise ValueError("Account does not exist in the cache")
        account = self.account_get(pubkey)
        account.comments.append(comment)
        self.account_save(account)

    def account_save(self, account: StellarAccount):
        """
        Save a Stellar account's information to the Redis cache.

        Args:
            account (StellarAccount): The account to save.
        """
        redis_key = f"stellar:{self.instance}:accounts:{account.public_key}"
        self.redis_client.setex(redis_key, 600, json.dumps(asdict(account)))

    def reload_cache(self):
        """
        Walk over all known accounts and reload their information.
        """
        for redis_key in self.redis_client.scan_iter(f"stellar:{self.instance}:accounts:*"):
            data = self.redis_client.get(redis_key) or ""
            if data:
                data = json.loads(str(data))
                public_key = data.get('public_key')
                if public_key:
                    self.account_get(public_key, reload=True)


    #format is PUBKEY,DESCRIPTION  in text format
    def load_accounts_csv(self, file_path:str):
        file_path=os.path.expanduser(file_path)
        if not os.path.exists(file_path):
            return Exception(f"Error: File '{file_path}' does not exist.")
        try:
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    if row and len(row) >= 2:  # Check if row is not empty and has at least 2 elements
                        pubkey = row[0].strip()
                        comment = ','.join(row[1:]).strip()
                        if self.account_exists(pubkey):
                            self.comment_add(pubkey, comment)
        except IOError as e:
            return Exception(f"Error reading file: {e}")
        except csv.Error as e:
            return Exception(f"Error parsing CSV: {e}")
        except Exception as e:
            return Exception(f"Error: {e}")

    def accounts_get(self) -> List[StellarAccount]:
        """
        Retrieve a list of all known Stellar accounts from the Redis cache.

        Returns:
            List[StellarAccount]: A list of StellarAccount objects.
        """
        accounts = []
        for redis_key in self.redis_client.scan_iter(f"stellar:{self.instance}:accounts:*"):
            pubkey = str(redis_key.split(':')[-1])
            accounts.append(self.account_get(key=pubkey))
        return accounts

    def toml_save(self):
        """
        Save the list of all known Stellar accounts to a TOML file.

        Args:
            file_path (str): The path where the list needs to be saved.
        """
        if self.tomlfile == "":
            raise ValueError("No TOML file path provided")
        accounts = self.accounts_get()
        accounts_dict = {account.public_key: asdict(account) for account in accounts}
        with open(self.tomlfile, 'w') as file:
            toml.dump( accounts_dict, file)

    def toml_load(self):
        """
        Load the list of Stellar accounts from a TOML file and save them to the Redis cache.

        Args:
            file_path (str): The path of the TOML file to load.
        """
        if not os.path.exists(self.tomlfile):
            return
            #raise FileNotFoundError(f"Error: File '{self.tomlfile}' does not exist.")
        with open(self.tomlfile, 'r') as file:
            accounts_dict = toml.load(file)
            for pubkey, account_data in accounts_dict.items():
                account_data['assets'] = [StellarAsset(**asset) for asset in account_data['assets']]
                account = StellarAccount(**account_data)
                self.account_save(account)



def new(instance: str = "default",owner: str = "", network: str = "main", tomlfile: str = "") -> HorizonServer:
    return HorizonServer(instance=instance, network=network, tomlfile=tomlfile,owner=owner)
