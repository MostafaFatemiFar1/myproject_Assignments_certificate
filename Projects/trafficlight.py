import tkinter as tk
import random
import time

class Car:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Light:
    def __init__(self):
        self.x = "red"
        self.t = 20
    
    def c(self):
        if self.x == "red":
            self.x = "green"
            self.t = 30
        elif self.x == "green":
            self.x = "yellow"
            self.t = 5
        elif self.x == "yellow":
            self.x = "red"
            self.t = 20
    
    def u(self):
        if self.t > 0:
            self.t -= 1
        if self.t == 0:
            self.c()
        return self.t

class Lane:
    def __init__(self, n):
        self.n = n
        self.cars = []
        self.l = Light()
    
    def add(self, c):
        self.cars.append(c)
    
    def rem(self):
        if self.cars:
            return self.cars.pop(0)
        return None
    
    def cnt(self):
        return len(self.cars)

class Cross:
    def __init__(self):
        self.lanes = [Lane("N"), Lane("E"), Lane("S"), Lane("W")]
        self.now = 0
        self.step = 0
    
    def go(self):
        if self.step % 30 == 0:
            for i in range(4):
                if i == self.now:
                    self.lanes[i].l.x = "green"
                    self.lanes[i].l.t = 30
                else:
                    self.lanes[i].l.x = "red"
                    self.lanes[i].l.t = 20
            self.now = (self.now + 1) % 4
        
        for i in range(4):
            if self.lanes[i].l.x == "green":
                if self.lanes[i].cars:
                    c = self.lanes[i].rem()
                    if c:
                        self.lanes[c.b].add(c)
        
        for i in range(4):
            self.lanes[i].l.u()
        
        self.step += 1
        return True
    
    def new(self, a, b):
        if a == b:
            return False
        c = Car(a, b)
        self.lanes[a].add(c)
        return True
    
    def total(self):
        t = 0
        for i in range(4):
            t += self.lanes[i].cnt()
        return t

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("چراغ راهنمایی")
        self.root.geometry("650x550")
        
        self.c = Cross()
        self.gui()
        self.up()
    
    def gui(self):
        tk.Label(self.root, text="شبیه‌ساز چراغ راهنمایی", 
                font=("Arial", 16)).pack(pady=5)
        
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack(pady=10)
        
        f = tk.Frame(self.root)
        f.pack(fill="both", expand=True, padx=20)
        
        self.info = tk.Label(f, text="", justify="right", font=("Arial", 10))
        self.info.pack(side="right", anchor="e")
        
        lf = tk.Frame(f)
        lf.pack(side="left", fill="both", expand=True)
        
        self.listbox = tk.Listbox(lf, height=4)
        self.listbox.pack(fill="both", expand=True, pady=5)
        
        bf = tk.Frame(self.root)
        bf.pack(pady=10)
        
        tk.Button(bf, text="خودرو تصادفی", command=self.rnd, 
                 bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="یک مرحله", command=self.step, 
                 bg="#2196F3", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="اتومات", command=self.auto, 
                 bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="ریست", command=self.reset, 
                 bg="#f44336", fg="white").pack(side="left", padx=5)
        
        self.status = tk.Label(self.root, text="آماده", fg="green")
        self.status.pack(pady=5)
    
    def draw(self):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(150, 150, 250, 250, fill="gray")
        self.canvas.create_line(200, 50, 200, 150, width=20, fill="lightgray")
        self.canvas.create_line(200, 250, 200, 350, width=20, fill="lightgray")
        self.canvas.create_line(50, 200, 150, 200, width=20, fill="lightgray")
        self.canvas.create_line(250, 200, 350, 200, width=20, fill="lightgray")
        
        n = ["شمال", "شرق", "جنوب", "غرب"]
        p = [(200, 80), (280, 200), (200, 320), (120, 200)]
        lp = [(200, 60), (300, 200), (200, 340), (100, 200)]
        
        for i in range(4):
            self.canvas.create_text(p[i][0], p[i][1], text=n[i], 
                                   font=("Arial", 12, "bold"))
            
            if self.c.lanes[i].l.x == "red":
                col = "red"
            elif self.c.lanes[i].l.x == "yellow":
                col = "yellow"
            else:
                col = "green"
            
            self.canvas.create_oval(lp[i][0]-10, lp[i][1]-10,
                                   lp[i][0]+10, lp[i][1]+10,
                                   fill=col, outline="black")
            
            if self.c.lanes[i].cnt() > 0:
                x = p[i][0] + 20
                y = p[i][1] + 30
                self.canvas.create_text(x, y, text=str(self.c.lanes[i].cnt()), 
                                       fill="blue", font=("Arial", 10, "bold"))
        
        self.canvas.create_text(200, 200, text="+", font=("Arial", 20))
    
    def up(self):
        self.draw()
        
        t = ""
        n = ["شمال", "شرق", "جنوب", "غرب"]
        light = {"red": "🔴", "yellow": "🟡", "green": "🟢"}
        
        for i in range(4):
            t += f"{n[i]}: {light[self.c.lanes[i].l.x]} {self.c.lanes[i].cnt()} خودرو\n"
        
        t += f"\nکل خودروها: {self.c.total()}"
        self.info.config(text=t)
        
        self.listbox.delete(0, "end")
        for i in range(4):
            for car in self.c.lanes[i].cars:
                self.listbox.insert("end", f"{n[i]} → {n[car.b]}")
    
    def rnd(self):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
        while b == a:
            b = random.randint(0, 3)
        
        n = ["شمال", "شرق", "جنوب", "غرب"]
        if self.c.new(a, b):
            self.status.config(text=f"خودرو جدید: {n[a]} → {n[b]}", fg="green")
            self.up()
    
    def step(self):
        self.c.go()
        self.status.config(text="یک مرحله انجام شد", fg="green")
        self.up()
    
    def auto(self):
        if self.c.total() == 0:
            self.status.config(text="خودرویی نیست", fg="orange")
            return
        
        for _ in range(30):
            self.c.go()
            self.up()
            self.root.update()
            time.sleep(0.15)
        
        self.status.config(text="انجام شد", fg="green")
    
    def reset(self):
        self.c = Cross()
        self.status.config(text="ریست شد", fg="blue")
        self.up()

root = tk.Tk()
app = App(root)
root.mainloop()
