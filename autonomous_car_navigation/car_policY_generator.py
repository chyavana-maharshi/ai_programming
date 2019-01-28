#!/usr/bin/env python 
from numpy import random
import numpy
import sys
from copy import deepcopy
import logging

SIZE = 0
CARS = []
ENDS = []
RESULT = []
#COST_MATRIX_TEMP = 
OBS = []
POLICY_HASH = {}

def print2darray(A):
    return '\n'.join([' '.join(['{:8}'.format(item) for item in row]) for row in A])

def read_inputs():
    """
        read the inputs from the file
    """
    global SIZE, CARS, ENDS, OBST, COST_MATRIX_TEMP
    file_handl = open('input.txt', 'r')
    input_lines = file_handl.readlines()
    SIZE = int(input_lines[0])
    COST_MATRIX_TEMP = numpy.array([[-1] * SIZE for i in range(SIZE)], dtype='float64')
    cur_index = 3
    num_cars = int(input_lines[1])
    num_obs = int(input_lines[2])
    
    for i in range(cur_index, cur_index + num_obs):
        (y_cor, x_cor) = map(int, input_lines[i].strip().split(','))
        COST_MATRIX_TEMP[x_cor][y_cor] = COST_MATRIX_TEMP[x_cor][y_cor] - 100
        OBS.append((x_cor, y_cor))
        
    cur_index += num_obs
    for i in range(cur_index, cur_index + num_cars):
        (y1_cor, x1_cor) = map(int, input_lines[i].strip().split(','))
        CARS.append((x1_cor, y1_cor))

    cur_index += num_cars

    #populate the car terminating condition
    for i in range(cur_index, cur_index + num_cars):
        (y1_cor, x1_cor) = map(int, input_lines[i].strip().split(','))
        ENDS.append((x1_cor, y1_cor))


    return COST_MATRIX_TEMP


def find_move(policies_car, pos):
    return policies_car[pos[0]][pos[1]]


def get_position(move, pos):
    """
    """
    global SIZE
    grid_size = SIZE
    pos_new = (0, 0)
    if move == 'North':
        pos_new = numpy.subtract(pos, (1, 0))
    
    if move == 'South':
        pos_new = numpy.subtract(pos, (-1, 0))

    if move == 'West':
        pos_new = numpy.subtract(pos, (0, 1))

    if move == 'East':
        pos_new = numpy.subtract(pos, (0, -1))

    pos_new = tuple(pos_new)
    if ( ((pos_new[0] >= 0 and pos_new[0] <= grid_size -1) and (pos_new[1] <= grid_size -1 and pos_new[1] >= 0))):
        return pos_new
    else:
        return pos

map_direction = {'North' : ('West', 'East'), 'South' : ('East', 'West'), 'East' : ('North', 'South'), 'West' : ('South', 'North')}

def check_status(i ,j):
    """
    """
    global SIZE
    if ( ((i >= 0 and i <= SIZE -1) and (j <= SIZE -1 and j >= 0))):
        return True

    return False

def all_possible_tp(utility_func, i , j):
    """
    """
    global SIZE
    if i-1 >= 0:
        north_val = numpy.float64(utility_func[i-1][j], precision=15)
    else:
        north_val =  numpy.float64(utility_func[i][j], precision=15)
        #north_val = 0

    if i+1 <= SIZE - 1:
        south_value =  numpy.float64(utility_func[i+1][j], precision=15)

    else:
        south_value =  numpy.float64(utility_func[i][j], precision=15)
        #south_value = 0


    if j-1 >= 0:
        west_value =  numpy.float64(utility_func[i][j-1], precision=15)
    else:
        west_value =  numpy.float64(utility_func[i][j], precision=15)
        #west_value = 0

    if j+1 <= SIZE - 1:
        east_value =  numpy.float64(utility_func[i][j+1], precision=15)
    else:
        east_value =  numpy.float64(utility_func[i][j], precision=15)
        #east_value = 0

    #utility_west = 0.7 * west_value + 0.1 * east_value +  0.1 * north_val  + 0.1 * south_value
    #utility_east = 0.7 * east_value + 0.1 * west_value +  0.1 * north_val  + 0.1 * south_value
    #utility_north = 0.7 * north_val + 0.1 * west_value +  0.1 * east_value  + 0.1 * south_value
    #utility_south = 0.7 * south_value + 0.1 * west_value +  0.1 * east_value  + 0.1 * north_val

    
    utility_north = (0.7 * north_val + 0.1 * south_value +  0.1 * east_value  + 0.1 * west_value)
    utility_south = (0.1 * north_val + 0.7 * south_value +  0.1 * east_value  + 0.1 * west_value)
    utility_east = (0.1 * north_val + 0.1 * south_value +  0.7 * east_value  + 0.1 * west_value)
    utility_west = (0.1 * north_val + 0.1 * south_value +  0.1 * east_value  + 0.7 * west_value)
    #utility_west = (0.7 * west_value) + (0.1 * east_value) +  (0.1 * north_val)  + (0.1 * south_value)
    #utility_east = (0.1 * west_value) + (0.7 * east_value) +  (0.1 * north_val)  + (0.1 * south_value)
    #utility_north = (0.1 * west_value) + (0.1 * east_value) +  (0.7 * north_val)  + (0.1 * south_value)
    #utility_south = (0.1 * west_value) + (0.1 * east_value) +  (0.1 * north_val)  + (0.7 * south_value)
    max_value = max(utility_east, utility_south, utility_west, utility_north)


    #if i in range(22,26) and j in range(20,31):
     #   print('Items being compared for (%s %s) = %.15f %.15f %.15f %.15f max= %.15f' % (i, j, utility_north, utility_south, utility_east, utility_west, max_value))

    if max_value == utility_north:
        #print("Max Direction being returned North")
        return [max_value, 'North']

    if max_value == utility_south:
        #print("Max Direction being returned South")
        return [max_value, 'South']

    if max_value == utility_east:
        #print("Max Direction being returned east")
        return [max_value, 'East']

    if max_value == utility_west:
        #print("Max Direction being returned west")
        return [max_value, 'West']


