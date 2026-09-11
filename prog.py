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
timeline = []
list_drinking = []
list_waiting = []
list_tasks = []

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

"""função para adquirir o tempo de chegada de um cliente"""
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

"""função para adquirir o tempo para encher um copo"""
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

"""função para adquirir o tempo para tomar um drink"""
def get_time_drink():
    return randint(5, 8)

"""função para adquirir quantos drinks um cliente irá pedir"""
def drinks():
    return randint(1,4)

"""
    Classe para representar um cliente. Possui os atributos:
    id: id inteiro sequencial
    name: nome do cliente (apenas a letra C seguida pelo id do cliente, ex C001)
    drinks: quantidade de drinks que um cliente irá pedir ainda
    drink_time: tempo que um cliente passará bebendo
    time_arrive: tempo de chegada do cliente no sistema
    queue_enter_time: tempo de entrada do cliente na fila de espera para encher o copo. Utilizado para verificar o total de tempo de espera do cliente
    total_wait_time: tempo total de espera do cliente na fila
    exit_time: tempo de saída do cliente do sistema
    status: O estado do cliente. Pode ser Drinking, Waiting ou Exited
"""
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

    """
    função para decrementar os drinks do cliente ao beber e randomizar sua saída de fato do sistema
    """
    def set_drinks(self):
        if self.drinks > 0:
            self.drinks -= 1
        else:
            if randint(0, 1) == 0:
                return -1
            else:
                self.drinks = drinks()
                return self.drinks
    """
    função para imprimir o estado do cliente no terminal
    """
    def to_string(self):
        if self.status == ClientStatus.Waiting:
            return f"{self.name}: {self.drinks} - {self.status} since {self.queue_enter_time}"
        elif self.status == ClientStatus.Drinking:
            return f"{self.name}: {self.drinks} - {self.status} - drink time: {self.drink_time}"
        elif self.status == ClientStatus.Exited:
            return f"{self.name}: {self.status} in {self.exit_time}"

"""
Classe para representar a garçonete no sistema. Possui os seguintes atributos:
    id: identificador sequencial inteiro
    name: mesmo que o cliente
    state: estado da garçonete. Pode ser Available, Filling ou Cleaning
    occupation_time: tempo que a garçonete gastara para realizar a tarefa.
    time_cleaning: tempo total gasto pela garçonete lavando copos
    time_filling: tempo total gasto pela garçonete enchendo copos
"""
class Waitress:
    _id_generator = count(start=1)
    def __init__(self):
        self.id = next(Waitress._id_generator)
        self.name = f"W{self.id:>03}"
        self.state = WaitressStatus.Available
        self.occupation_time = 0
        self.time_cleaning = 0
        self.time_filling = 0

    """
    Função para imprimir o estado da garçonete no terminal
    """
    def to_string(self):
        if self.state == WaitressStatus.Cleaning or self.state == WaitressStatus.Filling:
            return f"{self.name}: {self.state} - occupation_time = {self.occupation_time}"
        else:
            return f"{self.name}: {self.state}"

"""Função para retornar um cliente na lista de clientes pesquisando pelo nome"""
def find_client_by_name(name):
    for client in list_clients:
        if client.name == name:
            return client

"""Função para retornar uma task não atribuída na lista de tarefas"""
def find_task_unassigned():
    for task in list_tasks:
        if task["waitress"] is None:
            return task

"""Função para organizar a lista de tarefas. A lista de tarefas deve ser organizada da seguinte forma:
    Se glasses > limit_glasses, then:
        1. Tarefas atribuídas às garçonetes
        2. Fila dos clientes para encher copos
        3. Lista de tarefas de limpeza
    Se glasses < limit_glasses, then:
        1. Tarefas atribuídas às garçonetes
        2. Lista de tarefas de limpeza
        3. Fila dos clientes para encher copos
"""
def sort_task_list():
    pass

"""Função para inicializar a fila de chegada dos clientes, com a criação do objeto cliente e o tempo de chegada"""
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

"""Função para cadastrar a conclusão do evento de chegada na timeline"""
def add_arrival_event(client_name, time_event):
    global timeline

    timeline.append({"event": EventStatus.Arriving,
                     "client": client_name,
                     "clock": clock,
                     "time": time_event})


"""Função para cadastrar a conclusão do evento de bebida na timeline"""
def add_drink_event(client_name, time_event):
    global timeline

    timeline.append({"event": EventStatus.Drinking,
                     "client": client_name,
                     "clock": clock,
                     "time": time_event})

"""Função para cadastrar a conclusão do evento de enchimento na timeline"""
def add_filling_event(client_name, waitress_name, time_event):
    global timeline

    timeline.append({"event": EventStatus.Filling,
                     "client": client_name,
                     "clock": clock,
                     "waitress": waitress_name,
                     "time": time_event})

