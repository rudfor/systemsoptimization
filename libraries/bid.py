import copy
import sys
import libraries as libs
import random



class Bid:
    """
    Class Bid
    TT and Polling Tasks
    """
    def __init__(self, csv_file, seed=999, verbosity=0):
        self.csv_file = csv_file
        self.seed = seed
        self.verbosity = verbosity
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv_file)
        self.TT = TT
        sublistET = libs.PollingServer.get_event_sublists(ET, seed)
        PT = []
        for ps in sublistET:
            # Create a new Polling Task Server using a group of ET tasks
            testTask = libs.TaskModel(name=f'PT{ps}',
                                      computation=libs.Functions.computation(sublistET[ps]),
                                      period=libs.Functions.lcm(sublistET[ps]),
                                      priority=7,
                                      type='PT',
                                      deadline=libs.Functions.deadline(sublistET[ps]),
                                      separation=ps,
                                      assigned_events=(sublistET[ps])
                                      )
            PT.append(testTask)
        self.PT = PT

    def __repr__(self):
        pass

    def showTT(self, verbose=False):
        if (self.verbosity > 3 or verbose):
            for t in self.TT:
                print(f'{t}')
                if (self.verbosity > 4 or verbose): print(f'Task Hash : {t.__hash__()}')

    def showPT(self, verbose=False):
        if (self.verbosity > 3 or verbose):
            for t in self.PT:
                print(f'{t}')
                if (self.verbosity > 4 or verbose): print(f'Task Hash : {t.__hash__()}')


    def show(self, verbose=False):
        self.showTT(verbose)
        self.showPT(verbose)

    def get_neighbour(self, variation=3):
        """
        move Zero Task to another Polling server
        Conditions
        # source and destination Polling server will be different
        """
        neighbour = copy.deepcopy(self)
        for var in range(variation):
            zeros_list = []
            if neighbour.verbosity > 5: print(f'Number of Polling Servers{len(neighbour.PT)}')
            ps_count = 0
            for ps in neighbour.PT:
                et_count = 0
                for et in ps.assignedEvents:
                    # print(f'PT: {et.name}, {et.separation}')
                    if et.separation == 0:
                        zeros_list.append({'task': et_count, 'ps': ps_count})
                    et_count += 1
                ps_count += 1
            if neighbour.verbosity > 5: print(f'{zeros_list}\n')
            if len(zeros_list)==0:
                return neighbour

            choice = random.choice(zeros_list)
            source_ps = choice.get("ps")
            source_task = choice.get("task")
            if neighbour.verbosity > 5:
                print(f'RANDOM = {choice}')
                print(f'RANDOM = {choice.get("ps")}')
                print(f'{neighbour.PT[choice.get("ps")].assignedEvents[choice.get("task")]}')
            et_task = neighbour.PT[choice.get("ps")].assignedEvents.pop(source_task)
            destination_ps = random.randint(0, ps_count - 1)
            # Avoid Moving Back
            while destination_ps == source_ps:
                destination_ps = random.randint(0, ps_count - 1)
            if neighbour.verbosity > 5:
                print(f'{destination_ps}')
                print(f'{destination_ps}{neighbour.PT[destination_ps].assignedEvents}')
            neighbour.PT[destination_ps].assignedEvents.append(et_task)
            if neighbour.verbosity > 3:
                print(f'ET Task{et_task.name} moved from {choice.get("ps")} to {destination_ps}')

        # Update Deadline for PT based on new ET Tasks
        for pt in neighbour.PT:
            pt.deadline = libs.Functions.deadline(pt.assignedEvents)
            pt.computation = libs.Functions.computation(pt.assignedEvents)
            pt.period = libs.Functions.lcm(pt.assignedEvents)
        return neighbour

    def get_neighbour_swap(self, swaps=3):
        """
        Swap to random Zero Tasks
        Conditions
        # 2 unique polling servers will be selected
        # 2 individual random Tasks will be selected
        """
        neighbour = copy.deepcopy(self)
        for var in range(swaps):
            zeros_list = []
            if neighbour.verbosity > 5: print(f'Number of Polling Servers{len(neighbour.PT)}')
            ps_count = 0
            for ps in neighbour.PT:
                et_count = 0
                for et in ps.assignedEvents:
                    # print(f'PT: {et.name}, {et.separation}')
                    if et.separation == 0:
                        zeros_list.append({'task': et_count, 'ps': ps_count})
                    et_count += 1
                ps_count += 1
            if neighbour.verbosity > 5: print(f'{zeros_list}\n')
            choice = random.choice(zeros_list)
            choice2 = random.choice(zeros_list)
            while choice == choice2 or choice.get("ps") == choice2.get("ps"):
                choice2 = random.choice(zeros_list)

            source_ps = choice.get("ps")
            source_ps2 = choice2.get("ps")
            source_task = choice.get("task")
            source_task2 = choice2.get("task")
            if neighbour.verbosity > 5:
                print(f'RANDOM = {choice}')
                print(f'RANDOM = {source_ps}')
                print(f'{neighbour.PT[source_ps].assignedEvents[source_task]}')
                print(f'RANDOM = {choice2}')
                print(f'RANDOM = {source_ps2}')
                print(f'{neighbour.PT[source_ps2].assignedEvents[source_task2]}')
            et_task = neighbour.PT[source_ps].assignedEvents.pop(source_task)
            et_task2 = neighbour.PT[source_ps2].assignedEvents.pop(source_task2)

            neighbour.PT[source_ps2].assignedEvents.append(et_task)
            neighbour.PT[source_ps].assignedEvents.append(et_task2)
            if neighbour.verbosity > 3:
                print(f'ET Task{et_task.name} moved from {choice.get("ps")} to {source_ps2}')
                print(f'ET Task{et_task2.name} moved from {choice2.get("ps")} to {source_ps}')

        # Update Deadline for PT based on new ET Tasks
        for pt in neighbour.PT:
            pt.deadline = libs.Functions.deadline(pt.assignedEvents)
            pt.computation = libs.Functions.computation(pt.assignedEvents)
        return neighbour



    @staticmethod
    def search_solution(csv, seed, plot=False, verbosity=0):
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv)
        sublistET = libs.PollingServer.get_event_sublists(ET, seed)

        print(f'LCM: TT: {libs.Functions.lcm(TT)}')
        for listET in sublistET:
            print(f'LCM: ET: PS_{listET}: {libs.Functions.lcm(sublistET[listET])}')

        if (verbosity > 3):
            for t in TT:
                print(f'{t}')
                if (verbosity > 4): print(f'Task Hash : {t.__hash__()}')

        PT = []
        for ps in sublistET:
            # Create a new Polling Task Server using a group of ET tasks
            testTask = libs.TaskModel(name=f'PT{ps}',
                                      computation=libs.Functions.computation(sublistET[ps]),
                                      period=libs.Functions.lcm(sublistET[ps]),
                                      priority=7,
                                      type='PT',
                                      deadline=libs.Functions.deadline(sublistET[ps]),
                                      separation=ps,
                                      assigned_events=(sublistET[ps])
                                      )
            PT.append(testTask)

        if (verbosity > 3):
            for t in PT:
                print(f'{t}')
                if (verbosity > 4): print(f'Task Hash : {t.__hash__()}')

        schedule1, wcrt1, data_frame1, isSchedulable1 = libs.AlgoOne.scheduling_TT(TT, visuals=plot, return_df=True)
        schedule2, wcrt2, data_frame2, isSchedulable2 = libs.AlgoOne.scheduling_TT(PT, visuals=plot, return_df=True)

        schedule3, wcrt3, data_frame3, isSchedulable3 = libs.AlgoOne.scheduling_TT(TT+PT, visuals=plot, return_df=True)

        if plot:
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
            fig.suptitle('Horizontally stacked subplots')
            data_frame1_diff = data_frame1.diff()
            data_frame1_diff.plot(ax=ax1, label='auto label', title='Time Triggered Tasks')
            #ax1.set_yscale('log')
            plt.legend(ncol=3)
            data_frame2_diff = data_frame2.diff()
            data_frame2_diff.plot(ax=ax2, label='auto label', title='Polling Server ET Tasks')
            #ax2.set_yscale('log')
            plt.legend(ncol=3)
            data_frame3.plot(ax=ax3, label='auto label', title='Time Triggered and Polling Server')
            #ax3.set_yscale('log')
            plt.legend(ncol=3)
            plt.show()
            #fig, (ax1, ax2) = plt.subplots(1, 2)

        print(f'wcrt: {wcrt1}, schedulable={isSchedulable1}')
        print(f'wcrt: {wcrt2}, schedulable={isSchedulable2}')
        print(f'wcrt: {wcrt3}, schedulable={isSchedulable3}')