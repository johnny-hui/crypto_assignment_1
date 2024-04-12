def analyze_bit_differences(hex1: str, hex2: str):
    """
    Takes two hex strings and returns the differences between them.
    :param hex1:
    :param hex2:
    :return:
    """
    # Convert hex values to binary strings
    binary1 = hex_to_binary(hex1)
    binary2 = hex_to_binary(hex2)

    # Ensure both binary strings have the same length by padding them with zeros
    max_length = max(len(binary1), len(binary2))
    binary1 = binary1.zfill(max_length)
    binary2 = binary2.zfill(max_length)

    # Compare corresponding bits and count differences
    diff_count = sum(bit1 != bit2 for bit1, bit2 in zip(binary1, binary2))
    return diff_count


def hex_to_binary(hex_string):
    # Remove any whitespaces
    hex_string = hex_string.replace(" ", "")

    # Convert hex string to integer
    value = int(hex_string, 16)

    # Determine the number of bits required to represent the integer
    num_bits = len(hex_string) * 4

    # Convert integer to binary string with leading zeros
    binary_string = format(value, '0{}b'.format(num_bits))

    return binary_string


if __name__ == '__main__':
    he1 = hex_to_binary("102cce015fe1f4f83a92b21f4c387a64")  # ORIGINAL TEXT
    he2 = hex_to_binary("13DDF104FE1F4F83A92B21F4C387A64")
    print(he1)
    print(he2)
    print(f"Number of bit differences: {analyze_bit_differences(he1, he2)}")
