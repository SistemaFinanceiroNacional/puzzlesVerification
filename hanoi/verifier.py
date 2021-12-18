import sys
import subprocess
import re

timeoutInSeconds = 2
class InsufficientRun(Exception):
    def __init__(self,iteration,points):
        self.points=points
        self.iteration=iteration

class Disk:
    def __init__(self,size):
        self.thickness=size
    def size(self):
        return self.thickness
class Pin:
    def __init__(self,pinsInit=0):
        if pinsInit == 0:
            self.disks=[]
        else:
            self.disks=[Disk(i+1) for i in range(pinsInit)]
            self.disks.reverse()
    def isEmpty(self):
        return len(self.disks) == 0
    def top(self):
        return self.disks[-1]
    def push(self,disk):
        self.disks.append(disk)
    def pop(self):
        return self.disks.pop()
class GameState:
    def __init__(self,numberOfDisks):
        self.stepsNumber=0
        self.numberOfDisks=numberOfDisks
        self.pins=[Pin(numberOfDisks),Pin(),Pin()]
    def perform(self,move):
        movePattern=re.match("([123])->([123])",move)
        if movePattern:
            srcPinIndex=int(movePattern.group(1))-1
            dstPinIndex=int(movePattern.group(2))-1
            srcPin=self.pins[srcPinIndex]
            dstPin=self.pins[dstPinIndex]
            if srcPin.isEmpty() or ((not dstPin.isEmpty()) and srcPin.top().size() > dstPin.top().size()):
                raise Exception("SERIOUS? A NON-CONFORMANT MOVE? GO TO HELL")
            dstPin.push(srcPin.pop())
            self.stepsNumber+=1
    def isSolved(self):
        return self.pins[0].isEmpty() and self.pins[1].isEmpty()
    def numberOfSteps(self):
        return self.stepsNumber
    def minimumNumberOfSteps(self):
        return (2**self.numberOfDisks)-1
    

def pointsPerRun(disksNumber,output):
    points=0
    lines=output.splitlines()
    game=GameState(disksNumber)
    for l in lines:
        game.perform(l)
    if game.isSolved():
        points+=1
        if game.numberOfSteps() == game.minimumNumberOfSteps():
            points+=1
    return points

def main(args):
    points=0
    if len(args) != 2:
        raise ValueError("You must call me with a single argument")
    executable=args[1]
    for i in range(10):
        try:
            p=subprocess.run(executable,timeout=2,input=f"{i+1}",capture_output=True,encoding="utf-8")
        except subprocess.TimeoutExpired as e:
            raise InsufficientRun(i+1,points) from e
        points+=pointsPerRun(i+1,p.stdout)
    return points

if __name__ == "__main__":
    try:
        points = main(sys.argv)
        print(f"Your score is {points} from 20\n")
    except InsufficientRun as e:
        print(f"your run fail on {e.iteration} disks with acummulated score as {e.points}\n")
