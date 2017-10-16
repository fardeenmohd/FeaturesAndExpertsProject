import argparse
import csv


class Main:
    def __init__(self):
        self.data = None
        self.number_of_project = 0
        self.number_of_experts = 0
        self.number_of_features = 0
        self.experts = None
        self.number_of_project = None

    def print_everything(self):
        print("Input data parsed: \n")
        print(self.data)
        print("\n")
        print("Number of experts: " + str(self.number_of_experts))
        print("Number of projects: " + str(self.number_of_project))
        print("Number of features: " + str(self.number_of_features))

    def read_csv(self, file_path: str):
        #  This will read our CSV file into a 2D list
        print('Reading input file: ' + file_path)
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            self.data = list(reader)  # Here we store the input file
            self.obtain_header_data(self.data)
            self.print_everything()

    def obtain_header_data(self, row_list: list):
        header = row_list.__getitem__(0)
        self.number_of_project = int(header[0])
        self.number_of_experts = int(header[1])
        self.number_of_features = int(header[2])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # The argument is of the form -f or --file.
    # If -f or --file is given... for ex: "main.py -f" but no file is given then the "const" argument specifies the file
    # If no -f or --file option is given at all then the "default" argument specifies the file
    parser.add_argument('-f', '--file', nargs='?', type=str, default='../resources/test.csv',
                        const='../resources/test.csv', help='Path to input CSV file to be read')
    program_args = vars(parser.parse_args())
    main = Main()
    main.read_csv(program_args['file'])
