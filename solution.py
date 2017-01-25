assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    #display(values)
    # Find all instances of naked twins
    naked_twins = []
    for unit in unitlist:
        for box in unit:
            if len(values[box]) == 2:
                for other_box in peers[box]:
                    if values[box] == values[other_box]:
                        
                        naked_twins.append((box,other_box))
    # Eliminate the naked twins as possibilities for their peers
    #print(set(naked_twins))
    for unit in unitlist:
        for naked_twin in set(naked_twins):
           if naked_twin[0] in unit and naked_twin[1] in unit:
               for box in unit:
                   if box not in naked_twin:
                       values = assign_value(values, box, values[box].replace(values[naked_twin[0]][0],""))
                       values = assign_value(values, box, values[box].replace(values[naked_twin[0]][1],""))
    #print()
    #display(values)
    #print()
    #from solution_test import after_naked_twins
    #display(after_naked_twins)
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_unit1 = [char+cols[i] for i,char in enumerate(rows)]
diag_unit2 = [char+cols[-(i+1)] for i,char in enumerate(rows)]

unitlist = row_units + column_units + square_units + [diag_unit1] + [diag_unit2]
#print(unitlist)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    # Write a function that will take as an input, the sudoku in dictionary form,
    # run through all the boxes, applying the eliminate technique,
    # and return the resulting sudoku in dictionary form.
    for box in values.keys():
        if len(values[box]) == 1:
            for peer in peers[box]:
                #values[peer] = values[peer].replace(values[box],"")
                values = assign_value(values, peer, values[peer].replace(values[box],""))
    return values

def only_choice(values):
    # Write a function that will take as an input, the sudoku in dictionary form,
    # run through all the units, applying the only choice technique,
    # and return the resulting sudoku in dictionary form.
    for unit in unitlist:
        for digit in "123456789":
            boxes = []
            for box in unit:
                if digit in values[box]:
                    boxes.append(box)
            if len(boxes) == 1:
                #values[boxes[0]] = digit
                values = assign_value(values, boxes[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    return search(grid_values(grid))

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    
    values = reduce_puzzle(values)
    if values == False:
        return values

    # recursion end condition
    if all(len(values[box]) == 1 for box in boxes):
        return values

    # Chose one of the unfilled square s with the fewest possibilities
    min = 9
    for box in boxes:
        if len(values[box]) < min and len(values[box]) > 1:
            min = len(values[box])
            s = box
    
    # Now use recursion to solve each one of the resulting sudokus,
    # and if one returns a value (not False), return that answer!
    for digit in values[s]:
        try_values = values.copy()
        try_values[s] = digit
        attempt = search(try_values)
        if attempt:
            return attempt

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    #display(grid_values(diag_sudoku_grid))
    solve(diag_sudoku_grid)
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
