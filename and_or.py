import itertools

suck_retults_dict = {
    (0, (1, 1)) : [(0, (0, 1)), (0, (0, 0))],
    (1, (1, 1)) : [(1, (1, 0)), (1, (0, 0))],
    (0, (1, 0)) : [(0, (0, 0))],
    (1, (1, 0)) : [(1, (1, 0)), (1, (1, 1))],
    (0, (0, 1)) : [(0, (0, 1)), (0, (1, 1))],
    (1, (0, 1)) : [(1, (0, 0))],
    (0, (0, 0)) : [(0, (0, 0)), (0, (1, 0))],
    (1, (0, 0)) : [(1, (0, 0)), (1, (0, 1))]    
}

class PlanNode:
    def __init__(self, action, children=None):
        self.action = action
        self.children = children if children is not None else []

    def __repr__(self, level=0):
        indent = '  ' * level
        result = indent + self.action + '\n'
        for child in self.children:
            result += child.__repr__(level + 1)
        return result

def create_plan_tree(plan):
    if not plan:
        return []

    action = plan[0]
    children = []

    for subplans in plan[1:]:
        for subplan in subplans:
            children += create_plan_tree(subplan)

    return [PlanNode(action, children)]


class ErraticVacuumWorld:
    def __init__(self, state):
        self.state = state

    def actions(self):
        return ['Suck', 'Left', 'Right']

    
    def result(self, state, action):
        if action == 'Suck':
            return suck_retults_dict[state]
        elif action == 'Left':
            return [(0, state[1]), (state[0], state[1])]
        elif action == 'Right':
            return [(1, state[1]), (state[0], state[1])]

    def goal_test(self, state):
        return state[1] == (0, 0)

def AndOrGraphSearch(problem):
    def OrSearch(state, problem, path):
        if problem.goal_test(state):
            return []

        #Is cycle
        if state in path:
            return None

        result = []
        path = path + [state]
        for action in problem.actions():
            plan = AndSearch(problem.result(state, action), problem, path)
            if plan:
                if action == 'Left' or action == 'Right':
                    result.append(['While ' + action]+ plan)
                else:
                    result.append([action]+ plan)
        return result

    def AndSearch(states, problem, path):
        result = []
        for s in states:
            plan = OrSearch(s, problem, path)
            if plan is None:
                continue
            #return format must contingency plan
            result.append(('if',s, 'then',plan))
        return result

    return OrSearch(problem.state, problem, [])

initial_state = (0, (1, 1))
problem = ErraticVacuumWorld(initial_state)
plan = AndOrGraphSearch(problem)
print(plan)


"""
initial state = (0, (1, 1))

And-or search tree

['Suck', 
    ('if', (0, (0, 1)), 'then', 
        [['Right', 
            ('if', (1, (0, 1)), 'then', 
                [['Suck', 
                    ('if', (1, (0, 0)), 'then', 
                        [])]])]]), 

    ('if', (0, (0, 0)), 'then', [])],

['Right', 
    ('if', (1, (1, 1)), 'then', 
        [['Suck', 
            ('if', (1, (1, 0)), 'then', 
                [['Left', 
                    ('if', (0, (1, 0)), 'then', 
                        [['Suck', 
                            ('if', (0, (0, 0)), 'then', 
                                [])]])]]),

            ('if', (1, (0, 0)), 'then', [])]])]
"""

"""
Cyclic solution
[['Suck', 
    ('if', (0, (0, 1)), 'then', 
        [['While Right', 
            ('if', (1, (0, 1)), 'then', 
                [['Suck', ('if', (1, (0, 0)), 'then', [])]])]]), 

    ('if', (0, (0, 0)), 'then', [])], 

['While Right', 
    ('if', (1, (1, 1)), 'then', 
        [['Suck', 
            ('if', (1, (1, 0)), 'then', 
                [['While Left', 
                    ('if', (0, (1, 0)), 'then', 
                        [['Suck', 
                            ('if', (0, (0, 0)), 'then', [])]])]]),

            ('if', (1, (0, 0)), 'then', [])]])]]
"""