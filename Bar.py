import random

class Bar:
    def __init__(self, num_stations=2):
        self.num_stations = num_stations  # מספר עמדות שירות
        self.queue = []  # תור משותף לכל עמדות השירות
        self.station_status = [False] * num_stations  # סטטוס כל עמדת שירות (False = פנוי, True = תפוס)

        # סטטיסטיקות
        self.total_visits = 0  # סך כל הביקורים בבר
        self.total_revenue = 0  # סך ההכנסות מהבר
        self.total_service_time = 0  # סך זמני השירות
        self.total_queue_time = 0  # סך זמני ההמתנה בתור

#        הזמנת משקה לפי סוג הלקוח.
    def order_drink(self, customer_type):
        if customer_type == "family":
            drinks = ["Coffee", "Juice"]
            prices = [3, 3]
        else:
            drinks = ["Coffee", "Juice", "Beer", "Wine", "Cocktail"]
            prices = [3, 3, 3, 10, 15]

        drink = random.choice(drinks)  # בחירת משקה אקראית
        price = prices[drinks.index(drink)]
        print(f"Customer ordered {drink} for ${price}.")
        return price

#        הזמנת אוכל בבר.
    def order_food(self):
        foods = ["Toast", "Salad", "Ice Cream", "Chicken Nuggets"]
        prices = [10, 12, 3, 15]

        if random.random() < 0.3:  # 30% סיכוי להוסיף קינוח
            foods.append("Dessert")
            prices.append(7)

        food = random.choice(foods)
        price = prices[foods.index(food)]
        print(f"Customer ordered {food} for ${price}.")
        return price

#        שירות לקוח בבר, כולל זמן שירות וזיהוי משקה ואוכל.
    def serve_customer(self, customer_id, customer_type):
        # בדיקת זמינות עמדות שירות
        if not any(station == False for station in self.station_status):
            self.queue.append({"customer_id": customer_id, "time_added": self.total_service_time})
            print(f"Customer {customer_id} added to the queue.")
            return 0

        # מציאת עמדה פנויה
        station_index = self.station_status.index(False)
        self.station_status[station_index] = True

        print(f"Customer {customer_id} is being served at station {station_index + 1}.")

        # הזמנת משקה ואוכל
        total_cost = 0
        if random.random() < 0.5:  # 50% סיכוי להזמין משקה
            total_cost += self.order_drink(customer_type)

        if random.random() < 0.5:  # 50% סיכוי להזמין אוכל
            total_cost += self.order_food()

        # סימולציה של זמן שירות
        service_time = max(0, random.gauss(5, 1.5))  # זמן שירות ממוצע 5 דקות עם סטיית תקן 1.5
        self.total_service_time += service_time  # עדכון סטטיסטיקת זמן שירות
        print(f"Service time for customer {customer_id}: {service_time:.2f} minutes.")

        # שחרור העמדה לאחר זמן השירות
        self.station_status[station_index] = False

        # עדכון סטטיסטיקות
        self.total_revenue += total_cost
        self.total_visits += 1

        # שירות לקוחות בתור
        if self.queue:
            next_customer = self.queue.pop(0)
            queue_time = self.total_service_time - next_customer["time_added"]
            self.total_queue_time += queue_time  # עדכון זמן ההמתנה
            print(f"Customer {next_customer['customer_id']} waited {queue_time:.2f} minutes and is called from the queue to station {station_index + 1}.")

        return total_cost

#        זימון אורח לבר.
    def schedule_visit(self, guest):
        print(f"Guest {guest.guest_id} is visiting the bar.")
        self.serve_customer(guest.guest_id, guest.group_type)

    def get_status(self):
        return {
            "Queue Length": len(self.queue),
            "Available Stations": self.station_status.count(False),
            "Total Visits": self.total_visits,
            "Total Revenue": self.total_revenue,
            "Total Service Time": self.total_service_time,
            "Total Queue Time": self.total_queue_time,
        }