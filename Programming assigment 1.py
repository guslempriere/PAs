import random as random
import time
from tabulate import tabulate
random.seed(2026)
def main():
    data_table = []
    time_table = []
    for i in [1, 2, 3]:
        dim_data_list = [f"{i}D"]
        dim_time_list = [f"{i}D"]
        for j in [20, 200, 2000, 20000, 200000, 2000000]:
            time_taken, percent = do_thing(i, j, 100)
            dim_data_list.append(percent)
            dim_time_list.append(time_taken)
        data_table.append(dim_data_list)
        if i == 3:
            time_table.append(dim_time_list)
    
    data_headers = ["number of steps", "20", "200", "2000", "20000", "200000", "2000000"]
    table = tabulate(data_table, data_headers,  tablefmt = "grid")
    print(table)
    time_headers = ["time taken (s)", "20", "200", "2000", "20000", "200000", "2000000"]
    time_table = tabulate(time_table, time_headers, tablefmt = "grid", maxcolwidths = 6)
    print(time_table)
    
def do_thing(dimensions, maximum_steps, number_of_trials):
    time_start = time.time()
    trials_returning_to_zero = 0
    coords = []
    for i in range(number_of_trials):
        coords = [0 for i in range(dimensions)]
        for j in range(maximum_steps):
            coords[choose_dimension(dimensions)] += step_up_or_down()
            if check_if_at_zero(coords):
                trials_returning_to_zero += 1
                break
    time_end = time.time()
    percent_returning = trials_returning_to_zero * 100 / number_of_trials
    time_taken = float(time_end - time_start)
    return time_taken, percent_returning
    
def check_if_at_zero(coords):
    for i in coords:
        if i != 0:
            return False
    return True

def choose_dimension(n):
    return random.randint(0, n - 1)

def step_up_or_down():
    rand_list = [-1,1]
    return random.choice(rand_list)

main()