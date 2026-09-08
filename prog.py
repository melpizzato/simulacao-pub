import numpy as np
from random import uniform, randint
from enum import Enum
from itertools import count

class Status(Enum):
    Available = 1
    Filling = 2
    Cleaning = 3

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
    def __init__(self):
        self.id = next(Client._id_generator)
        self.name = f"C{self.id:>03}"
        self.drinks = drinks()
        self.drink_time = get_time_drink()

    def get_name(self):
        return self.name

    def set_drinks(self):
        if self.drinks > 0:
            self.drinks -= 1
            self.drink_time = get_time_drink()
        else:
            if randint(0, 1) == 0:
                return -1
            else:
                self.drinks = drinks()
                self.drink_time = get_time_drink()

    def get_drinks(self):
        return self.drinks

    def get_drink_time(self):
        return self.drink_time

    def set_drink_time(self):
        self.drink_time = get_time_drink()

    def to_string(self):
        return f"{self.name}: {self.drinks}\ndrink time: {self.drink_time}"

class Waitress:
    _id_generator = count(start=1)
    def __init__(self):
        self.id = next(Waitress._id_generator)
        self.name = f"W{self.id:>03}"
        self.state = Status.Available
        self.occupation_time = 0
        print(f"{self.name} arrived!")

    def get_state(self):
        return self.state
    
    def get_occupation_time(self):
        return self.occupation_time

    def set_state(self, state):
        self.state = state

    def set_occupation_time(self, occupation_time):
        self.occupation_time = occupation_time

    def to_string(self):
        return f"{self.name}: state = {self.state}\noccupation_time = {self.occupation_time}"

clock = 0
num_glasses = 50
limit_glasses = 20
list_clients = []
list_waitresses = [Waitress(), Waitress()]

def print_state():
    print("-"*25)
    print(f"Clock: {clock}")
    print(f"Waitresses:")
    print(f"\t{list_waitresses[0].to_string}")
    print(f"\t{list_waitresses[1].to_string}")
    print(f"Clients:")
    for client in list_clients:
        print(f"\t{client.to_string}")
    print("-"*25)

if __name__ == "__main__":
    print_state()
    time_client = get_time_arrive()

    while (True):
        if clock > 30 and not list_clients:
            break

        if clock < 30:
            clock += time_client
            list_clients.append(Client())
            

