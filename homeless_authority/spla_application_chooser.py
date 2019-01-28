#!/usr/bin/python3 
"""
    assignment 2

"""
from copy import deepcopy
import sys
import logging
import signal
#generic static methods used to parse the lines
present_sum = -1
new_solution = []
spla_dict = {}
lhsa_dict = {}
cur_best_move = ''
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

"""
    Generate all the permutations using
    discard the duplicate entries
    calculate the maximum subset generated 
    return the best solution
"""
class HomelessAgent:
    """
    Class Holding application details
    """
    lhsa_applicants = []
    spla_applicants = []
    #list to be processes

    lhsa_available_applicant = {}
    spla_available_applicant = {}
    valid_both_applicants = {}

    #beds count
    beds_left = []
    parking_slot_left = []


    spla_id_list = []
    lhsa_id_list = []

    parking_slot = 0
    beds_slot = 0

    def __init__(self, line='', is_spla=0, is_lhsa=0):
        """
            constructor
        """
        
        self.applicant_info = HomelessAgent.process_applicant(line)

        if self.applicant_info['appl_id'] in HomelessAgent.spla_id_list:
            logging.debug('Adding spla candidate %s', self.applicant_info['appl_id'])
            print(self)
            HomelessAgent.spla_applicants.append(self)
            [status, HomelessAgent.parking_slot_left] =  HomelessAgent.reduce_slot_count(self.applicant_info['week_allocated'], HomelessAgent.parking_slot_left)


        elif self.applicant_info['appl_id'] in HomelessAgent.lhsa_id_list:
            HomelessAgent.lhsa_applicants.append(self)
            [status, HomelessAgent.beds_left] = HomelessAgent.reduce_slot_count(self.applicant_info['week_allocated'], HomelessAgent.beds_left)
        else:
            [valid_spla, valid_lhsa] = HomelessAgent.find_valid_category(self.applicant_info)
            if valid_spla and valid_lhsa:
                HomelessAgent.valid_both_applicants[self.applicant_info['appl_id']] = self.applicant_info['week_allocated']
            elif valid_spla:
                HomelessAgent.spla_available_applicant[self.applicant_info['appl_id']] = self.applicant_info['week_allocated']
            elif valid_lhsa:
                HomelessAgent.lhsa_available_applicant[self.applicant_info['appl_id']] = self.applicant_info['week_allocated']
            else:
                logging.debug("Invalid applicant Ignoring. %s" % self)

        

    @staticmethod
    def return_best_sum(item_hash, slots_left):
        """
            sort the applicant based on the applicant list
        """
        sum_v = -1
        id_v  = 'ZZZZZZ' 
        for items in item_hash:
            if not HomelessAgent.reduce_slot_count(item_hash[items], slots_left)[0]:
                continue
            temp = sum(item_hash[items])
            if temp >= sum_v:
                if temp == sum_v:
                    if items < id_v:
                        id_v = items
                else:
                    id_v = items

                sum_v = temp
                

        return id_v

    @staticmethod
    def get_max_ans(list_of_solu, spla_index, lhsa_index):
        """
            get the maximum solution
        """
        max_solution = []
        min_beds = sys.maxsize
        for solution in list_of_solu:
            spla_pa = HomelessAgent.parking_slot_left
            beds_pa = HomelessAgent.beds_left
            for game_pair in solution:
                week_slot = []
                if game_pair[spla_index] in HomelessAgent.valid_both_applicants:
                    week_slot =  HomelessAgent.valid_both_applicants[game_pair[spla_index]]
                else:
                    week_slot =  HomelessAgent.spla_available_applicant[game_pair[spla_index]]
                    
                [status, spla_pa] = HomelessAgent.reduce_slot_count(week_slot, spla_pa)
                if not status:
                    break

                week_slot = []
                if game_pair[lhsa_index] in HomelessAgent.valid_both_applicants:
                    week_slot =  HomelessAgent.valid_both_applicants[game_pair[lhsa_index]]
                else:
                    week_slot =  HomelessAgent.spla_available_applicant[game_pair[lhsa_index]]
                    
                [status, beds_pa] = HomelessAgent.reduce_slot_count(week_slot, beds_pa)
                if not status:
                    break

            temp = sum(spla_pa)
            if temp <= min_beds:
                max_solution.append(zip(*solution)[spla_index])


    @staticmethod
    def is_parking_slot_sufficient():
        """
            calculate the parking slot availability
        """
        solution_list = [0] * 7
        for cand in HomelessAgent.valid_both_applicants.keys():
            solution_list = map(lambda x,y: x+y, solution_list, HomelessAgent.valid_both_applicants[cand])

        for cand in HomelessAgent.spla_available_applicant.keys():
            solution_list = map(lambda x,y: x+y, solution_list, HomelessAgent.spla_available_applicant[cand])

        for slots in range(7):
            if (HomelessAgent.parking_slot_left[slots] - solution_list[slots] < 0):
                return False

        return True


    @staticmethod
    def return_best_sumUtil(common_hash, agent_alone, slot_left):
        if len(common_hash) != 0:
            idx = HomelessAgent.return_best_sum(common_hash, slot_left)
            if idx != 'ZZZZZZ':
                return idx
        return HomelessAgent.return_best_sum(agent_alone, slot_left)

