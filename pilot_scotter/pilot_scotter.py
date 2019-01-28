#!/usr/bin/python2
import numpy
import logging
import pprint
"""
    read the inputs
    Find the weight matrix
    sort the array into one dimension
    generate the subset and start comparing from the solution set
"""
NUM_OF_OFFICERS = 1
WEIGHT_MATRIX = []
INDEX_MAP ={}
SORT_LIST = []
MAX_POINTS = 0
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
city_width = 0

    
def calculate_weight_matrix(cor_array_points, city_width):
    """ calulate the weight matrix of the solution """
    input_list = [[0 for i in range(0, city_width)] for j in range(0, city_width)]
    for i in range(0, len(cor_array_points)):
        [x, y] = map(int, cor_array_points[i].strip().split(','))
        input_list[x][y] = input_list[x][y] + 1

    pprint.pprint(input_list)
    return input_list

def read_inputs():
    """
        read the inputs of from the file
    """
    global NUM_OF_OFFICERS, WEIGHT_MATRIX, city_width
    file_handl = open('input.txt')
    input_array = file_handl.readlines()
    file_handl.close()

    city_width = int(input_array[0])
    NUM_OF_OFFICERS = int(input_array[1])
    WEIGHT_MATRIX = calculate_weight_matrix(input_array[3:], city_width)

def create_map():
    """
        create a 1d map of index
    """
    for i in range(0, city_width):
        for j in range(0, city_width):
            SORT_LIST.append(WEIGHT_MATRIX[i][j])
            if WEIGHT_MATRIX[i][j] in INDEX_MAP.keys():
                INDEX_MAP[WEIGHT_MATRIX[i][j]].append((i, j))
            else:
                INDEX_MAP[WEIGHT_MATRIX[i][j]] = [(i, j)]
    
    #sort the array
    SORT_LIST.sort(reverse=True)
        
def is_valid_placement():
    """
        get the valid positions
    """
    
def get_max_possible():
    """
        get the maximum activity point possible
    """
    max_sum_possible  = 0 
    for i in SORT_LIST[0:NUM_OF_OFFICERS]:
        max_sum_possible = max_sum_possible + i

    return max_sum_possible


def reduce_space(matrix, row, col):
    for rows in range(len(matrix)):
        for cols in range(len(matrix[0])):
            if(abs(row -rows) == abs(col - cols)):
                matrix[rows][cols] = -1


    np = numpy.array(matrix)
    np = numpy.delete(np, row, axis=0)
    np = numpy.delete(np, col, axis=1)
    max_value = numpy.amax(np)
    return [max_value, np.tolist(), zip(*numpy.where(np == max_value))]


def apply_greedy(row, col, copy_matrix, officer_count):
    """
    """
    temp_cost = 0
    while (officer_count != 0):
        [max_sum, copy_matrix, index_list] = reduce_space(copy_matrix, row, col)
        temp_cost = temp_cost + max_sum
        officer_count -= 1
        row, col = index_list[0]
    
    return temp_cost

def find_greedy_sol(num):

    global MAX_POINTS
    list_of_indices = INDEX_MAP[num]
    num_of_off = NUM_OF_OFFICERS
    num_of_off -= 1
    for (row, col) in list_of_indices:
        copy_matrix = WEIGHT_MATRIX
        cost_value = num + apply_greedy(row, col, copy_matrix, num_of_off)
        if cost_value > MAX_POINTS:
            MAX_POINTS = cost_value 

def run_dfs():
    """
        run dfs
    """
    res = []
    global MAX_POINTS, NUM_OF_OFFICERS
    def dfs(queens, ddiff, ssum):
        global MAX_POINTS
        p = len(queens)
        if p == NUM_OF_OFFICERS:
            row = 0
            sum_value = 0
            for cols in queens:
                sum_value = sum_value + WEIGHT_MATRIX[row][cols]
                row = row + 1
            print "Solution with %s is %s\n" % (sum_value, queens)
 
            if sum_value > MAX_POINTS:
                MAX_POINTS = sum_value
            return
        for q in range(NUM_OF_OFFICERS):
            if q in queens or p - q in ddiff or p + q in ssum: continue
            dfs(queens + [q],
                ddiff + [p - q],
                ssum + [p + q])
    dfs([], [], [])
    return


if __name__ == "__main__":
    #calculate the weight matrix

    global NUM_OF_OFFICERS
    global city_width 
    global WEIGHT_MATRIX
    read_inputs()
    create_map()
    if NUM_OF_OFFICERS == city_width:
        run_dfs()
    else:
        for nums in SORT_LIST:
            find_greedy_sol(nums)

    file_handl = open('output.txt', 'w')
    file_handl.write(str(MAX_POINTS))
    file_handl.close()
    print ("\nSolution mama %s" % MAX_POINTS)
