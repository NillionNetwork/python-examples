import hashlib

CONFIG = {
    "nr_candidates": 2,
    "nr_voters": 3,
}

CONFIG_CANDIDATES = ["Dave", "Emma"]


# Alice
CONFIG_PARTY_1 = {
    "private_key": hashlib.sha256(b"alice_seed").digest(),
    "party_name": "Alice",
    "party_role": "Voter0",
    "secret_votes": {
        "v0_c0": 1,
        "v0_c1": 2,
    },
}

# Bob and Charlie
CONFIG_N_PARTIES = [
    {
        "private_key": hashlib.sha256(b"bob_seed").digest(),
        "party_name": "Bob",
        "party_role": "Voter1",
        "secret_votes": {
            "v1_c0": 1,
            "v1_c1": 2,
        },
    },
    {
        "private_key": hashlib.sha256(b"charlie_seed").digest(),
        "party_name": "Charlie",
        "party_role": "Voter2",
        "secret_votes": {
            "v2_c0": 2,
            "v2_c1": 1,
        },
    },
]
