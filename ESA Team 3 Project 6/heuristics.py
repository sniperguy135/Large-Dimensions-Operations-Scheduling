import sys, os, re
import multiprocessing
from multiprocessing import Process
from functools import reduce
from copy import deepcopy
import more_itertools

"""
heuristics.py -- Operations scheduling module
Solution Generation System

Methods to call:
heuristics_main(job_dictionary: dict, capacity_dictionary:dict)
where both are outputs from data_input.data_input_main()

--------------

What the code does:

magic
i'm sorry
please read through the inline documentation


Output: 
List of dictionaries, each dictionary
    keys: Operation name, Start time, End time, Machine

    
---------------------------
    
Things to sort out:
- any data validations? << only after heuristics complete

"""

def heuristics_main(job_dictionary: dict, capacity_dictionary:dict):
    # take the things
    # then do something
    # sort the dictionary by the keys
    # Python version >3.7
    job_dictionary = dict(sorted(job_dictionary.items()))

    # The way that multiprocessing processes return things is by setting up a "global dictionary"
    # then each function "returns" their output by 
    heuristics_manager = multiprocessing.Manager()
    heuristics_return_dict = heuristics_manager.dict()

    # setup the heuristics as their own processes so they can be run in parallel
    heur_NEH_proc = Process(target=heuristic_NEH_identifier, args=(job_dictionary, heuristics_return_dict))
    heur_LETSA_proc = Process(target=heuristic_LETSA, args=(job_dictionary, capacity_dictionary, heuristics_return_dict))
    heur_LPT_proc = Process(target=heuristic_LPT, args=(job_dictionary, capacity_dictionary, heuristics_return_dict))
    heur_dom_proc = Process(target=heuristic_dominance, args=(job_dictionary, capacity_dictionary, heuristics_return_dict))

    # Run the heuristics in parallel
    heur_NEH_proc.start()
    heur_LETSA_proc.start()
    heur_LPT_proc.start()
    heur_dom_proc.start()

    # wait for all to be completed
    heur_NEH_proc.join()
    heur_LETSA_proc.join()
    heur_LPT_proc.join()
    heur_dom_proc.join()

    # interpret the final results
    # note that NEH may not run if the assumptions for NEH are not met
    # can give string that is either "DNS - Backtracking" or "DNS - Ordering"
    if isinstance(heuristics_return_dict['NEH'], str) or heuristics_return_dict['NEH'] == None:
        main_NEH_norun = heuristics_return_dict.pop('NEH') # store in a variable if want to refer

    best_solution, best_makespan = "", float('inf') # set best makespan as bad value
    for heur_name, heur_soln in heuristics_return_dict.items(): # this runs 4 times, 3 if NEH is not valid
        if heur_soln == None:
            continue
        # find the makespan for the particular heuristic
        # max('end time') - min('start time')
        makespan = max([oper_dict['end time'] for oper_dict in heur_soln]) - min([oper_dict['start time'] for oper_dict in heur_soln])

        # FOR TEST DATA RESULT PRODUCTION
        with open(f"heuristic {heur_name} schedule.txt", "w") as output:
            output.write(str(heur_soln))
        
        if makespan < best_makespan: # if heuristic gives good solution, store
            best_solution, best_makespan = heur_name, makespan

    if best_solution == "":
        raise Exception("Error with code: Notify the team of this error - heuristics not pointed")
    # return the best result at the end 
    return heuristics_return_dict[best_solution]


#
# Heuristics
#

""" 
NEH and helper functions 
"""

def heuristic_NEH_identifier(neh_idnt_job_dictionary: dict, NEH_return_dict):
    # to verify if all jobs follow a specific machine order
    # does not matter if it is 1->2->3 or 2->3->1 as long as they follow the same order for all
    # and does not matter if it skips (so 1->3 or 2->1 respectively)
    # [x for x in re.split('(\d+)',num_and_part) if x != '']

    # take the first of each operation, eg B.10-1, B.20-1, etc
    # condense to part name eg "B"
    # then put into a new dictionary, key part name value machine order list
    neh_idnt_uniq_part_dict = {}
    for neh_idnt_oper_name in [x for x in sorted(list(neh_idnt_job_dictionary.keys())) if x.split("-")[-1] == "1"]:
        # neh_idnt_oper_name_mod = "".join(neh_idnt_oper_name.split("-")[:-1])
        neh_idnt_part_name = [x for x in re.split('(\d+)',neh_idnt_oper_name) if x != ''][0]
        if neh_idnt_uniq_part_dict.get(neh_idnt_part_name, None) == None:
            neh_idnt_uniq_part_dict[neh_idnt_part_name] = [neh_idnt_job_dictionary[neh_idnt_oper_name]['Machine']]
        else:
            if neh_idnt_uniq_part_dict[neh_idnt_part_name][-1] != neh_idnt_job_dictionary[neh_idnt_oper_name]['Machine']:
                neh_idnt_uniq_part_dict[neh_idnt_part_name].append(neh_idnt_job_dictionary[neh_idnt_oper_name]['Machine'])
    # print(neh_idnt_uniq_part_dict)

    # no machine backtrack and all same order check
    for neh_idnt_mach_order in neh_idnt_uniq_part_dict.values():
        if len(neh_idnt_mach_order) != len(set(neh_idnt_mach_order)): # no machine backtrack
            NEH_return_dict['NEH'] = "DNS - Backtracking"
            print("NEH did not run due to machine backtracking")
            return
        # start checks for same order
        elif len(neh_idnt_mach_order) == 1:
            continue
        # check the common elements, and if they do not agree in order then can dismiss
        # VERY COMPUTATIONALLY STUPID
        for neh_idnt_mach_order_sub in neh_idnt_uniq_part_dict.values():
            neh_idnt_agree_a = [x for x in neh_idnt_mach_order if x in neh_idnt_mach_order_sub]
            neh_idnt_agree_b = [x for x in neh_idnt_mach_order_sub if x in neh_idnt_mach_order]
            if len(neh_idnt_agree_a) <= 1: #if no jobs agree or only 1 agree
                continue
            elif neh_idnt_agree_a != neh_idnt_agree_b: #if they have 2 or more common jobs, and the order disagree
                NEH_return_dict['NEH'] = "DNS - Ordering"
                print("NEH did not run due to ordering conflicts")
                return

    # if the verification is successful, call the actual NEH heuristic, and return the result to the main function
    # else, return something that can help to identify that the heuristic PURPOSELY did not run

    NEH_return_dict['NEH'] = heuristic_NEH(neh_idnt_job_dictionary)
    return