def value_iteration(policy, cost_matrix, x, y):

    global SIZE
    #utility =  numpy.zeros((SIZE, SIZE), dtype='float64')
    utility = numpy.array(deepcopy(cost_matrix), dtype='float64')
    #utility[x][y] = 99
    gamma = 0.9
    error = 0.1
    expected_error = error * ((1 - gamma)  / gamma)
    #print "Before starting the simulation. cost matrix %s\n Utility is %s \n plicy is %s" % ( numpy.matrix(cost_matrix), numpy.matrix(utility), numpy.matrix(policy))
    #sys.exit(0)
    while True:
        delta = 0.0
        updated_utility = deepcopy(utility)
        #for each possible states generate calculate delta
        for i in range(len(utility)):
            for j in range(len(utility[0])):
                if i == x and j == y:
                    #utility[i][j] = 99.0
                    continue
                else:
                    [utility_value, dire] = all_possible_tp(updated_utility, i, j)
                    utility[i][j] = cost_matrix[i][j] + 0.9 * utility_value
                    policy[i][j] = dire
                delta = max(delta, abs((utility[i][j] - updated_utility[i][j])))

        if delta < expected_error:
            numpy.set_printoptions(precision=15)
            utility_copy = utility
            #utility_copy = utility[22:25, 20:30]
            numpy.set_printoptions(precision=15)
            #print(numpy.matrix(utility_copy))
            policy = numpy.array(policy)
            #print("\npolicy %s\n" % numpy.matrix(policy))
            #print("\npolicy %s\n" % numpy.matrix(policy[22:25, 20:30]))
            #sys.exit(0)
            return policy

def simulate(cost_matrix_temp):
    """
    """
    global RESULT, COST_MATRIX_TEMP, ENDS, CARS, POLICY_HASH
    for i in range(len(CARS)):
        #print("Value of i is %s" % i)
        cost_matrix = deepcopy(cost_matrix_temp)
        tuple_value = ENDS[i]
        cost_matrix[tuple_value[0]][tuple_value[1]] += 100
        policy_matrix = [[None] * SIZE for iop in range(SIZE)]
        if tuple_value in POLICY_HASH.keys():
            policy_matrix = POLICY_HASH[tuple_value]
        else:
            policy_matrix = value_iteration(policy_matrix, cost_matrix, tuple_value[0], tuple_value[1])
            POLICY_HASH[tuple_value] = policy_matrix

        cost_value = 0
        total_reward = 0
        #print("Policy for the car %s is \n %s" % (i, print2darray(policy_matrix)))
        for j in range(10):
            pos = CARS[i]
            if pos[0] == ENDS[i][0] and pos[1] == ENDS[i][1]:
                cost_value = 100 * 10
                break
            numpy.random.seed(j)
            swerve = numpy.random.random_sample(10000000)
            k=0
            while pos[0] != ENDS[i][0] or pos[1] != ENDS[i][1]:
                move = find_move(policy_matrix, pos)
                if swerve[k] > 0.7:
                    if swerve[k] > 0.8:
                        if swerve[k] > 0.9:
                            #left left
                            move = map_direction[map_direction[move][1]][1]
                        else:
                            #left changing to right
                            move = map_direction[move][1]
                    else:
                        #right left
                        move = map_direction[move][0]
                

                k += 1
                pos = get_position(move, pos)
                #print(str(pos))
                cost_value += cost_matrix[pos[0]][pos[1]]
            #in range group
        
        total_reward = float(numpy.floor(cost_value/10))
        #print("Mean %s" % total_reward)
        #sys.exit(0)
        RESULT.append(int(total_reward))

if __name__ == "__main__":

    cost_matrix = read_inputs()
    simulate(cost_matrix)
    print(RESULT)
    file_handl = open('output.txt', 'w')
    for num in RESULT:
        file_handl.write("%s\n" % str(num))
    file_handl.close()