"""Função para cadastrar a conclusão do evento de limpeza de copo na timeline"""
def add_cleaning_event(waitress_name):
    global timeline

    timeline.append({"event": EventStatus.Cleaning,
                     "clock": clock,
                     "waitress": waitress_name,
                     "time": 5})

"""Função para adicionar a tarefa de encher copo à fila de tarefas das garçonetes
OBS: Ainda falta adicionar a função de sort ao final desta função para a organização correta da fila"""
def add_filling_task(client_name):
    global list_tasks

    list_tasks.append({"event": EventStatus.Filling,
                       "client": client_name,
                       "time": get_time_fill(),
                       "waitress": None})
    #add list_tasks.sort(key=func)
"""Função para adicionar a tarefa de limpar copo à fila de tarefas das garçonetes
OBS: Ainda falta adicionar a função de sort ao final desta função para a organização correta da fila
"""
def add_cleaning_task():
    global list_tasks
    
    list_tasks.append({"event": EventStatus.Cleaning,
                       "time": 5,
                       "waitress": None})

    #add list_tasks.sort(key=func)

"""Função que resolve o evento de chegada de um cliente.
    1. Atera o estado do cliente
    2. Adiciona o cliente nas listas de clientes no sistema e na fila de espera
    3. Gera uma tarefa para encher na lista de tarefas das garçonetes
    4. Registra a chegada na timeline
"""
def resolve_arrive_event(event):
    global list_clients
    global list_arrivals
    global list_waiting

    client = event["client"]
    client.status = ClientStatus.Waiting
    client.queue_enter_time = clock
    
    list_clients.append(client)
    list_waiting.append(client)
    list_arrivals.remove(event)
    add_filling_task(client)
    add_arrival_event(client.name, event["time_arrival"])

"""Resolve o término da bebida de um cliente.
    1. Registra o evento na timeline
    2. Adiciona uma tarefa de limpeza na lista das garçonetes
    3. Se o cliente não quiser mais beber, ele sai do sistema, se ainda tiver bebidas,
    ele volta para a fila de espera e gera uma tarefa de encher na fila de tarefa das garçonetes
"""
def resolve_drink_event(client):
    global list_drinking
    global list_waiting

    list_drinking.remove(client)
    add_drink_event(client.name, client.drink_time)
    add_cleaning_task()

    if client.set_drinks() == -1:
        client.exit_time = clock
        client.status = ClientStatus.Exited
    else:
        list_waiting.append(client)
        client.enter_queue_time = clock
        client.status = ClientStatus.Waiting
        add_filling_task(client.name)

"""Resolve o termino da tarefa de encher da garçonete
    1. decrementa o número de copos disponíveis
    2. modifica o estado do cliente e altera as respectivas filas
    3. registra o término do evento na timeline
    4. se houver outras tarefas na fila, atribui a garçonete a estas tarefas. Senão altera seu estado para Available
"""
def resolve_filling_task(task, waitress):
    global list_waiting
    global list_drinking
    global num_glasses
    global list_tasks

    num_glasses -= 1

    client = find_client_by_name(task["client"])
    if client is None:
        return
    list_waiting.remove(client)
    list_drinking.append(client)
    add_filling_event(client.name, waitress.name, task["time"])

    client.status = ClientStatus.Drinking
    client.total_wait_time += clock - client.queue_enter_time
    client.drink_time = get_time_drink()

    waitress.time_filling += waitress.occupation_time
    new_task = find_task_unassigned()
    if new_task is None:
        waitress.status = WaitressStatus.Available
        waitress.occupation_time = 0
    elif new_task["event"] == EventStatus.Filling:
        new_task["waitress"] = waitress.name
        waitress.status = WaitressStatus.Filling
        waitress.occupation_time = new_task["time"]
    elif new_task["event"] == EventStatus.Cleaning:
        new_task[waitress] = waitress.name
        waitress.status = WaitressStatus.Cleaning
        waitress.occupation_time = new_task["time"]

"""Resolve a tarefa de limpeza de copos
    1. incrementa o número de copos no sistema
    2. se houver tarefas na lista, atribui a garçonete a tarefa. Senão altera seu estado para Available 
"""
def resolve_cleaning_task(waitress):
    global num_glasses
    global list_tasks

    num_glasses += 1
    add_cleaning_event(waitress.name)

    new_task = find_task_unassigned()
    if new_task is None:
        waitress.status = WaitressStatus.Available
        waitress.occupation_time = 0
    elif new_task["event"] == EventStatus.Filling:
        new_task["waitress"] = waitress.name
        waitress.status = WaitressStatus.Filling
        waitress.occupation_time = new_task["time"]
    elif new_task["event"] == EventStatus.Cleaning:
        new_task[waitress] = waitress.name
        waitress.status = WaitressStatus.Cleaning
        waitress.occupation_time = new_task["time"]
    
"""Printa o estado do sitema. Tempo do relógio e estado dos clientes e garçonetes do sistema
"""
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
        if clock > 30 and not list_tasks:
            break