def heuristic_NEH(neh_job_dictionary: dict):
    
    # find all parts in the job dictionary
    # NEH_jobs_ls = [([j for j in re.split('(\d+)',x) if j != ''][0], [j for j in re.split('(\d+)',x) if j != ''][-1]) for x in NEH_job_dictionary.keys() if [j for j in re.split('(\d+)',x) if j != ''][1] == "10"]
    NEH_jobs_operations_dict = dict()
    for NEH_operation in neh_job_dictionary.keys():
        NEH_operation_name_breakdown = [j for j in re.split('(\d+)',NEH_operation) if j != '']
        if NEH_jobs_operations_dict.get((NEH_operation_name_breakdown[0],NEH_operation_name_breakdown[-1]), None) == None:
            NEH_jobs_operations_dict[(NEH_operation_name_breakdown[0],NEH_operation_name_breakdown[-1])] = [{**{"Operation": NEH_operation},**neh_job_dictionary[NEH_operation]}]
        else:
            NEH_jobs_operations_dict[(NEH_operation_name_breakdown[0],NEH_operation_name_breakdown[-1])].append({**{"Operation": NEH_operation},**neh_job_dictionary[NEH_operation]})
            
    NEH_jobs_operations_dict = dict(sorted(NEH_jobs_operations_dict.items(), key=lambda x: -sum([j['Process time'] for j in x[1]])))
    # NEH_jobs_operations_dict IS SORTED BY DECREASING TOTAL PROCESS TIME!!!
    NEH_unique_part_list = []
    NEH_unique_operation_dict = {}
    for neh_k in NEH_jobs_operations_dict.keys():
        NEH_unique_part_list.append(neh_k) if neh_k not in NEH_unique_part_list and neh_k[1] == "1" else None
        if NEH_unique_operation_dict.get(neh_k, None) == None and neh_k[1] == "1":
            NEH_unique_operation_dict[neh_k] = NEH_jobs_operations_dict[neh_k]

    # NEH_proc_time_sanity_check = dict([(k,sum([j['Process time'] for j in v])) for k, v in NEH_jobs_operations_dict.items()])
    # print("NEH_jobs_operations_dict: ", NEH_jobs_operations_dict.keys())
    # print([k[0] for k in NEH_jobs_operations_dict.keys()])
    # print(NEH_proc_time_sanity_check)
    # print("NEH_unique_part_list: ", NEH_unique_part_list)
    # print("NEH_unique_operation_dict: ", NEH_unique_operation_dict)
    # quit()

    # since we are repeating jobs, only the letter number sequence matters
    # regardless of how many number of jobs each letter number has
    # so we only need to check which letter number comes before or after which letter number
    # in improved NEH, we only need to check if in front, or behind
    # should create a helper function to check which has lowest makespan
    NEH_remain_part_list = deepcopy(NEH_unique_part_list)
    NEH_current_sequence = [NEH_remain_part_list.pop(0)]

    while len(NEH_remain_part_list) > 0: # means there are jobs remaining, also works when only 1 unique part
        neh_next_longest = NEH_remain_part_list.pop(0)
        NEH_current_sequence = NEH_order_check_helper(NEH_current_sequence, neh_next_longest,NEH_unique_operation_dict)

    # after best sequence found, scheduling
    NEH_final_seq_ls = []
    for neh_oper_tuple in NEH_current_sequence:
        for neh_find_part_num in NEH_jobs_operations_dict.keys():
            NEH_final_seq_ls.append(neh_find_part_num) if neh_oper_tuple[0] == neh_find_part_num[0] else None
            # possible to make faster by doing a state machine
    
    # print(set(NEH_final_seq_ls) == set(NEH_jobs_operations_dict.keys()))
    # quit()

    NEH_operation_schedule, NEH_final_makespan = NEH_scheduler_helper(NEH_final_seq_ls, NEH_jobs_operations_dict)
    # print(NEH_operation_schedule)
    # print(NEH_final_makespan)
    return NEH_operation_schedule # NEH is different because its called by heuristic_NEH_identifier
    # heuristic_NEH_identifier will store it into the return_dict


