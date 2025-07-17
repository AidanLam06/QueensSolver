from ortools.sat.python import cp_model
colors = []
grid = [] 
x = {}
model = cp_model.CpModel()

# initialize side length
side_len = int(input("Enter the side length of the square: "))

# initialize colorset
while True:
    colorsin = input(f"Enter the {side_len} chars for each color: ").lower().split()
    if len(colorsin) != side_len:
        print(f"There are {side_len} colors per puzzle. Enter {side_len} and only {side_len} colors")
    else:
        colors = colorsin
        break

print(colors)

# intialize grid
for r in range(side_len):
    while True:
        row = input(f"Enter row {r+1}: ").lower().split()
        if len(row) != side_len:
            print(f"The row you enter must have exactly {side_len} tiles. Try again")
            continue
        invalid = [b for b in row if b not in colors]
        if invalid:
            in_format = ", ".join(invalid)
            color_format = ", ".join(colors)
            print(f"{in_format} are invalid colors. Use : ({color_format})\n")
        else:
            grid.append(row)
            break

# grid legitimacy check
for a in grid:
    for g in a:
        if len(g) > 1:
            print("Your grid is invalid. Restart the program")
            exit(1)

# initialize variables x_(i,j,c) 
for i in range(side_len):
    for j in range(side_len):
        for c in range(side_len):
            if grid[i][j] == colors[c]:
                x[i,j,c] = model.NewBoolVar(f"x_{i}_{j}_{c}")

# 1) only one crown per color
for c in range(side_len):
    model.Add(sum(x[i,j,c] for i in range(side_len) for j in range(side_len) if (i,j,c) in x) == 1) 


# 2) only one crown per tile
for i in range(side_len):
    for j in range(side_len):
        model.Add(sum(x[i,j,c] for c in range(side_len) if (i,j,c) in x) <= 1)

# 3) only one crown per row
for i in range(side_len):
    model.Add(sum(x[i,j,c] for j in range(side_len) for c in range(side_len) if (i,j,c) in x) == 1) 

# 4) only one crown per column
for j in range(side_len):
    model.Add(sum(x[i,j,c] for i in range(side_len) for c in range(side_len) if (i,j,c) in x) == 1)
    
# 5) a crown can only occupy a space where all four of its diagonally adjacent tiles (+-1 diagonally) do not contain a crown
for i in range(side_len):
    for j in range(side_len):
        for di, dj in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            if 0 <= i+di < side_len and 0 <= j+dj < side_len:
                for c1 in range(side_len):
                    for c2 in range(side_len):
                        if (i,j,c1) in x and (i+di,j+dj,c2) in x:
                            model.Add(x[i,j,c1] + x[i+di,j+dj,c2] <= 1)

solver = cp_model.CpSolver()
status = solver.solve(model)

if status == cp_model.OPTIMAL:
    solution = [["·" for _ in range(side_len)] for _ in range(side_len)]

    for i in range(side_len):
        for j in range(side_len):
            for c in range(side_len):
                if (i,j,c) in x and solver.Value(x[i,j,c]) == 1:
                    solution[i][j] = "♕"

    print("\nSolution:")
    print("+" + "---+" * side_len)
    for row in solution:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * side_len)
else:
    print("No solution found")

print("\nSolver stats:")
print(f"Status: {solver.StatusName(status)}")
print(f"Conflicts: {solver.NumConflicts()}")
print(f"Branches: {solver.NumBranches()}")