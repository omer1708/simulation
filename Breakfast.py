import random

class Breakfast:

    def __init__(self, max_guests=60, start_time=6.5, end_time=11.5):
        self.max_guests = max_guests  # הקיבולת המקסימלית
        self.start_time = start_time  # שעת פתיחה
        self.end_time = end_time  # שעת סגירה
        self.current_guests = 0  # מספר האורחים שנמצאים כעת
        self.waiting_list = []  # רשימת המתנה

        # סטטיסטיקות
        self.total_visits = 0  # סך כל הביקורים בארוחת הבוקר
        self.total_wait_time = 0  # סך כל זמני ההמתנה
        self.total_revenue = 0  # סך ההכנסות מארוחת הבוקר

#        בודק אם חדר האוכל פתוח בשעה הנוכחית.

    def is_open(self, current_time):
        return self.start_time <= current_time <= self.end_time

#        מושיב אורחים לארוחת הבוקר אם יש מקום פנוי.
    def seat_guests(self, guests, current_time):
        groups = [5] * (guests // 5) + ([guests % 5] if guests % 5 != 0 else [])

        seated = False
        for group in groups:
            if self.current_guests + group <= self.max_guests:
                self.current_guests += group
                self.total_visits += group  # עדכון סטטיסטיקה של ביקורים
                self.total_revenue += group * 250  # עדכון הכנסות (250$ לאדם)
                print(f"Seated a group of {group} guests. Current total: {self.current_guests}.")
                seated = True
            else:
                self.add_to_waiting_list(group, current_time)

        return seated

#        מוסיף אורחים לרשימת ההמתנה.

    def add_to_waiting_list(self, guests, current_time):
        self.waiting_list.append({"group_size": guests, "time_added": current_time})
        print(f"Added a group of {guests} to the waiting list. Total waiting: {len(self.waiting_list)}.")

#        משחרר מקום לאחר סיום ארוחת הבוקר של אורחים.
    def clear_table(self, guests):
        self.current_guests -= guests
        print(f"Cleared a table for {guests} guests. Current total: {self.current_guests}.")

        # מושיב אורחים מרשימת ההמתנה אם יש מקום
        while self.waiting_list and self.current_guests + self.waiting_list[0]["group_size"] <= self.max_guests:
            next_group = self.waiting_list.pop(0)
            wait_time = self.sample_wait_time(next_group["time_added"])
            self.total_wait_time += wait_time  # עדכון סטטיסטיקת זמן המתנה
            print(f"Group of {next_group['group_size']} waited {wait_time:.2f} minutes.")
            self.seat_guests(next_group["group_size"], current_time=self.start_time)

#        מחשב את זמן ההמתנה של קבוצה לפי זמן ההוספה לרשימה.
    def sample_wait_time(self, time_added):
        return max(0, self.start_time - time_added)

#        סימולציה של זמן שהייה בארוחת הבוקר לפי התפלגות נורמלית.

    def sample_breakfast_time(self):
        return max(0, random.normalvariate(45, 10))  # זמן ממוצע של 45 דקות עם סטיית תקן של 10 דקות

#        מדמה האם האוכל היה לטעם האורח ומשפיע על הדירוג.
    def rate_food(self, guest):
        if random.random() < 0.1:  # סיכוי של 10% שהאוכל לא ימצא חן
            guest.update_rating(0.025)
            print(f"Guest {guest.guest_id} did not like the breakfast. Rating decreased.")

    def get_status(self):
        return {
            "Current Guests": self.current_guests,
            "Waiting List": len(self.waiting_list),
            "Max Guests": self.max_guests,
            "Total Visits": self.total_visits,
            "Total Wait Time": self.total_wait_time,
            "Total Revenue": self.total_revenue,
        }
