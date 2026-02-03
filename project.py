from collections import deque


class SeatNode:
    def __init__(self, seat_no, section):
        self.seat_no = seat_no
        self.section = section
        self.booked = False
        self.passenger = None
        self.rac_passengers = []   
        self.left = None
        self.right = None


class IRCTCSystem:
    def __init__(self):
        self.root = None                      
        self.booking_stack = []               
        self.waiting_list = deque()           
        self.rotation_deque = deque()        

        self.sections = {
            "Front": [],
            "Mid": [],
            "Rear": []
        }
        self.order = ["Front", "Mid", "Rear"]
        self.ptr = 0

    def add_seat(self, seat_no, section):
        node = SeatNode(seat_no, section)
        self.sections[section].append(node)
        self.rotation_deque.append(seat_no)

        def _insert(root, n):
            if not root:
                return n
            if n.seat_no < root.seat_no:
                root.left = _insert(root.left, n)
            else:
                root.right = _insert(root.right, n)
            return root

        self.root = _insert(self.root, node)

    
    def book_ticket(self, name, gender, ptype="Normal"):
        gender = gender.lower()
        if gender == "m":
            gender = "male"
        elif gender == "f":
            gender = "female"

        target = None
        for _ in range(3):
            sec = self.order[self.ptr]
            self.ptr = (self.ptr + 1) % 3

            for seat in self.sections[sec]:
                if not seat.booked:
                    target = seat
                    break
            if target:
                break

        if target:
            target.booked = True
            target.passenger = {"name": name, "gender": gender}
            self.booking_stack.append(target)
            print(f" {name} →  Seat {target.seat_no} [{target.section}]")
            return

       
        for sec in self.sections.values():
            for s in sec:
                if len(s.rac_passengers) < 2:
                    if not s.rac_passengers or s.rac_passengers[0]["gender"] == gender:
                        s.rac_passengers.append({"name": name, "gender": gender})
                        print(f" RAC → {name} Seat {s.seat_no}")
                        return

        
        pdata = {"name": name, "gender": gender}
        if ptype.lower() == "tatkal":
            self.waiting_list.appendleft(pdata)
            print(f"WAITING (Tatkal) → {name}")
        else:
            self.waiting_list.append(pdata)
            print(f" WAITING → {name}")

   
    def cancel_ticket(self):
        if not self.booking_stack:
            print(" No tickets to cancel")
            return

        seat = self.booking_stack.pop()
        print(f" CANCELLED → {seat.passenger['name']} Seat {seat.seat_no}")

        if seat.rac_passengers:
            seat.passenger = seat.rac_passengers.pop(0)
            self.booking_stack.append(seat)
            print(f" RAC PROMOTED → {seat.passenger['name']}")

        elif self.waiting_list:
            seat.passenger = self.waiting_list.popleft()
            self.booking_stack.append(seat)
            print(f" WL PROMOTED → {seat.passenger['name']}")

        else:
            seat.booked = False
            seat.passenger = None
            print("Seat now Available")

    
    def rotate_seats(self, direction):
        if direction.lower() == "left":
            self.rotation_deque.rotate(-1)
        else:
            self.rotation_deque.rotate(1)
        print("Seat Order:", list(self.rotation_deque))

 
    def admin_report(self):
        if not self.root:
            print("No seats")
            return

        inorder = []
        level = []

        def dfs(n):
            if n:
                dfs(n.left)
                inorder.append(n.seat_no)
                dfs(n.right)

        dfs(self.root)

        q = deque([self.root])
        while q:
            n = q.popleft()
            level.append(n.seat_no)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)

        print("\n--- ADMIN REPORT ---")
        print("Inorder:", inorder)
        print("Level Order:", level)
        print("Waiting List:", [p["name"] for p in self.waiting_list])



def main():
    irctc = IRCTCSystem()
    

    n = int(input("Total seats you need to create: "))
    for i in range(n):
        s = int(input("Seat Number: "))
        sec = input("Section (Front/Mid/Rear): ").capitalize()
        irctc.add_seat(s, sec)

    while True:
        print("\nSelect an option:")
        print("1. Book Ticket")
        print("2. Cancel Ticket")
        print("3. Admin Report")
        print("4. Rotate Seats")
        print("5. Exit")

        ch = input("Choice: ")

        if ch == "1":
            irctc.book_ticket(
                input("Name: "),
                input("Gender (M/F): "),
                input("Type (Normal/Tatkal): ")
            )
        elif ch == "2":
            irctc.cancel_ticket()
        elif ch == "3":
            irctc.admin_report()
        elif ch == "4":
            irctc.rotate_seats(input("Direction (Left/Right): "))
        elif ch == "5":
            break

if __name__ == "__main__":
    main()
