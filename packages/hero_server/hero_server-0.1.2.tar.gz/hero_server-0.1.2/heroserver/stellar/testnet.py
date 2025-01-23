from typing import Tuple
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset, Signer, TransactionEnvelope
import redis
import requests
import json
import time

def create_account_on_testnet() -> Tuple[str, str]:

    def fund(public_key: str) -> float:
        # Request funds from the Stellar testnet friendbot
        response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
        if response.status_code != 200:
            raise Exception("Failed to fund new account with friendbot")
        time.sleep(1)
        return balance(public_key)

    def create_account() -> Tuple[str, str]:
        # Initialize Redis client
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

        # Generate keypair
        keypair = Keypair.random()
        public_key = keypair.public_key
        secret_key = keypair.secret
        account_data = {
            "public_key": public_key,
            "secret_key": secret_key
        }
        redis_client.set("stellartest:testaccount", json.dumps(account_data))
        time.sleep(1)
        return public_key, secret_key

    # Check if the account already exists in Redis
    if redis_client.exists("stellartest:testaccount"):
        account_data = json.loads(redis_client.get("stellartest:testaccount"))
        public_key = account_data["public_key"]
        secret_key = account_data["secret_key"]
        r = balance(public_key)
        if r < 100:
            fund(public_key)
            r = balance(public_key)
        return public_key, secret_key
    else:
        create_account()
        return create_account_on_testnet()
