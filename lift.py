class Dinglemouse(object):
    def __init__(self, queues, capacity):
        self.queues = [list(q) for q in queues]
        self.capacity = capacity
        self.floorRequests = []
        self.direction = 1
        self.currentFloor = 0
        self.passengers = []
        self.history = [0]

    def check_floor_requests(self):
        if self.direction == 1:
            print(f'Checking floor requests above (and equal to) {self.currentFloor}')
            for floorIdx in range(self.currentFloor, len(self.queues)):  # Might cause problems starting at curr floor?
                if len(self.queues[floorIdx]) > 0:
                    print(f'Service requested on floor {floorIdx}')
                    if floorIdx not in self.floorRequests:
                        self.floorRequests.append(floorIdx)
            self.floorRequests.sort()
        elif self.direction == -1:
            print(f'Checking floor requests below (and equal to) {self.currentFloor}')
            for floorIdx in range(self.currentFloor, -1, -1):
                if len(self.queues[floorIdx]) > 0:
                    print(f'Service requested on floor {floorIdx}')
                    if floorIdx not in self.floorRequests:
                        self.floorRequests.append(floorIdx)
            self.floorRequests.sort(reverse=True)

    def moveElevator(self):
        self.currentFloor = self.floorRequests[0]
        print(
            f'Elevator moving to floor {self.currentFloor}. Passengers {self.queues[self.currentFloor]} waiting at this floor')
        self.floorRequests.pop(0)

    def unloadElevator(self, serviced):
        print(f'Unload passenger check: {self.passengers}')
        if len(self.passengers) > 0:
            for passengerIdx, passenger in enumerate(self.passengers):
                if passenger == self.currentFloor:
                    serviced = True
                    print(f'Passenger {passenger} has left the elevator')
                    self.passengers[passengerIdx] = 'x'
            return serviced, [p for p in self.passengers if p != 'x']
        else:
            return serviced, []

    def loadElevator(self, serviced):

        def addPassenger():
            print(f'Passenger {passenger} is boarding elevator')
            self.passengers.append(passenger)
            self.queues[self.currentFloor][passengerIdx] = 'x'
            if passenger not in self.floorRequests:
                self.floorRequests.append(passenger)

        for passengerIdx, passenger in enumerate(self.queues[self.currentFloor]):  # People waiting

            if self.direction == 1:
                if passenger > self.currentFloor:
                    serviced = True
                    if len(self.passengers) < self.capacity:
                        addPassenger()
                    else:
                        print('Elevator Full')
                        break  # Elevator is full
                else:
                    print(f'Passenger: {passenger} not eligible to ride')
            elif self.direction == -1:
                if passenger < self.currentFloor:
                    serviced = True
                    if len(self.passengers) < self.capacity:
                        addPassenger()
                    else:
                        print('Elevator Full')
                        break  # Elevator is full
                else:
                    print(f'Passenger: {passenger} not eligible to ride')

        self.queues[self.currentFloor] = [x for x in self.queues[self.currentFloor] if x != 'x']
        if self.direction == 1:
            self.floorRequests.sort()
        else:
            self.floorRequests.sort(reverse=True)
        print('Loading passengers complete...')
        return serviced

    def checkService(self):
        for floor in self.queues:
            if len(floor) != 0:
                return True
        if len(self.passengers) > 0:
            return True
        else:
            return False

    def theLift(self):  # Only changes direction when at max/min height with people waiting
        self.check_floor_requests()

        def elevatorController():
            print(f'Elevator Service History: {self.history}')
            if not self.checkService():
                print('No more passengers waiting')
                if self.currentFloor != 0:
                    self.history.append(0)  # Finally move elevator to floor zero.
                return self.history
            self.moveElevator()  # Elevator goes to next floor in floorRequest Queue
            serviced = False  # For determining if an unload/load event took place at a floor
            serviced, self.passengers = self.unloadElevator(serviced)
            serviced = self.loadElevator(serviced)

            print(f'Current floor requests: {self.floorRequests}')
            if len(self.floorRequests) > 0:
                if serviced:
                    if self.history[-1] != self.currentFloor:
                        self.history.append(self.currentFloor)
                    # serviced = False
                return elevatorController()
            else:
                self.direction *= -1
                print(f'Elevator has changed direction. Moving {self.direction}')
                serviced = self.loadElevator(serviced)
                if serviced:  # Adding history in twice because of this line
                    if self.history[-1] != self.currentFloor:
                        self.history.append(self.currentFloor)
                self.check_floor_requests()
                return elevatorController()

        return elevatorController()


_queues0 = ((), (), (5, 5, 5), (), (), (), ())
_queues1 = ((), (), (1, 1), (), (), (), ())
_queues2 = ((), (3,), (4,), (), (5,), (), ())
_queues3 = ((), (0,), (), (), (2,), (3,), ())
lift = Dinglemouse(_queues3, 5)
h = lift.theLift()
print(f'Result: {h}')
# I have the floor requests. Move to the lowest number floor in requests. Remove request. While there are people there,
# load them onto elevator if capacity allows is. Update queue, update floorRequest (sorted).


'''
Check all floors
If elevator is going up and there are people on a floor, if the floor index is greater than elevator index, add it to queue
If elevator is going up and there are people on a floor, if the floor index is greater than elevator index, add it to queue
If there are people waiting for service, elevator continues service
Elevator moves to first floor in floor Request queue
If people need to go to that floor, unload the people
If people need to get on above floor, load people. 
'''

''' Elevator shouldnt record history if noone is eligible to ride elevator'''