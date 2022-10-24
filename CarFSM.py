from random import randint
from time import clock

class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
    
    def Execute(self):
        pass

# States

class Stopped(State):
    def __init__(self, FSM):
        super(Stopped, self).__init__(FSM)
    
    def Execute(self):
        print("Stopped")

class Accelerating(State):
    def __init__(self, FSM):
        super(Accelerating, self).__init__(FSM)

    def Execute(self):
        print("Accelerating")

class BrakingFromFast(State):
    def __init__(self, FSM):
        super(BrakingFromFast, self).__init__(FSM)

    def Execute(self):
        print("BrakingFromFast")

class BrakingFromMedium(State):
    def __init__(self, FSM):
        super(BrakingFromMedium, self).__init__(FSM)
    
    def Execute(self):
        print("BrakingFromMedium")
    
class BrakingFromSlow(State):
    def __init__(self, FSM):
        super(BrakingFromSlow, self).__init__(FSM)
    
    def Execute(self):
        print("BrakingFromSlow")

class ConstantSpeed(State):
    def __init__(self, FSM):
        super(ConstantSpeed, self).__init__(FSM)

    def Execute(self):
        print("ConstantSpeed")

##========================================================
class Transition(object):
    def __init__(self, toState : str):
        self.toState = toState
    
    def Execute(self):
        print("Transitioning")




# Input

class InputValues():
    def __init__(self, objectInFront: bool = True, speed: float = 0, distanceToObject: float = 0):
        self.object_in_front = objectInFront
        self.speed = speed
        self.distance_to_object = distanceToObject
    
    def ChangeInput(self, objectInFront: bool, speed: float, distanceToObject: float):
        self.object_in_front = objectInFront
        self.speed = speed
        self.distance_to_object = distanceToObject



# FSM

class FSM(object):
    def __init__(self, char):
        self.char = char
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.curStateName = None
        self.trans = None
    
    def SetState(self, stateName : str):
        self.curStateName = stateName
        self.curState = self.states[stateName]

    def AddState(self, stateName : str, state : State):
        self.states[stateName] = state

    def AddTransition(self, transitionName : str, transition : State):
        self.transitions[transitionName] = transition

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]

    def Execute(self):
        if (self.trans):
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.trans = None

        self.curState.Execute()


# assumes that we start from a stopped state
brakeThresholdLow = 15
brakeThresholdHigh = 45
desiredSpeed = 60
class Char(object):
    def __init__(self):
        self.FSM = FSM(self)
        self.input = InputValues()
        self.FSM.AddState("Stopped", Stopped(self.FSM))
        self.FSM.AddState("BrakingFromFast", BrakingFromFast(self.FSM))
        self.FSM.AddState("BrakingFromMedium", BrakingFromMedium(self.FSM))
        self.FSM.AddState("BrakingFromSlow", BrakingFromSlow(self.FSM))
        self.FSM.AddState("ConstantSpeed", ConstantSpeed(self.FSM))
        self.FSM.AddState("Accelerating", Accelerating(self.FSM))

        self.FSM.AddTransition("toStopped", Transition("Stopped"))
        self.FSM.AddTransition("toBrakingFromFast", Transition("BrakingFromFast"))
        self.FSM.AddTransition("toBrakingFromMedium", Transition("BrakingFromMedium"))
        self.FSM.AddTransition("toBrakingFromSlow", Transition("BrakingFromSlow"))
        self.FSM.AddTransition("toConstantSpeed", Transition("ConstantSpeed"))
        self.FSM.AddTransition("toAccelerating", Transition("Accelerating"))

        self.FSM.SetState("Stopped")


    # need to change these transitions to actually depend on object distance
    # didn't add transitions from states to itself
    def SetTransition(self):
        if self.FSM.curStateName == "Stopped":
            if self.speed < desiredSpeed:
                self.FSM.ToTransition("toAccelerating")

        elif self.FSM.curStateName == "Accelerating":
            if self.input.object_in_front and self.input.speed >= brakeThresholdHigh:
                self.FSM.ToTransition("toBrakingFromFast")
            elif self.input.object_in_front and self.input.speed < brakeThresholdHigh and self.input.speed >= brakeThresholdLow:
                self.FSM.ToTransition("toBrakingFromMedium")
            elif self.input.object_in_front and self.input.speed < brakeThresholdLow:
                self.FSM.ToTransition("toBrakingFromSlow")

            # might want to change this so that it's within a certain range instead of exactly this value
            elif self.input.speed == desiredSpeed:
                self.FSM.ToTransition("toConstantSpeed")
        
        elif self.FSM.curStateName == "ConstantSpeed":
            if (self.input.object_in_front or self.input.speed > desiredSpeed) and self.input.speed >= brakeThresholdHigh:
                self.FSM.ToTransition("toBrakingFromFast")
            elif (self.input.object_in_front or self.input.speed > desiredSpeed) and self.input.speed < brakeThresholdHigh and self.input.speed >= brakeThresholdLow:
                self.FSM.ToTransition("toBrakingFromMedium")
            elif (self.input.object_in_front or self.input.speed > desiredSpeed) and self.input.speed < brakeThresholdLow:
                self.FSM.ToTransition("toBrakingFromSlow")
            elif not self.input.object_in_front and self.input.speed < desiredSpeed:
                self.FSM.ToTransition("toAccelerating")
            # The model showed a transition to stopped, but I don't know the criteria
        
        elif self.FSM.curStateName == "BrakingFromFast":
            if (self.input.object_in_front or self.input.speed > desiredSpeed) and self.input.speed < brakeThresholdHigh and self.input.speed >= brakeThresholdLow:
                self.FSM.ToTransition("toBrakingFromMedium")
            elif not self.input.object_in_front and self.input.speed < desiredSpeed:
                self.FSM.ToTransition("toAccelerating")
            elif self.input.speed == desiredSpeed:
                self.FSM.ToTransition("toConstantSpeed")

        elif self.FSM.curStateName == "BrakingFromMedium":
            if (self.input.object_in_front or self.input.speed > desiredSpeed) and self.input.speed < brakeThresholdLow:
                self.FSM.ToTransition("toBrakingFromSlow")
            elif not self.input.object_in_front and self.input.speed < desiredSpeed:
                self.FSM.ToTransition("toAccelerating")
            elif self.input.speed == desiredSpeed:
                self.FSM.ToTransition("toConstantSpeed")

        elif self.FSM.curStateName == "BrakingFromSlow":
            # should maybe add a state to account for overshooting to negative speed
            if (self.input.speed <= 0):
                self.FSM.ToTransition("toStopped")
            elif not self.input.object_in_front and self.input.speed < desiredSpeed:
                self.FSM.ToTransition("toAccelerating")
            elif self.input.speed == desiredSpeed:
                self.FSM.ToTransition("toConstantSpeed")

    def Execute(self, objectInFront: bool, speed: float, distanceToObject: float):
        self.input.ChangeInput(objectInFront, speed, distanceToObject)
        self.FSM.Execute()

    

if __name__ == "__main__":
    while True:
        pass


    
    
        
