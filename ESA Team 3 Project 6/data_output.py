import os, subprocess, sys, re
from multiprocessing import Process
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
from copy import deepcopy

"""
data_output.py -- Data input handling and interpreting module
Data output subsystem

Methods to call:
<update>

--------------

What the code does:

idk brother this is black magic

Output: Directory to the photo of the gantt chart


Things to sort out:
- what data to take in, how is it structured
- how to pass the data into my functions
- any data validations?
- filters/sorting

- display by (y axis)
    > machine/workcentre (saw, handtools, welder)
    > part (A, B, C), 
    > by operation (A.10-1, A.20-1, A.10-2, A.20-2, B.10-1, B.20-1), 
    > or operation grouped (A.10, A.20, B.10, B.20)?

"""

def data_output_main(main_ls_of_dicts: list, target_mc: str = None):
    if target_mc != None:
        try:
            if ',' in target_mc:
                target_mc_list = target_mc.split(',')
            else:
                target_mc_list = [target_mc]
            output_machine(main_ls_of_dicts, target_mc_ls= target_mc_list)
        except Exception as errExp:
            raise Exception("Invalid input", str(errExp))
    else:
        mc_charter_proc = Process(target=output_machine,  args=(main_ls_of_dicts,))
        job_charter_proc = Process(target=output_jobs,  args=(main_ls_of_dicts,))

        mc_charter_proc.start()
        job_charter_proc.start()
        
        mc_charter_proc.join()
        job_charter_proc.join()
    
    return 


def output_machine(scheduled_list_of_dict_mc: list, target_mc_ls: list = None):
    fig, gnt_mc = plt.subplots()
    # gnt_mc.grid(True)

    # List of unique machines
    machines_list = []
    for operation_dict in scheduled_list_of_dict_mc:
        if operation_dict['machine'] not in machines_list:
            machines_list.append(operation_dict['machine'])
    
    if target_mc_ls != None:
        assert [x for x in target_mc_ls if x in machines_list] == target_mc_ls, "Machine not found"
        machines_list = target_mc_ls

    # X and Y label
    gnt_mc.set_xlabel('Time since start')
    gnt_mc.set_ylabel('Machines')

    # X and Y limits
    # Y-axis height
    gnt_mc.set_ylim(0, 7*len(machines_list))
    gnt_mc.set_xlim(0, max([x['end time'] for x in scheduled_list_of_dict_mc if x['machine'] in machines_list]) + 1)

    # Setting ticks on y-axis
    # store this value later so that can access
    machine_to_yheight = dict(zip(machines_list[::-1],[4+7*x for x in list(range(0,len(machines_list)))]))

    gnt_mc.set_yticks(list(machine_to_yheight.values()))
    # Labelling tickes of y-axis
    gnt_mc.set_yticklabels(list(machine_to_yheight.keys()))

    # 4. assign each job 1 colour
    jobs_colour_dict, job_colour_palette = {}, [color for color in mcolors.TABLEAU_COLORS.keys()]
    for operation_dict in scheduled_list_of_dict_mc:
        if jobs_colour_dict.get([x for x in re.split('(\d+)',operation_dict['operation name']) if x != ''][0],None) == None:
            if len(job_colour_palette) == 0:
                job_colour_palette = [color for color in mcolors.TABLEAU_COLORS.keys()]
            jobs_colour_dict[[x for x in re.split('(\d+)',operation_dict['operation name']) if x != ''][0]] = job_colour_palette.pop(random.choice(list(range(len(job_colour_palette)))))

    # 5. Make a list, and add all the start and end time tuples to a list
    # Make sure to add the corresponding colour to another list
    # 6. For each machine, call gnt.broken_barh

    for machine_name in machines_list:
        # make a list to store the time tuples
        # need to convert the colour list into tuple later
        machine_time_tuple_ls, machine_time_tuple_colour = [], []
        # get only the jobs for the machine in question
        for mc_operation_dict in [x for x in scheduled_list_of_dict_mc if x['machine'] == machine_name]:
            machine_time_tuple_ls.append((mc_operation_dict['start time'],mc_operation_dict['end time']))
            machine_time_tuple_colour.append(jobs_colour_dict[[x for x in re.split('(\d+)',mc_operation_dict['operation name']) if x != ''][0]])
        # after all jobs for machine added, put into gantt chart
        gnt_mc.broken_barh(machine_time_tuple_ls, (machine_to_yheight[machine_name] - 3, 5), facecolors = machine_time_tuple_colour)

    # 7. save the gantt chart in the same folder as this file
    # plt.legend()
    plt.savefig("gantt machine.png")


    
