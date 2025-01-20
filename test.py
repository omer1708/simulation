import heapq
import random
import numpy as np


def sample_check_in():
    rate = 0.14
    scale = 1 / rate
    return np.random.exponential(scale)


def sample_check_out():
    rate = 0.2
    scale = 1 / rate
    return np.random.exponential(scale)


def sample_length_stay_hotel():
    u = random.random()
    if u < 0.25:
        return 1
    elif u < 0.25 + 0.46:
        return 2
    elif u < 0.25 + 0.46 + 0.2:
        return 3
    elif u < 0.25 + 0.46 + 0.2 + 0.05:
        return 4
    else:
        return 5


def sample_arrival_guest(hotel):
    rooms_total = 110
    rooms_available = hotel.available_rooms_count
    average_rating = hotel.rating
    b1 = 1.5
    b2 = 2
    a = 20
    if rooms_available > 0:
        lamda = a * ((rooms_available / rooms_total) ** b1) * (average_rating / 10) ** b2
        return np.random.exponential(lamda)
    return None


def sample_breakfast_arrival():
    rate = 15 / 60  # converting per hour to per minute
    return np.random.exponential(1 / rate)  # the scale parameter is the inverse of rate

# 6. זמן ארוחת בוקר
def sample_breakfast_time():
    while True:
        u1, u2 = np.random.uniform(0, 1, 2)
        z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        X = z * 10 + 40
        if X >= 0:
            return X


class Hotel:
    def __init__(self):
        self.rooms = []  # List of rooms in the hotel
        self.create_rooms()
        self.rating = 7.0  # Initial rating of the hotel
        self.available_rooms_count = 110  # Initially set to total number of rooms, adjusted below
        print("Hotel initialized with 110 rooms and rating of 7")

    def create_rooms(self):
        # Creating different types of rooms
        for i in range(1, 31):
            self.rooms.append(Room(room_number=i, room_type="family", max_capacity=5, min_capacity=4))
        for i in range(31, 71):
            self.rooms.append(Room(room_number=i, room_type="family", max_capacity=3, min_capacity=2))
        for i in range(71, 101):
            self.rooms.append(Room(room_number=i, room_type="couple", max_capacity=2, min_capacity=1))
        for i in range(101, 111):
            self.rooms.append(Room(room_number=i, room_type="suite", max_capacity=2, min_capacity=1))
        print("Rooms created.")


    def find_available_room(self, group_size, group_type, suite):
        # Finding a suitable room based on group type, size and whether it's a suite
        print(f"Finding available room for group of type {group_type}, size {group_size}, suite={suite}.")
        for room in self.rooms:
            if not room.occupied and room.max_capacity >= group_size >= room.min_capacity:
                if suite == (room.room_type == 'suite'):
                    print(f"Room {room.room_number} found for the group.")
                    return room
        print("No suitable room found.")
        return None

    def available_rooms(self):
        # Calculate the number of available rooms
        return sum(1 for room in self.rooms if not room.occupied)

    def update_available_rooms(self):
        # Update the available rooms count property
        self.available_rooms_count = self.available_rooms()



class Room:
    def __init__(self, room_number, room_type, max_capacity, min_capacity):
        self.room_number = room_number  # מזהה ייחודי.
        self.room_type = room_type  # סוג החדר.
        self.max_capacity = max_capacity  # הקיבולת המרבית.
        self.min_capacity = min_capacity  # הקיבולת המרבית.
        self.occupied = False  # האם החדר תפוס כרגע?
        self.group = None
        self.remaining_days = 0
        self.price = 0

    def check_in(self, group):
        self.occupied = True
        self.group = group


    def check_out(self):
        self.occupied = False
        self.group = None
        self.remaining_days = 0
        print(f"Room {self.room_number} checked out.")


class Group:
    def __init__(self, group_type, group_size, suite):
        self.group_type = group_type  # סוג הקבוצה
        self.group_size = group_size  # מספר אנשים בקבוצה
        self.suite = suite  # האם הקבוצה בסוויטה
        self.room = None

    def check_in(self, room):
        self.room = room

    def check_out(self):
        self.room = None





class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def handle(self, simulation):
        print("Handle method must be implemented by subclasses")
        pass


class ArrivalEvent(Event):
    def handle(self, simulation):
        if simulation.hotel.available_rooms() > 0:
            print(f"new guest arrived to the hotel at time {simulation.hour(self.time)}")
            # אם הלקוח הגיע עד 17
            next_arrival_time = self.time + sample_arrival_guest(simulation.hotel)
            if next_arrival_time%1440 <= 17*60 and next_arrival_time < simulation.simulation_time:
                simulation.schedule_event(ArrivalEvent(next_arrival_time))
            group = simulation.create_group()
            print(f"Group created: {group.group_type}, size {group.group_size}, suite={group.suite}")
            room = simulation.hotel.find_available_room(group.group_size, group.group_type, group.suite)
            if room:
                room.check_in(group)
                group.check_in(room)
                room.price = 250 * group.group_size + (120 if room.suite else 0)
                room.remaining_days = sample_length_stay_hotel()
                print(f"Room {room.room_number} checked in for {room.remaining_days} days.")
                if simulation.is_reception_available():
                    simulation.assign_to_reception(self.time, group, 'checkin')
                else:
                    simulation.reception_queue.append((self.time ,group, 'checkin'))
            else:
                print("No room available, guest leaves.")



