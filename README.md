# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The contraint is that any two boxes in the same unit sharing the same two digits and only these digits mean those digits are the only possible solutions.  This means the two digits can be removed as possible solutions to all other boxes in the unit.  As with eliminate and one choice we can iteratively apply naked twins to propagate the local contraint such that it induces a state in another region off the space where we can apply another constraint reducing the space to be searched.

   The implementation iterates through each unit and each box in that unit.  When we find a box with only two digits as possible solutions we check all other boxes in the unit to see if there is a naked twin (a box with the same two digits as its only possible solution).  If we find a pair of naked twins we append them to a list of known naked twins and continue the search for any remaining naked twins.
   
   When we have found them all we again loop through each unit and check if there are naked twins in that unit.  If naked twins are in the unit we loop through all other boxes  in that unit and remove the two digits as possible solutions for those boxes.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: All the constraints that apply to other units apply equally to diagonal units.  The implementations of eliminate, one_choice and naked_twins mean we can simply add the diagonal units to the list of units.  This means that when we call reduce_puzzle the diagonal units are now taken into consderation.  A contraint applied to a diagonal unit will reduce the search space and could result in other regions of the space being solvable by one of our contraints.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
