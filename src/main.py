import argparse
import csv


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.number_of_projects = 0
        self.number_of_experts = 0
        self.number_of_features = 0
        self.experts = []
        self.projects = []

    def print_everything(self):
        print("Input data parsed: \n")
        print(self.data)
        print("\n")
        print("Number of projects: " + str(self.number_of_projects))
        print("Number of experts: " + str(self.number_of_experts))
        print("Number of features: " + str(self.number_of_features))
        print("Obtained projects: " + str(self.projects))
        print("Obtained experts: " + str(self.experts))

    def read_csv(self):
        #  This will read our CSV file into a 2D list
        print('Reading input file: ' + self.file_path)
        with open(self.file_path, 'r') as f:
            reader = csv.reader(f)
            self.data = list(reader)  # Here we store the input file
            self.obtain_header_data()
            self.obtain_projects()
            self.obtain_experts()
            self.print_everything()

    def obtain_header_data(self):
        header = self.data[0]
        self.number_of_projects = int(header[0])
        self.number_of_experts = int(header[1])
        self.number_of_features = int(header[2])

    def obtain_projects(self):
        for x in range(1, self.number_of_projects + 1):
            self.projects.append(self.data[x])

    def obtain_experts(self):
        for x in range(self.number_of_projects + 1, self.number_of_projects + self.number_of_experts + 1):
            self.experts.append(self.data[x])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # The argument is of the form -f or --file.
    # If -f or --file is given... for ex: "main.py -f" but no file is given then the "const" argument specifies the file
    # If no -f or --file option is given at all then the "default" argument specifies the file
    parser.add_argument('-f', '--file', nargs='?', type=str, default='../resources/test.csv',
                        const='../resources/test.csv', help='Path to input CSV file to be read')
    program_args = vars(parser.parse_args())
    main = Main(program_args['file'])
    main.read_csv()
