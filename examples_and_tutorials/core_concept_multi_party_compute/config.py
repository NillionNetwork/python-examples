# replace this with your name
CONFIG_PROGRAM_NAME = "addition_simple_multi_party"

# 1st party
CONFIG_PARTY_1 = {
    "seed": "party_1_seed",
    "party_name": "Party1",
    "secrets": {
        "my_int1": 1,
    },
}

# N other parties
CONFIG_N_PARTIES = [
    {
        "seed": "party_2_seed",
        "party_name": "Party2",
        "secret_name": "my_int2",
        "secret_value": 5,
    },
    {
        "seed": "party_3_seed",
        "party_name": "Party3",
        "secret_name": "my_int3",
        "secret_value": 2,
    },
]