class CheckInEvent(Event):
    def handle(self, simulation):
        simulation.completed_checkin += 1
        print(f"the group finished check in event at time {simulation.hour(self.time)}")
        if self.time%1440 <= 15*60:
            print("schedule pool event at 15:00")
           # simulation.schedule_event(PoolEvent(15*60))
        else:
            print("go straight to pool")
            #simulation.schedule_event(PoolEvent(self.time))
        simulation.reception_busy -= 1
        if simulation.reception_queue:
            time, group, service = simulation.reception_queue.pop(0)
            simulation.assign_to_reception(self.time, group, service)



class CheckOutEvent(Event):
    def handle(self, simulation):
        simulation.completed_checkout += 1
        print(f"the group finished check out event at time {simulation.hour(self.time)}")
        simulation.reception_busy -= 1
        if simulation.reception_queue:
            time, group, service = simulation.reception_queue.pop(0)
            simulation.assign_to_reception(self.time, group, service)


class EndOfDayEvent(Event):
    def handle(self, simulation):
        # תזמון האירוע הבא של סוף היום לחצות הבאה ואירוע הגעה ל-8 בבוקר
        next_end_of_day = self.time + 1440  # הוספת 24 שעות לזמן הנוכחי
        if next_end_of_day < simulation.simulation_time:
            simulation.schedule_event(EndOfDayEvent(next_end_of_day))

        # איסוף רשימת החדרים התפוסים שצריכים להגיע מחר לארוחת בוקר
        occupied_rooms = [room for room in simulation.hotel.rooms if room.occupied]

        # עדכון מספר החדרים הזמינים (לפני שינוי מצב החדרים בצ'ק אאוט)
        simulation.hotel.update_available_rooms()

        # ביצוע שינויים: עדכון מצב החדרים שצריכים לבצע צ'ק אאוט
        check_out_tomorrow = 0
        for room in occupied_rooms:
            room.remaining_days -= 1
            if room.remaining_days == 0:
                check_out_tomorrow += 1
                room.occupied = False

        print(len(occupied_rooms))

        # יצירת אירועי תחילת יום לכל החדרים התפוסים
        start_time = self.time + 6.5 * 60
        while occupied_rooms:
            random_room = random.choice(occupied_rooms)
            occupied_rooms.remove(random_room)
            next_arrival_time = start_time + sample_breakfast_arrival()
            if next_arrival_time < simulation.simulation_time:
                if random_room.remaining_days == 0 and next_arrival_time % 1440 >= 11 * 60:  # מוודא שמי שצריך לעשות צ'ק אאוט יגיע עד 11 לקבלה
                    if simulation.is_reception_available():
                        simulation.assign_to_reception(self.time+11*60, random_room.group, 'checkout')
                    else:
                        simulation.reception_queue.append((self.time+11*60, random_room.group, 'checkout'))
                else:
                    simulation.schedule_event(StartOfDayEvent(next_arrival_time, random_room))
            start_time = next_arrival_time

        simulation.hotel.update_available_rooms()
        if simulation.hotel.available_rooms_count > 0:
            simulation.schedule_event(ArrivalEvent(self.time + 8*60))

        # הדפסת סיכום יום (לפני השינויים בצ'ק אאוט)
        print(f"\nDay {self.time // 1440} ended")
        print(f"Number of guests checked in today: {simulation.completed_checkin}")
        print(f"Number of guests checked out today: {simulation.completed_checkout}")
        print(f"Number of guests will check out tomorrow: {check_out_tomorrow}")
        print(f"Rooms available: {simulation.hotel.available_rooms_count}\n")

        # איפוס ספירת צ'ק אין וצ'ק אאוט ליום הבא
        simulation.completed_checkin = 0
        simulation.completed_checkout = 0
        simulation.count=0



class StartOfDayEvent(Event):
    def __init__(self, time, room):
        super().__init__(time)
        self.room = room

    def handle(self, simulation):
        if self.room.remaining_days == 0:# אם הם צריכים לעשות צק אאוט היום
                if simulation.is_breakfast_available(self.room.group):
                    simulation.assign_to_breakfast(self.time, self.room.group, check_out_day=True)
                else:
                    simulation.breakfast_queue.append((self.room.group, True))

        elif self.room.remaining_days > 0: # אם לא צריכים לעשות צק אאוט
            #אם קמו לפני 11:30 שלח לארוחת בוקר
            if self.time % 1440 < 11.5*60:
                if simulation.is_breakfast_available(self.room.group):
                    simulation.assign_to_breakfast(self.time, self.room.group, check_out_day=False)
                else:
                    simulation.breakfast_queue.append((self.room.group, False))
            else: # אם לא התעוררו לארוחת בוקר שימשיכו ביום שלהם
                print(f"room {self.room.room_number} waked up at time {simulation.hour(self.time)} and missed breakfast.")



