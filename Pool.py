import random
class Pool:

    def __init__(self, capacity):
        self.capacity = capacity  # קיבולת מקסימלית
        self.current_occupancy = 0  # מספר האנשים שנמצאים כרגע בבריכה
        self.waiting_list = []  # רשימת המתנה עבור הבריכה

        # סטטיסטיקות
        self.total_visits = 0  # סך כל הביקורים בבריכה
        self.total_wait_time = 0  # סך כל זמני ההמתנה בבריכה
        self.total_stay_time = 0  # סך כל זמני השהייה בבריכה

#        הוספת קבוצה לבריכה אם יש מקום פנוי.
    def enter_pool(self, guest):
        if self.current_occupancy  <= self.capacity:
            self.current_occupancy +=1
            self.total_visits += 1  # עדכון סטטיסטיקה של ביקורים
            print(f"Guest {guest.guest_id} entered the pool. Total in pool: {self.current_occupancy}.")
            stay_time = sample_time_at_pool()
            retun stay_time
        else:
            self.add_to_waiting_list(guest)
            print(f"No space in the pool. Guest {guest.guest_id} added to the waiting list.")

#        הוצאת קבוצה מהבריכה.
    def leave_pool(self, group_size):
        if self.current_occupancy - group_size >= 0:
            self.current_occupancy -= group_size
            print(f"{group_size} אנשים עזבו את הבריכה. סך הכל בבריכה: {self.current_occupancy}.")
        else:
            print(f"שגיאה: ניסיון להוציא יותר אנשים ממה שנמצאים בבריכה. {group_size} אנשים.")
            self.current_occupancy = 0

        # הכנסה של אנשים מרשימת ההמתנה אם יש מקום
        while self.waiting_list and self.current_occupancy + self.waiting_list[0]['group_size'] <= self.capacity:
            next_guest = self.waiting_list.pop(0)
            wait_time = self.sample_wait_time(next_guest['time_added'])
            self.total_wait_time += wait_time  # עדכון סטטיסטיקת זמן המתנה
            print(f"Group of {next_guest['group_size']} waited {wait_time:.2f} minutes.")
            self.enter_pool(next_guest['group_size'], next_guest['guest'])

#        מוסיף קבוצה לרשימת ההמתנה.
    def add_to_waiting_list(self, group_size, guest):
        self.waiting_list.append({"group_size": group_size, "guest": guest, "time_added": 0})
        print(f"קבוצה בגודל {group_size} נוספה לרשימת ההמתנה.")

#        סימולציה של זמן שהייה בבריכה.
    def sample_stay_time(self, group_size):
        stay_time = max(0, random.normalvariate(60, 15))  # זמן ממוצע של 60 דקות עם סטיית תקן של 15 דקות
        self.total_stay_time += stay_time  # עדכון סטטיסטיקת זמן שהייה
        print(f"קבוצה בגודל {group_size} תשהה בבריכה למשך {stay_time:.2f} דקות.")
        return stay_time

#        זימון אורח לבריכה.
    def schedule_visit(self, guest):
        print(f"Guest {guest.guest_id} is visiting the pool.")
        self.enter_pool(guest.group_size, guest)
        self.sample_stay_time(guest.group_size)

#זמן המתנה בבריכה
    def sample_wait_time(self, time_added):
        return max(0, random.uniform(5, 15))  # זמן המתנה ממוצע של בין 5 ל-15 דקות

#        מחזיר את הסטטוס הנוכחי של הבריכה.
    def get_status(self):
        return {
            "Current Occupancy": self.current_occupancy,
            "Waiting List": len(self.waiting_list),
            "Max Capacity": self.capacity,
            "Total Visits": self.total_visits,
            "Total Wait Time": self.total_wait_time,
            "Total Stay Time": self.total_stay_time,
        }