def NEH_order_check_helper(NEH_helper_current_seq:list, NEH_helper_next_part:tuple, NEH_unique_jobs_operations_dict: dict):
    NEH_helper_nextbefore_seq = [NEH_helper_next_part] + NEH_helper_current_seq
    NEH_helper_nextafter_seq = NEH_helper_current_seq + [NEH_helper_next_part]
    NEH_helper_new_current_seq = NEH_helper_nextbefore_seq if NEH_scheduler_helper(NEH_helper_nextbefore_seq,NEH_unique_jobs_operations_dict)[1] < NEH_scheduler_helper(NEH_helper_nextafter_seq,NEH_unique_jobs_operations_dict)[1] else NEH_helper_nextafter_seq
    return NEH_helper_new_current_seq


def NEH_scheduler_helper(NEH_sched_helper_ordered_list:list, NEH_sched_helper_job_dictionary: dict):
    NEH_sched_helper_relevant_machines = []
    for sched_help_ls_of_dicts in NEH_sched_helper_job_dictionary.values():
        for sched_help_oper_dict in sched_help_ls_of_dicts:
            NEH_sched_helper_relevant_machines.append(sched_help_oper_dict['Machine']) if sched_help_oper_dict['Machine'] not in NEH_sched_helper_relevant_machines else None
    NEH_sched_helper_machine_current_time = dict([(m, 0.0) for m in sorted(NEH_sched_helper_relevant_machines)])
    # go through NEH_sched_helper_ordered_list
    # take the set of operations with that part name, schedule and assign times
    # refer to NEH_machine_current_time for last known time, then remember to update the time as well
    # if there was a preceding operation (C.30 has C.20 has C.10), need to hold the time from the precedence job
    # since each neh_sched_part_list_of_oper_dict is in 10 20 30 ... order, set before job end time
    # take the max between before job end time and machine current time
    NEH_schedule_helper_sched = []
    for neh_sched_part_and_num in NEH_sched_helper_ordered_list:
        neh_sched_part_list_of_oper_dict = NEH_sched_helper_job_dictionary[neh_sched_part_and_num]
        neh_preceding_job_end_time = 0.0
        for neh_sched_oper_dict in neh_sched_part_list_of_oper_dict:
            neh_sched_oper_earliest_start = max(NEH_sched_helper_machine_current_time[neh_sched_oper_dict['Machine']], neh_preceding_job_end_time)
            NEH_schedule_helper_sched.append({'operation name': neh_sched_oper_dict['Operation'], 'start time': neh_sched_oper_earliest_start, 'end time': neh_sched_oper_earliest_start + neh_sched_oper_dict['Process time'], 'machine': neh_sched_oper_dict['Machine']})
            neh_preceding_job_end_time = neh_sched_oper_earliest_start + neh_sched_oper_dict['Process time']
            NEH_sched_helper_machine_current_time[neh_sched_oper_dict['Machine']] += neh_sched_oper_dict['Process time']

    neh_helper_makespan = max(NEH_sched_helper_machine_current_time.values())
    # to give out: the schedule list, and the makespan
    # schedule list format: [ {'operation name': string, 'start time': float, 'end time': float, 'machine': string}, {<another operation>} ,... ]
    return NEH_schedule_helper_sched, neh_helper_makespan


""" 
LPT and helper functions 
"""

