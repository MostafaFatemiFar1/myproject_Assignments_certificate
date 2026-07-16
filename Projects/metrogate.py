import tkinter as tk
import random
import time

class P:
    def __init__(self, n):
        self.n = n
        self.c = True

class C:
    def __init__(self, o):
        self.o = o
        self.m = random.randint(10000, 50000)
    
    def p(self):
        if self.m >= 3000:
            self.m -= 3000
            return True
        return False

class S:
    def __init__(self):
        self.d = False
    
    def sc(self, c):
        if c:
            if c.p():
                self.d = True
                return True
        return False

class M:
    def __init__(self):
        self.o = False
    
    def op(self):
        self.o = True
    
    def cl(self):
        self.o = False

class G:
    def __init__(self, n):
        self.n = n
        self.m = M()
        self.s = S()
        self.ps = []
        self.w = []
    
    def en(self, p, c):
        if self.s.sc(c):
            self.ps.append(p)
            self.m.op()
            return True
        else:
            self.w.append(p)
            return False
    
    def ex(self, p):
        if p in self.ps:
            self.ps.remove(p)
            self.m.cl()
            return True
        return False
    
    def cnt(self):
        return len(self.ps)
    
    def wc(self):
        return len(self.w)

class St:
    def __init__(self):
        self.gs = [G("ورودی 1"), G("ورودی 2"), G("خروجی 1"), G("خروجی 2")]
        self.t = 0
        self.pl = []
    
    def add(self):
        n = f"مسافر {len(self.pl) + 1}"
        p = P(n)
        c = C(p)
        self.pl.append((p, c))
        return p, c
    
    def en(self, gn, p, c):
        if 0 <= gn < 4:
            if self.gs[gn].en(p, c):
                self.t += 1
                return True
        return False
    
    def ex(self, gn, p):
        if 0 <= gn < 4:
            if self.gs[gn].ex(p):
                return True
        return False
    
    def tot(self):
        t = 0
        for g in self.gs:
            t += g.cnt()
        return t
    
    def tw(self):
        t = 0
        for g in self.gs:
            t += g.wc()
        return t

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("گیت مترو")
        self.root.geometry("600x550")
        
        self.st = St()
        self.gui()
        self.up()
    
    def gui(self):
        tk.Label(self.root, text="شبیه‌ساز گیت مترو", 
                font=("Arial", 16)).pack(pady=5)
        
        self.canvas = tk.Canvas(self.root, width=500, height=300, bg="white")
        self.canvas.pack(pady=10)
        
        f = tk.Frame(self.root)
        f.pack(fill="both", expand=True, padx=20)
        
        self.info = tk.Label(f, text="", justify="right", font=("Arial", 10))
        self.info.pack(side="right", anchor="e")
        
        lf = tk.Frame(f)
        lf.pack(side="left", fill="both", expand=True)
        
        self.listbox = tk.Listbox(lf, height=5)
        self.listbox.pack(fill="both", expand=True, pady=5)
        
        bf = tk.Frame(self.root)
        bf.pack(pady=10)
        
        tk.Button(bf, text="مسافر تصادفی", command=self.rnd, 
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
        
        gs = ["ورودی 1", "ورودی 2", "خروجی 1", "خروجی 2"]
        pos = [(80, 80), (180, 80), (280, 80), (380, 80)]
        
        for i in range(4):
            x, y = pos[i]
            
            if self.st.gs[i].m.o:
                col = "green"
                st = "باز"
            else:
                col = "red"
                st = "بسته"
            
            self.canvas.create_rectangle(x, y, x+60, y+80, fill=col, outline="black")
            self.canvas.create_text(x+30, y+40, text=gs[i], font=("Arial", 8), fill="white")
            self.canvas.create_text(x+30, y+95, text=st, font=("Arial", 9, "bold"))
            
            c = self.st.gs[i].cnt()
            if c > 0:
                self.canvas.create_text(x+30, y+115, text=f"{c}", fill="blue")
            
            w = self.st.gs[i].wc()
            if w > 0:
                self.canvas.create_text(x+30, y+135, text=f"{w}", fill="orange")
    
    def up(self):
        self.draw()
        
        t = ""
        gs = ["ورودی 1", "ورودی 2", "خروجی 1", "خروجی 2"]
        
        for i in range(4):
            st = "باز" if self.st.gs[i].m.o else "بسته"
            t += f"{gs[i]}: {st} | {self.st.gs[i].cnt()} نفر\n"
        
        t += f"\nکل داخل: {self.st.tot()} | منتظران: {self.st.tw()}"
        self.info.config(text=t)
        
        self.listbox.delete(0, "end")
        for i in range(4):
            for p in self.st.gs[i].ps:
                self.listbox.insert("end", f"{gs[i]} → {p.n}")
    
    def rnd(self):
        p, c = self.st.add()
        g = random.randint(0, 1)
        
        if self.st.en(g, p, c):
            gs = ["ورودی 1", "ورودی 2", "خروجی 1", "خروجی 2"]
            self.status.config(text=f"{p.n} وارد {gs[g]} شد", fg="green")
            self.up()
    
    def step(self):
        if self.st.tot() > 0:
            g = random.randint(0, 3)
            if self.st.gs[g].ps:
                p = self.st.gs[g].ps[0]
                if self.st.ex(g, p):
                    gs = ["ورودی 1", "ورودی 2", "خروجی 1", "خروجی 2"]
                    self.status.config(text=f"{p.n} از {gs[g]} خارج شد", fg="green")
                    self.up()
                    return
        
        self.status.config(text="مسافری برای خروج نیست", fg="orange")
        self.up()
    
    def auto(self):
        for _ in range(20):
            if random.random() < 0.6:
                p, c = self.st.add()
                g = random.randint(0, 1)
                self.st.en(g, p, c)
            
            if self.st.tot() > 0:
                g = random.randint(0, 3)
                if self.st.gs[g].ps:
                    p = self.st.gs[g].ps[0]
                    self.st.ex(g, p)
            
            self.up()
            self.root.update()
            time.sleep(0.2)
        
        self.status.config(text="انجام شد", fg="green")
    
    def reset(self):
        self.st = St()
        self.status.config(text="ریست شد", fg="blue")
        self.up()

root = tk.Tk()
app = App(root)
root.mainloop()
