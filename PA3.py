import tabulate as tabulate
import random as random

SECONDS_PER_ITEM = 4
OVERHEAD_SECONDS = 45
AVG_CUSTOMER_TIME = 30
EXPRESS_COUNT = 1
REGULAR_COUNT = 4
LOWEST_NUMBER_OF_ITEMS = 6
HIGHEST_NUMBER_OF_ITEMS = 20

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []
    
    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    
class Register:
    #initializes Register and values to keep track of
    def __init__(self, is_express = False):
        self._is_express = is_express
        self._queue = Queue()
        self._customers_served = 0
        self._items_served = 0
        self._idle_time = 0
        self._time_at_least_one_customer = 0
        self._current_job = None
        self._time_left_on_current_job = 0
    
    def __repr__(self):
        return str(self._items_served)
    #adds a customer to the register
    def add_customer(self, new_customer):
        self._queue.enqueue(new_customer)
    
    #deques customer at front of line 
    def checkout_customer(self):
        self._current_job = self._queue.dequeue()
        self._time_left_on_current_job = OVERHEAD_SECONDS + self._current_job.get_number_of_items() * 4
    
    def tick(self):
        #check if register has a job
        if self._current_job == None:
            #if queue is empty, add to idle time
            if self._queue.isEmpty():
                self._idle_time += 1
            #if queue is not empty, dequeue next customer
            else:
                self.checkout_customer()
        else:
            #tick one second off current job
            self._time_left_on_current_job -= 1
            #if time left on current job is zero (job is done), add to items and customers served and make current job = None
            if self._time_left_on_current_job == 0:
                self._customers_served += 1
                self._items_served += self._current_job.get_number_of_items()
                self._current_job = None
            #if job has time left, subract one second from time
            else:
                self._time_left_on_current_job -= 1
        #if there are poeple in line, add to that counter
        if not(self._queue.isEmpty()):
            self._time_at_least_one_customer += 1

            
    #returns number of customers in line
    def get_customers_in_line(self):
        return self._queue.size()
    
    #returns True if express, False if regular
    def get_type(self):
        return self._is_express
    
    def get_queue(self):
        return self._queue
    
    def get_stats(self):
        return [self._customers_served, self._items_served, self._idle_time,
                self._time_at_least_one_customer]
    
    def get_current_job(self):
        return self._current_job


class Customer:
    #initialize customer class with a random number of items between specified constants
    def __init__(self):
        self._number_of_items = random.randint(LOWEST_NUMBER_OF_ITEMS, HIGHEST_NUMBER_OF_ITEMS)
   
    #repr function for purpose of debugging
    def __repr__(self):
        return str(self._number_of_items)
    
    def get_number_of_items(self):
        return self._number_of_items
    

#searches for register with smallest line and returns that register object
def find_smallest_line(register_list):
    smallest_line = register_list[0].get_customers_in_line()
    smallest_register = register_list[0]
    for register in register_list:
        line = register.get_customers_in_line()
        if line < smallest_line:
            smallest_line = line
            smallest_register = register
    return smallest_register

def assign_register(new_customer, express_registers, regular_registers):
    #if express eligible, assign to empty express lane, if no empty express lane, assign to smallest lane
    done = False
    if new_customer.get_number_of_items() <= 10:
        register_number = 0
        while not(done) and (register_number < len(express_registers)):
            if express_registers[register_number].get_customers_in_line() == 0:
                express_registers[register_number].add_customer(new_customer)
                done = True
                print("register assigned")
        #if no express register with 0 customers in line, finds register
        #with smallest line and adds customer to that register
        if not done:
            smallest_line = find_smallest_line(express_registers + regular_registers)
            smallest_line.add_customer(new_customer)
            print("register assigned")
    #if not express eligible, adds to smallest non express lane
    else:
        smallest_regular_line = find_smallest_line(regular_registers)
        smallest_regular_line.add_customer(new_customer)
        print("register assigned")



#print info about registers every 50 seconds
#show number of items in current job and all jobs in queue
def fifty_second_check(register_list, second):
    register_counter = 0
    print(f"time = {second}\nreg#\tcustomers")
    for register in register_list:
        #if register has no job, display "--"
        if register.get_current_job() == None:
            print(f"{register_counter}.\t\t--")
        else:
            #display the number of items in the current job
            print(f"{register_counter}.\t\t{register.get_current_job().get_number_of_items()}", 
                  end = "")
            #if customers in line, display the number of items for each customer in line
            if register.get_customers_in_line() > 0:
                print(" | ")
                for waiting_customer in range(register.get_queue().size()):
                    print("kms
        register_counter += 1
        
def main():
    for sim_number in range(1):
        express_registers = [Register(True) for i in range(EXPRESS_COUNT)]
        regular_registers = [Register() for i in range(REGULAR_COUNT)]
        for second in range(500):
            #add a customer to registers every thirty seconds
            #run the 50 second check eveyr 50 seconds
            if second % 30 == 0:
                new_customer = Customer()
                print(new_customer.get_number_of_items())
                assign_register(new_customer, express_registers, regular_registers)
            for register in express_registers:
                register.tick()
            for register in regular_registers:
                register.tick()
            if second % 50 == 0:
                fifty_second_check(express_registers + regular_registers, second)
    for register in express_registers + regular_registers:
        print(register.get_stats())
        
        
main()