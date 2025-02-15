import hashlib
import importlib
import argparse
import asyncio
import os
import sys
from nillion_client.client_retry import GRPCError, Status
from nillion_client.ids import UUID
import pytest

from nillion_client import (
    Network,
    NilChainPayer,
    NilChainPrivateKey,
    VmClient,
    PrivateKey,
)
from dotenv import load_dotenv


home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


async def main(args=None):
    parser = argparse.ArgumentParser(
        description="Check that retrieval permissions on a Secret have been revoked"
    )
    parser.add_argument(
        "--values_id",
        required=True,
        type=str,
        help="Values ID from the writer client store operation",
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
    signing_key = PrivateKey(hashlib.sha256(b"seed_1").digest())
    client = await VmClient.create(signing_key, network, payer)
    values_id = UUID(args.values_id)
    reader_user_id = client.user_id

    try:
        await client.retrieve_values(values_id).invoke()
        print(
            f"⛔ FAIL: {reader_user_id} user id with revoked permissions was allowed to access secret",
            file=sys.stderr,
        )
        client.close()
    except GRPCError as e:
        if e.status == Status.PERMISSION_DENIED:
            print(
                f"🦄 Success: After user permissions were revoked, {reader_user_id} was not allowed to access secret",
                file=sys.stderr,
            )
            client.close()
        else:
            raise (e)


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    fetch_reader_userid = importlib.import_module("01_fetch_reader_userid")
    store_permissioned_secret = importlib.import_module("02_store_permissioned_secret")
    retrieve_secret = importlib.import_module("03_retrieve_secret")
    revoke_read_permissions = importlib.import_module("04_revoke_read_permissions")
    result = await fetch_reader_userid.main()
    args = ["--retriever_user_id", str(result)]
    result = await store_permissioned_secret.main(args)
    args = ["--values_id", str(result)]
    result = await retrieve_secret.main(args)
    args = ["--values_id", str(result[0]), "--revoked_user_id", str(result[1])]
    result = await revoke_read_permissions.main(args)
    args = ["--values_id", str(result)]
    await main(args)