class BreakfastDepartureEvent(Event):
    def __init__(self, time, group):
        super().__init__(time)
        self.group = group

    def handle(self, simulation):
        group_size = self.group.group_size
        simulation.current_breakfast_occupancy -= group_size
        print(f"Group of {group_size} left breakfast at time {simulation.hour(self.time)}. Current occupancy: {simulation.current_breakfast_occupancy}")
        if simulation.breakfast_queue:
            next_group, check_out_day = simulation.breakfast_queue.pop(0)
            if simulation.is_breakfast_available(next_group):
                simulation.assign_to_breakfast(self.time, next_group, check_out_day)

    # אם הקבוצה ביום צק אאוט
class BreakfastDepartureEvent2(Event):
    def __init__(self, time, group):
        super().__init__(time)
        self.group = group

    def handle(self, simulation):
        group_size = self.group.group_size
        simulation.current_breakfast_occupancy -= group_size
        print(f"Group of {group_size} left breakfast at time {simulation.hour(self.time)}. Current occupancy: {simulation.current_breakfast_occupancy}")
        if simulation.breakfast_queue:
            next_group, check_out_day = simulation.breakfast_queue.pop(0)
            if simulation.is_breakfast_available(next_group):
                simulation.assign_to_breakfast(self.time, next_group, check_out_day)
        if simulation.is_reception_available():
            simulation.assign_to_reception(self.time, self.group, 'checkout')
        else:
            simulation.reception_queue.append((self.time, self.group, 'checkout'))



class HotelSimulation:
    def __init__(self, simulation_time):
        self.hotel = Hotel()
        self.event_queue = []
        self.simulation_time = simulation_time
        self.num_receptionists = 2
        self.reception_busy = 0
        self.reception_queue = []
        self.breakfast_capacity = 60
        self.breakfast_queue = []
        self.current_breakfast_occupancy = 0
        print(f"Hotel simulation started with {simulation_time} simulation time.")
        self.completed_checkin = 0
        self.completed_checkout = 0
        self.count = 0


    def schedule_event(self, event):
        heapq.heappush(self.event_queue, event)

    def hour(self, time):
        minutes_in_day = time % 1440
        hour = round(minutes_in_day // 60)
        minute = round(minutes_in_day % 60)
        return f"{hour:02}:{minute:02}"


    def create_group(self):
        group_type = np.random.choice(['family', 'couple', 'single'], p=[0.4, 0.4, 0.2])
        if group_type == 'family':
            group_size = np.random.choice([3, 4, 5], p=[0.3, 0.2, 0.5])
        elif group_type == 'couple':
            group_size = 2
        else:
            group_size = 1
        suite = np.random.random() < 0.1 and group_type in ['couple', 'single']
        return Group(group_type, group_size, suite)

    def is_reception_available(self):
        return self.reception_busy < self.num_receptionists

    def is_breakfast_available(self, group):
        return self.current_breakfast_occupancy + group.group_size <= self.breakfast_capacity

    def assign_to_reception(self, time, group, service_type):
        if service_type == 'checkin':
            self.reception_busy += 1  # מסמנים שעמדה תפוסה
            service_time = sample_check_in()  # חישוב זמן השירות
            self.schedule_event(CheckInEvent(time + service_time))
            print(f"group started to check in for room {group.room.room_number} at {self.hour(time)}. service time: {service_time}")

        if service_type == 'checkout':
            self.reception_busy += 1  # מסמנים שעמדה תפוסה
            group.room.check_out()
            group.check_out()
            service_time = sample_check_out()  # חישוב זמן השירות
            self.schedule_event(CheckOutEvent(time + service_time))
            print(f"group started check out at time {self.hour(time)}. service time: {service_time}")



    def assign_to_breakfast(self, time, group, check_out_day):
        print(f"Group of {group.group_size} arrived to breakfast at time {self.hour(time)}. Current occupancy: {simulation.current_breakfast_occupancy}")
        group_size = group.group_size
        breakfast_departure_time = time + sample_breakfast_time()
        self.current_breakfast_occupancy += group_size
        if check_out_day:
            if breakfast_departure_time % 1440 > 11 * 60:
                self.schedule_event(BreakfastDepartureEvent2((time // 1440) * 1440 + 11 * 60, group))
            else:
                self.schedule_event(BreakfastDepartureEvent2(breakfast_departure_time, group))
        else:
            if breakfast_departure_time % 1440 > 11.5 * 60:
                self.schedule_event(BreakfastDepartureEvent((time // 1440) * 1440 + 11.5 * 60, group))
            else:
                self.schedule_event(BreakfastDepartureEvent(breakfast_departure_time, group))





    def run(self):
        print("Starting simulation...")
        self.schedule_event(ArrivalEvent(480))
        self.schedule_event(EndOfDayEvent(1440))
        while self.event_queue and self.event_queue[0].time < self.simulation_time:
            event = heapq.heappop(self.event_queue)
            event.handle(self)




# יצירת אובייקט סימולציה והרצתה
simulation = HotelSimulation(simulation_time=14401)
simulation.run()
