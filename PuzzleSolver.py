from heapq import heappush, heappop


# Goal State, uses 0 as placeholder for blank
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
#List of moves depending on placement/index on the board of 0/blankst
MOVES = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}

#Manhattan Distance heuristic
def manhattan(state):
    total = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue  # don't count the blank
        
        #goal position of each tile is the index less than its number
        goal_pos = tile - 1

         #each iteration of total would add the row + column distance of each tile's number (except 0/blank)
         #current_row = i // 3
         #current _col = i % 3
         #goal_row = goal_pos // 3
         #goal_col = goal_pos % 3
        total += abs((i // 3) - (goal_pos // 3)) + abs((i % 3) - (goal_pos % 3))

    return total

def astar(start_state):
    start_state = tuple(start_state)

    # The priority queue stores: (f(n), g(n), state)
    pq = []
    heappush(pq, (manhattan(start_state), 0, start_state))

    # Parent dictionary to reconstruct the final path
    parent = {}

    # g-cost dictionary: cost to reach each state
    g_cost = {start_state: 0}

    # Visited set to avoid reprocessing states
    visited = set()

    while pq:
        f, g, state = heappop(pq)  # pick state with lowest f(n)

        if state == GOAL:
            # Goal reached! Reconstruct path
            path = [state]
            while state in parent:
                state = parent[state]
                path.append(state)
            path.reverse()
            return path

        if state in visited:
            continue
        visited.add(state)

        zero = state.index(0)

        for move in MOVES[zero]:
            new_state = list(state)
            new_state[zero], new_state[move] = new_state[move], new_state[zero]
            new_state = tuple(new_state)

            new_g = g + 1  # cost to reach neighbor

            # if we haven't seen this state or found a cheaper path
            if new_state not in g_cost or new_g < g_cost[new_state]:
                g_cost[new_state] = new_g
                parent[new_state] = state
                f = new_g + manhattan(new_state)
                heappush(pq, (f, new_g, new_state))


#prints the states 
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i+1], state[i+2])
    print("------")

# User Input
def read_initial_state():
    print("Enter your puzzle configuration (0 = blank).")
    print("Make sure no numbers repeat or it will not run")
    print("Example of one row: 1 2 3\n")

    state = []
    for i in range(3):
        row = input(f"Row {i+1}: ").strip().split()
        if len(row) != 3:
            raise ValueError("Each row must have exactly 3 numbers.")
        nums = list(map(int, row))
        state.extend(nums)

    if sorted(state) != list(range(9)):
        raise ValueError("Puzzle must contain all numbers from 0 to 8 exactly once.")

    return tuple(state)

def solve_puzzle(start_state, algorithm):
    " call the chosen search algorithm. algorithm: astar"

    if algorithm == "astar":
        return astar(start_state)
    else:
        raise ValueError("Unknown algorithm: choose 'astar' or '[insert]'")

if __name__ == "__main__":
    start = read_initial_state()

    print("\nInitial board:")
    print_state(start)

    # Choose the algorithm here
    algorithm = input("Choose algorithm (astar/[insert]) ").strip().lower()

    path = solve_puzzle(start, algorithm=algorithm)

    if path:
        print(f"Solution found in {len(path)-1} moves:\n")
        for step in path:
            print_state(step)
    else:
        print("No solution found.")


