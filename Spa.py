import random
class Spa:

    def __init__(self):

        self.room_capacity = 3  # מספר חדרי טיפול זוגיים
        self.salt_pool_capacity = 10  # מקסימום אנשים בבריכת מלח
        self.sauna_capacity = 10  # מקסימום אנשים בכל סאונה (רטובה/יבשה)
        self.therapists = 4  # מספר המטפלים הזמינים

        self.room_occupancy = 0  # מספר חדרי הטיפול בשימוש
        self.salt_pool_occupancy = 0  # מספר האנשים בבריכת מלח
        self.sauna_occupancy = {"wet": 0, "dry": 0}  # תפוסת הסאונות

        self.waiting_list = []  # רשימת המתנה לספא

        # סטטיסטיקות
        self.total_visits = 0  # סך כל הביקורים בספא
        self.total_revenue = 0  # סך ההכנסות מהספא
        self.total_wait_time = 0  # סך זמני ההמתנה בכל השירותים
        self.total_service_time = 0  # סך זמני השירות בכל השירותים

#        הוספת קבוצה לבריכת המלח אם יש מקום פנוי.
    def enter_salt_pool(self, group_size):
        if self.salt_pool_occupancy + group_size <= self.salt_pool_capacity:
            self.salt_pool_occupancy += group_size
            self.total_visits += group_size
            self.total_revenue += group_size * 50  # הכנסה של 50$ לאדם לבריכת מלח
            print(f"{group_size} אנשים נכנסו לבריכת המלח. סך הכל בבריכה: {self.salt_pool_occupancy}.")
        else:
            self.add_to_waiting_list("salt_pool", group_size)
            print(f"אין מקום בבריכת המלח. {group_size} אנשים נוספו לרשימת ההמתנה.")

#        הוצאת קבוצה מבריכת המלח.
    def leave_salt_pool(self, group_size):
        self.salt_pool_occupancy -= group_size
        print(f"{group_size} אנשים עזבו את בריכת המלח. סך הכל בבריכה: {self.salt_pool_occupancy}.")

        # הכנסה של אנשים מרשימת ההמתנה
        self._process_waiting_list("salt_pool")

#        הוספת קבוצה לסאונה אם יש מקום פנוי.
    def enter_sauna(self, group_size, sauna_type):
        if self.sauna_occupancy[sauna_type] + group_size <= self.sauna_capacity:
            self.sauna_occupancy[sauna_type] += group_size
            self.total_visits += group_size
            self.total_revenue += group_size * 30  # הכנסה של 30$ לאדם לסאונה
            print(f"{group_size} אנשים נכנסו לסאונה {sauna_type}. סך הכל בסאונה: {self.sauna_occupancy[sauna_type]}.")
        else:
            self.add_to_waiting_list("sauna", group_size, sauna_type)
            print(f"אין מקום בסאונה {sauna_type}. {group_size} אנשים נוספו לרשימת ההמתנה.")

#        הוצאת קבוצה מהסאונה.
    def leave_sauna(self, group_size, sauna_type):
        self.sauna_occupancy[sauna_type] -= group_size
        print(f"{group_size} אנשים עזבו את הסאונה {sauna_type}. סך הכל בסאונה: {self.sauna_occupancy[sauna_type]}.")

        # הכנסה של אנשים מרשימת ההמתנה
        self._process_waiting_list("sauna", sauna_type)

#התחלת טיפול זוגי.
    def start_treatment(self, group_size):
        if self.room_occupancy + 1 <= self.room_capacity and group_size * 2 <= self.therapists:
            self.room_occupancy += 1
            self.therapists -= group_size * 2
            self.total_visits += group_size
            self.total_revenue += group_size * 100  # הכנסה של 100$ לאדם לטיפול זוגי
            print(f"חדר טיפול זוגי בשימוש. {group_size} מטופלים החלו טיפול. מטפלים זמינים: {self.therapists}.")
        else:
            self.add_to_waiting_list("treatment", group_size)
            print(f"אין מקום בטיפול זוגי. {group_size} אנשים נוספו לרשימת ההמתנה.")

# סיום טיפול זוגי.
    def end_treatment(self, group_size):
        self.room_occupancy -= 1
        self.therapists += group_size * 2
        print(f"חדר טיפול זוגי שוחרר. {group_size} מטופלים סיימו טיפול. מטפלים זמינים: {self.therapists}.")

        # הכנסה של אנשים מרשימת ההמתנה
        self._process_waiting_list("treatment")

#        מוסיף קבוצה לרשימת ההמתנה עבור שירות מסוים.
    def add_to_waiting_list(self, service_type, group_size, sauna_type=None):
        entry = {"service_type": service_type, "group_size": group_size}
        if sauna_type:
            entry["sauna_type"] = sauna_type
        self.waiting_list.append(entry)
        print(f"קבוצה בגודל {group_size} נוספה לרשימת ההמתנה עבור {service_type}.")

#        מטפל ברשימת ההמתנה עבור שירותים שונים בספא.
    def _process_waiting_list(self, service_type, sauna_type=None):
        for entry in self.waiting_list:
            if service_type == "treatment" and entry["service_type"] == "treatment":
                self.start_treatment(entry["group_size"])
                self.waiting_list.remove(entry)
            elif service_type == "salt_pool" and entry["service_type"] == "salt_pool":
                self.enter_salt_pool(entry["group_size"])
                self.waiting_list.remove(entry)
            elif service_type == "sauna" and entry["service_type"] == "sauna" and entry.get("sauna_type") == sauna_type:
                self.enter_sauna(entry["group_size"], sauna_type)
                self.waiting_list.remove(entry)

#        מדמה זמן שירות לפי סוג השירות.
    def sample_service_time(self, service_type):
        if service_type == "treatment":
            return max(0, random.normalvariate(60, 15))  # טיפול זוגי - ממוצע 60 דקות, סטיית תקן 15
        elif service_type == "salt_pool":
            return max(0, random.normalvariate(30, 10))  # בריכת מלח - ממוצע 30 דקות, סטיית תקן 10
        elif service_type == "sauna":
            return max(0, random.normalvariate(20, 5))  # סאונה - ממוצע 20 דקות, סטיית תקן 5

#        מנהל את רשימת ההמתנה ומעדכן את דירוג הלקוחות במקרה של עיכוב ממושך.
    def manage_waiting_list(self):
        for entry in self.waiting_list:
            service_type = entry["service_type"]
            guest = entry.get("guest")
            if guest:
                guest.add_wait_time(5)  # מוסיף זמן המתנה ללקוח
                if guest.wait_time > guest.max_wait_time:
                    guest.update_rating(0.03)  # עדכון דירוג במקרה של עיכוב ממושך
                    print(f"Guest {guest.guest_id} rating updated due to delay in {service_type}.")

    def get_status(self):
        return {
            "Room Occupancy": self.room_occupancy,
            "Salt Pool Occupancy": self.salt_pool_occupancy,
            "Sauna Occupancy": self.sauna_occupancy,
            "Therapists Available": self.therapists,
            "Waiting List": len(self.waiting_list),
            "Total Visits": self.total_visits,
            "Total Revenue": self.total_revenue,
            "Total Wait Time": self.total_wait_time,
            "Total Service Time": self.total_service_time,
        }