def heuristic_LPT(LPT_job_dictionary: dict, LPT_capacity_dictionary: dict, LPT_return_dict):
    # i m ignoring the capacity
    None
    # Setup:
    # 0: find the machines needed for all the relevant jobs
    LPT_relevant_machines = list(set([x['Machine'] for x in LPT_job_dictionary.values()]))
    # if only 1 relevant machine: check for precedence constraints and adjust, then skip all further steps
    LPT_only1mc_bool = True if len(LPT_relevant_machines) == 1 else False

    # if 2 or more relevant machines: still check for precedence constraints for first machine
    # BUT we sort the machines by the number of first operations (total how many A.10s B.10s C.10s etc)
    # we consider the machines in the order of decreasing number of first operations
    # LPT_mc_num_of_10s gives the machine names sorted in decreasing order of number of '10' operations
    # so that can work on the machines that have the most prereq jobs first
    if not LPT_only1mc_bool:
        LPT_mc_by_num_of_10s = dict([(machine,0) for machine in LPT_relevant_machines])
        for LPT_mc_name in LPT_relevant_machines:
            LPT_mc_by_num_of_10s[LPT_mc_name] = len([x for x in LPT_job_dictionary.keys() if [j for j in re.split('(\d+)',x) if j != ''][1] == "10" and LPT_job_dictionary[x]['Machine'] == LPT_mc_name])
        LPT_mc_by_num_of_10s = [j[0] for j in sorted(LPT_mc_by_num_of_10s.items(), key=lambda x: -x[1])]
    else:
        LPT_mc_by_num_of_10s = LPT_relevant_machines

    # 1. Find number of times to do each part
    # 2. Find the part network: So like eg B.10 mc 1, B.20 mc 1, B.30 mc 2, B.40 mc 1
    #   Then in the network dict, {"B.": {10: "1", 20: "1", 30: "2", ...}} with the sub dict values being the machine number/name
    # 3. Assign the jobs into their respective machines (LPT_operation_by_machines)
    #   Use LPT_mc_num_of_10s to create the keys in order of decreasing number of 10s operations
    # Useful for later
    LPT_part_times_dict, LPT_oper_network, LPT_operation_by_machines = {}, {}, dict([(machine,[]) for machine in LPT_mc_by_num_of_10s])
    for LPT_setup_oper_name in LPT_job_dictionary.keys():
        LPT_setup_oper_name_breakdown = [x for x in re.split('(\d+)',LPT_setup_oper_name) if x != '']

        # 3. flatten the dictionary for easier handling
        # so each dictionary value will be a list of dictionaries
        # each dictionary will be {"Operation": "name", "Process time": float, "Machine": "mc name"}
        LPT_operation_by_machines[LPT_job_dictionary[LPT_setup_oper_name]['Machine']].append({**{"Operation": LPT_setup_oper_name},**LPT_job_dictionary[LPT_setup_oper_name]})

        # 1
        if LPT_part_times_dict.get(LPT_setup_oper_name_breakdown[0], None) == None:
            LPT_part_times_dict[LPT_setup_oper_name_breakdown[0]] = max([int([j for j in re.split('(\d+)',x) if j != ''][-1]) for x in LPT_job_dictionary.keys() if [j for j in re.split('(\d+)',x) if j != ''][0] == LPT_setup_oper_name_breakdown[0]])
        # 2
        if LPT_oper_network.get(LPT_setup_oper_name_breakdown[0], None) == None:
            # get the oper numbers for the part
            # then put into the parts sub dictionary
            LPT_oper_network[LPT_setup_oper_name_breakdown[0]] = {}
            LPT_setup_oper_nums = [int([j for j in re.split('(\d+)',x) if j != ''][1]) for x in LPT_job_dictionary.keys() if [j for j in re.split('(\d+)',x) if j != ''][0] == LPT_setup_oper_name_breakdown[0] and [j for j in re.split('(\d+)',x) if j != ''][-1] == "1"]
            for LPT_setup_oper_num in LPT_setup_oper_nums:
                LPT_oper_network[LPT_setup_oper_name_breakdown[0]][LPT_setup_oper_num] = LPT_job_dictionary[f"{LPT_setup_oper_name_breakdown[0]}{LPT_setup_oper_num}-1"]['Machine']

    # By now, the values of the dictionary LPT_operation_by_machines should be lists of dictionaries
    # 2 more more relevant machines: take second machine, check for precedence constraints within second machine
    # then check precedence constraints with previous machines
    # if the first job of the queue comes before that of the prev machines, give negative timing
    # after scheduled with gaps or not, then make sure that the timings are added by the most negative time
    # after complete, add to list of machines that have been checked
    

    # consider first (and maybe only) machine with most precedent items
    # create a dictionary to hold the schedules by machine name
    
    LPT_schedule_by_mc = dict([(x,[]) for x in LPT_operation_by_machines.keys()])

    for LPT_mc_name in LPT_schedule_by_mc.keys():
        # only schedule the first machine by LPT
        if not LPT_dict_val_list_not_empty([len(x) for x in LPT_schedule_by_mc.values()]): # no other machines scheduled        

            LPT_mc_operset = [x['Operation'] for x in LPT_operation_by_machines[LPT_mc_name] if [x for x in re.split('(\d+)',x['Operation']) if x != ''][-1] == "1"]
            LPT_mc_parts = list(set([[x for x in re.split('(\d+)',x['Operation']) if x != ''][0] for x in LPT_operation_by_machines[LPT_mc_name] if [x for x in re.split('(\d+)',x['Operation']) if x != ''][-1] == "1"]))
            LPT_mc_oper_by_part = dict([(part_name,[]) for part_name in LPT_mc_parts])
            for LPT_uniq_oper in LPT_mc_operset:
                LPT_mc_oper_by_part[[x for x in re.split('(\d+)',LPT_uniq_oper) if x != ''][0]].append(int([x for x in re.split('(\d+)',LPT_uniq_oper) if x != ''][1]))
            for LPT_mc_part in LPT_mc_oper_by_part.keys():
                LPT_mc_oper_by_part[LPT_mc_part] = list(more_itertools.split_when(LPT_mc_oper_by_part[LPT_mc_part], lambda x,y: y-x != 10))

            LPT_mc_Queue_dict = dict([(key,[]) for key in LPT_mc_oper_by_part.keys()])
            for part_letter in LPT_mc_Queue_dict.keys():
                part_job_ls = []
                for subls in LPT_mc_oper_by_part[part_letter]:
                    # eg first iter = [10,20] 
                    # second iter = [40]
                    # i want [{},{}], [{},{}] for first iter
                    # then [{}], [{}] for second iter
                    # first create the list
                    # find the number of the part to do
                    # then for every part number we add the part-operation number-times for every times
                    for times in range(1,LPT_part_times_dict[part_letter]+1):
                        times_holding_ls = []
                        for oper_num in subls:
                            times_holding_ls.append({**{'Operation':f"{part_letter}{oper_num}-{times}"},**LPT_job_dictionary[f"{part_letter}{oper_num}-{times}"]})
                        part_job_ls.append(times_holding_ls)
                    
                    # number_of_times = max([x for x in ])
                LPT_mc_Queue_dict[part_letter] = part_job_ls
            
            # LPT queue dict values are lists of lists of dictionaries
            # to schedule by LPT, consider all the first list in queue for each of the parts
            # so that all the consecutive operations are sequenced
            # this is the start of the sequencing
            LPT_mc_schedule_ls, LPT_mc_schedule_timenow = [], 0.0
            while LPT_dict_val_list_not_empty([len(x) for x in LPT_mc_Queue_dict.values()]):
                # find the longest (combined) processing time to be scheduled
                LPT_queue_consider_proctime = dict([(consider_part_name, sum([oper_dict['Process time'] for oper_dict in LPT_mc_Queue_dict[consider_part_name][0]])) for consider_part_name in LPT_mc_parts if LPT_mc_Queue_dict[consider_part_name] != []])
                LPT_queue_consider_lpt_oper_dict_list = LPT_mc_Queue_dict[max(LPT_queue_consider_proctime, key=LPT_queue_consider_proctime.get)].pop(0)
                for oper_dict in LPT_queue_consider_lpt_oper_dict_list:
                    LPT_mc_schedule_ls.append({'operation name': oper_dict['Operation'], 'start time': LPT_mc_schedule_timenow, 'end time': LPT_mc_schedule_timenow+oper_dict['Process time'], 'machine': oper_dict['Machine']})
                    LPT_mc_schedule_timenow+=oper_dict['Process time']

            if LPT_only1mc_bool:
                LPT_return_dict['LPT'] = LPT_mc_schedule_ls
                return
        else: # if any other machine has been scheduled
            # get the jobs on the machine
            # then sort into 3 categories, with successors, with predecessors (eg non 10s), and other (10s with no downstream)
            for operation in []:
                pass
            # for jobs with successors, schedule from back to start: whichever successor is the latest
            # for jobs with predecessors, schedule from front to back: whicever predecessor is the earliest
            # for other jobs, slot in whenever earliest possible

            pass 

        # at the end after checking, add to schedule dictionary
        LPT_schedule_by_mc[LPT_mc_name] = LPT_mc_schedule_ls
        break
    

    # print("LPT_mc_name: ", LPT_mc_name)
    # print("LPT_mc_operset: ", LPT_mc_operset)
    # print("LPT_mc_parts: ", LPT_mc_parts)
    # print("LPT_mc_oper_by_part: ", LPT_mc_oper_by_part)
    # print("LPT_mc_Queue_dict: ", LPT_mc_Queue_dict)
    # print("LPT_mc_schedule_ls: ", LPT_mc_schedule_ls) # gives for the last machine
    quit()
    

    # check for negative times and add by most negative time to all timings
    LPT_combined_sched = reduce(lambda x,y: x+y, LPT_schedule_by_mc.values())
    min_start_time = min([x['start time'] for x in LPT_combined_sched])
    if min_start_time < 0:
        shortfall = 0.0-min_start_time
        for oper_dict in LPT_combined_sched:
            oper_dict['start time'] += shortfall

    # To give the schedule back to the main process
    LPT_return_dict['LPT'] = reduce(lambda x,y: x+y, LPT_schedule_by_mc.values())
    return # this is just to mark the end of the function    


