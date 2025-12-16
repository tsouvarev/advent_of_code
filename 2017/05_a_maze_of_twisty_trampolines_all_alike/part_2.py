"""
Now, the jumps are even stranger:
after each jump, if the offset was three or more, instead decrease it by 1.
Otherwise, increase it by 1 as before.

Using this rule with the above example, the process now takes 10 steps,
and the offset values after finding the exit are left as 2 3 2 3 -1.

How many steps does it now take to reach the exit?
"""

type Jump = int
type Maze = list[Jump]


def run(maze: Maze) -> int:
    instruction_pointer, steps = 0, 0

    while instruction_pointer < len(maze):
        offset = maze[instruction_pointer]
        maze[instruction_pointer] += -1 if offset >= 3 else 1
        instruction_pointer += offset
        steps += 1

    return steps


assert run([0, 3, 0, 1, -3]) == 10


with open("2017/05_a_maze_of_twisty_trampolines_all_alike/input.txt") as f:
    maze = [int(line.strip()) for line in f]
    print(run(maze))
