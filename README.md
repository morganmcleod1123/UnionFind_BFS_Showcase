# Percolation Simulation
This program creates an NxN grid and randomly removes squares from the grid until percolation is achieved. At that point,
it returns a path between squares in the top and bottom to validate the percolation.

The point of this program is to practice and demonstrate the Union-Find and Breadth-First search algorithms as they apply to
solve the given problem.
## Basic Structure
Our grid is a size NxN 2D array of Square objects. Each Square object has an enum for its status: open, closed, or visited.
At the start, our grid has all of its squares closed. Until percolation is achieved, a random closed square is opened and
the program evaluates whether this achieved percolation.

When percolation is achieved, the program returns the path that forms percolation as well as the percentage of squares that
had to be opened to achieve it.
## Algorithms Utilized
### Union-Find
The union-find, or disjoint-set, algorithm was used to group adjacent open squares on the grid. If one set of open squares
suddenly touches another one after a square is opened, the sets are all merged into one. This is the "union" aspect of 
union-find.

The program checks if percolation has been achieved by evaluating the open squares on the top and bottom of the grid. It
finds if any of the top squares belong to the same set as a bottom square. If this is true, it means there is a set of
adjacent open squares between a top and bottom square. This is the "find" aspect of union-find and proves percolation.
### Breadth-First Search
Breadth-first search is utilized to return the percolation path. Once the program confirms that percolation has been achieved,
it performs a breadth-first search from the last square that was opened. The breadth-first search terminates only when a square
from the top and bottom of the grid have both been found. This gives the shortest path that proves percolation in the grid.
