class Hotel:
    def __init__(self):
        self.rooms = []  # רשימת חדרים במלון
        self.guests = []  # רשימת אורחים במלון
        self.reservations = []  # רשימת הזמנות במלון
        self.rating = 7.0  # דירוג ראשוני של המלון
        self.statistics = {  # סטטיסטיקות המלון
            "total_customers": 0,
            "total_checkins": 0,
            "total_checkouts": 0,
            "daily_ratings": [],
            "total_revenue": 0,
            "breakfast_visits": 0,
            "breakfast_departures": 0,
            "average_wait_time": 0,
        }

# יצירת חדרים במלון לפי סוגים וקיבולות מוגדרות מראש
    def create_rooms(self):
        for i in range(1, 31):
            self.rooms.append(Room(room_number=i, room_type="family_large", capacity=5))
        for i in range(31, 71):
            self.rooms.append(Room(room_number=i, room_type="family_medium", capacity=3))
        for i in range(71, 101):
            self.rooms.append(Room(room_number=i, room_type="couple", capacity=2))
        for i in range(101, 111):
            self.rooms.append(Room(room_number=i, room_type="suite", capacity=2))

# מוסיף אורח חדש לרשימת האורחים
    def add_guest(self, guest):
        self.guests.append(guest)
        self.update_statistics("total_customers", 1)
        print(f"Guest {guest.guest_id} added to the hotel.")

# מסיר אורח מהרשימה לאחר עזיבתו את המלון.
    def remove_guest(self, guest):
        if guest in self.guests:
            self.guests.remove(guest)
            print(f"Guest {guest.guest_id} removed from the hotel.")

#        יוצר הזמנה לאורח על ידי מציאת חדר פנוי.
    def create_reservation(self, guest):
        room = self.find_available_room(guest.group_size)
        if room:
            reservation = Reservation(guest, room, group_size=guest.group_size, stay_duration=guest.stay_duration)
            self.reservations.append(reservation)
            reservation.confirm_reservation()
            self.add_guest(guest)
            self.update_statistics("total_checkins", 1)
            print(f"Reservation created for Guest {guest.guest_id}.")
        else:
            print(f"No available room for Guest {guest.guest_id}. Adding to waitlist.")
#מבטל הזמנה קיימת במלון.
    def cancel_reservation(self, reservation):
        if reservation in self.reservations:
            reservation.cancel_reservation()
            self.reservations.remove(reservation)
            self.remove_guest(reservation.guest)
            self.update_statistics("total_checkouts", 1)
            print(f"Reservation for Guest {reservation.guest.guest_id} canceled.")

#      מחפש חדר פנוי שמתאים לגודל הקבוצה של האורח.
    def find_available_rooms(self):
        rooms_available = 0
        for room in self.rooms:
            if not room.occupied:  # Check if the room is not occupied
                rooms_available += 1  # Correctly increment the count of available rooms

        return rooms_available  # Return the total count of available rooms


    #        מנהל את סדר היום של כל האורחים במלון.

    def daily_activities(self):
        for guest in self.guests:
            guest.daily_schedule()

#        מעדכן את דירוג המלון על בסיס דירוגי כל האורחים.

    def update_rating(self):
        total_ratings = [guest.rating for guest in self.guests if guest.rating is not None]
        self.rating = sum(total_ratings) / len(total_ratings) if total_ratings else self.rating
        self.update_statistics("daily_ratings", self.rating)
        print(f"Hotel rating updated to {self.rating:.2f}.")

#        מחשב את התפוסה היומית של החדרים במלון.

    def calculate_daily_occupancy(self):
        occupied_rooms = sum(1 for room in self.rooms if room.occupied)
        daily_occupancy = (occupied_rooms / len(self.rooms)) * 100
        self.update_statistics("daily_occupancy", daily_occupancy)
        return daily_occupancy
#        מחשב את סך ההכנסות של המלון.

    def calculate_total_revenue(self):
        room_revenue = sum(room.calculate_revenue() for room in self.rooms)
        service_revenue = (  # הכנסות משירותים נוספים
            self.statistics["breakfast_visits"] * 250  # הכנסה לדוגמה מארוחת בוקר
        )
        total_revenue = room_revenue + service_revenue
        self.update_statistics("total_revenue", total_revenue)
        return total_revenue

    def get_hotel_status(self):
        return {
            "Hotel Rating": self.rating,
            "Rooms": [room.get_status() for room in self.rooms],
            "Guests": [guest.get_details() for guest in self.guests],
            "Reservations": [reservation.get_reservation_details() for reservation in self.reservations]
        }

#        מעדכן סטטיסטיקות של המלון.

    def update_statistics(self, stat_key, value):
        if stat_key in self.statistics:
            if isinstance(self.statistics[stat_key], list):
                self.statistics[stat_key].append(value)
            else:
                self.statistics[stat_key] += value
        else:
            print(f"Statistic {stat_key} not found.")


