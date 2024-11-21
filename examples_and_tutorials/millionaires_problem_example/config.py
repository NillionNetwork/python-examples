import hashlib

# Alice
CONFIG_PARTY_1 = {
    "private_key": hashlib.sha256(b"alice_seed").digest(),
    "party_name": "Alice",
    "secret_name": "alice_salary",
    "secret_value": 10000,
}

# Bob and Charlie
CONFIG_N_PARTIES = [
    {
        "private_key": hashlib.sha256(b"bob_seed").digest(),
        "party_name": "Bob",
        "secret_name": "bob_salary",
        "secret_value": 8000,
    },
    {
        "private_key": hashlib.sha256(b"charlie_seed").digest(),
        "party_name": "Charlie",
        "secret_name": "charlie_salary",
        "secret_value": 12000,
    },
]
