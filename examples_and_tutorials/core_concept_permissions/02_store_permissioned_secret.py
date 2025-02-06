import hashlib
import argparse
import asyncio
import os
import pytest

from nillion_client import (
    Network,
    NilChainPayer,
    NilChainPrivateKey,
    Permissions,
    SecretInteger,
    UserId,
    VmClient,
    PrivateKey,
)
from dotenv import load_dotenv


home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


async def main(args=None):
    parser = argparse.ArgumentParser(
        description="Create a secret on the Nillion network with set read/retrieve permissions"
    )
    parser.add_argument(
        "--retriever_user_id",
        required=True,
        type=str,
        help="User ID of the reader python client (derived from private key)",
    )
    args = parser.parse_args(args)

    # Use the devnet configuration generated by `nillion-devnet`
    network = Network.from_config("devnet")

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    nilchain_key: str = os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0")  # type: ignore
    payer = NilChainPayer(
        network,
        wallet_private_key=NilChainPrivateKey(bytes.fromhex(nilchain_key)),
        gas_limit=10000000,
    )

    # We will identify ourselves with the pre-configured private key
    signing_key = PrivateKey(hashlib.sha256(b"seed_2").digest())
    client = await VmClient.create(signing_key, network, payer)

    # Adding funds to the client balance so the upcoming operations can be paid for
    funds_amount = 5000000
    print(f"💰  Adding some funds to the client doing the storing balance: {funds_amount} uNil")
    await client.add_funds(funds_amount)

    # Create secret
    secret_name_1 = "my_int1"
    secret_1 = SecretInteger(10)

    secret_name_2 = "my_int2"
    secret_2 = SecretInteger(32)
    values = {secret_name_1: secret_1, secret_name_2: secret_2}

    retriever_user_id = UserId.parse(args.retriever_user_id)
    # Writer gives themself default core_concept_permissions
    permissions = Permissions.defaults_for_user(client.user_id)
    # Writer gives the reader permission to read/retrieve secret
    permissions.allow_retrieve(retriever_user_id)

    allowed_readers = permissions.retrieve
    if retriever_user_id not in allowed_readers:
        raise Exception("failed to set core_concept_permissions")

    print(
        f"ℹ️ Permissions set: Reader {retriever_user_id} is allowed to retrieve the secret"
    )

    # Writer stores the permissioned secrets, resulting in the secrets' store id
    print(f"ℹ️  Storing permissioned secrets: {values}")
    values_id = await client.store_values(
        values=values, ttl_days=5, permissions=permissions
    ).invoke()

    print("ℹ️ VALUES ID:", values_id)
    print(
        "\n\nRun the following command to retrieve the secret by store id as the reader"
    )
    print(f"\n📋 python3 03_retrieve_secret.py --values_id {values_id}")
    return values_id


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    pass
