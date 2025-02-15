##########################################################################################

#                                   VOTING  --  PART 1

##########################################################################################


import asyncio
import os
from nillion_client.payer import DummyPayer
from dotenv import load_dotenv

from nillion_client import (
    Network,
    NilChainPayer,
    NilChainPrivateKey,
    VmClient,
    PrivateKey,
)

from config import (
    CONFIG_PARTY_1,CONFIG_N_PARTIES
)

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


# Alice stores the voting program in the network
async def main():
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
            "4": "voting_dishonest_robust_6",
        }

        if choice in programs:
            program_name = programs[choice]
            print("You have chosen:", program_name)
            print(" _         _   _                  _                  _ _   _     ")
            print("| |    ___| |_( )___  __   _____ | |_ ___  __      _(_) |_| |__  ")
            print(
                "| |   / _ \\ __|// __| \\ \\ / / _ \\| __/ _ \\ \\ \\ /\\ / / | __| '_ \\ "
            )
            print(
                "| |__|  __/ |_  \\__ \\  \\ V / (_) | ||  __/  \\ V  V /| | |_| | | |"
            )
            print(
                "|_____\\___|\\__| |___/   \\_/_\\___/ \\__\\___|   \\_/\\_/ |_|\\__|_| |_|"
            )
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

    # Use the devnet configuration generated by `nillion-devnet`
    network = Network.from_config("devnet")

    # Create payments config and set up Nillion wallet with a private key to pay for operations
    nilchain_key: str = os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0")  # type: ignore
    payer = NilChainPayer(
        network,
        wallet_private_key=NilChainPrivateKey(bytes.fromhex(nilchain_key)),
        gas_limit=10000000,
    )
    signing_key = PrivateKey(CONFIG_PARTY_1["private_key"])

    client = await VmClient.create(signing_key, network, payer)

    # Adding funds to the client balance so the upcoming operations can be paid for
    funds_amount = 3000000
    print(f"💰  Adding some funds to the executor client balance: {funds_amount} uNIL")
    await client.add_funds(funds_amount)

    # Normally, the other party could disclose the user id to us, but we're just going
    # to build the user_id from our config
    for party_info in CONFIG_N_PARTIES:
        other_payer = DummyPayer()
        other_sk = PrivateKey(party_info["private_key"])
        other_client = await VmClient.create(other_sk, network, other_payer)
        reader_user_id = other_client.user_id
        print(f"🙏  As a paymaster, add some funds to the other client balance: {funds_amount} uNIL")
        await client.add_funds(funds_amount, target_user=reader_user_id)

    #####################################
    # 2. Storing program                #
    #####################################

    program_mir_path = f"../nada_programs/target/{program_name}.nada.bin"
    if not os.path.exists(program_mir_path):
        raise FileNotFoundError(
            f"The file '{program_mir_path}' does not exist.\nMake sure you compiled the PyNada programs with './compile_programs.sh'.\nCheck README.md for more details."
        )

    # Store program in the Network
    print(f"Storing program in the network: {program_name}")
    program = open(program_mir_path, "rb").read()
    program_id = await client.store_program(program_name, program).invoke()
    print(f"Program id is: {program_id}")

    #####################################
    # 3. Send program ID                #
    #####################################

    # This requires its own mechanism in a real environment.
    print(f"Alice stored {program_name} program at program_id: {program_id}")
    print("Alice tells Bob and Charlie her user_id and the voting program_id")

    print(
        "\n📋⬇️ Copy and run the following command to store Bob and Charlie's votes in the network"
    )
    print(
        f"\npython3 02_store_secret_party_n.py --user_id_1 {client.user_id} --program_id {program_id} --program_name {program_name}"
    )


asyncio.run(main())
