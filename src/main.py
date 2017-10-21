import argparse
import csv
import itertools
from typing import List


class Solution:
    def __init__(self, experts_used: List[int], projects_solved: List[int]):
        self.experts_used = experts_used
        self.num_of_experts_used = len(experts_used)
        self.projects_solved = projects_solved
        '''
        for i in range(len(projects)):
            if all([val == 0 for val in projects[i]]):
                self.projects_solved.append(projects[i])
        '''

        self.num_of_projects_solved = len(self.projects_solved)

    def print_result(self):
        print("--SOLUTION RESULT--")
        print("Number of projects solved: " + str(self.num_of_projects_solved))
        print("Number of experts used: " + str(self.num_of_experts_used))
        print("Experts used: " + str(self.experts_used))
        print("Projects solved: " + str(self.projects_solved))


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.number_of_projects = 0
        self.number_of_experts = 0
        self.number_of_features = 0
        self.experts = []
        self.projects = []
        self.expert_combinations = []
        self.project_combinations = []
        self.solutions = []

    def print_everything(self):
        print("Input data parsed:")
        print(self.data)
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
            self.projects.append(list(map(int, self.data[x])))

    def obtain_experts(self):
        for x in range(self.number_of_projects + 1, self.number_of_projects + self.number_of_experts + 1):
            self.experts.append(list(map(int, self.data[x])))

    def solve_brute_force(self):
        expert_indices = [i for i in range(len(self.experts))]  # Get list of indices of experts
        project_indices = [i for i in range(len(self.projects))]

        # Find every combination of expert indices (of length len(self.experts))
        self.expert_combinations = list(itertools.permutations(expert_indices, len(self.experts)))

        # Find every combination of project indices
        for length in range(1, len(self.projects) + 1):
            for subset in itertools.permutations(project_indices, length):
                self.project_combinations.append(list(subset))

        # Loop through every combination of experts and projects and find a solution
        for expert_combination in self.expert_combinations:
            for project_combination in self.project_combinations:
                # Copy list of experts and projects to a temp variable so we can distinguish between solutions
                current_experts = list([list(self.experts[i]) for i in expert_combination])
                current_projects = list([list(self.projects[i]) for i in project_combination])
                print("Current Projects: " + str(current_projects))
                print("Current experts: " + str(current_experts))
                expert_idx = 0
                experts_used = []
                projects_solved = []
                for expert in current_experts:
                    expert_was_used = False
                    project_idx = 0
                    # Try to apply expert to all projects
                    for project in current_projects:
                        if not expert_was_used:
                            for j in range(self.number_of_features):
                                if project[j] > 0 and expert[j] > 0:
                                    project[j] -= 1
                                    # expert[j] = 0  # So this expert does not get used again
                                    expert_was_used = True
                                    experts_used.append(expert_combination[expert_idx])
                                    if all([val == 0 for val in project]):
                                        projects_solved.append(project_combination[project_idx])
                                    break
                        project_idx += 1
                    expert_idx += 1
                self.solutions.append(Solution(experts_used, projects_solved))

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
    main.solve_brute_force()
    for solution in main.solutions:
        solution.print_result()