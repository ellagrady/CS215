import process


# shortest remaining time first
class SRTF:

    # initialize SRTF object
    def __init__(self, numProcesses, arrivalTimes, burstTimes):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.processQueue = []

    # return list of process ids given numProcesses: (1 - numProcesses)
    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    # create list of processes
    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            id = i + 1
            currentProcess = process.process(id, self.arrivalTimes[i], self.burstTimes[i], self.burstTimes[i])
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    # calculate processesOrder, returns list of dictionaries
    def srtf(self):
        processArray = self.createProcesses()
        completedProcesses = []
        inProgressProcesses = []
        processesOrder = []  # fill with dictionary items {id: start time}
        time = 0  # current time
        processOne = processArray[0]
        if processOne.arrivalTime > 0 and {"null" : ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
            self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})
        while len(completedProcesses) < self.numProcesses:
            # add arrived processes to list of in progress processes
            for current in processArray:
                if current.arrivalTime <= time and current not in inProgressProcesses and current not in completedProcesses:
                    inProgressProcesses.append(current)
                # if no processes currently running, advance time
                if not inProgressProcesses:
                    time += 1
                else:  # sort in progress processes by time remaining
                    inProgressProcesses.sort(key=lambda x: x.remainingTime)

                    # current process is executed for one time unit
                    currentProcess = inProgressProcesses[0]
                    currentProcess.remainingTime -= 1
                    processesOrder.append({currentProcess.processID: time})
                    if {currentProcess.processID: time+1} not in self.processQueue:
                        self.processQueue.append({currentProcess.processID: time+1})

                    # once process is completed, it's removed from list of in progress processes
                    if currentProcess.remainingTime == 0:
                        inProgressProcesses.remove(currentProcess)
                        completedProcesses.append(currentProcess)
                        if {currentProcess.processID: time+1} not in self.processQueue:
                            self.processQueue.append({currentProcess.processID: time+1})

                    time += 1

        return processesOrder

    # return processQueue, for use in making diagram
    def makeQueue(self):
        return self.processQueue

    # calculate completion times, return list of dictionaries
    def completionTimes(self):
        processesOrder = self.srtf()
        processArray = self.createProcesses()
        completionTimes = []
        for currentProcess in processArray:
            eachProcess = []
            for partProcess in processesOrder:
                if list(partProcess.keys())[0] == currentProcess.processID:
                    partProcess[currentProcess.processID] = (partProcess.get(currentProcess.processID) + 1)
                    eachProcess.append(partProcess)
            completionTimes.append(eachProcess[-1])
        return completionTimes

    # calculate turnaround times, returns list of dictionaries
    #   turnaround times = completion times - arrival times
    def turnAroundTimes(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        turnAroundTimes = []
        for i in processArray:
            for j in completionTimes:
                if i.processID == list(j.keys())[0]:
                    completionTime = j.get(i.processID)
                    arrivalTime = i.arrivalTime
                    turnaround = int(completionTime) - int(arrivalTime)
                    turnaroundProcess = {i.processID: turnaround}
                    turnAroundTimes.append(turnaroundProcess)
        return turnAroundTimes

    # calculate avg turnaround time
    def avgTAT(self):
        turnAroundTimes = self.turnAroundTimes()
        sumTAT = 0
        for currentProcess in turnAroundTimes:
            sumTAT += list(currentProcess.values())[0]

        avg = (sumTAT / self.numProcesses)
        return avg

    # calculate waiting times for processes, returns list of dictionaries
    #   waiting time = turnaround time - burst time
    def waitingTime(self):
        processArray = self.createProcesses()
        turnAroundTimes = self.turnAroundTimes()
        waitingTimes = []
        for i in processArray:
            for j in turnAroundTimes:
                if i.processID == list(j.keys())[0]:
                    turnaroundTime = j.get(i.processID)
                    burstTime = i.burstTime
                    waiting = turnaroundTime - burstTime
                    waitingProcess = {i.processID: waiting}
                    waitingTimes.append(waitingProcess)
        return waitingTimes

    # calculate avg wait time
    def avgWT(self):
        waitingTimes = self.waitingTime()
        sumWT = 0
        for currentProcess in waitingTimes:
            sumWT += list(currentProcess.values())[0]

        avg = (sumWT / self.numProcesses)
        return avg

    # calculate schedule length, last completion time - first arrival time
    def scheduleLength(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        firstProcess = processArray[0].arrivalTime
        lastProcess = list(max(completionTimes, key=lambda x: max(x.values())).values())[0]  # time stored in arrival time of process
        scheduleLength = lastProcess - firstProcess
        return scheduleLength

    # calculate throughput, numProcesses/schedule length
    def throughput(self):
        scheduleLength = self.scheduleLength()
        throughputDec = self.numProcesses/scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput


srtf = SRTF(6, [0, 1, 2, 3, 4, 5], [7, 5, 3, 1, 2, 1])
print("processesOrder:", srtf.srtf())
print("completionTimes:", srtf.completionTimes())
print("turn around times:", srtf.turnAroundTimes())
print("avg TAT:", srtf.avgTAT())
print("waiting times:", srtf.waitingTime())
print("avg WT:", srtf.avgWT())
print("schedule length:", srtf.scheduleLength())
print("throughput:", srtf.throughput())



