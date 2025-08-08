# QueensSolver
A program made to solve LinkedIn Queens grids

## Dependencies
You will need to install ortools to be able to use this program
```powershell
pip install ortools
```

## Purpose
This program uses Google's OR-Tools Constraint Programming and Boolean Satisfiability (CP-SAT) solver to process mathematical constraints, and use them to create a solution which is translated into a readable grid by this program, in order to solve a LinkedIn Queens problem

## Instructions

- Open up a terminal and navigate to the directory where you cloned/downloaded the repository to
--> example:
  ```Powershell
  cd "C:\Users\user\Documents\GitHub\QueensSolver"
  ```
- Take a screenshot of the Queens board such that the entire board is within the frame. The screenshot doesn't have to be perfect since the program handles borders and crops the image automatically, but do keep it close since the program won't work if the image doesn't handle as a grid.

example:


<img width="297" height="302" alt="queens1" src="https://github.com/user-attachments/assets/8f7b1f09-6c32-4fd5-9709-9aba34548017" />


- In the terminal, write the following
```Powershell
python solver.py --image your-image-path --length side-length
```
--> replacing your-image-path with the path to the screenshot you took of the board and side-length being the number of tiles along the side of the grid (for example the image above would have a side length of 9)

### Output:
The program will return a board with the correct placements for the crowns or if there is no solution will return a status of "INFEASIBLE"

## The Math
### For this problem, the constraints are:
- each crown must occupy a space in a colored square
- only one crown can be in a square
- no crown can be in any sqaure within the row or column that another crown already occupies
- no crown can be 1 square away diagonally from any other crown

### Mathematically, this would be represented as:
variables:
- c = color
- (i,j) are coordinates
- diagonals = {(di,dj)|di,dj elementof {-1,1} = {(-1,-1),(-1,1),(1,-1),(1,1)}}

1) $\\sum_{i,j} x_{i,j,c} = 1 \quad \forall c\$ --> one crown in color c at coordinates (i,j)
2) $\\sum_{c} x_{i,j,c} \leq 1 \quad \forall i,j\$ --> no tile (i,j) can have more than one crown
3) $\\sum_{j,c} x_{i,j,c} \leq 1 \quad \forall i\$ --> no crown can have another crown in the same row
4) $\\sum_{i,c} x_{i,j,c} \leq 1 \quad \forall j\$ --> no crown can have another crown in the same column
5) $\ x_{i,j,c} + x_{i+di, j+dj, c'} \leq 1 \quad \forall i,j,c,c',(di,dj)\$ --> no crown can have another crown diagonally adjacent to it

## Issues
If you encounter a situation where you use this to solve a LinkedIn Queens problem and it returns "INFEASIBLE" I would greatly appreaciate it if you could screenshot the board and send it through the issues tab in this repository

Every LinkedIn Queens problem has a solution so if you are getting "INFEASIBLE" then there is an underlying issue in my code I need to fix
