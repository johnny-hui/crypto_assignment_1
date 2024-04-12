from utilities.init import parse_arguments
from utilities.utility import analyze_avalanche_effect, generate_graph

if __name__ == '__main__':
    json_file_path, encrypt_method, criteria = parse_arguments()

    # Perform analysis
    if encrypt_method == 'DES':
        results = analyze_avalanche_effect(file_path=json_file_path, encryption=encrypt_method, criteria=criteria)
        generate_graph(results, encrypt_method, criteria)

    if encrypt_method == 'AES':
        results = analyze_avalanche_effect(file_path=json_file_path, encryption=encrypt_method, criteria=criteria)
        generate_graph(results, encrypt_method, criteria)
