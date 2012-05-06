#Finding the best path using Dynamic Programming with Stochastic Motion

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]

goal = [0, len(grid[0])-1] # Goal is in top right corner

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

success_prob = 0.5                      
failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
collision_cost = 100                    
cost_step = 1

def stochastic_value():
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True
    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'
                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):

                        v2 = cost_step

                        for i in range(-1, 2):
                            a2 = (a + i) % len(delta)
                            x2 = x + delta[a2][0]
                            y2 = y + delta[a2][1]

                            if i == 0:
                                p2 = success_prob
                            else:
                                p2 = (1.0 - success_prob) / 2.0

                            if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                                v2 += p2 * value[x2][y2]
                            else:
                                v2 += p2 * collision_cost

                        if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                                policy[x][y] = delta_name[a]
    for i in range(len(value)):
        print map(lambda x:float("%.3f"%x),value[i])
    for i in range(len(policy)):
        print policy[i]
    return value, policy

print stochastic_value()[0]