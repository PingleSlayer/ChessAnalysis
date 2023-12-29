import csv


def load_openings():
    tsv_files = ['a.tsv', 'b.tsv', 'c.tsv', 'd.tsv', 'e.tsv']
    fen_dict = {}

    # Iterate through each TSV file
    for tsv_file in tsv_files:
        with open(f'Openings/{tsv_file}', 'r', newline='') as file:
            reader = csv.DictReader(file, delimiter='\t')

            # Iterate through each row in the TSV file
            for row in reader:
                # Extract relevant columns
                eco = row['eco']
                opening_name = row['name']
                fen = row['epd']

                # Combine eco and opening_name into a single string
                eco_opening = f"{eco} - {opening_name}"

                # Add entry to the dictionary with FEN as the key and eco + opening_name as the value
                fen_dict[fen] = eco_opening

    return fen_dict
