import heapq
import numpy as np
from Algorithm_Sampels import sample_arrival_guest, sample_time_at_pool, sample_bar_time
from Group import Group

class Event:
    def __init__(self, time):
        self.time = time

    def __lt__(self, other):
        return self.time < other.time

    def handle(self, queue):
        print("Handle method must be implemented by subclasses")
        pass



class ArrivalEvent(Event):
    def handle(self, simulation):
        # תזמון הגעה הבאה
        next_arrival_time = self.time + sample_arrival_guest()
        if next_arrival_time < simulation.simulation_time:
            simulation.schedule_event(ArrivalEvent(next_arrival_time))
        group = simulation.create_group()
        # חיפוש חדר פנוי
        for room in queue.rooms:
            if not room.is_occupied and room.capacity >= guest.group_size:
                room.check_in()
                guest.check_in(room)
                print(f"Guest {guest.guest_id} checked into room {room.room_id}.")
                break
        else:
            # אם אין חדר פנוי, הוספת האורח לרשימת המתנה
            queue.waiting_list.append(guest)
            print(f"Guest {guest.guest_id} added to waiting list.")



class ArrivalPoolEvent(Event):
    def __init__(self, time, guest):
        super().__init__(time)
        self.guest = guest  # Guest object

    def handle(self, simulation):
        if simulation.is_pool_available():
            # Assign the guest to the pool
            simulation.assign_to_pool(self.time, self.guest)
            print(f"Guest {self.guest.guest_name} entered the pool at {self.time}.")
            departure_time = self.time + sample_time_at_pool()
            if departure_time < simulation.simulation_time:
                simulation.schedule_event(PoolDepartureEvent(departure_time, self.guest))
        else:
            # Pool is full → Add guest to the queue
            simulation.pool_queue.append((self.guest, self.time))
            print(f"Guest {self.guest.guest_name} added to the pool queue at {self.time}.")

            # Schedule reneging event if the guest waits too long
            reneging_time = self.time + self.guest.generate_max_wait_time()
            if reneging_time < simulation.simulation_time:
                simulation.schedule_event(RenegingEvent(reneging_time, self.guest))

class PoolDepartureEvent(Event):
    def __init__(self, time, guest):
        super().__init__(time)
        self.guest = guest  # Store the guest for spa redirection

    def handle(self, simulation):
        # Guest leaves the pool → decrease occupancy
        simulation.current_occupancy -= 1
        print(f"Guest {self.guest.guest_name} has left the pool at {self.time}.")

        # If there are guests in the queue, let the next guest enter the pool
        if simulation.pool_queue:
            next_guest = simulation.pool_queue.pop(0)
            simulation.assign_to_pool(self.time, next_guest)

        # If the guest is a couple or single, schedule SpaArrivalEvent
        if self.guest.group_type in ['couple', 'single']:
            spa_arrival_time = self.time
            simulation.schedule_event(SpaArrivalEvent(spa_arrival_time, self.guest))



class RenegingEvent(Event):
    def __init__(self, time, guest):
        super().__init__(time)
        self.guest = guest


    def handle(self, queue):
        # Check if the customer is still in the queue
        def handle(self, simulation):
            if (self.guest, self.guest.guest_id) in simulation.pool_queue:
                simulation.pool_queue.remove((self.guest, self.guest.guest_id))
                print(f"Guest {self.guest.guest_id} ({self.guest.group_type}) reneged due to long wait at {self.time}.")


class BarArrivalEvent(Event):
    def __init__(self, time, guest):
        super().__init__(time)
        self.guest = guest
        self.time = time

    def handle(self, simulation):
        # הוספת הלקוח לתור
        if simulation.is_bar_available():
            simulation.assign_to_bar(self.time)
            process_order(self.guest)
        else:
            simulation.queue.append(self.time)


class BarDepartureEvent(Event):
    def __init__(self, time, guest):
        super().__init__(time)


class HotelSimulation:
    """
    מחלקה לניהול סימולציית המלון.
    """

    def __init__(self, arrival_rate, service_rate, simulation_time, pool_capacity,
                 num_bartenders):
       # initialize simulation
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_time = simulation_time

       #employees
        self.num_bartenders = num_bartenders

       #pool state
        self.pool_capacity = 50
        self.current_occupancy = 0
        self.pool_queue = []

        #bar state
        self.revenue = 0
        self.bartenders_busy = 0
        self.bar_queue = []

    def schedule_event(self, event):
        heapq.heappush(self.event_queue, event)

    def create_group(self):
        # בחירת סוג קבוצה: משפחה, זוג או יחיד
        group_type = np.random.choice(['family', 'couple', 'single'], p=[0.4, 0.4, 0.2])
        # הגדרת מספר אנשים בקבוצה לפי סוג
        if group_type == 'family':
            group_size = np.random.choice([3, 4, 5], p=[0.3, 0.2, 0.5])
        elif group_type == 'couple':
            group_size = 2
        else:  # 'single'
            group_size = 1
        # הגדרת האם הקבוצה בסוויטה
        suite = np.random.random() < 0.1 and group_type in ['couple', 'single']
        # יצירת והחזרת אובייקט קבוצה
        return Group(group_type, group_size, suite)


    def is_bar_available(self):
        return self.bartenders_busy < self.num_bartenders

    def assign_to_bar(self, time):
        self.bartenders_busy += 1
        service_time = sample_bar_time()  # זמן שירות ממוצע
        self.schedule_event(BarDepartureEvent(time + service_time))

    def process_order(self, guest):
        # בחירת משקה
        drink_probability = 0.5
        food_probability = 0.5
        drink_prices = {"coffee": 3, "juice": 3, "beer": 3, "wine": 10, "cocktail": 15}
        food_prices = {"toast": 10, "salad": 12, "ice_cream": 3, "nuggets": 15}

        total_cost = 0
        if np.random.rand() <= drink_probability:
            drink = np.random.choice(list(drink_prices.keys()))
            total_cost += drink_prices[drink]

        if np.random.rand() <= food_probability:
            food = np.random.choice(list(food_prices.keys()))
            total_cost += food_prices[food]

        return total_cost

    def is_pool_available(self):
        return self.current_occupancy < self.pool_capacity

    def assign_to_pool(self, time, guest):
        self.current_occupancy += 1
        stay_time = sample_time_at_pool()
        departure_time = time + stay_time
        self.schedule_event(PoolDepartureEvent(departure_time, guest))

    simulation_time_pool = 480

    def run(self):
        """
        הפעלת הסימולציה.
        """
        current_time = 0

        while self.event_list:
            event = self.event_list.pop(0)
            current_time = event["time"]

            if current_time > self.simulation_end_time:
                break

            print(f"Handling event: {event['type']} at time {current_time}.")
            if event["type"] == "arrival":
                self.handle_arrival(event["details"])
            elif event["type"] == "checkout":
                self.handle_checkout(event["details"])
            elif event["type"] == "rating_update":
                self.update_daily_rating()
            elif event["type"] == "activity":
                self.handle_activity(event["details"])