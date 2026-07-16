import tkinter as tk
import random
import time

class Person:
    def __init__(self, start, target):
        self.start = start
        self.target = target

class Floor:
    def __init__(self, num):
        self.num = num
        self.waiting = []
    
    def add(self, p):
        self.waiting.append(p)
    
    def remove(self, p):
        if p in self.waiting:
            self.waiting.remove(p)
    
    def count(self):
        return len(self.waiting)

class Elevator:
    def __init__(self):
        self.floor = 0
        self.passengers = []
        self.dir = 0
        self.door = False
        self.moving = False
    
    def load(self, p):
        if len(self.passengers) < 8:
            self.passengers.append(p)
            return True
        return False
    
    def unload(self):
        new_list = []
        for p in self.passengers:
            if p.target != self.floor:
                new_list.append(p)
        self.passengers = new_list
    
    def count(self):
        return len(self.passengers)
    
    def go_up(self):
        if self.floor < 9:
            self.floor += 1
            self.dir = 1
            self.moving = True
            return True
        return False
    
    def go_down(self):
        if self.floor > 0:
            self.floor -= 1
            self.dir = -1
            self.moving = True
            return True
        return False
    
    def stop(self):
        self.dir = 0
        self.door = True
        self.moving = False

class Controller:
    def __init__(self, building):
        self.building = building
        self.elevator = building.elevator
        self.requests = []
    
    def add(self, floor, direction):
        if (floor, direction) not in self.requests:
            self.requests.append((floor, direction))
    
    def process(self):
        if not self.requests:
            return False
        
        target, _ = self.requests.pop(0)
        
        while self.elevator.floor != target:
            if self.elevator.floor < target:
                self.elevator.go_up()
            else:
                self.elevator.go_down()
            self.check_floor()
        
        self.elevator.stop()
        self.elevator.unload()
        
        floor_obj = self.building.floors[target]
        for p in floor_obj.waiting[:]:
            if self.elevator.count() < 8:
                if self.elevator.load(p):
                    floor_obj.remove(p)
        
        self.elevator.door = False
        return True
    
    def check_floor(self):
        current = self.elevator.floor
        floor_obj = self.building.floors[current]
        
        for p in floor_obj.waiting[:]:
            if self.elevator.dir == 1 and p.target > current:
                if self.elevator.load(p):
                    floor_obj.remove(p)
            elif self.elevator.dir == -1 and p.target < current:
                if self.elevator.load(p):
                    floor_obj.remove(p)

class Building:
    def __init__(self):
        self.floors = []
        for i in range(10):
            self.floors.append(Floor(i))
        
        self.elevator = Elevator()
        self.controller = Controller(self)
    
    def add_person(self, start, target):
        if start == target:
            return False
        
        p = Person(start, target)
        self.floors[start].add(p)
        
        if target > start:
            direction = 1
        else:
            direction = -1
        
        self.controller.add(start, direction)
        return True
    
    def total_waiting(self):
        total = 0
        for f in self.floors:
            total += f.count()
        return total
    
    def has_requests(self):
        return len(self.controller.requests) > 0

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("آسانسور")
        self.root.geometry("600x500")
        
        self.building = Building()
        self.setup_gui()
        self.update()
    
    def setup_gui(self):
        label = tk.Label(self.root, text="شبیه‌ساز آسانسور", 
                        font=("Arial", 16))
        label.pack(pady=5)
        
        self.canvas = tk.Canvas(self.root, width=180, height=450, 
                               bg="white")
        self.canvas.pack(side="left", padx=10)
        
        frame = tk.Frame(self.root)
        frame.pack(side="right", fill="both", expand=True, padx=10)
        
        self.info = tk.Label(frame, text="", justify="right", font=("Arial", 10))
        self.info.pack(anchor="e")
        
        self.listbox = tk.Listbox(frame, height=6)
        self.listbox.pack(fill="both", expand=True, pady=5)
        
        btn1 = tk.Button(frame, text="مسافر تصادفی", 
                        command=self.add_random)
        btn1.pack(fill="x", pady=2)
        
        btn2 = tk.Button(frame, text="یک مرحله", 
                        command=self.step)
        btn2.pack(fill="x", pady=2)
        
        btn3 = tk.Button(frame, text="اتومات", 
                        command=self.auto)
        btn3.pack(fill="x", pady=2)
        
        btn4 = tk.Button(frame, text="ریست", 
                        command=self.reset)
        btn4.pack(fill="x", pady=2)
        
        self.status = tk.Label(self.root, text="آماده", fg="green")
        self.status.pack(pady=5)
    
    def draw(self):
        self.canvas.delete("all")
        e = self.building.elevator
        
        y = 400 - (e.floor * 40)
        
        if e.door:
            color = "green"
        elif e.moving:
            color = "orange"
        else:
            color = "blue"
        
        self.canvas.create_rectangle(50, y, 130, y+35, 
                                    fill=color)
        
        self.canvas.create_text(90, y+17, text=str(e.count()),
                               fill="white")
        
        if e.dir == 1:
            self.canvas.create_text(90, y-10, text="▲")
        elif e.dir == -1:
            self.canvas.create_text(90, y-10, text="▼")
        
        for i in range(10):
            floor = self.building.floors[9-i]
            if floor.count() > 0:
                self.canvas.create_text(30, 400 - i*40 + 10, 
                                       text=str(floor.count()),
                                       fill="red")
    
    def update(self):
        self.draw()
        
        e = self.building.elevator
        
        if e.dir == 1:
            d = "بالا"
        elif e.dir == -1:
            d = "پایین"
        else:
            d = "ایستاده"
        
        text = f"طبقه: {e.floor}\n"
        text += f"مسافران: {e.count()}\n"
        text += f"در: {'باز' if e.door else 'بسته'}\n"
        text += f"جهت: {d}\n"
        text += f"درخواست‌ها: {len(self.building.controller.requests)}\n"
        text += f"منتظران: {self.building.total_waiting()}"
        
        self.info.config(text=text)
        
        self.listbox.delete(0, "end")
        for p in e.passengers:
            self.listbox.insert("end", f"{p.start} → {p.target}")
    
    def add_random(self):
        s = random.randint(0, 9)
        t = random.randint(0, 9)
        
        while t == s:
            t = random.randint(0, 9)
        
        if self.building.add_person(s, t):
            self.status.config(text=f"مسافر جدید: {s} → {t}", fg="green")
            self.update()
    
    def step(self):
        if self.building.controller.process():
            self.status.config(text="یک مرحله انجام شد", fg="green")
            self.update()
        else:
            self.status.config(text="مسافری نیست", fg="orange")
    
    def auto(self):
        if not self.building.has_requests():
            self.status.config(text="مسافری نیست", fg="orange")
            return
            
        for _ in range(30):
            if not self.building.controller.requests:
                break
            self.building.controller.process()
            self.update()
            self.root.update()
            time.sleep(0.2)
        
        self.status.config(text="انجام شد", fg="green")
    
    def reset(self):
        self.building = Building()
        self.status.config(text="ریست شد", fg="blue")
        self.update()

root = tk.Tk()
app = App(root)
root.mainloop()
