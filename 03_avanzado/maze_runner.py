def maze_runner(maze, directions):
    row, col = 0, 0
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 2:
                row, col = r, c

    for direction in directions:
        if direction == "N":
            row -= 1
        elif direction == "S":
            row += 1
        elif direction == "E":
            col += 1
        elif direction == "W":
            col -= 1

        if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):
            return "Dead"
        elif maze[row][col] == 1:
            return "Dead"
        elif maze[row][col] == 3:
            return "Finish"
    return "Lost"

print(maze_runner([1,1,1,1,1,1,1]))