import asyncio
import os
import pytest

from nillion_client import (
    Network,
    NilChainPayer,
    NilChainPrivateKey,
    Permissions,
    SecretBlob,
    VmClient,
    PrivateKey,
)
from dotenv import load_dotenv


home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


# Store and retrieve a SecretBlob using the Python Client
async def main():
    # Use the devnet configuration generated by `nillion-devnet`
    network = Network.from_config("devnet")

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    nilchain_key: str = os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0")  # type: ignore
    payer = NilChainPayer(
        network,
        wallet_private_key=NilChainPrivateKey(bytes.fromhex(nilchain_key)),
        gas_limit=10000000,
    )
    signing_key = PrivateKey()
    client = await VmClient.create(signing_key, network, payer)

    # Adding funds to the client balance so the upcoming operations can be paid for
    funds_amount = 1000
    print(f"💰  Adding some funds to the client balance: {funds_amount} uNIL")
    await client.add_funds(funds_amount)

    ##### STORE SECRET
    print("-----STORE SECRET")

    # Create a SecretBlob
    secret_name = "my_blob"

    # create a bytearray from the string using UTF-8 encoding
    secret_value = bytearray("gm, builder!", "utf-8")

    # Create a secret
    values = {
        secret_name: SecretBlob(secret_value),
    }

    # Create a permissions object to attach to the stored secret
    permissions = Permissions.defaults_for_user(client.user_id)

    # Store the secret
    values_id = await client.store_values(
        values, ttl_days=5, permissions=permissions
    ).invoke()

    print(f"The secret is stored at: {values_id}")

    ##### RETRIEVE SECRET
    print("-----RETRIEVE SECRET")

    retrieved_values = await client.retrieve_values(values_id).invoke()
    value: SecretBlob = retrieved_values[secret_name]  # type: ignore

    decoded_secret_value = value.value.decode("utf-8")
    print(f"The secret value is '{decoded_secret_value}'")
    balance = await client.balance()
    print(f"💰  Final client balance: {balance.balance} uNIL")
    client.close()
    return decoded_secret_value


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == "gm, builder!"
