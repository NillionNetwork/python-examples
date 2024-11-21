import hashlib

# replace this with your name
CONFIG_PROGRAM_NAME = "addition_simple_multi_party"

# 1st party
CONFIG_PARTY_1 = {
    "private_key": hashlib.sha256(b"party_1_seed").digest(),
    "party_name": "Party1",
    "secrets": {
        "my_int1": 1,
    },
}

# N other parties
CONFIG_N_PARTIES = [
    {
        "private_key": hashlib.sha256(b"party_2_seed").digest(),
        "party_name": "Party2",
        "secret_name": "my_int2",
        "secret_value": 5,
    },
    {
        "private_key": hashlib.sha256(b"party_3_seed").digest(),
        "party_name": "Party3",
        "secret_name": "my_int3",
        "secret_value": 2,
    },
]
