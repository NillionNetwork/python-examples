##########################################################################################

#                                   VOTING  --  PART 1

##########################################################################################


import asyncio
import py_nillion_client as nillion
import os
import sys
from dotenv import load_dotenv

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

from py_nillion_client import NodeKey, UserKey

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from helpers.nillion_client_helper import (
    create_nillion_client,
    pay,
    create_payments_config,
)

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

# Alice stores the voting program in the network
async def main():
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")

    while True:

        # Below, you can choose which voting program to use. In case you choose a voting program 
        # different from the robust version ('voting_dishonest_robust_6'), you can complete  
        # either 'digest_plurality_vote_honest_result()' or 'digest_plurality_vote_dishonest_with_abort_result()' 
        # functions to digest the result.
        #
        # Existing voting nada_programs:
        #
        # program_name = "voting_honest_1"  
        # program_name = "voting_honest_2"  
        # program_name = "voting_dishonest_abort_5"      
        # program_name = "voting_dishonest_robust_6"

        print("Choose a program to test:")
        print("1. voting_honest_1")
        print("2. voting_honest_2")
        print("3. voting_dishonest_abort_5")
        print("4. voting_dishonest_robust_6")

        choice = input("Enter the number corresponding to your choice: ")

        programs = {
            "1": "voting_honest_1",
            "2": "voting_honest_2",
            "3": "voting_dishonest_abort_5",
            "4": "voting_dishonest_robust_6"
        }

        if choice in programs:
            program_name = programs[choice]
            print("You have chosen:", program_name)
            print(" _         _   _                  _                  _ _   _     ")
            print("| |    ___| |_( )___  __   _____ | |_ ___  __      _(_) |_| |__  ")
            print("| |   / _ \\ __|// __| \\ \\ / / _ \\| __/ _ \\ \\ \\ /\\ / / | __| '_ \\ ")
            print("| |__|  __/ |_  \\__ \\  \\ V / (_) | ||  __/  \\ V  V /| | |_| | | |")
            print("|_____\\___|\\__| |___/   \\_/_\\___/ \\__\\___|   \\_/\\_/ |_|\\__|_| |_|")
            print("                    _____(_) | (_) ___  _____| |                 ")
            print("                   |  _  | | | | |/ _ \\|  _  | |                 ")
            print("                   | | | | | | | | (_) | | | |_|                 ")
            print("                   |_| |_|_|_|_|_|\\___/|_| |_(_)                 ")
            print("                                                                 ")
            break  # Exit the loop if a valid choice is made
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    #####################################
    # 1. Parties initialization         #
    #####################################

    #############################
    # 1.1 Owner initialization  #
    #############################

    # Create client
    alice_seed = "alice_seed"
    client_alice = create_nillion_client(
        UserKey.from_seed(alice_seed), NodeKey.from_seed(alice_seed)
    )

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )

    #####################################
    # 2. Storing program                #
    #####################################

    # Get cost quote, then pay for operation to store program
    receipt_store_program = await pay(
        client_alice,
        nillion.Operation.store_program(),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    program_mir_path = f"../../programs-compiled/{program_name}.nada.bin"
    if os.path.exists(program_mir_path):
        None
    else:
        raise FileNotFoundError(f"The file '{program_mir_path}' does not exist.\nMake sure you compiled the PyNada programs with './compile_programs.sh'.\nCheck README.md for more details.")

    # Store program in the Network
    print(f"Storing program in the network: {program_name}")
    action_id = await client_alice.store_program(
        cluster_id, program_name, program_mir_path, receipt_store_program
    )
    print("action_id is: ", action_id)
    user_id_alice = client_alice.user_id
    program_id = f"{user_id_alice}/{program_name}"
    print("program_id is: ", program_id)

    #####################################
    # 3. Send program ID                #
    #####################################

    # This requires its own mechanism in a real environment. 
    print(f"Alice stored {program_name} program at program_id: {program_id}")
    print(f"Alice tells Bob and Charlie her user_id and the voting program_id")

    print("\n📋⬇️ Copy and run the following command to store Bob and Charlie's votes in the network")
    print(f"\npython3 02_store_secret_party_n.py --user_id_1 {user_id_alice} --program_id {program_id}")

asyncio.run(main())