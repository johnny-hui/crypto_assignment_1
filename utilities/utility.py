import json
import os
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from utilities.constants import GRAPH_LABEL_SKAC, GRAPH_LABEL_SPAC, SAVE_GRAPH_DIR


def __print_exp_info(experiment, control, criteria):
    if criteria == "SPAC":
        print("Task:", experiment["task"])
        print("Original Plaintext (in Binary):")
        print(hex_to_binary(control["plain_text"]))
        print("Modified Plaintext (in Binary):")
        print(hex_to_binary(experiment["plain_text"]))
        print("Plain Text:", experiment["plain_text"])
        print("Key:", experiment["key"])
        print("Method:", experiment["method"])
        print("=" * 80)
    else:
        print("Task:", experiment["task"])
        print("Original Key (in Binary): ", hex_to_binary(control["key"]))
        print("Modified Key (in Binary): ", hex_to_binary(experiment["key"]))
        print("Plain Text:", experiment["plain_text"])
        print("Key:", experiment["key"])
        print("Method:", experiment["method"])
        print("=" * 80)


def analyze_bit_differences(hex1: str, hex2: str):
    """
    Takes two hex strings and returns the bit differences between them.

    @param hex1:
        String representing first hex

    @param hex2:
        String representing second hex

    @return bit_difference:
        The bit difference between two hex strings (Int)
    """
    # Convert hex values to binary strings
    binary1 = hex_to_binary(hex1)
    binary2 = hex_to_binary(hex2)

    # Ensure both binary strings have the same length by padding them with zeros
    max_length = max(len(binary1), len(binary2))
    binary1 = binary1.zfill(max_length)
    binary2 = binary2.zfill(max_length)

    # Compare corresponding bits and count differences
    bit_difference = sum(bit1 != bit2 for bit1, bit2 in zip(binary1, binary2))
    return bit_difference


def hex_to_binary(hex_string):
    """
    Takes a hex string and returns the binary representation of it.

    @param hex_string:
        String representing the hex string

    @return: binary_string
        String representing the converted hex (binary)
    """
    # Remove any whitespaces
    hex_string = hex_string.replace(" ", "")

    # Convert hex string to integer
    value = int(hex_string, 16)

    # Determine the number of bits required to represent the integer
    num_bits = len(hex_string) * 4

    # Convert integer to binary string with leading zeros
    binary_string = format(value, '0{}b'.format(num_bits))
    return binary_string


def print_summary(data: dict):
    """
    Prints all experiments (rounds) for a given encryption
    algorithm and the criteria (SPAC or SKAC).

    @param data:
        A dictionary containing experiment results

    @return: None
    """
    for task, data_list in data.items():
        table = PrettyTable()
        table.title = task
        table.field_names = ["Round", "Original Cipher",
                             "Modified Cipher", "Bit Differences"]

        for row in data_list:
            table.add_row(row)

        print(table)
        print("\n")


def generate_graph(data: dict, encrypt_method: str, criteria: str):
    """
    Generates a line graph for representation of
    the avalanche effect, and saves it to as a
    PNG file under graphs/AES or graphs/DES directory.

    @param data:
        A dictionary containing experiment results

    @param encrypt_method:
        A string representing the encryption method (AES or DES)

    @param criteria:
        A string representing the criteria (SPAC or SKAC)

    @return: None
    """
    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot a line for each experiment from the results
    for key, value in data.items():
        rounds = [int(item[0]) for item in value]
        bit_diff = [item[3] for item in value]
        ax.plot(rounds, bit_diff, label=key)

    # Set labels and title (according to criteria)
    ax.set_xlabel('Rounds')
    ax.set_ylabel('Bit Difference')

    # Create directory to save graph
    if not os.path.exists(SAVE_GRAPH_DIR.format(encrypt_method)):
        os.makedirs(SAVE_GRAPH_DIR.format(encrypt_method))

    # Set title, legend and save graph
    if criteria == "SPAC":
        ax.set_title(f'{encrypt_method} Avalanche Effect (Bit Difference per Round - SPAC)')
        ax.legend(GRAPH_LABEL_SPAC, loc='lower right')
        plt.savefig(os.path.join(SAVE_GRAPH_DIR.format(encrypt_method), f'avalanche_effect_plot_{criteria}.png'))
    else:
        ax.set_title(f'{encrypt_method} Avalanche Effect (Bit Difference per Round - SKAC)')
        ax.legend(GRAPH_LABEL_SKAC, loc='lower right')
        plt.savefig(os.path.join(SAVE_GRAPH_DIR.format(encrypt_method), f'avalanche_effect_plot_{criteria}.png'))


