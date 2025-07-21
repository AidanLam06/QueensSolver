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

1) The program will first prompt you for a grid size, which is just the side length of the square grid that the game gives you
2) Then you will be asked for the color variables. The number of colors on the grid is the same number as the grid size, so for an 8x8 grid you would enter the 8 colors presented on the board in the following format:
```
p o b g e r y
```
p-purple
o-orange
b-blue
g-green
e-grey
r-red
y-yellow

The variables you pick for each color don't actually matter, the only constraint is that each color must have a different variable assigned to it

3) You will then be prompted for each row of the grid which you enter like:
```
p p p o o g r y
```
each color variable must be separated by a space

example:


<img width="410" height="406" alt="image" src="https://github.com/user-attachments/assets/7d494f9d-4da3-4a0e-b258-6e52ecda85ba" />




would be represented as:
```
p p p p p p p
p p o p b b p
p o o g g b b
p o e e g g b
p p p e e b b
p p r r y y b
p p p r r y y
```

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
= diagonals = {(di,dj)|di,dj elementof {-1,1} = {(-1,-1),(-1,1),(1,-1),(1,1)}}

1) $\\sum_{i,j} x_{i,j,c} = 1 \quad \forall c\$ --> one crown in color c at coordinates (i,j)
2) $\\sum_{c} x_{i,j,c} \leq 1 \quad \forall i,j\$ --> no tile (i,j) can have more than one crown
3) $\\sum_{j,c} x_{i,j,c} \leq 1 \quad \forall i\$ --> no crown can have another crown in the same row
4) $\\sum_{i,c} x_{i,j,c} \leq 1 \quad \forall j\$ --> no crown can have another crown in the same column
5) $\ x_{i,j,c} + x_{i+di, j+dj, c'} \leq 1 \quad \forall i,j,c,c',(di,dj)\$ --> no crown can have another crown diagonally adjacent to it

## Issues
If you encounter a situation where you use this to solve a LinkedIn Queens problem and it returns "INFEASIBLE" I would greatly appreaciate it if you could screenshot the board and send it through the issues tab in this repository

Every LinkedIn Queens problem has a solution so if you are getting "IFEASIBLE" then there is an underlying issue in my code I need to fix