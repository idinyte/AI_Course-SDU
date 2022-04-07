import time

class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})
    
    def optimized_backtracking_search(self):
        return self.optimized_recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result:
                    return result
                del assignment[var]

        return False

    def optimized_recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                    assignment[var] = value
                    if self.forward_checking(assignment, var, value):
                        result = self.optimized_recursive_backtracking(assignment)
                        if result:
                            return result
                        del assignment[var]

        return False
    
    def forward_checking(self, assignment, var, value):
        for neighbour in self.neighbours[var]:
            if neighbour not in assignment:
                if value in self.domains[neighbour]:
                    self.domains[neighbour].remove(value)
                    if len(self.domains[neighbour]) == 1:
                        self.arc_consistency(neighbour, assignment)
                    if not self.domains[neighbour]: # if empty
                        return False
        return True

    def arc_consistency(self, neighbour, assignment):
        for higher_order_neighbour in self.neighbours[neighbour]:
            if higher_order_neighbour not in assignment:
                if self.domains[neighbour][0] in self.domains[higher_order_neighbour]:
                    self.domains[higher_order_neighbour].remove(self.domains[neighbour][0])
                    if len(self.domains[higher_order_neighbour]) == 1:
                        self.arc_consistency(higher_order_neighbour, assignment)

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        return self.domains[variable][:]

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(value, neighbour_value):
                    return False
        return True


def create_south_america_csp():
    s, br, fg, g, v, co, pe, e, bo, pa, a, ch, u, fi, tat = 'S', 'BR', 'FG', 'G', 'V', 'CO', 'PE', 'E', 'BO', 'PA', 'A', 'CH', 'U', 'FI', 'TAT'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [s, br, fg, g, v, co, pe, e, bo, pa, a, ch, u, fi, tat]
    domains = {
        s: values[:],
        br: values[:],
        fg: values[:],
        g: values[:],
        v: values[:],
        co: values[:],
        pe: values[:],
        e: values[:],
        bo: values[:],
        pa: values[:],
        a: values[:],
        ch: values[:],
        u: values[:],
        fi: values[:],
        tat: values[:]
    }
    neighbours = {
        s: [br, fg, g],
        br: [fg, s, g, v, co, pe, bo, pa, a, u],
        fg: [s, br],
        g: [v, s, br],
        v: [g, br, co],
        co: [v, e, br, pe],
        pe: [e, co, br, bo, ch],
        e: [co, pe],
        bo: [pe, br, ch, pa, a],
        pa: [bo, br, a],
        a: [ch, u, pa, bo, br],
        ch: [pe, bo, a],
        u: [a, br],
        fi: [],
        tat: [],
    }

    def constraint_function(first_value, second_value):
        return first_value != second_value

    constraints = {
        s: constraint_function,
        br: constraint_function,
        fg: constraint_function,
        g: constraint_function,
        v: constraint_function,
        co: constraint_function,
        pe: constraint_function,
        e: constraint_function,
        bo: constraint_function,
        pa: constraint_function,
        a: constraint_function,
        ch: constraint_function,
        u: constraint_function,
        fi: constraint_function,
        tat: constraint_function
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    south_america = create_south_america_csp()
    tic = time.time()
    result = south_america.backtracking_search()
    toc = time.time()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))
    print("Elapsed time - {} \n".format(toc-tic))

    # CSP with forward checking and arc consistency, doesn't seem like my implementation made code faster
    tic = time.time()
    result = south_america.optimized_backtracking_search()
    toc = time.time()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))
    print("Elapsed time - {}".format(toc-tic))

    # Check at https://www.mapchart.net/americas.html
