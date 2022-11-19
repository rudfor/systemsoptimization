import sys
import copy
import math
import libraries as libs


class PollingServer:
    """
    Adds Polling Tasks to the TT
    return TT_and_PT, ET_WCRT, PT_created
    """
    # usage of algorithm 2
    @staticmethod
    def add_PT(TT, ET, polling_counter=None):
        TT_and_PT = TT
        # Stop if no ET given
        if len(ET) < 1:
            return TT, 0, 0

        # Identify all given separations
        separations = libs.Functions.get_separations(ET)

        # Prepare event sublists for which we will create polling tasks
        sublistETs = PollingServer.get_event_sublists(ET)

        # For a given polling server, the search space for the period can be
        # between 2 and the hyperperiod of all TT tasks (2nd hint in pdf)
        lcm = libs.Functions.lcm(copy.deepcopy(TT_and_PT))
        pollingPeriod = libs.Functions.get_polling_task_period(lcm)
        deadline = pollingPeriod
        print('Polling period:', pollingPeriod)

        # Decide how many polling servers we need based of how many separations we have
        PTs = len(sublistETs)
        ET_WCRT = 0
        PT_created = 0
        while len(separations) > 0:
            # The maximum response is the whole period,
            # we init the value as such in order to set a penalty for a sublist
            # not able to be scheduled, this way we can accept "wrong"
            # solutions but avoid picking them as the final solution
            bestResponseTime = pollingPeriod

            # Find a separation which tasks can be schedulable
            foundSchedulableSeparation = False

            # Get FIRST available separation
            # if separations = [1,2,3,4,5] then it will pop 1
            separation = separations.pop(0)

            # Extract events for separation
            sublistET = sublistETs[separation]

            # Init performance runtime memory for the current separation
            performanceTable = []

            # Best budget calculation is based on Hill Climbing
            # We start from 1 with step 1 until we reach the period
            # The climb will stop early if wet the same wcrt 3 times
            attemptsDuringPlateau = 3
            for budget in range(1, pollingPeriod):
                # Init the polling task attributes
                pollingTask = [budget, pollingPeriod, deadline]

                # Check if sublistET is schedulable
                schedulable, responseTime = libs.AlgoTwo.scheduling_ET(
                    pollingTask[0],
                    pollingTask[1],
                    pollingTask[2],
                    sublistET
                )

                # If separation is schedulable for budget then we store
                # the successful configuration into the performance table
                # Here we use response time as cost of our binary search
                # in order to determine the best budget.
                if (schedulable == True and responseTime <= bestResponseTime):
                    # Store wcrt and according period
                    performanceTable.append([budget, responseTime, separation, pollingPeriod, sublistET])

                    bestResponseTime = responseTime
                    foundSchedulableSeparation = True

                    # Decrease attempts during plateau
                    if bestResponseTime == responseTime:
                        attemptsDuringPlateau -= 1

                    # Terminate search once consumed all plateau attempts
                    if attemptsDuringPlateau < 1:
                        print('plateau')
                        break

            # Get budget for polling task
            if foundSchedulableSeparation:
                # pollingConfig = [budget, responseTime, separation, pollingPeriod, sublistET]
                pollingConfig = PollingServer.get_Min_Budget_Min_Period_Config(performanceTable)
                bestResponseTime = pollingConfig[1]
                budget = pollingConfig[0]

            # When the sublist of events is not schedulable,
            # we create a polling task with bad period as a penalty
            # for this polling task in order to allow "wrong" solutions
            # but avoid picking them as final solution in simulated annealing
            else:
                budget = bestResponseTime

            # Create polling task
            task = libs.get_polling(separation, budget, pollingPeriod, sublistET)

            print(
                '\n',
                'Add pooling schedulable task with name:', task.name, '\n',
                'and with separation:', task.separation, '\n',
                'and computation:', task.computation, '\n',
                'and period:', task.period, '\n',
                'and assigned events:', task.assignedEvents,
            )

            # Add polling task to Time Triggered tasks
            TT_and_PT.append(task)

            ET_WCRT += bestResponseTime

            PTs -= 1
            PT_created += 1

        return TT_and_PT, ET_WCRT, PT_created

    @staticmethod
    def get_event_sublists(ET):
        # initialize event sublists
        sublistETs = dict()

        # Get sublist of ET tasks with the same separation also for zeros
        for event in ET:
            if event.separation not in sublistETs.keys():
                sublistETs[event.separation] = []
            sublistETs[event.separation].append(event)

        # Check if we have events with zero separation and
        # split them among the rest of the separations
        #
        # Code block bellow will do the following:
        # From:  {0: [ET1,ET2], 1: [ET3], 2: [ET4]}
        # To:    {1: [ET3,ET1], 2: [ET4,ET2]}
        if 0 in sublistETs.keys() and len(sublistETs) > 1:
            # get the events of the key for zero separation
            # and remove the key from sublistETs
            zeros = sublistETs.pop(0, None)

            # Split events with zero separation among the rest of separations
            # Adds one zero_event to each of the rest of the separations and
            # until all zero_events are all distributed completely
            print('\n')
            print('separation[separation]', sublistETs)
            while len(zeros) > 0:
                for separation, events in sublistETs.items():
                    if separation == 0:
                        continue
                    # get an event from the zeros
                    print(len(zeros))
                    zeroEvent = zeros.pop()

                    # and add it to the current separation
                    sublistETs[separation].append(zeroEvent)

                    if len(zeros) == 0:
                        break

            print('separation[separation]', sublistETs)
        return sublistETs

    @staticmethod
    def get_Min_Budget_Min_Period_Config(performanceTable):
        # Pick 5 min WCRTs
        performanceTable.sort(key=lambda performance: performance[1])
        topWCRTs = performanceTable[:5]

        # Pick the min budget
        topWCRTs.sort(key=lambda performance: performance[0])
        pollingConfig = topWCRTs[:1][0]

        return pollingConfig
