class Room:
    def __init__(self, room_number, room_type, capacity):
        self.room_number = room_number  # מזהה ייחודי.
        self.room_type = room_type  # סוג החדר.
        self.capacity = capacity  # הקיבולת המרבית.
        self.occupied = False  # האם החדר תפוס כרגע?
        self.days_occupied = 0  # מספר הימים שהחדר תפוס.
        self.current_guest = None  # שמירת פרטי האורח הנוכחי.

#        מסמן את החדר כתפוס כאשר אורח עושה צ'ק-אין.
    def check_in(self, guest):
        if self.occupied:
            raise ValueError(f"Room {self.room_number} is already occupied.")
        self.occupied = True
        self.current_guest = guest
        print(f"Room {self.room_number} is now occupied by {guest.name}.")

#        מסמן את החדר כלא תפוס כאשר אורח עושה צ'ק-אאוט.
    def check_out(self):
        if not self.occupied:
            raise ValueError(f"Room {self.room_number} is already vacant.")
        self.occupied = False
        self.current_guest = None
        self.days_occupied = 0  # איפוס מספר הימים שהחדר תפוס.
        print(f"Room {self.room_number} is now vacant.")


#       מפעיל אירוע הקשור לחדר זה
    def generate_event(self, event_type, *args):
        if event_type == "check_in":
            self.check_in(*args)
        elif event_type == "check_out":
            self.check_out()
        else:
            raise ValueError(f"Unknown event type: {event_type}")

    def get_status(self):
        return {
            "Room Number": self.room_number,
            "Type": self.room_type,
            "Capacity": self.capacity,
            "Occupied": self.occupied,
            "Days Occupied": self.days_occupied,
            "Average Rating": self.average_rating()
        }