def output_jobs(scheduled_list_of_dict_jb:list):
    fig, gnt_jb = plt.subplots()
    # plt.rcParams["figure.figsize"] = (3840*2, 2160)
    gnt_jb.tick_params(axis='y', which='major', labelsize=0.5)
    gnt_jb.tick_params(axis='y', which='minor', labelsize=0.5)
    

    # gnt_jb.grid(True)
    # X and Y label
    gnt_jb.set_xlabel('Time since start')
    gnt_jb.set_ylabel('Parts')

    # List of unique jobs
    # slightly different, have to take the number modifier at the end of the operation name also
    parts_list = []
    for operation_dict in scheduled_list_of_dict_jb:
        jb_tmp_ls = [x for x in re.split('(\d+)',operation_dict['operation name']) if x != '']
        if (jb_tmp_ls[0], jb_tmp_ls[-1]) not in parts_list:
            parts_list.append((jb_tmp_ls[0], jb_tmp_ls[-1]))    #eg ("B.", "1")

    # X and Y limits
    # Y-axis height
    gnt_jb.set_ylim(0, 7*len(parts_list))
    gnt_jb.set_xlim(0, max([x['end time'] for x in scheduled_list_of_dict_jb]) + 1)

    # Setting ticks on y-axis
    # store this value later so that can access
    job_to_yheight = dict(zip(parts_list[::-1],[4+7*x for x in list(range(0,len(parts_list)))]))
    gnt_jb.set_yticks(list(job_to_yheight.values()))
    # Labelling tickes of y-axis
    gnt_jb.set_yticklabels(list(job_to_yheight.keys()))

    # 4. assign each machine 1 colour
    machine_colour_dict, machine_colour_palette = {}, [color for color in mcolors.TABLEAU_COLORS.keys()]
    for operation_dict_jb in scheduled_list_of_dict_jb:
        if machine_colour_dict.get(operation_dict_jb['machine'],None) == None:
            if len(machine_colour_palette) == 0:
                machine_colour_palette = [color for color in mcolors.TABLEAU_COLORS.keys()]
            machine_colour_dict[operation_dict_jb['machine']] = machine_colour_palette.pop(random.choice(list(range(len(machine_colour_palette)))))

    # 5. Make a list, and add all the start and end time tuples to a list
    # Make sure to add the corresponding colour to another list
    # 6. For each part and number, call gnt.broken_barh

    for parts_name_num in parts_list:
        # make a list to store the time tuples
        # need to convert the colour list into tuple later
        parts_name_num_time_tuple_ls, parts_name_num_time_tuple_colour = [], []
        # get only the machines for the job in question
        # print(parts_name_num)
        # print([x for x in scheduled_list_of_dict_jb if ([x for x in re.split('(\d+)',x['operation name']) if x != ''][0], [x for x in re.split('(\d+)',x['operation name']) if x != ''][-1]) == parts_name_num])
        for jb_operation_dict in [x for x in scheduled_list_of_dict_jb if ([x for x in re.split('(\d+)',x['operation name']) if x != ''][0], [x for x in re.split('(\d+)',x['operation name']) if x != ''][-1]) == parts_name_num]:
            # print(jb_operation_dict)
            parts_name_num_time_tuple_ls.append((jb_operation_dict['start time'], jb_operation_dict['end time']))
            parts_name_num_time_tuple_colour.append(machine_colour_dict[jb_operation_dict['machine']])
        # after all jobs for part/number added, put into gantt chart
        gnt_jb.broken_barh(parts_name_num_time_tuple_ls, (job_to_yheight[parts_name_num] - 3, 5), facecolors = parts_name_num_time_tuple_colour)

    # 7. save the gantt chart in the same folder as this file
    plt.savefig("gantt jobs.png", dpi = 1000)




# https://www.geeksforgeeks.org/python-basic-gantt-chart-using-matplotlib/
# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt
 
def test_code():
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()
    
    # Setting Y-axis limits
    gnt.set_ylim(0, 50)
    
    # Setting X-axis limits
    gnt.set_xlim(0, 160)
    
    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time since start')
    gnt.set_ylabel('Machine')
    
    # Setting ticks on y-axis
    gnt.set_yticks([15, 25, 35])
    # Labelling tickes of y-axis
    gnt.set_yticklabels(['1', '2', '3'])
    
    # Setting graph attribute
    gnt.grid(True)
    
    # gnt.broken_barh([(start_time, duration)],(lower_yaxis, height),facecolors=('tab:colours'))
    # https://matplotlib.org/stable/gallery/lines_bars_and_markers/broken_barh.html
    # Declaring a bar in schedule
    gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange'))
    
    # Declaring multiple bars in at same level and same width
    gnt.broken_barh([(110, 10), (150, 10)], (10, 9), facecolors ='tab:blue')
    
    gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9), facecolors =('tab:red','tab:blue','tab:orange'))

    
    
    plt.savefig("gantt1.png") # save to local directory
    # plt.savefig("C:\\Users\\Sean\\Downloads\\gantt1.png") # save to specific directory
    # can be saved as .png or .pdf
    return

if __name__ == "__main__":
    None
    # test_code()
    holder_dict = {}
    import data_input, heuristics
    file_dir_splitter = "\\" if sys.platform == "win32" else "/"
    cwd_prefix = os.getcwd() + file_dir_splitter
    
    job_dict_eg, capacity_dict_eg = data_input.data_input_main(cwd_prefix+"bicycle-routing.csv", cwd_prefix+"bicycle-MRP.csv", cwd_prefix+"bicycle-capacity.csv", "R", "AB")
    heuristics.heuristic_LETSA(job_dict_eg, capacity_dict_eg, holder_dict)
    data_output_main(holder_dict['LETSA'],"2,4")