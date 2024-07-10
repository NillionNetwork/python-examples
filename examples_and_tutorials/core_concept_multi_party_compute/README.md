# Multi Party Example

This is an example using the Nillion Python Client to store a program, and run multi party compute, computation involving secret inputs from multiple parties.

## Run the example

1. Ensure the `nillion-devnet` is running (this will write the local devnet congifs to your machine, which will be picked up by the the examples in this repo) or ensure you are reading the real network environments into the examples.

2. Ensure the multi party program you want to run (defined in `config.py`) is compiled, by running `nada build` in the `nada_programs` directory.

3. Run the scripts in number order, starting with `01_store_secret_party1.py`, check the ouputs of each script to get the inputs to the next.
