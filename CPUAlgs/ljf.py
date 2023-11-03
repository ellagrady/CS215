import process

# longest job first
class LJF:

    # initialize LJF object
    def __init__(self, numProcesses, arrivalTimes, burstTimes):
        self.numProcesses = numProcesses
        self.arrivalTimes = arrivalTimes  # array of arrival times ordered by process id least to greatest, len = numProcesses
        self.burstTimes = burstTimes  # array of burst times ordered by process id least to greatest, len = numProcesses
        self.processQueue = []

    # for numProcesses, returns array of process ids (1-numProcesses)
    def getProcessIDs(self):
        idArray = []
        for i in range(self.numProcesses):
            idArray.append(i + 1)
        return idArray

    # create the processes, return list of process objects
    def createProcesses(self):
        processArray = []
        for i in range(self.numProcesses):
            id = i + 1
            currentProcess = process.process(id, self.arrivalTimes[i], self.burstTimes[i])
            processArray.append(currentProcess)
        processArray.sort(key=lambda x: x.arrivalTime)
        return processArray

    # return processQueue, for use in making diagram
    def makeQueue(self):
        return self.processQueue

    # calculate completion times of processes, returns list of dictionaries
    def completionTimes(self):
        processArray = self.createProcesses()
        completionTimes = []
        # handle process with processId 1
        processOne = processArray[0]
        completedTime = processOne.arrivalTime + processOne.burstTime
        completedProcess = {processOne.processID: completedTime}
        completionTimes.append(completedProcess)
        # add completed process to processQueue
        if completedProcess not in self.processQueue:
            if processOne.arrivalTime > 0 and {"null": ("0 -> " + str(processOne.arrivalTime))} not in self.processQueue:
                self.processQueue.append({"null": ("0 -> " + str(processOne.arrivalTime))})
            self.processQueue.append(completedProcess)
        processArray.remove(processOne)
        # for all other processes
        while len(processArray) > 0:
            longestBurst = max(processArray, key=lambda x: x.burstTime)
            completedTime += longestBurst.burstTime
            completedProcess = {longestBurst.processID: completedTime}
            if completedProcess not in self.processQueue:
                self.processQueue.append(completedProcess)
            completionTimes.append(completedProcess)
            processArray.remove(longestBurst)
        return completionTimes

    # calculate turnaround times, return list of dictionaries
    #   turnaround time = completion time - arrival time
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

    # calculate avg tat
    def avgTAT(self):
        turnAroundTimes = self.turnAroundTimes()
        sum = 0
        for currentProcess in turnAroundTimes:
            sum += list(currentProcess.values())[0]

        avg = (sum / self.numProcesses)
        return avg

    # calculate waiting times for each process, returns list of dictionaries
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
        turnAroundTimesArray = []
        sum = 0
        for currentProcess in waitingTimes:
            # turnAroundTimesArray.append(list(currentProcess.values())[0])
            sum += list(currentProcess.values())[0]

        avg = (sum / self.numProcesses)
        return avg

    # calculate schedule length, last process completion time - first process arrival time
    def scheduleLength(self):
        processArray = self.createProcesses()
        completionTimes = self.completionTimes()
        lastProcess = max(completionTimes, key=lambda x: max(x.values()))
        startProcess = min(processArray, key=lambda x: x.arrivalTime)

        scheduleLength = (list(lastProcess.values())[0]) - startProcess.arrivalTime
        return scheduleLength

    # calculate throughput, numProcesses/scheduleLength
    def throughput(self):
        scheduleLength = self.scheduleLength()
        throughputDec = self.numProcesses / scheduleLength
        throughput = str(self.numProcesses) + "/" + str(scheduleLength) + " (or " + str(throughputDec) + ")"
        return throughput


ljf = LJF(5, [1, 2, 3, 4, 5], [7, 5, 1, 2, 8])
print("completion times:", ljf.completionTimes())
print("turn around times:", ljf.turnAroundTimes())
print("waiting times:", ljf.waitingTime())
print("schedule length:", ljf.scheduleLength())
print("throughput:", ljf.throughput())
print("average turn around time:", ljf.avgTAT())
print("average waiting time:", ljf.avgWT())