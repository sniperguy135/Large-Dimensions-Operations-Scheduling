# Operations Scheduling for Very Large Dimension Problems
Large Dimensions Operations Scheduling for SUTD ESD Term 5 ESA - Team 3 Project 6

## Project Description

Operations scheduling involves arranging the sequence and timing of jobs to efficiently use an organization's resources. In manufacturing and industrial engineering, scheduling can be computationally intensive due to the large number of jobs, making it challenging to find an optimal solution. As a result, a balance is often struck between achieving an optimal schedule and producing it within a reasonable timeframe.

Our scheduling software is designed for use across various industries and can rapidly generate near-optimal operation schedules to minimize the total completion time (makespan) for a large number of jobs on multiple machines. It utilizes heuristic methods to determine the best possible schedule within 10 minutes.


## How to Install and Run Project

This project should run on all mainstream operating systems with a working installation of Python 3.10 or later. Supported systems include Windows 10, Windows 11 and macOS 10.9 or later.

1) Unzip the file “ESA Team 3 Project 6.zip”.

2) Open the newly created folder “ESA Team 3 Project 6”.

3) Run “UIpage1.py”. **A network connection may be required to install missing dependencies if you are running the program for the first time.**


## How to Use the Project


### Template files

The program requires data inputs in a specific format. To aid with the use of the program, you may find template files in the “TemplateFiles” folder, within the “ESA Team 3 Project 6” folder. Template files can also be found at this link (also found on the Startup Page): https://tinyurl.com/opsschedulingtemplatefiles.



1. Startup Page

To produce an operations schedule, the data inputs required are the Material Requirements Planning (MRP), the Routing and the Capacity. 

Ensure that your data input files match the formatting of the template files. Files can be accepted in csv, xlsx, xls or tsv file format. Please close all input files before continuing.

1) State the directory linked to your MRP file.

2) Indicate your starting and ending period by entering the corresponding column letters based on your MRP file. A maximum of 10 consecutive periods can be chosen from the MRP. 

3) Press the 'submit' button to continue.

4) State the directory linked to your Routing file. The Routing file can based on a Bill-of-Materials (BOM) with a maximum of 14 layers and 7 children per node.

5) Press the 'Submit' button to continue.

6) State the directory linked to your Capacity file.

7) Press the 'Submit' button to continue.



2. Loading Page

1) Wait for the loading bar to reach 100%. The process can take up to 10 minutes.

2) Press the “Next Page” button to continue.



3. Output / Result Page

1) The Gantt chart or operations schedule is displayed on the left side of the screen.

2) You may choose to display the jobs on the vertical axis instead of machines. Press the “job” button to display jobs as the vertical axis. You may press the “machine” button to display machines as the vertical axis.

3) You may generate another Gantt chart based on different data inputs or time periods. Press the “restart” button to restart the entire process. You will be brought back to the Startup page.


## Future Improvements



* Customizable user interface
    * Currently, the user is limited to the existing user interface. In the future, allowing the user to change aesthetic features such as font, font size, and theme colors could make for a more pleasant viewing experience and increase the user-friendliness of the operations scheduler.
* Intuitive data input system
    * Currently, the user inputs data by keying in the directory linked to their input files as a string. This method is rather counterintuitive and has a high potential for typographical errors which would disrupt the operations scheduling process, making for an unpleasant user experience. A future improvement would be to make the method of data input more instinctive, either through the use of a drag-and-drop file uploader or by opening a directory from which the user can select their input file.
* Dropdown list for periods to be scheduled
    * Currently, the user must input the column letters for both the first and last period to be scheduled for. While the system will generate an error message in the event that the user selects more than 10 periods for scheduling, there is no indication of what the latest period available for selection is. A future improvement would be to have a dropdown list of last periods for scheduling, based on the user’s input for the first period to be scheduled.
* Schedule for more than 10 periods at a time
    * In this iteration of the operations scheduler, the user can select only up to 10 periods for scheduling. In the future, the number of periods available for selection could be increased to give the user more flexibility and functionality.
* More heuristics
    * As of now, the heuristics used only consider workcenters with one machine each. In the future, heuristics which allow for workcenters with multiple machines can be implemented to improve the capabilities of the operations scheduler. Additionally, more heuristics can be implemented to improve the optimality of the solutions generated.
* Progressive results
    * In this iteration of the operations scheduler, the user can only view the operations schedule generated after (1) all heuristics have been run, or (2) 10 minutes have elapsed, which comes first. A future improvement would be to allow for progressive results, where the user has the option of terminating scheduling as soon as an operations schedule has been successfully generated, even before all heuristics have been run or 10 minutes have passed. This would be useful if the user needs to generate the operations schedule urgently.
* Filter function for data output
    * In the future, the data output could be improved by adding a function where the user can filter by machines or jobs. This would remove unnecessary information from the data output, better meeting the user’s needs.


## Credits


### Software and Libraries



* [Python](https://www.python.org/) for the programming language
* [PyQt5](https://pypi.org/project/PyQt5/) for the user interface
* [openpyxl](https://pypi.org/project/openpyxl/) for Excel file handling
* [networkx](https://networkx.org/) for building Bill-of-Materials (BOM) trees
* [numpy](https://numpy.org/) for the array functions
* [Docs to MD](https://workspace.google.com/marketplace/app/docs_to_markdown/700168918607) for converting Google Docs to Markdown file format


### Special Thanks

Dr Sun Zeyu 

Professor Rakesh Nagi 

Singapore University of Technology and Design

Engineering Systems and Design Pillar Team