#############################################################################################
    @staticmethod
    def all_applicant_zero(lis1):
        return all(v==0 for v in lis1)


    @staticmethod   
    def wrapper(spla_list, parking_slot_left, solution_list, index=0, map_value={}):
       
        new_solution = []
        def next_move_spla(spla_list, parking_slot_left, solution_list, index=0):
            global present_sum
            global new_solution
            if HomelessAgent.all_applicant_zero(parking_slot_left):
                temp_sum = HomelessAgent.calculate_sum(solution_list, map_value)
                if temp_sum > present_sum:
                    present_sum = temp_sum
                    pre_sol = deepcopy(solution_list)
                    new_solution = [pre_sol]
                elif temp_sum == present_sum:
                    pre_sol = deepcopy(solution_list)
                    new_solution.append(pre_sol)
        
                return
            
            if index == len(spla_list) - 1:
                 
                temp_sum = HomelessAgent.calculate_sum(solution_list, map_value)
                if temp_sum > present_sum:
                    present_sum = temp_sum
                    pre_sol = deepcopy(solution_list)
                    new_solution = [pre_sol]
                elif temp_sum == present_sum:
                    pre_sol = deepcopy(solution_list)
                    new_solution.append(pre_sol)
        
                return
        
            for i in range(index, len(spla_list)):
                if spla_list[i] in solution_list:
                    continue
                [status, new_reduction_list] = HomelessAgent.reduce_slot_count(map_value[spla_list[i]], parking_slot_left)
                if status:
                    solution_list.append(spla_list[i])
                    next_move_spla(spla_list, new_reduction_list,
                                   solution_list, i)
       
                    solution_list.pop()
        
                elif (i == len(spla_list) - 1):
                    temp_sum = HomelessAgent.calculate_sum(solution_list, map_value)
                    
                    if temp_sum > present_sum:
                        present_sum = temp_sum
                        pre_sol = deepcopy(solution_list)
                        new_solution = [pre_sol]
                    elif temp_sum == present_sum:
                        pre_sol = deepcopy(solution_list)
                        new_solution.append(pre_sol)
       
         
        next_move_spla(spla_list, parking_slot_left, [], 0)
        if len(new_solution) == 0:
            new_solution = [[]]
        #####################################################################################
    @staticmethod
    def generate_optimal_subsetUtil(common_agent, spec_agent):
        """
        """
        global new_solution
        final_dict = dict(common_agent.items() + spec_agent.items())
        HomelessAgent.wrapper(list(final_dict.keys()), HomelessAgent.parking_slot_left, [], 0, final_dict)
        copy_solution = deepcopy(new_solution)
        new_solution = []
        new_set = list(set(copy_solution[0]).intersection(set(common_agent.keys())))
        if len(new_set) == 1:
            return new_set[0]
        else:
            temp_hash = {}
            for ids in copy_solution[0]:
                temp_hash[ids] = spec_agent[ids]
            return HomelessAgent.return_best_sum(temp_hash, HomelessAgent.parking_slot_left)

    @staticmethod
    def calculate_sum(list2, map_value):
        """
        """
        solution_list = [0] * 7
        for items in list2:
            solution_list = map(lambda x, y: x+ y, solution_list, map_value[items])


        return sum(solution_list)


