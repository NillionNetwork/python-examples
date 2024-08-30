# Nillion Python Examples <a href="https://github.com/NillionNetwork/nillion-python-starter/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>

This repo contains examples to go along with the Nillion Python Client docs: https://docs.nillion.com/python-client

- core_concept_multi_party_compute - This is an example using the Nillion Python Client to store a program, and run multi party compute, computation involving secret inputs from multiple parties
- core_concept_permissions - This multi part example demonstrates storing and retrieving permissioned secrets and revoking permissions.
- core_concept_single_party_compute - The examples in this directory run programs that involve one party.
- core_concept_store_and_retrieve_secrets
- millionaires_problem_example - An example of Multi Party Compute with the Millionaires Problem Example
- nada_programs - Single and multi party Nada programs and tests
- voting_tutorial - An example of Multi Party Compute with voting examples

## Using this repo

### Install dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Compile programs

From the repo root:

```
cd examples_and_tutorials/nada_programs
nada build
```

### Run the nillion-devnet

```
nillion-devnet
```

This writes an Nillion config environment file to your local machine that is used in examples: `load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")`

Keep the devnet running in your terminal.

### Run examples

Open another terminal and navigate to `examples_and_tutorials`, which holds all examples. From the repo root:

```
cd examples_and_tutorials
```

Run any examples.