def LPT_dict_val_list_not_empty(lenlist: list):
    return True if [x for x in lenlist if x!=0] else False


""" 
LETSA and helper functions 
"""

def heuristic_LETSA(LETSA_job_dict: dict, LETSA_capacity_dict:dict, LETSA_return_dict):
    LETSA_schedule = []
    # create dictionary with available machines as keys
    avail_machines_key = list(LETSA_capacity_dict.keys())
    avail_machines = dict.fromkeys(avail_machines_key, 0)

    # 1. Make F
    LETSA_job_list = list(LETSA_job_dict.keys()) # list with remaining jobs to sort
    LETSA_job_paths = [] # list with nested lists of network paths
    F = {} # dictionary with final operations: total processing time

    for operation in LETSA_job_list:
        # obtain operation as split list
        current_operation_split = [x for x in re.split('(\d+)',operation) if x != '']

        if 'old_operation_split' not in locals():
            pass
        else:
            if current_operation_split[0] != old_operation_split[0]:
                for no_times_to_make in range(1, int(old_operation_split[3])+1):
                    F["".join(old_operation_split[0:3]) + str(no_times_to_make)] = 0

        old_operation_split = current_operation_split
    
    # 2. For each i in F, find all possible network paths and their total processing times
    F_keys = sorted(F.keys())
    F = {i:F[i] for i in F_keys}
    for final_operations in F:
        jobs_same_part_times = []
        # go through all operations and add to list if same part and times to make
        for operation in LETSA_job_list:
            all_operations_split = [x for x in re.split('(\d+)',operation) if x != '']
            final_operations_split = [x for x in re.split('(\d+)',final_operations) if x != '']

            if all_operations_split[0]==final_operations_split[0] and all_operations_split[3]==final_operations_split[3]:
                jobs_same_part_times.append(operation)
        # app respective final operation to list
        LETSA_job_paths.append(jobs_same_part_times)
        # calculate total processing time
        tpt = 0
        for operation in jobs_same_part_times:
            tpt += LETSA_job_dict[operation]['Process time']
        # store total processing time in dictionary
        F[final_operations] = tpt

    # create dictionary with maximum operation
    max_operation_no = {}
    for operation in F.keys():
        split = [x for x in re.split('(\d+)',operation) if x != '']
        max_operation_no[split[0]] = split[1]


    while len(F) != 0:
        # 3. Choose operation in F from critical path
        crit_path_tpt = max(F.values())
        # create variable for max key
        Jc = ""
        for key_final_op, value_tpt in F.items():
            if value_tpt == crit_path_tpt:
                Jc = key_final_op
                break
        
        # 4. Set Jc tentative completion time, Cc
        Jc_split = [x for x in re.split('(\d+)',Jc) if x != '']
        Cc = 0
        successors = []
        # if Jc has no successor, Cc = due date, 0
        if Jc_split[1] == max_operation_no[Jc_split[0]]:
            pass
        else:
            for a_network_path in LETSA_job_paths:
                if Jc in a_network_path:
                    for i in range(a_network_path.index(Jc)+1,len(a_network_path)):
                        Cc -= float(LETSA_job_dict[a_network_path[i]]['Process time'])
                        successors.append(a_network_path[i])

        # 5. Define starting time, Sc    
        Jc_machine = LETSA_job_dict[Jc]['Machine']

        Sc = 0
        if avail_machines[Jc_machine] == 0:
            Sc = Cc - LETSA_job_dict[Jc]['Process time']
        else:
            if len(successors) == 0:
                Sc = avail_machines[Jc_machine] - LETSA_job_dict[Jc]['Process time']
            else:
                actualCc = avail_machines[Jc_machine]
                for suc in successors:
                    for LETSA_schedule_dict in LETSA_schedule:
                        if LETSA_schedule_dict['operation name'] == suc:
                            actualCc = min(actualCc, LETSA_schedule_dict['start time'])
                Sc = actualCc - LETSA_job_dict[Jc]['Process time']
        avail_machines[Jc_machine] = Sc

        # 6. Schedule Jc on Sc
        new = {'operation name':Jc, 
            'start time':float(Sc), 
            'end time':float(Sc+LETSA_job_dict[Jc]['Process time']), 
            'machine':Jc_machine}
        LETSA_schedule.append(new)

        # 7. Remove Jc from F
        # get immediate predecessor
        for a_network_path in LETSA_job_paths:
            if Jc in a_network_path[1:]:
                predecessor = a_network_path[a_network_path.index(Jc)-1]
                # remove Jc and add predecessor
                F[predecessor] = F.get(Jc) - LETSA_job_dict[Jc]['Process time']
                break
        del F[Jc]          

    # 8. Adjust times to non-negative
    for LETSA_schedule_dict in LETSA_schedule:
        my_machine = LETSA_schedule_dict['machine']
        latest_start = -(avail_machines[my_machine])

        LETSA_schedule_dict['start time'] += latest_start
        LETSA_schedule_dict['end time'] += latest_start

    # 9. To give the schedule back to the main process
    LETSA_return_dict['LETSA'] = LETSA_schedule
    return # this is just to mark the end of the function
    

