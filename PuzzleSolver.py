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

def reconstruct_path(parent, end):
    path = [end]
    while path[-1] in parent:
        path.append(parent[path[-1]])
    return list(reversed(path))

def astar(start_state):
    start_state = tuple(start_state)

    pq = []
    heappush(pq, (manhattan(start_state), 0, start_state))

    parent = {}
    g_cost = {start_state: 0}
    visited = set()

    while pq:
        f, g, state = heappop(pq)

        if state == GOAL:
            return reconstruct_path(parent, state)

        if state in visited:
            continue
        visited.add(state)

        zero = state.index(0)

        for move in MOVES[zero]:
            new_state = list(state)
            new_state[zero], new_state[move] = new_state[move], new_state[zero]
            new_state = tuple(new_state)

            new_g = g + 1

            if new_state not in g_cost or new_g < g_cost[new_state]:
                g_cost[new_state] = new_g
                parent[new_state] = state
                f = new_g + manhattan(new_state)
                heappush(pq, (f, new_g, new_state))

    return None

def greedy(start_state):
    start_state = tuple(start_state)

    pq = []
    heappush(pq, (manhattan(start_state), start_state))

    parent = {}
    visited = set()

    while pq:
        h, state = heappop(pq)

        if state == GOAL:
            return reconstruct_path(parent, state)

        if state in visited:
            continue
        visited.add(state)

        zero = state.index(0)

        for move in MOVES[zero]:
            new_state = list(state)
            new_state[zero], new_state[move] = new_state[move], new_state[zero]
            new_state = tuple(new_state)

            if new_state not in visited:
                parent[new_state] = state
                heappush(pq, (manhattan(new_state), new_state))

    return None
          

#prints boards side by side
#numbers separated by space
#boars separated by ||
def print_boards(board1, board2):
    for i in range(3):
        #excluded 0
        row1 = ' '.join(str(x) if x != 0 else ' ' for x in board1[i*3:i*3+3])
        row2 = ' '.join(str(x) if x != 0 else ' ' for x in board2[i*3:i*3+3])
        print(f"{row1}     ||     {row2}")
    print("------    ||    ------\n")

# User Input
def read_initial_state():
    print("Enter 9 numbers for the puzzle (0 = blank).")
    print("Example: 1 2 3 4 5 6 7 8 0\n")

    nums = input("Enter puzzle: ").strip().split()
    
    if len(nums) != 9:
        raise ValueError("You must enter exactly 9 numbers.")

    # Convert to integers
    state = list(map(int, nums))

    # Validate numbers are 0-9
    if sorted(state) != list(range(9)):
        raise ValueError("Puzzle must contain all numbers from 0 to 8 exactly once.")

    return tuple(state)

def is_solvable(state):
    #Checks inversion count by checking the number of reverse orgered pairs
    arr = [x for x in state if x != 0]  
    inv_count = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] > arr[j]:
                inv_count += 1
    # Odd-width grid (3x3): solvable if inversions count is even
    return inv_count % 2 == 0


# Main driver
if __name__ == "__main__":
    start = read_initial_state()
    print("\nInitial board:")
    print_boards(start, start)
    
    if not is_solvable(start):
        print("This puzzle configuration is NOT solvable.")
        exit()

    path_astar = astar(start)
    path_greedy = greedy(start)

    # Check if each algorithm found a solution
    #Even if complete, A* could fail due to memory issues maybe?
    if path_astar is None:
        print("A* did not find a solution.")
    if path_greedy is None:
        print("Greedy did not find a solution.")

    # Pad shorter path to show side by side completely
    #have to use due to the nature of zip to stop on shorter iteration
    prepaddedg_len = len(path_greedy)-1
    prepaddeda_len = len(path_astar)-1
    max_len = max(len(path_astar), len(path_greedy))
    path_astar += [path_astar[-1]] * (max_len - len(path_astar))
    path_greedy += [path_greedy[-1]] * (max_len - len(path_greedy))
    
    print("Greedy BFS||  A* Search")
    counter = 0
    for step_astar, step_greedy in zip(path_astar, path_greedy):
        if counter == 0:
            print("Initial State:")
        else:
            print(f"Step {counter}:")
        print_boards(step_greedy, step_astar)
        counter += 1
    print("Greedy BFS||  A* Search")
    print("Soln found|| Soln found")
    print(f"in {prepaddedg_len} moves||in {prepaddeda_len} moves ")



