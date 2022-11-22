# Systems Optimization Challenge - Group 24

## Project Requirements
For all bellow modules, they are not included by default in python. Their installation is done by executing the command `pip install <module>`
- numpy 
- copy 

## Scripts description
### main.py
Here is the scheduling logic.

#### schedule()
1. Extracts time triggered tasks (TT) from csv
2. Extracts time triggered tasks (ET) from csv, if any
3. Adds polling task(s) to the TT
4. Fetches the scheduled table of theTT.

#### addPollingTasks()
The amount of polling tasks (PT) that will be added, is controlled by a given attribute. Default is 1. <br>
Since the ET tasks have separation groups, and there can only be one separation category in one polling task, plus the non-separated ETs (zero separation), then a polling task represents a group of ETs with the same separation. 
The PT will inherit the separation number from its assigned ETs and will indicate which ETs will be checked for schedulability. 
Once a schedulable group of ETs with the same separation is found, then we add the respective PT in the TT list until the amount of the added PT is met.
1. Extracts the different separation categories of the ET, if there are any ET tasks.
2. Calculates the server period
3. We start from the lowest separation number, and we check if their tasks can be scheduled.
4. We add one PT to the TT for each schedulable sublist of ETs with the same separation number until the amount of PT is reached.
   - In all different separations we include the ET with non separation restrictions, zero separation ET. 
   - During the search of a schedulable separation, we also search for the best budget for the respected separation 
   by doing a Hill Climbing from 1 till server period and with a cost function the response time of the separation group. 
   There is a plateau criterion which terminates the search in case the search meets a plateau 3 times.
5. If there is any sublist of ET from the same separation that can be scheduled, then we create a PT for this separation.
6. Lastly, we add the PT in the TT list.

#### schedulingTT()
This is the implementation of algorithm 1.
Given a list of TT and PT, it calculates a schedule table of all TT and PT tasks and their worst response time.

#### schedulingET()
This the implementation of algorithm 2. 
Given a sublist of ET, the server budget, period and deadline, it checks if the ETs can be scheduled in the PT.
When the sublist of ET is schedulable then it returns the response time of the PT.
- Server budget is the computation time of the PT
- Server period is the period of the PT
- Server deadline is the same as server period (as a starting point)

The above are calculated during the creation of the PT.

### utils.py
Here are our tools that are used during the scheduling.

### task.py
Here is the generic TaskModel as well as the getters for Idle and Polling TaskModels.

### csv_reader.py
This is a tool we made in order to read 7 or 8 column csv and create a list of TaskModels.

### To-Do
#### neighborhood function should do 
decide how many polling servers, redistribute zero event task, decide period and budget based on the previous solution
#### failed solution penatly 
should be a multiple of the cost
#### responseTime inside Algo 2 
save of each task into a list and return it 