""" 
Dominance and helper functions 
"""

def heuristic_dominance(dominance_job_dictionary: dict, dominance_capacity_dictionary: dict, dominance_return_dict):
    # define final schedule (list with nested dictionaries)
    dominance_schedule = []

    """ Sort and Join Operations into Jobs """
    # obtain list of operations
    dominance_operation_list = list(dominance_job_dictionary.keys())
    # create new list to store sub-lists of each job
    dominance_jobs_list = []
    
    # organise each operation into jobs 
    for operation_name in dominance_operation_list:
        # split the operation name
        operation_name_split = [x for x in re.split('(\d+)',operation_name) if x != '']
        added_to_sublist = False

        for job_set in dominance_jobs_list:
            # if the same part and number of times found in a sub list
            if operation_name_split[0] in job_set and operation_name_split[3] in job_set:
                # add to that sub list
                job_set.append(operation_name)
                added_to_sublist = True
                # exist inner for loop (since already sorted)
                continue

        for job_set in dominance_jobs_list:
            # loop through individual operations in job_set
            for operation_name_sub in job_set:
                # split this individual operation name
                operation_name_sub_split = [x for x in re.split('(\d+)',operation_name_sub) if x != '']
                # if same part and number of times, add operation_name to this sub list
                if operation_name_split[0]==operation_name_sub_split[0] and operation_name_split[3]==operation_name_sub_split[3]:
                    job_set.append(operation_name)
                    added_to_sublist = True
                    # exit inner loop (since already sorted)
                    break
            
            if added_to_sublist == True:
                break
            
        # if operation did not get sorted
        if added_to_sublist == False:
            # create new sub_list
            dominance_jobs_list.append([operation_name])


    """ Create Job Shop Table """
    job_shop_table = {}

    # for each job
    for job in dominance_jobs_list:
        job_split = [x for x in re.split('(\d+)',job[0]) if x != '']
        # job_name = (e.g) 'A.2'
        job_name = job_split[0]+job_split[3]
        # create key:value pair of job_name:[(PT, Machine),...]
        job_shop_table[job_name] = []

        # for each operation in job
        for operation in job:
            # create tuple with (PT, Machine)
            information_tuple = (dominance_job_dictionary[operation]['Process time'], dominance_job_dictionary[operation]['Machine'])
            # add tuple to the empty list value information_tuple
            job_shop_table[job_name].append(information_tuple)


    """ Stage 0 Table """
    # format of stage_table_jobmachine:
    #stage_table_jobmachine = [
    #    [j1m1, j1m2, ...]
    #    [j2m1, j2m2, ...]
    #    ...
    #]

    # 1. Job and Machine Matrix
    stage_table_jobmachine = []

    # rows: number of jobs
    for row_job in range(len(job_shop_table)):
        row = []
        # columns: number of machines
        for col_machine in range(len(dominance_capacity_dictionary)):
            row.append(0)
        stage_table_jobmachine.append(row)


    # format of stage_table_machines:
    #stage_table_machines = {
    #    'machine1': {'release':value, 'idle':value}
    #    'machine2': {...}
    #    ...
    #}

    # 2. Machines Dictionary
    stage_table_machines = {}

    # for each machine
    for machine in list(dominance_capacity_dictionary.keys()):
        # key: machine name, value:{'release':0, 'idle':0}
        stage_table_machines[machine] = {'release':0, 'idle':0}
    

    # format of stage_table_jobs:
    #stage_table_jobs = {
    #    'job1':{'unscheduled': [machno_op1, machno_op2,...], 'TPT':value, 'WT':value, 'ST':value} 
    #    'job2':{...}
    #    ...
    #}


    # 3. Jobs Dictionary
    stage_table_jobs = {}
    
    # for each job
    for job in list(job_shop_table.keys()):
        # key:job name, value:{'unscheduled':0, 'TPT':0, 'WT':0, 'ST':0} (initialization)
        stage_table_jobs[job] = {'unscheduled':[], 'TPT':0, 'WT':0, 'ST':0}
        # for each operation of current job
        for operation_tuple in job_shop_table[job]:
            # append machine numbers (from first to last operation)
            stage_table_jobs[job]['unscheduled'].append(operation_tuple[1])
            # update total processing time
            stage_table_jobs[job]['TPT'] += operation_tuple[0]


    """ Stage K Table """
    # create dictionary to track what number of operations each job has scheduled
    tracking_operation_number = {}
    for job in list(stage_table_jobs.keys()):
        tracking_operation_number[job] = 0

    # calculate sum of all TPT
    AllTPT = 0
    for job in list(stage_table_jobs.keys()):
        AllTPT += stage_table_jobs[job]['TPT']

    while(AllTPT != 0):
        """ Update Variables """
        # 1. Starting Time
        ST_idx = 0
        # for each job
        for job in list(stage_table_jobs.keys()):
            # ST = ST + previous WT + previous PT
            stage_table_jobs[job]['ST'] += stage_table_jobs[job]['WT'] + sum(stage_table_jobmachine[ST_idx])
            ST_idx += 1

        # 2. Release Time
        RT_idx = 0
        # for each machine
        for machine in list(stage_table_machines.keys()): 
            machine_col_sum = 0
            # for each job
            for rows in range(len(stage_table_jobmachine)):
                # sum up PT under current machine
                machine_col_sum += stage_table_jobmachine[rows][RT_idx]
            # RT = RT + previous idle + previous PT
            stage_table_machines[machine]['release'] += stage_table_machines[machine]['idle'] + machine_col_sum
            RT_idx += 1

        # 3. Reset stage_table_jobmachine to 0s
        # rows: number of jobs
        for row_job in range(len(job_shop_table)):
            # columns: number of machines
            for col_machine in range(len(dominance_capacity_dictionary)):
                stage_table_jobmachine[row_job][col_machine] = 0


        """ Carry out Scheduling """
        # 1. Identify All Jobs Per Machine
        jobs_per_machine = {}
        # for each machine
        for machine in list(stage_table_machines.keys()):
            # key:machine, value:[] (initialization)
            # value will contain name of jobs scheduled for machine j at stage k
            jobs_per_machine[machine] = []

        # loop through each job's 1st operation's machine
        for job in list(stage_table_jobs.keys()):
            # if there are jobs remained to schedule
            if len(stage_table_jobs[job]['unscheduled']) != 0:
                # add job name (e.g. A.2) to machine value
                jobs_per_machine[stage_table_jobs[job]['unscheduled'][0]].append(job)
        

        # 2. Sequence by Conditions
        for machine in list(jobs_per_machine.keys()):
            # get machine's column number
            machine_index = list(dominance_capacity_dictionary.keys()).index(machine)

            # Case 1: Machine has no job scheduled
            if len(jobs_per_machine[machine]) == 0:
                # set idle time to 0
                stage_table_machines[machine]['idle'] = 0
                continue
            
            # Case 2: Machine has 1 job scheduled
            elif len(jobs_per_machine[machine]) == 1:
                # get job name
                job_to_schedule = jobs_per_machine[machine][0]
            
            # Case 3: Machine has more than 1 job scheduled
            elif len(jobs_per_machine[machine]) > 1:
                # Round 1: Schedule job with earliest starting time
                ST_comparison = []

                # loop through all jobs to obtain 'ST'
                for job in jobs_per_machine[machine]:
                    ST_comparison.append(stage_table_jobs[job]['ST'])
                
                # if all ST are unique
                if len(set(ST_comparison)) == len(jobs_per_machine[machine]):
                    # get maximum ST value
                    maximumST = max(ST_comparison)
                    # get job index (for jobs_per_machine list, equivalent to index of ST_comparison)
                    job_to_schedule_index_JPM = ST_comparison.index(maximumST)
                    # get job name
                    job_to_schedule = jobs_per_machine[machine][job_to_schedule_index_JPM]

                else:
                    # get list of tied jobs names
                    jobs_tied1 = []
                    # loop through ST_comparison
                    for idx in range(len(ST_comparison)):
                        # if job has tied maximum ST
                        if ST_comparison[idx] == max(ST_comparison):
                            # add to jobs_tied
                            jobs_tied1.append(jobs_per_machine[machine][idx])

                    # Round 2: Schedule job with largest TPT
                    TPT_comparison = []

                    # loop through all jobs to obtain 'TPT'
                    for contesting_jobs in jobs_tied1:
                        TPT_comparison.append(stage_table_jobs[contesting_jobs]['TPT'])
                    
                    # if all TPT are unique
                    if len(set(TPT_comparison)) == len(jobs_tied1):
                        # get maximum TPT value
                        maximumTPT = max(TPT_comparison)
                        # get job index (for jobs_tied list, equivalent to index of TPT_comparison)
                        job_to_schedule_index_JT = TPT_comparison.index(maximumTPT)
                        # get job name
                        job_to_schedule = jobs_tied1[job_to_schedule_index_JT]

                    else:
                        # get list of tied jobs' names
                        jobs_tied2 = []
                        for idx in range(len(TPT_comparison)):
                            if TPT_comparison[idx] == max(TPT_comparison):
                                jobs_tied2.append(jobs_tied1[idx])
                        
                        PT_comparison = []
                        
                        # Round 3: Shortest PT
                        # loop through job_shop_table to get individual PT
                        for job in jobs_tied2:
                            PT_comparison.append(job_shop_table[job][0][0])
                        
                        # if all PT unique
                        if len(set(PT_comparison)) == len(jobs_tied2):
                            # get maximum PT value
                            minimumPT = min(PT_comparison)
                            # get job's index (for jobs_tied, equivalent to index for PT_comparison)
                            job_to_schedule_index_JT = PT_comparison.index(minimumPT)
                            # get job's name
                            job_to_schedule = jobs_tied2[job_to_schedule_index_JT]
                        
                        else:
                            # Round 4: Arbitrary Choice
                            job_to_schedule = jobs_tied2[0]

            # get job_to_schedule's index (for job_shop_table)
            job_to_schedule_index = list(job_shop_table.keys()).index(job_to_schedule)
            # schedule chosen job's first operation to machine
            stage_table_jobmachine[job_to_schedule_index][machine_index] = job_shop_table[job_to_schedule][tracking_operation_number[job_to_schedule]][0]


            # 3. Update Schedule
            job_to_schedule_split = [x for x in re.split('(\d+)',job_to_schedule) if x != '']

            for job_operations in dominance_jobs_list:
                # split operation
                job_operation_split = [x for x in re.split('(\d+)',job_operations[0]) if x != '']

                # if operation matches job_to_schedule
                if job_operation_split[0]==job_to_schedule_split[0] and job_operation_split[3]==job_to_schedule_split[1]:
                    # get index of current operation scheduled
                    index = len(job_operations) - len(stage_table_jobs[job_to_schedule]['unscheduled'])
                    # get operation name
                    operation_name = job_operations[index]
                    break

            new = {'operation name': operation_name,
                   'start time': float(stage_table_jobs[job_to_schedule]['ST']),
                   'end time': float(stage_table_jobs[job_to_schedule]['ST'] + job_shop_table[job_to_schedule][tracking_operation_number[job_to_schedule]][0]),
                   'machine': machine, 
                   }
            dominance_schedule.append(new)


            """ Change Variables """
            # 1. Remove job from respective 'unscheduled'
            stage_table_jobs[job_to_schedule]['unscheduled'].pop(0) 

            # 2. Decrease job's TPT
            stage_table_jobs[job_to_schedule]['TPT'] -= job_shop_table[job_to_schedule][tracking_operation_number[job_to_schedule]][0]
            
            # 3. Add 1 to tracking_operation_number
            tracking_operation_number[job_to_schedule] += 1

            # 4. Adjust Idle Time
            # calculate starting time - release time
            possibility = stage_table_jobs[job_to_schedule]['ST'] - stage_table_machines[machine]['release']
            stage_table_machines[machine]['idle'] = max(possibility, 0)

        # 5. Adjust Waiting Times
        WT_outeridx = 0
        for job_row in stage_table_jobmachine:
            if sum(job_row) == 0:
                # identify job name
                job = list(job_shop_table.keys())[WT_outeridx]
                # set WT = 0
                stage_table_jobs[job]['WT'] = 0
            else:
                WT_inneridx = 0
                for value in job_row:
                    if value != 0:
                        # identify which column (i.e. machine) is non-zero
                        machine = list(dominance_capacity_dictionary.keys())[WT_inneridx]
                        # identify job name
                        job = list(job_shop_table.keys())[WT_outeridx]
                        # calculate release time - starting time
                        possibility = stage_table_machines[machine]['release'] - stage_table_jobs[job]['ST']
                        stage_table_jobs[job]['WT'] = max(0, possibility)
                        break
                    WT_inneridx += 1
            WT_outeridx += 1


        """ Re-calculate AllTPT """
        AllTPT = 0
        for job in list(stage_table_jobs.keys()):
            AllTPT += stage_table_jobs[job]['TPT']


    # To give the schedule back to the main process
    dominance_return_dict['Dominance'] = dominance_schedule
    return # this is just to mark the end of the function


