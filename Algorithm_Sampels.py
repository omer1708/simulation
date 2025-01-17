import random
import numpy as np

# 5. זמן טיפול בספא (פונקציה מותאמת)
def sample_spa_time():
    u = np.random.uniform(0, 1)
    if u < 0.5:
        return 0.5 + np.sqrt(u / 8)
    else:
        return 1 - np.sqrt((1 - u) / 8)

# 2. זמן שירות בר
def sample_bar_time():
    while True:
        u1, u2 = np.random.uniform(0, 1, 2)
        z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        X = z * np.sqrt(1.5) + 5
        if X >= 0:
            return X

# 3. זמן שהיה בסאונה רטובה
def sample_wet_sauna_time():
    while True:
        u1, u2 = np.random.uniform(0, 1, 2)
        z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        X = z * np.sqrt(5) + 15
        if X >= 0:
            return X

# 4. זמן שהיה בסאונה יבשה
def sample_dry_sauna_time():
    while True:
        u1, u2 = np.random.uniform(0, 1, 2)
        z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        X = z * np.sqrt(3) + 10
        if X >= 0:
            return X

def sample_breakfast_arrival():
    lower_bound = 6.5
    upper_bound = 11.5
    lmbda = 15

    u = np.random.uniform(0, 1)
    X = -np.log(1 - u * (1 - np.exp(-lmbda * lower_bound))) / lmbda

    if X <= upper_bound:
        return X
    else:
        return sample_breakfast_arrival()


# 6. זמן ארוחת בוקר
def sample_breakfast_time():
    while True:
        u1, u2 = np.random.uniform(0, 1, 2)
        z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        X = z * 10 + 40
        if X >= 0:
            return X

 # זמן שהייה בבריכה דגימה
def sample_time_at_pool():
    u = random.random()  # This generates a random float uniformly in the range [0.0, 1.0)

    if u < 0.25:
        return 60 * (np.sqrt(12 * u + 1))
    elif u < 0.875:
        return 60 * (-5 + np.sqrt(441 + 640 * u)) / 8
    else:
        return 60 * (3 + 8 * u)



def sample_length_stay_hotel():  #זמן שהייה במלון דגימה
    u = random.Random()
    if u < 0.25:
        return 1  # 1 night with probablity of 0.25
    elif u <0.25 + 0.46:
        return 2   #2 nights with probablity 0.46
    elif u< 0.25+0.46+0.2:
        return 3  #3 nights with probablity 0.2
    elif u < 0.25+0.46+0.2+0.05:
        return 4             #4 night with probablity 0.05
    else:         # 5 nights at probablity of 0.04
        return 5


def sample_check_in(rate=0.14):            #check in דגימה
    scale = 1 / rate
    return np.random.exponential(scale)


def sample_check_out(rate=0.2):            #check out דגימה
    scale = 1 / rate
    return np.random.exponential(scale)


# Example usage within a simulation framework
next_check_in = sample_check_in()
print(f"Next guest will check in after {next_check_in:.2f} units of time.")

next_check_out = sample_check_out()
print(f"Guest will check out after {next_check_out:.2f} units of time from check-in.")



Rtotal = 110
RoomAvailable = find_available_rooms()
averageRating = 7
B1 = 1.5
B2 = 2
alfa = 20


def sample_arrival_guest():
    if RoomAvailable > 0 :
        lamda = alfa * ((RoomAvailable/Rtotal)^B1 ) * (averageRating/10)^B2
        np.random.exponential(lamda)
    else:
        return None



