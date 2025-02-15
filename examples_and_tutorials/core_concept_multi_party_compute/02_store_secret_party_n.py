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

from config import CONFIG_N_PARTIES

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


# N other parties store a secret
async def main(args=None):
    parser = argparse.ArgumentParser(
        description="Create a secret on the Nillion network with set read/retrieve permissions"
    )
    parser.add_argument(
        "--user_id_1",
        required=True,
        type=str,
        help="User ID of the user who will compute with the secret being stored",
    )
    parser.add_argument(
        "--program_id",
        required=True,
        type=str,
        help="The id of the program that will run on the uploaded secrets",
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
    uploader_user_id = UserId.parse(args.user_id_1)

    # start a list of values ids to keep track of stored secrets
    values_ids = []
    user_ids = []

    for party_info in CONFIG_N_PARTIES:
        signing_key = PrivateKey(party_info["private_key"])
        client = await VmClient.create(signing_key, network, payer)
        party_name = party_info["party_name"]
        secret_name = party_info["secret_name"]
        secret_value = party_info["secret_value"]

        # Create a secret for the current party
        values = {secret_name: SecretInteger(secret_value)}

        # Create permissions object
        permissions = Permissions.defaults_for_user(client.user_id).allow_compute(
            uploader_user_id, args.program_id
        )

        # Store the permissioned secret
        values_id = await client.store_values(
            values=values, ttl_days=5, permissions=permissions
        ).invoke()

        values_ids.append(values_id)
        user_ids.append(client.user_id)

        print(
            f"\n🎉N Party {party_name} stored {secret_name}: {secret_value} at store id: {values_id} using user id {client.user_id}"
        )
        print(
            f"\n🎉Compute permission on the secret granted to user_id: {args.user_id_1}\n--------------------------------"
        )

    user_ids_to_values_ids = " ".join(
        [f"{party_id}:{store_id}" for party_id, store_id in zip(user_ids, values_ids)]
    )

    print(
        "\n📋⬇️ Copy and run the following command to run multi party computation using the secrets"
    )
    print(
        f"\npython3 03_multi_party_compute.py --user_ids_to_values_ids {user_ids_to_values_ids} --program_id {args.program_id}"
    )
    return [user_ids_to_values_ids, args.program_id]


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    pass
