import asyncio
import py_nillion_client as nillion
import os
import pytest

from py_nillion_client import NodeKey, UserKey
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

# Store and retrieve a SecretInteger using the Python Client
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    seed = "my_seed"
    userkey = UserKey.from_seed((seed))
    nodekey = NodeKey.from_seed((seed))
    client = create_nillion_client(userkey, nodekey)

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    ##### STORE SECRET
    print("-----STORE SECRET")

    # Create a SecretInteger
    secret_name = "my_int1"
    secret_value = 100
    stored_secret = nillion.NadaValues(
        {
            secret_name: nillion.SecretInteger(secret_value),
        }
    )

    # Create a permissions object to attach to the stored secret
    permissions = nillion.Permissions.default_for_user(client.user_id)

    # Get cost quote, then pay for operation to store the secret
    receipt_store = await get_quote_and_pay(
        client,
        nillion.Operation.store_values(stored_secret, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # Store a secret, passing in the receipt that shows proof of payment
    store_id = await client.store_values(
        cluster_id, stored_secret, permissions, receipt_store
    )

    print(f"The secret is stored at store_id: {store_id}")

    ##### RETRIEVE SECRET
    print("-----RETRIEVE SECRET")

    # Get cost quote, then pay for operation to retrieve the secret
    receipt_retrieve = await get_quote_and_pay(
        client,
        nillion.Operation.retrieve_value(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    result_tuple = await client.retrieve_value(
        cluster_id, store_id, secret_name, receipt_retrieve
    )
    print(f"The secret name as a uuid is {result_tuple[0]}")
    print(f"The secret value is {result_tuple[1].value}")
    return result_tuple[1].value


if __name__ == "__main__":
    asyncio.run(main())


@pytest.mark.asyncio
async def test_main():
    result = await main()
    assert result == "gm, builder!"
