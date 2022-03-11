A = 'A'
B = 'B'
percepts = []
table = {
((A, 'Clean'),): 'Right',
((A, 'Dirty'),): 'Suck',
((B, 'Clean'),): 'Left',
((B, 'Dirty'),): 'Suck',
((A, 'Clean'), (A, 'Clean')): 'Right',
((A, 'Clean'), (A, 'Dirty')): 'Suck',
# ...
((A, 'Clean'), (A, 'Clean'), (A, 'Clean')): 'Right',
((A, 'Clean'), (A, 'Clean'), (A, 'Dirty')): 'Suck',
((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left',
# ...
}

def LOOKUP(percepts, table): # Lookup appropriate action for percepts
  action = table.get(tuple(percepts))
  return action

def TABLE_DRIVEN_AGENT(percept): # Determine action based on table and percepts
  percepts.append(percept) # Add percept
  action = LOOKUP(percepts, table) # Lookup appropriate action for percepts
  return action

def run(): # run agent on several sequential percepts
  print('Action\tPercepts' )
  print(TABLE_DRIVEN_AGENT((A, 'Clean')), '\t', percepts)
  print(TABLE_DRIVEN_AGENT((A, 'Dirty')), '\t', percepts)
  print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts)

# 1.
run()

# 2.

# fails because history with 4 tuples doesn't exist, we need to expand table or discard some of the earlier entries in history
print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts)

# 3.
# 4 entries

# 4.
# 4^T entries