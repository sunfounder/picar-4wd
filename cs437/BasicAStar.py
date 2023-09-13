import heapq

# Define the 4 possible movements: up, down, left, right
movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def heuristic(current, goal):
    # Calculate the Manhattan distance as the heuristic
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def astar_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []  # Priority queue of nodes to be evaluated
    closed_set = set()  # Set of nodes already evaluated
    came_from = {}  # Dictionary to store the path
    
    # Initialize the open set with the starting node
    heapq.heappush(open_set, (0, start))
    
    # Initialize scores for each node to infinity
    g_score = {position: float('inf') for row in grid for position in row}
    g_score[start] = 0
    
    # Main A* loop
    while open_set:
        current_g, current_node = heapq.heappop(open_set)
        
        if current_node == goal:
            # Reconstruct the path if the goal is reached
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]  # Return the path in reverse order
        
        closed_set.add(current_node)
        
        for dr, dc in movements:
            r, c = current_node[0] + dr, current_node[1] + dc
            neighbor = (r, c)
            
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != 1 and neighbor not in closed_set:
                tentative_g_score = g_score[current_node] + 1
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
    
    return None  # If no path is found

# Example usage
grid = [
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

print(grid[4][4])

path = astar_search(grid, start, goal)
if path:
    print("Path found:", path)
else:
    print("No path found")
