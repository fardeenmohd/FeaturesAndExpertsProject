import argparse
import csv


def read_csv(file_path: str):
    #  This will read our CSV file into a 2D list
    print('Reading input file: ' + file_path)
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)  # Here we store the input file
        print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # The argument is of the form -f or --file.
    # If -f or --file is given... for ex: "main.py -f" but no file is given then the "const" argument specifies the file
    # If no -f or --file option is given at all then the "default" argument specifies the file
    parser.add_argument('-f', '--file', nargs='?', type=str, default='../resources/test.csv',
                        const='../resources/test.csv', help='Path to input CSV file to be read')
    program_args = vars(parser.parse_args())
    read_csv(program_args['file'])