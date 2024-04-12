import json


def __print_task_info(experiment, control, criteria):
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


def analyze_avalanche_effect(file_path: str, encryption: str, criteria: str):
    """
    Analyzes the avalanche effect for DES.

    @param file_path:
        A string representing the file path to data JSON

    @param criteria:
        A string representing the avalanche effect criteria
        (SPAC or SKAC)

    @return: None
    """
    # Load JSON data
    with open(file_path) as json_file:
        data = json.load(json_file)

    # Control Group: no changes in plaintext
    control = data[0]

    # Experimental Group: plaintext with bit changes
    for experiment in data[1:]:
        __print_task_info(experiment, control, criteria)

        # Iterate through the rounds
        for round_num, round_data in experiment["round"].items():
            print("[+] Round {} Bit Difference".format(round_num))

            # Get original control data
            control_round_data = control["round"][round_num]

            if encryption == "DES":
                # Get Original Round Cipher (L + R)
                control_round_ciphertext = hex_to_binary(control_round_data["l" + round_num]
                                                         + control_round_data["r" + round_num])
                print("\tOriginal Intermediate Cipher:")
                print(f"\t{control_round_ciphertext}")

                # Get Modified Round Cipher (L + R)
                round_ciphertext = hex_to_binary(round_data["l" + round_num]
                                                 + round_data["r" + round_num])
                print("\tModified Intermediate Cipher:")
                print(f"\t{round_ciphertext}")

                # Calculate Round Bit Differences
                bit_diff = analyze_bit_differences(control_round_ciphertext, round_ciphertext)
                print(f"\tNumber of bit differences: {bit_diff}\n")
            else:
                # Get original block state
                control_round_block_state = control_round_data["block_state"]
                print("\tOriginal Block State:")
                print(f"\t{control_round_block_state}")

                # Get modified block state
                exp_round_block_state = experiment["round"][round_num]["block_state"]
                print("\tModified Block State:")
                print(f"\t{exp_round_block_state}")

                # Calculate Round Bit Differences
                bit_diff = analyze_bit_differences(hex_to_binary(control_round_block_state),
                                                   hex_to_binary(exp_round_block_state))
                print(f"\tNumber of bit differences: {bit_diff}\n")

        # Calculate Final Bit Difference
        print("Final Ciphertext (Original):   {}".format(hex_to_binary(control["final_ciphertext"])))
        print("Final Ciphertext (Experiment): {}".format(hex_to_binary(experiment["final_ciphertext"])))
        bit_diff = analyze_bit_differences(control["final_ciphertext"], experiment["final_ciphertext"])
        print(f"Bit difference: {bit_diff}")
        print("=" * 80)


if __name__ == '__main__':
    print(analyze_bit_differences("0f1571c947d9e8590cb7add6af7f6798", "1E0460D856D9E8590CB7ADD6AF7F6798"))
