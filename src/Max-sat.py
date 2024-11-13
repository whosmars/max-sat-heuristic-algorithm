import random;

#Solution class envolves all the logic of the maxsat solution, it has two inner classes, Clause and Variable
class Solution:

    #Clause are a disjuntion of variables, it has three, a function it also has a f evaluate the clause using the python boolean operators
    class Clause:
        def __init__(self, a, b, c):
            self.variables = [a, b, c]


        def evaluar(self):
            val = any([variable.evaluate() for variable in self.variables])
            print ("The clause is: ", val)
            return val
    
        def __str__(self):
            return f"Clause({self.variables[0]} v {self.variables[1]} v {self.variables[2]})"
    
    #Variable class has a name, a value and a negated value, it has a function evaluate to return the value of the variable, NEGATION ATTRIBUTE IS A ESENTIAL PART
    class Variable:
            def __init__(self, name, value=None, is_negated=False):
                self.name = name
                self.value = value

                self.is_negated = is_negated
            
            def set_negated(self):
                self.is_negated = True


            def set_var(self, value):
                self.value = value

            def set_name(self, name):
                self.name = name

            def evaluate(self):
                return not self.value if self.is_negated else self.value
            
            def __str__(self):
                negated = "~" if self.is_negated else ""
                value_str = f"value={self.value}"
                return f"{negated}{self.name}({value_str})"
        
        

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.variables = []
        self.clauses = []
        self.solution = []
    
    def get_number_of_clauses(self):
        return self.m

    #Depending n value, it sets the available variables, if n is 4 then the available variables are A, B, C, D
    def set_available_vars(self):
        AVAILABLE_VARIABLES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                                 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                 'U', 'V', 'W', 'X', 'Y', 'Z']
        if self.n > len(AVAILABLE_VARIABLES):
            raise ValueError('The number of variables must be less than 26')
        self.variables = AVAILABLE_VARIABLES[:self.n]

        print("Available Variables:")
        for var in self.variables:
            print(f"  {var}")

    #Generate the clauses selection randomly from available variables before defined with  set_available_vars
    def set_clauses(self):
        for _ in range(self.m):
            name_vars = random.sample(self.variables, 3)
            
            clause_vars = []
            for var in name_vars:
                new_var = self.Variable(var)
                if random.choice([True, False]):
                    new_var.set_negated()
                clause_vars.append(new_var)
            
            clause = self.Clause(clause_vars[0], clause_vars[1], clause_vars[2])
            self.clauses.append(clause)


    #Esto corresponde al PUNTO 3 de la practica
    def number_of_satisfied_clauses(self):
        return sum([clause.evaluar() for clause in self.clauses])
    
    def error_in_solution(self):
        return self.get_number_of_clauses() - self.number_of_satisfied_clauses()
                        
    def print_clauses(self):
        print("\nClauses:")
        for clause in self.clauses:
            print(f"  {clause}")     

    #los primeros 3 puntos de esta funcion llaman a otras funciones que engloban el PUNTO 2a. requerido en la practica
    #set the problem step by step, first the available variables, then the clauses, then the aproximation algorithm and finally check the number of satisfied clauses
    def set_maxsat(self):
        self.set_available_vars()
        self.set_clauses()
        self.approximation_algorithm()
        print ("The assigned values are the following:", self.solution)
        self.print_clauses()

    #only instaciates the values of the variables depending on the values of the array of booleans
    def assign_values(self, arr_bool):
        if len(arr_bool) != len(self.variables):
            raise ValueError('The number of values must be equal to the number of variables')
        for clause in self.clauses:
            for i in range(len(arr_bool)):
                for variable in clause.variables:
                    if variable.name == self.variables[i]:
                        variable.set_var(arr_bool[i])



    #Este es el PUNTO 2.b de la practica
    #my aproximation (heuristic) algorithm works counting the number of negated and not negated of each available vars name
    #then it assigns the value depend on the greater value
    def approximation_algorithm(self):
        #create dictionaries to count the number of negated and not negated ocurrences for each variable name
        negated_count = {var_name: 0 for var_name in self.variables}
        not_negated_count = {var_name: 0 for var_name in self.variables}
        #counting negated and not negated for each name var
        for clause in self.clauses:
            for variable in clause.variables:
                if variable.is_negated:
                    negated_count[variable.name] += 1
                else:
                    not_negated_count[variable.name] += 1
        #restart the value of the solution asociated to the variables
        self.solution = []
        print("\nAprox algorithm assign part:")
        for var in self.variables:
            if negated_count[var] > not_negated_count[var]:
                self.solution.append(False)
                print(f"  {var} assigned value: {False}")
            else:
                self.solution.append(True)
                print(f"  {var} assigned value: {True}")

        # After assigning values, evaluate the number of satisfied clauses
        self.assign_values(self.solution)
        satisfied_clauses = self.number_of_satisfied_clauses()
        print(f"\nNumber of clauses: {self.get_number_of_clauses()}")
        print(f"\nNumber of satisfied clauses after heuristic assignment: {satisfied_clauses}")

    def obtener_numero_variables():
        while True:
            try:
                num_variables = int(input("Enter the number of variables (between 3 and 26): "))
                if 3 <= num_variables <= 26:
                    return num_variables
                else:
                    print("Please, enter a number between 3 and 26.")
            except ValueError:
                print("Invalid input. Please, enter an integer number.")

    def obtener_numero_clausulas():
        while True:
            try:
                num_clauses = int(input("Enter the number of clauses (minimum 8): "))
                if num_clauses >= 8:
                    return num_clauses
                else:
                    print("Please, enter a number greater or equal to 8.")
            except ValueError:
                print("Invalid input. Please, enter an integer number.")

                

if __name__ == "__main__":
    num_var = Solution.obtener_numero_variables()
    num_clauses = Solution.obtener_numero_clausulas()
    solution = Solution(num_var, num_clauses)
    solution.set_maxsat()
    satisfied_clauses = solution.number_of_satisfied_clauses()