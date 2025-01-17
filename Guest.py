class Guest:
    def __init__(self, guest_name, group_type, group_size, stay_duration):
        self.guest_name = guest_name  # שם האורח
        self.group_type = group_type  # סוג הקבוצה
        self.group_size = group_size  # מספר האנשים בקבוצה
        self.stay_duration = stay_duration  # משך השהייה
        self.room = None  # החדר שהוקצה לאורח
        self.rating = 10  # דירוג אישי התחלתי של האורח
        self.wait_time = 0  # זמן המתנה מצטבר


    def generate_max_wait_time(self):
        if self.group_type == "family":
            return 10  # Max wait time for family
        elif self.group_type == "couple":
            return 15  # Max wait time for couple
        elif self.group_type == "single":
            return 20  # Max wait time for single

#         מבצע צ'ק-אין לאורח ומקצה לו חדר.
    def check_in(self, room):
        if self.room:
            raise ValueError(f"Guest {self.guest_id} is already checked in.")
        self.room = room
        room.check_in()
        print(f"Guest {self.guest_id} checked into room {room.room_number}.")

#         מבצע צ'ק-אאוט לאורח ומשחרר את החדר שהוקצה לו.
    def check_out(self):
        if not self.room:
            raise ValueError(f"Guest {self.guest_id} has no assigned room.")
        self.room.check_out()
        print(f"Guest {self.guest_id} checked out from room {self.room.room_number}.")
        self.room = None

#        מעדכן את הדירוג האישי של האורח.
    def update_rating(self, decrement):
        self.rating = max(0, self.rating - decrement)
        print(f"Guest {self.guest_id} rating updated to {self.rating:.2f}.")

#        מוסיף זמן המתנה לאורח.
    def add_wait_time(self, minutes):
        self.wait_time += minutes
        if self.wait_time > self.max_wait_time:
            self.update_rating(0.03)
            print(f"Guest {self.guest_id} exceeded max wait time.")
        else:
            print(f"Guest {self.guest_id} wait time increased by {minutes} minutes.")

#        גנרטור המבצע את פעילויות היום של האורח לפי סוג הקבוצה.
    def daily_schedule(self):
        if self.group_type == "family":
            yield f"Guest {self.guest_id}: Going to pool."
            yield f"Guest {self.guest_id}: Visiting bar."
        elif self.group_type == "couple":
            yield f"Guest {self.guest_id}: Visiting spa."
            yield f"Guest {self.guest_id}: Going to pool."
        elif self.group_type == "single":
            yield f"Guest {self.guest_id}: Going to pool."
            yield f"Guest {self.guest_id}: Visiting bar."

    def get_details(self):
        return {
            "Guest ID": self.guest_id,
            "Name": self.guest_name,
            "Group Type": self.group_type,
            "Group Size": self.group_size,
            "Stay Duration": self.stay_duration,
            "Room Number": self.room.room_number if self.room else None,
            "Rating": self.rating,
            "Wait Time": self.wait_time,
            "Max Wait Time": self.max_wait_time
        }