def analyze_avalanche_effect(file_path: str, encryption: str, criteria: str):
    """
    Analyzes the avalanche effect (~50% bit differences in
    ciphertext when bit changes are made in plaintext
    or key).

    @param file_path:
        A string representing the file path to data JSON

    @param encryption:
        A string representing the encryption algorithm to use
        (DES or AES)

    @param criteria:
        A string representing the avalanche effect criteria
        (SPAC or SKAC)

    @return analysis_results:
        A dictionary containing the results of the avalanche effect
    """
    # Load JSON data
    with open(file_path) as json_file:
        data = json.load(json_file)

    # Control Group: no changes in plaintext
    control = data[0]

    # Initialize dictionary to store results
    analysis_results = {}

    # Experimental Group: plaintext with bit changes
    for experiment in data[1:]:
        __print_exp_info(experiment, control, criteria)
        task_results = []

        # Iterate through the rounds
        for round_num, round_data in experiment["round"].items():
            print("[+] Round {} Bit Difference".format(round_num))

            # Get original control data
            control_round_data = control["round"][round_num]

            if encryption == "DES":
                # Get Original and Modified Round Ciphers (L + R)
                control_round_ciphertext = control_round_data["l" + round_num] + control_round_data["r" + round_num]
                control_round_ciphertext_binary = hex_to_binary(control_round_ciphertext)
                round_ciphertext = round_data["l" + round_num] + round_data["r" + round_num]
                round_ciphertext_binary = hex_to_binary(round_ciphertext)

                # Print the ciphers
                print("\tOriginal Intermediate Cipher:")
                print(f"\t{control_round_ciphertext_binary}")
                print("\tModified Intermediate Cipher:")
                print(f"\t{round_ciphertext_binary}")

                # Calculate Round Bit Differences
                bit_diff = analyze_bit_differences(control_round_ciphertext_binary, round_ciphertext_binary)
                print(f"\tNumber of bit differences: {bit_diff}\n")

                # Add results to list
                task_results.append([round_num, control_round_ciphertext, round_ciphertext, bit_diff])
            else:
                # Get original and modified block states
                control_round_block_state = control_round_data["block_state"]
                exp_round_block_state = experiment["round"][round_num]["block_state"]

                # Print the block states
                print("\tOriginal Block State:")
                print(f"\t{control_round_block_state}")
                print("\tModified Block State:")
                print(f"\t{exp_round_block_state}")

                # Calculate Round Bit Differences
                bit_diff = analyze_bit_differences(hex_to_binary(control_round_block_state),
                                                   hex_to_binary(exp_round_block_state))
                print(f"\tNumber of bit differences: {bit_diff}\n")

                # Add results to list
                task_results.append([round_num, control_round_block_state, exp_round_block_state, bit_diff])

        # Add round experiments to the dictionary
        analysis_results[experiment["task"]] = task_results

        # Calculate Final Bit Difference
        print("Final Ciphertext (Original):   {}".format(hex_to_binary(control["final_ciphertext"])))
        print("Final Ciphertext (Experiment): {}".format(hex_to_binary(experiment["final_ciphertext"])))
        bit_diff = analyze_bit_differences(control["final_ciphertext"], experiment["final_ciphertext"])
        print(f"Bit difference: {bit_diff}")
        print("=" * 80)

    print_summary(analysis_results)
    return analysis_results
