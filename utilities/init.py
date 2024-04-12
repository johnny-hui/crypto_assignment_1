import getopt
import sys


def parse_arguments():
    """
    Parse the command line for arguments.

    @return: json_file_path, encrypt_method, criteria
        Strings representing JSON file path, encryption method
        (DES or AES), and criteria (SPAC or SKAC)
    """
    # Initialize variables
    json_file_path, encrypt_method, criteria = "", "", ""
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments, 'f:e:c:')

    if len(opts) == 0:
        sys.exit("[+] No arguments provided!")

    for opt, argument in opts:
        if opt == '-f':  # For JSON file path
            try:
                with open(argument, "r"):
                    json_file_path = argument
            except FileNotFoundError:
                sys.exit("[+] ERROR: File not found in path provided ({})".format(argument))

        if opt == '-e':  # For encryption method
            if argument in {"DES", "AES"}:
                encrypt_method = argument
            else:
                sys.exit("[+] ERROR: An invalid encryption method was provided! (-e option)")

        if opt == '-c':  # For avalanche criteria
            if argument in {"SPAC", "SKAC"}:
                criteria = argument
            else:
                sys.exit("[+] ERROR: An invalid avalanche criteria was provided! (-c option)")

    # Check if parameters are provided
    if len(json_file_path) == 0:
        sys.exit("[+] ERROR: JSON file path was not provided! (-f option)")

    if len(encrypt_method) == 0:
        sys.exit("[+] ERROR: An Encryption method (SPAC or SKAC) was not provided! (-e option)")

    if len(criteria) == 0:
        sys.exit("[+] ERROR: An avalanche criteria was not provided! (-c option)")

    return json_file_path, encrypt_method, criteria
