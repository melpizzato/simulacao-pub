from random import uniform, randint
from enum import Enum
from itertools import count

clock = 0
num_glasses = 50
limit_glasses = 20
smallest_time_pass = -1
list_clients = []
list_waitresses = []
list_arrivals = []
list_events = []
list_drinking = []
list_waiting = []

class WaitressStatus(Enum):
    Available = 1
    Filling = 2
    Cleaning = 3
    def __format__(self, spec):
        return f'{self.name}'

class ClientStatus(Enum):
    Waiting = 1
    Drinking = 2
    Exited = 3
    def __format__(self, spec):
        return f'{self.name}'

class EventStatus(Enum):
    Arriving = 1
    Drinking = 2
    Filling = 3
    Cleaning = 4
    def __format__(self, spec):
        return f'{self.name}'


def get_time_arrive():
    num = uniform(0, 100)
    if num < 54.72:
        return 2.5
    elif num < 75.47:
        return 7.5
    elif num < 92.54:
        return 12.5
    elif num < 94.34:
        return 17.5
    else:
        return 22.5

def get_time_fill():
    num = uniform(0, 100)
    if num < 1.43:
        return 3
    elif num < 7.14:
        return 4
    elif num < 25.71: 
        return 5
    elif num < 84.28:
        return 6
    else:
        return 7

def get_time_drink():
    return randint(5, 8)

def drinks():
    return randint(1,4)

class Client:
    _id_generator = count(start=1)
    def __init__(self, time_arrive):
        self.id = next(Client._id_generator)
        self.name = f"C{self.id:>03}"
        self.drinks = drinks()
        self.drink_time = 0
        self.time_arrive = time_arrive
        self.queue_enter_time = 0
        self.total_wait_time = 0
        self.exit_time = -1
        self.status: ClientStatus | None = None

    def set_drinks(self):
        if self.drinks > 0:
            self.drinks -= 1
        else:
            if randint(0, 1) == 0:
                return -1
            else:
                self.drinks = drinks()
                return self.drinks

    def to_string(self):
        if self.status == ClientStatus.Waiting:
            return f"{self.name}: {self.drinks} - {self.status} since {self.queue_enter_time}"
        elif self.status == ClientStatus.Drinking:
            return f"{self.name}: {self.drinks} - {self.status} - drink time: {self.drink_time}"
        elif self.status == ClientStatus.Exited:
            return f"{self.name}: {self.status} in {self.exit_time}"

class Waitress:
    _id_generator = count(start=1)
    def __init__(self):
        self.id = next(Waitress._id_generator)
        self.name = f"W{self.id:>03}"
        self.state = WaitressStatus.Available
        self.occupation_time = 0
        self.time_cleaning = 0
        self.time_filling = 0

    def to_string(self):
        if self.state == WaitressStatus.Cleaning or self.state == WaitressStatus.Filling:
            return f"{self.name}: {self.state} - occupation_time = {self.occupation_time}"
        else:
            return f"{self.name}: {self.state}"

def fill_arrival_list():
    global list_arrivals
    count_clock = 0
    while (True):
        time_arrival = get_time_arrive()
        if count_clock + time_arrival < 30:
            break
        count_clock += time_arrival
        list_arrivals.append({"client": Client(count_clock),
                              "time_arrival": time_arrival})

def add_drink_event(client):
    global list_events
    time_event = get_time_drink()
    list_events.append({"event": EventStatus.Drinking,
                        "client": client,
                        "clock": clock,
                        "time": time_event})
    list_events.sort(key=lambda x :x["time"])

def add_filling_event(client):
    global list_events
    time_event = get_time_fill()
    list_events.append({"event": EventStatus.Filling,
                        "client": client,
                        "clock": clock,
                        "time": time_event})
    list_events.sort(key=lambda x :x["time"])


def add_cleaning_event():
    global list_events
    time_event = 5
    list_events.append({"event": EventStatus.Cleaning,
                        "clock": clock,
                        "time": time_event})
    list_events.sort(key=lambda x :x["time"])

def resolve_arrive_event(event):
    global list_clients
    global list_events
    global list_arrivals

    client = event["client"]
    client.status = ClientStatus.Waiting
    client.queue_enter_time = clock

    list_clients.append(client)
    list_arrivals.remove(event)
    add_drink_event(client)

def resolve_drink_event(event):
    global list_events
    global list_drinking
    global list_waiting

    client = event["client"]
    list_drinking.remove(client)
    list_events.remove(event)

    if client.set_drinks() == -1:
        client.exit_time = clock
        client.status = ClientStatus.Exited
    else:
        list_waiting.append(client)
        client.enter_queue_time = clock
        client.status = ClientStatus.Waiting
        add_filling_event(client)

def resolve_filling_event(event, waitress):
    global list_events
    global list_waiting
    global list_drinking
    global num_glasses

    num_glasses -= 1

    client = event["client"]
    list_waiting.remove(client)
    list_drinking.append(client)
    client.status = ClientStatus.Drinking
    client.total_wait_time += clock - client.queue_enter_time
    client.drink_time = get_time_drink()

    waitress.time_filling += waitress.occupation_time
    task_list = [x for x in list_events if x["event"] == EventStatus.Filling or x["event"] == EventStatus.Cleaning]
    if task_list:
        if num_glasses < limit_glasses:
            waitress.status = WaitressStatus.Cleaning
            waitress.occupation_time = 5


    
    
    

def print_state():
    print("-"*25)
    print(f"Clock: {clock}")
    print(f"Waitresses:")
    print(f"\t{list_waitresses[0].to_string()}")
    print(f"\t{list_waitresses[1].to_string()}")
    print(f"Clients:")
    for client in list_clients:
        print(f"\t{client.to_string()}")
    print("-"*25)

if __name__ == "__main__":
    list_waitresses.append(Waitress())
    list_waitresses.append(Waitress())
    print_state()
    

    while (True):
        if clock > 30 and not list_events:
            break



            