#####################################################################################################################################
    @staticmethod
    def available_actions(list_of_appl, space_left):
        """
        """
        action_list = {}
        for ids in list_of_appl:
           if all(space_left[i] - list_of_appl[ids][i] >= 0 for i in range(0, 7)):
                action_list[ids] = list_of_appl[ids]
        
        return action_list

    
    @staticmethod
    def max_spla_solution(spla_list_dict, lhsa_list_dict, parking_space_left, beds_space_left, solution_list_spla, solution_list_lhsa, spla_max, lhsa_max):
        """
        """
            #main terminating conditions
        global spla_dict
        global lhsa_dict
        global cur_best_move
        global new_solution
        cur_next_move = ''
        actions_spla = HomelessAgent.available_actions(spla_list_dict, parking_space_left)
        if len(spla_list_dict) == 0 or len(actions_spla) == 0:
           #what to do for the termination 
            sum_all_spla = 0
            sum_all_lhsa = 0
            for ids in solution_list_spla:
                sum_all_spla += sum(spla_dict[ids])
        
            for ids in solution_list_lhsa:
                sum_all_lhsa += sum(lhsa_dict[ids])
        
            if len(lhsa_list_dict) != 0:
                HomelessAgent.wrapper(lhsa_list_dict.keys(), beds_space_left, [], 0, lhsa_dict)
                print('New solution %s' % new_solution)
                if len(new_solution):
                    soln = new_solution[0]
                    if len(soln) != 0:
                        for ids in soln:
                            sum_all_lhsa += sum(spla_list_dict[ids])
        
            new_solution = []
            print('spla and lhsa value from spla_move %s %s' % (sum_all_spla, sum_all_lhsa)) 
            return (sum_all_spla, sum_all_lhsa, '')
         
             
        for spla_id, week_list in actions_spla.items():
            solution_list_spla.append(spla_id)
            cur_move = spla_id
            [x, new_parking_lot] = HomelessAgent.reduce_slot_count(week_list, parking_space_left)
            new_spla_list_dict = deepcopy(spla_list_dict)
            new_lhsa_list_dict = deepcopy(lhsa_list_dict)
            if spla_id in new_lhsa_list_dict:
                del new_lhsa_list_dict[spla_id]
            del new_spla_list_dict[spla_id]
        
            copy_spla_max = deepcopy(spla_max)
            copy_lhsa_max = deepcopy(lhsa_max)
            (temp_spla_max, temp_lhsa_max, next_move) = HomelessAgent.max_lhsa_solution(new_spla_list_dict, new_lhsa_list_dict, new_parking_lot, beds_space_left, solution_list_spla, solution_list_lhsa, copy_spla_max, copy_lhsa_max)

            print('spla comparing itself spla %s %s' % (temp_lhsa_max, lhsa_max))
            if temp_spla_max > spla_max:
                if temp_spla_max == spla_max and cur_best_move < spla_id:
                    cur_best_move = cur_best_move
                else:
                    cur_best_move = spla_id
                spla_max = temp_spla_max
                lhsa_max = temp_lhsa_max
                cur_next_move = next_move
            solution_list_spla.pop() 
           
        return (spla_max, lhsa_max, cur_next_move)


    @staticmethod
    def max_lhsa_solution(spla_list_dict, lhsa_list_dict, parking_space_left, beds_space_left, solution_list_spla, solution_list_lhsa, spla_max, lhsa_max):
        """
        #main terminating conditions):
        """
    
        global new_solution
        global spla_dict
        global lhsa_dict
        actions_lhsa = HomelessAgent.available_actions(lhsa_list_dict, beds_space_left)
        cur_next_move = ''
        if len(lhsa_list_dict) == 0 or len(actions_lhsa) == 0:
           #what to do for the termination 
            sum_all_spla = 0
            sum_all_lhsa = 0
            for ids in solution_list_spla:
                sum_all_spla += sum(spla_dict[ids])
    
            for ids in solution_list_lhsa:
                sum_all_lhsa += sum(lhsa_dict[ids])
    
            #results[repr(solution_list)] = sum_all
            if len(spla_list_dict) != 0:
                HomelessAgent.wrapper(spla_list_dict.keys(), parking_space_left, [], 0, spla_dict)
                soln = new_solution[0]
                if (len(soln) != 0):
                    for ids in soln:
                        print(ids)
                        sum_all_spla += sum(spla_list_dict[ids])
    
            new_solution = []
            print('spla and lahsa value from lhsa_move' % (sum_all_spla, sum_all_lhsa)) 
            return (sum_all_spla, sum_all_lhsa, '')


    
        for lhsa_id, week_list in actions_lhsa.items():
            solution_list_lhsa.append(lhsa_id)
            new_lhsa_list_dict = deepcopy(lhsa_list_dict)
            [x,new_beds_space] = HomelessAgent.reduce_slot_count(week_list, beds_space_left)
            del new_lhsa_list_dict[lhsa_id]
            new_spla_list_dict = deepcopy(spla_list_dict)
            if lhsa_id in new_spla_list_dict:
                del new_spla_list_dict[lhsa_id]
            copy_spla_max = deepcopy(spla_max)
            copy_lhsa_max = deepcopy(lhsa_max)
            (temp_spla_max, temp_lhsa_max, next_move) = HomelessAgent.max_spla_solution(new_spla_list_dict, new_lhsa_list_dict, parking_space_left, new_beds_space, solution_list_spla, solution_list_lhsa, copy_spla_max, copy_lhsa_max)

            print('Lhsa comparing itself spla %s %s and available lhsa moves %s' % (temp_lhsa_max, lhsa_max, new_lhsa_list_dict))
            if temp_lhsa_max > lhsa_max:
                lhsa_max = temp_lhsa_max
                cur_next_move = next_move
                spla_max = temp_spla_max
            solution_list_lhsa.pop()
            
        return (spla_max, lhsa_max, cur_next_move)


       #####################################################################################################################################
    @staticmethod
    def find_best_move_spla():
        """
            move the best possible moves
        """
        cur_best_move = ''
        if HomelessAgent.parking_slot >= len(HomelessAgent.valid_both_applicants) + len(HomelessAgent.spla_available_applicant):
            return HomelessAgent.return_best_sumUtil(HomelessAgent.valid_both_applicants, HomelessAgent.spla_available_applicant, HomelessAgent.parking_slot_left)

        elif HomelessAgent.is_parking_slot_sufficient():
            return HomelessAgent.return_best_sumUtil(HomelessAgent.valid_both_applicants, HomelessAgent.spla_available_applicant, HomelessAgent.parking_slot_left)

        elif len(HomelessAgent.valid_both_applicants) == 0:
            return HomelessAgent.return_best_sum(HomelessAgent.spla_available_applicant, HomelessAgent.parking_slot_left)
        elif len(HomelessAgent.valid_both_applicants) == 1:
            return HomelessAgent.generate_optimal_subsetUtil(HomelessAgent.valid_both_applicants, HomelessAgent.spla_available_applicant)

        else:
            #generate all subset of the spla
            print('Came here')
            spla_list_dict = dict(HomelessAgent.valid_both_applicants.items() + HomelessAgent.spla_available_applicant.items())
            lhsa_list_dict = dict(HomelessAgent.valid_both_applicants.items() + HomelessAgent.lhsa_available_applicant.items())
            solution_list_spla = []
            solution_list_lhsa = []
            spla_max = -sys.maxsize
            beds_space_left = HomelessAgent.beds_left
            for spla_id, week_list in spla_list_dict.items():
                solution_list_spla.append(spla_id)
                cur_move = spla_id
                print('Picking the element %s' % spla_id)
                [x, new_parking_lot] = HomelessAgent.reduce_slot_count(week_list, HomelessAgent.parking_slot_left)
                new_spla_list_dict = deepcopy(spla_list_dict)
                new_lhsa_list_dict = deepcopy(lhsa_list_dict)
                if spla_id in new_lhsa_list_dict:
                    del new_lhsa_list_dict[spla_id]
                del new_spla_list_dict[spla_id]
                (temp_spla_max, temp_lhsa_max, next_move) = HomelessAgent.max_lhsa_solution(new_spla_list_dict, new_lhsa_list_dict, new_parking_lot, beds_space_left, solution_list_spla, solution_list_lhsa, -sys.maxsize, -sys.maxsize)
                print('Value being checked at each point %s %s | %s' % (spla_id, temp_spla_max,spla_max))
                if temp_spla_max > spla_max:
                    cur_best_move = spla_id
                    spla_max = temp_spla_max
                solution_list_spla.pop() 

            return cur_best_move
                
            
    @staticmethod
    def process_applicant(line):
        """
            process_applicant and add to appropriate list
        """
        applicant_info = {}
        applicant_info['appl_id'] = line[0:5]
        applicant_info['gender'] = line[5]
        applicant_info['age'] = int(line[6:9])
        applicant_info['pets'] = line[9]
        applicant_info['medical_cond'] = line[10]
        applicant_info['car'] = line[11]
        applicant_info['dl'] = line[12]
        applicant_info['week_allocated'] = map(lambda x : int(x), line[13:20])

        return applicant_info

    @staticmethod
    def find_valid_category(applicant_info):
        """
            find the catefory to which applicant belongs
        """
        valid_lhsa = 0
        valid_spla = 0
        if applicant_info['car'] == 'Y' and applicant_info['dl'] == 'Y' and \
           applicant_info['medical_cond'] == 'N':
           valid_spla = 1

        if applicant_info['gender'] == 'F' and applicant_info['age'] > 17 and \
           applicant_info['pets'] == 'N':
           valid_lhsa = 1

        return [valid_spla, valid_lhsa]

    @staticmethod
    def reduce_slot_count(week_list, reduction_list):
        """
            reduce the slot after the occupiant adoption
        """
        status = 1
        new_reduction_list = deepcopy(reduction_list)
        for i in range(0, 7):
            new_reduction_list[i] = new_reduction_list[i] - week_list[i]
            if new_reduction_list[i] < 0:
                status = 0
                new_reduction_list[i] = 0

        
        return [status, new_reduction_list]


    def __str__(self):
        """
            print object
        """
        return str(self.applicant_info)
        
    def __repr__(self):

        return str(self.applicant_info)



