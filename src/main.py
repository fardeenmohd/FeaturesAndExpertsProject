import argparse
import csv
import itertools
from typing import List
from copy import deepcopy

class Expert:
    def __init__(self):
        self.features = []
        self.used_for_feature = -1


class Project:

    def __lt__(self, other):
        sum1 = sum(self.experts_needed)
        sum2 = sum(other.experts_needed)
        return sum1 < sum2

    def __eq__(self, other):
        sum1 = sum(self.experts_needed)
        sum2 = sum(other.experts_needed)
        return sum1 == sum2

    def __init__(self):
        self.experts_needed = []
        self.experts_used = []


class Solution:
    def __init__(self, projects: List[Project] = None):
        self.projects = projects
        self.projects_solved = []
        self.num_of_experts_used = 0
        self.num_of_projects_solved = 0
        count = 0
        for i in range(len(self.projects)):
            # print('Project ' + str(i))
            # print(str(self.projects[i].experts_needed))
            # print('Experts used: ' + str(self.projects[i].experts_used))
            count += len(self.projects[i].experts_used)
            if all([val == 0 for val in self.projects[i].experts_needed]):
                self.projects_solved.append(i)
        self.num_of_experts_used = count
        self.num_of_projects_solved = len(self.projects_solved)

    def print_result(self):
        print("--SOLUTION RESULT--")
        for i in range(len(self.projects)):
            print('Project ' + str(i))
            print('Experts used: ' + str(self.projects[i].experts_used))
        print('Num of projects solved: ' + str(self.num_of_projects_solved))
        print("Projects solved: " + str(self.projects_solved))
        print("Number of experts used: " + str(self.num_of_experts_used))


class Main:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = None
        self.number_of_projects = 0
        self.number_of_experts = 0
        self.number_of_features = 0
        self.experts_as_lists = []
        self.projects_as_lists = []
        self.projects = []
        self.experts = []
        self.expert_combinations = []
        self.project_combinations = []
        self.solutions = []

    def print_everything(self):
        print("Input data parsed:")
        print(self.data)
        print("Number of projects: " + str(self.number_of_projects))
        print("Number of experts: " + str(self.number_of_experts))
        print("Number of features: " + str(self.number_of_features))
        print("Obtained projects: " + str(self.projects_as_lists))
        print("Obtained experts: " + str(self.experts_as_lists))

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
            self.projects_as_lists.append(list(map(int, self.data[x])))
            project = Project()
            project.experts_needed = list(map(int, self.data[x]))
            project.experts_used = list()
            self.projects.append(project)

    def obtain_experts(self):
        for x in range(self.number_of_projects + 1, self.number_of_projects + self.number_of_experts + 1):
            self.experts_as_lists.append(list(map(int, self.data[x])))
            expert = Expert()
            expert.features = list(map(int, self.data[x]))
            self.experts.append(expert)

    def solve_brute_force(self, find_all_solutions: bool = False):
        self.solutions.clear()
        expert_indices = [i for i in range(len(self.experts))]  # Get list of indices of experts
        project_indices = [i for i in range(len(self.projects))]

        # Find every combination of expert indices (of length len(self.experts))
        self.expert_combinations = list(itertools.permutations(expert_indices, len(self.experts)))

        # Find every combination of project indices
        for length in range(1, len(self.projects_as_lists) + 1):
            for subset in itertools.permutations(project_indices, length):
                self.project_combinations.append(list(subset))

        # print("Project combinations: " + str(self.project_combinations))
        # print("Expert combinations: " + str(self.expert_combinations))
        print("Expected amount of iterations: " + str(len(self.project_combinations) * len(self.expert_combinations) * self.number_of_experts * self.number_of_projects))
        best_solution = Solution(projects=list())
        # Loop through every combination of experts and projects and find a solution
        for expert_combination in self.expert_combinations:
            for project_combination in self.project_combinations:
                # Copy list of experts and projects to a temp variable so we can distinguish between solutions
                current_experts = list([deepcopy(self.experts[i]) for i in expert_combination])
                current_projects = list([deepcopy(self.projects[i]) for i in project_combination])
                # print("Current Projects: " + str(project_combination))
                # print("Current experts: " + str(expert_combination))
                expert_idx = 0
                for expert in current_experts:
                    expert_was_used = False
                    # Try to apply expert to all projects
                    for project in current_projects:
                        if not expert_was_used:
                            for j in range(self.number_of_features):
                                if project.experts_needed[j] > 0 and expert.features[j] > 0:
                                    project.experts_needed[j] -= 1
                                    expert_was_used = True
                                    project.experts_used.append(expert_combination[expert_idx])
                                    # expert.used_for_feature = j
                                    break
                    expert_idx += 1
                new_solution = Solution(list(current_projects))
                if find_all_solutions:
                    self.solutions.append(new_solution)
                else:
                    if new_solution.num_of_projects_solved > best_solution.num_of_projects_solved:
                        best_solution = new_solution

        if not find_all_solutions:
            self.solutions.append(best_solution)

    def solve_gman(self):
        self.solutions.clear()
        self.projects.sort()
        sorted_projects = [x.experts_needed for x in self.projects]
        print("Sorted projects: " + str(sorted_projects))
        for i in range(self.number_of_experts):
            expert_was_used = False
            # print(str(self.projects[i].experts_used))
            for j in range(self.number_of_projects):
                # Check if expert is needed for a given project:
                if not expert_was_used:
                    for k in range(self.number_of_features):
                        if self.projects[j].experts_needed[k] > 0 and self.experts[i].features[k] > 0:
                            self.projects[j].experts_needed[k] -= 1
                            self.projects[j].experts_used.append(i)
                            self.experts[i].used_for_feature = k
                            expert_was_used = True
                            break

        # TODO implement swapping of remaining experts
        self.solutions.append(Solution(projects=self.projects))

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
    # main.solve_gman()
    for solution in main.solutions:
        solution.print_result()