""" 
Other functions 
"""

def heuristic_validator():
    # LOW PRIORITY
    # function for each heuristic to call
    # check that all operations scheduled
    # check that all process times not violated
    return 



if __name__ == "__main__":
    None
    holder_dict = {}
    import data_input
    file_dir_splitter = "\\" if sys.platform == "win32" else "/"
    cwd_prefix = os.getcwd() + file_dir_splitter + "TemplateFiles" + file_dir_splitter
    
    job_dict_eg, capacity_dict_eg = data_input.data_input_main(cwd_prefix+"bicycle-routing.csv", cwd_prefix+"bicycle-MRP.csv", cwd_prefix+"bicycle-capacity.csv", "R", "AA")
    # checking NEH identifier
    # heuristic_NEH_identifier(job_dict_eg, holder_dict)

    # heuristic_LPT(job_dict_eg, capacity_dict_eg, holder_dict)
    # heuristic_LETSA(job_dict_eg, capacity_dict_eg, holder_dict)
    # print(holder_dict)
    # print(max([x['end time'] for x in holder_dict['LETSA']]))

    # Test all
    heuristics_main(job_dict_eg,capacity_dict_eg)



# https://stackoverflow.com/questions/10415028/how-can-i-get-the-return-value-of-a-function-passed-to-multiprocessing-process