def handler(SIGNUM, frame):
    out_handl = open('output.txt', 'w')
    value = HomelessAgent.return_best_sumUtil(HomelessAgent.valid_both_applicants, HomelessAgent.spla_available_applicant, HomelessAgent.parking_slot_left)
    out_handl.write(value)
    out_handl.close()
    sys.exit(0)
    
if __name__ == "__main__":

    file_handl =  open('input.txt', 'r')
    input_lines = map(lambda x: x.strip(), file_handl.readlines())
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(177)
    HomelessAgent.beds_slot = int(input_lines[0])
    HomelessAgent.beds_left = [int(input_lines[0])] * 7
    HomelessAgent.parking_slot = int(input_lines[1])
    HomelessAgent.parking_slot_left = [int(input_lines[1])] * 7
    num_of_lhsa = int(input_lines[2])
    #local varaibles for lhsa_id and spla_id

    for line in input_lines[3:3 + num_of_lhsa]:
        HomelessAgent.lhsa_id_list.append(line)

    cur_in = 3 + num_of_lhsa
    num_of_spla = int(input_lines[cur_in])
    cur_in = cur_in + 1
    for lines in input_lines[cur_in:cur_in+num_of_spla]:
        HomelessAgent.spla_id_list.append(lines)

    cur_in = cur_in + num_of_spla
    num_of_appl = int(input_lines[cur_in])
    cur_in = cur_in + 1
    for lines in input_lines[cur_in:cur_in+num_of_appl]:
        HomelessAgent(line=lines)

    spla_dict = dict(HomelessAgent.valid_both_applicants.items() + HomelessAgent.spla_available_applicant.items())
    lhsa_dict = dict(HomelessAgent.valid_both_applicants.items() + HomelessAgent.lhsa_available_applicant.items())
    value = HomelessAgent.find_best_move_spla()


    out_handl = open('output.txt', 'w')
    out_handl.write(value)
    out_handl.close()

