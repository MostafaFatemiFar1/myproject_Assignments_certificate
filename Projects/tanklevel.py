import tkinter as tk
import time

class T:
    def __init__(self):
        self.c = 100
        self.l = 30
        self.i = 0
        self.o = 0
    
    def u(self):
        self.l += self.i - self.o
        if self.l > self.c:
            self.l = self.c
        if self.l < 0:
            self.l = 0
        return self.l
    
    def set_i(self, v):
        self.i = v
    
    def set_o(self, v):
        self.o = v
    
    def get(self):
        return self.l
    
    def p(self):
        return (self.l / self.c) * 100

class P:
    def __init__(self):
        self.on = False
        self.f = 0
    
    def start(self):
        self.on = True
        self.f = 5
    
    def stop(self):
        self.on = False
        self.f = 0
    
    def get(self):
        return self.f

class C:
    def __init__(self, t, p):
        self.t = t
        self.p = p
        self.m = "onoff"
        self.sp = 50
        self.e = 0
        self.s = 0
    
    def set_m(self, m):
        self.m = m
    
    def onoff(self):
        l = self.t.get()
        if l < self.sp - 5:
            self.p.start()
        elif l > self.sp + 5:
            self.p.stop()
    
    def pid(self):
        l = self.t.get()
        e = self.sp - l
        
        kp = 2.0
        ki = 0.1
        kd = 0.5
        
        self.s += e
        d = e - self.e
        
        out = kp * e + ki * self.s + kd * d
        self.e = e
        
        if out > 5:
            self.p.start()
        else:
            self.p.stop()
    
    def u(self):
        if self.m == "onoff":
            self.onoff()
        else:
            self.pid()
        
        self.t.set_i(self.p.get())
        self.t.u()
        return self.t.get()

class S:
    def __init__(self):
        self.t = T()
        self.p = P()
        self.c = C(self.t, self.p)
        self.h = []
        self.time = 0
    
    def set_m(self, m):
        self.c.set_m(m)
    
    def step(self):
        l = self.c.u()
        self.h.append(l)
        if len(self.h) > 100:
            self.h.pop(0)
        self.time += 1
        return l
    
    def get_h(self):
        return self.h

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("مخزن آب")
        self.root.geometry("700x600")
        
        self.s = S()
        self.s.set_m("onoff")
        self.r = False
        self.gui()
        self.up()
    
    def gui(self):
        tk.Label(self.root, text="شبیه‌ساز مخزن آب", 
                font=("Arial", 16)).pack(pady=5)
        
        f = tk.Frame(self.root)
        f.pack(fill="both", expand=True, padx=10)
        
        self.canvas = tk.Canvas(f, width=300, height=400, bg="white")
        self.canvas.pack(side="left", padx=10)
        
        rf = tk.Frame(f)
        rf.pack(side="right", fill="both", expand=True, padx=10)
        
        self.info = tk.Label(rf, text="", justify="right", font=("Arial", 10))
        self.info.pack(anchor="e")
        
        self.graph = tk.Canvas(rf, width=300, height=150, bg="white")
        self.graph.pack(pady=5)
        
        cf = tk.Frame(self.root)
        cf.pack(pady=10)
        
        tk.Button(cf, text="On-Off", command=self.set_onoff, 
                 bg="#4CAF50", fg="white").pack(side="left", padx=5)
        tk.Button(cf, text="PID", command=self.set_pid, 
                 bg="#2196F3", fg="white").pack(side="left", padx=5)
        
        bf = tk.Frame(self.root)
        bf.pack(pady=5)
        
        tk.Button(bf, text="یک مرحله", command=self.step, 
                 bg="#FF9800", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="اتومات", command=self.auto, 
                 bg="#FF5722", fg="white").pack(side="left", padx=5)
        tk.Button(bf, text="ریست", command=self.reset, 
                 bg="#f44336", fg="white").pack(side="left", padx=5)
        
        self.status = tk.Label(self.root, text="آماده - On-Off", fg="green")
        self.status.pack(pady=5)
    
    def draw_t(self):
        self.canvas.delete("all")
        
        l = self.s.t.get()
        c = self.s.t.c
        
        self.canvas.create_rectangle(50, 50, 250, 350, outline="black", width=2)
        
        h = (l / c) * 300
        y = 350 - h
        
        if l < 30:
            col = "red"
        elif l < 60:
            col = "yellow"
        else:
            col = "green"
        
        self.canvas.create_rectangle(50, y, 250, 350, fill=col)
        self.canvas.create_text(150, 370, text=f"{l:.1f} / {c}", font=("Arial", 12))
        self.canvas.create_text(150, 30, text=f"{self.s.t.p():.0f}%", font=("Arial", 14, "bold"))
        
        if self.s.p.on:
            self.canvas.create_text(50, 30, text="پمپ روشن", anchor="w", fill="blue")
        else:
            self.canvas.create_text(50, 30, text="پمپ خاموش", anchor="w", fill="gray")
        
        self.canvas.create_text(150, 390, text=f"ورودی: {self.s.t.i:.1f}  خروجی: {self.s.t.o:.1f}", font=("Arial", 9))
    
    def draw_g(self):
        self.graph.delete("all")
        h = self.s.get_h()
        
        if not h:
            return
        
        self.graph.create_text(150, 10, text="نمودار سطح", font=("Arial", 9))
        
        w = 300
        hh = 130
        y0 = 140
        
        for i in range(len(h) - 1):
            x1 = (i / 100) * w
            y1 = y0 - (h[i] / 100) * hh
            x2 = ((i + 1) / 100) * w
            y2 = y0 - (h[i + 1] / 100) * hh
            self.graph.create_line(x1, y1, x2, y2, fill="blue", width=2)
        
        self.graph.create_line(0, y0, w, y0, fill="gray", dash=(2, 2))
        
        sp = self.s.c.sp
        y_sp = y0 - (sp / 100) * hh
        self.graph.create_line(0, y_sp, w, y_sp, fill="red", dash=(4, 4))
    
    def up(self):
        self.draw_t()
        self.draw_g()
        
        m = self.s.c.m
        l = self.s.t.get()
        p = "روشن" if self.s.p.on else "خاموش"
        
        text = f"حالت: {m.upper()}\n"
        text += f"سطح: {l:.1f}\n"
        text += f"درصد: {self.s.t.p():.0f}%\n"
        text += f"پمپ: {p}\n"
        text += f"هدف: {self.s.c.sp}\n"
        text += f"زمان: {self.s.time}"
        
        self.info.config(text=text)
    
    def set_onoff(self):
        self.s.set_m("onoff")
        self.status.config(text="حالت On-Off", fg="green")
        self.up()
    
    def set_pid(self):
        self.s.set_m("pid")
        self.status.config(text="حالت PID", fg="blue")
        self.up()
    
    def step(self):
        self.s.step()
        self.up()
    
    def auto(self):
        if self.r:
            return
        self.r = True
        self.status.config(text="در حال اجرا...", fg="orange")
        
        for _ in range(50):
            self.s.step()
            self.up()
            self.root.update()
            time.sleep(0.1)
        
        self.r = False
        self.status.config(text="انجام شد", fg="green")
    
    def reset(self):
        self.s = S()
        self.s.set_m("onoff")
        self.r = False
        self.status.config(text="ریست شد - On-Off", fg="blue")
        self.up()

root = tk.Tk()
app = App(root)
root.mainloop()
