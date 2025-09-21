

"""
routelink_with_mini_calendar.py

RouteLink — stepwise workflow with built-in calendar fallback and college holidays.
- Start: small window with Register / Login buttons (modal dialogs).
- After login: Calendar tab is shown.
- Click a date on the calendar -> Route Details tab appears for that date.
- Double-click a route -> Link Details tab appears for that route/date.
- Built-in MiniCalendar used when tkcalendar is not installed.
- Holidays: deterministic pseudo-random sample of dates for the current year, highlighted on the calendar and listed.
"""

import os
import re
import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import calendar
import random

# Try optional libs
try:
    from tkcalendar import Calendar as TKCalendar
    TKCAL_AVAILABLE = True
except Exception:
    TKCAL_AVAILABLE = False

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

DB = "routelink.db"
LOGO_PATH = "logo.png"


# ---------------- DB Setup ----------------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, email TEXT UNIQUE, password_hash TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_no TEXT, end_point TEXT, major_stops TEXT,
        time TEXT, transport_type TEXT, no_of_people INTEGER)""")
    c.execute("""CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, drop_point TEXT, phone TEXT,
        course_year TEXT, branch TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS calendar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        travel_date TEXT, route_id INTEGER, link_id INTEGER,
        FOREIGN KEY(route_id) REFERENCES routes(id),
        FOREIGN KEY(link_id) REFERENCES links(id))""")
    conn.commit()
    conn.close()


def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def user_exists(email: str) -> bool:
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email=?", (email,))
    r = c.fetchone()
    conn.close()
    return bool(r)


# ---------------- Holiday generator ----------------
def generate_holidays_for_year(year: int, seed: int = 42):
    """
    Generate a deterministic set of sample holiday dates for the given year.
    This simulates "college holidays" and is deterministic (same seed => same holidays).
    """
    random.seed(seed + year)
    holidays = set()
    # add some fixed familiar academic holidays
    fixed = [
        (1, 26),   # Republic Day (India)
        (5, 1),    # Labour Day
        (8, 15),   # Independence Day
        (10, 2),   # Gandhi Jayanti (example)
        (12, 25)   # Christmas
    ]
    for m, d in fixed:
        try:
            holidays.add(date(year, m, d).isoformat())
        except Exception:
            pass

    # add 6 pseudo-random "college holidays" (like breaks)
    while len(holidays) < 11:
        month = random.randint(1, 12)
        day = random.randint(1, calendar.monthrange(year, month)[1])
        holidays.add(date(year, month, day).isoformat())
    return sorted(holidays)


# ---------------- MiniCalendar for fallback ----------------
class MiniCalendar(tk.Frame):
    def __init__(self, parent, year=None, month=None, on_select=None, holidays=None):
        super().__init__(parent)
        self.on_select = on_select
        today = date.today()
        self.year = year or today.year
        self.month = month or today.month
        self.holidays = set(holidays or [])
        self._build()

    def _build(self):
        header = tk.Frame(self)
        header.pack(fill="x", pady=4)
        tk.Button(header, text="<", width=3, command=self.prev_month).pack(side="left")
        self.lbl = tk.Label(header, text=f"{calendar.month_name[self.month]} {self.year}", font=("Arial", 11, "bold"))
        self.lbl.pack(side="left", padx=8)
        tk.Button(header, text=">", width=3, command=self.next_month).pack(side="left")
        days = tk.Frame(self)
        days.pack(fill="x", pady=(6, 0))
        for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            tk.Label(days, text=d, width=6, bg="#dfeff6").pack(side="left", padx=1)
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(pady=8)
        self.draw()

    def draw(self):
        # clear
        for child in self.grid_frame.winfo_children():
            child.destroy()
        cal = calendar.Calendar(firstweekday=0)  # Monday-first
        for week in cal.monthdayscalendar(self.year, self.month):
            row = tk.Frame(self.grid_frame)
            row.pack()
            for day in week:
                if day == 0:
                    tk.Label(row, text="", width=6, height=2, relief="flat").pack(side="left", padx=1, pady=1)
                else:
                    iso = date(self.year, self.month, day).isoformat()
                    is_hol = iso in self.holidays
                    # button color variations
                    if is_hol:
                        bg = "#ffefef"
                        fg = "#b33"
                        text = f"{day}\n★"
                    else:
                        bg = "#ffffff"
                        fg = "#000"
                        text = str(day)
                    b = tk.Button(row, text=text, width=6, height=2, bg=bg, fg=fg,
                                  command=lambda d=day: self._on_click(d))
                    b.pack(side="left", padx=1, pady=1)

    def _on_click(self, day):
        iso = date(self.year, self.month, day).isoformat()
        if callable(self.on_select):
            self.on_select(iso)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.lbl.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self.draw()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.lbl.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self.draw()

    def update_holidays(self, holidays):
        self.holidays = set(holidays or [])
        self.draw()


# ---------------- Main App ----------------
class RouteLinkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RouteLink — Every Link Counts, Every Route Matters")
        self.geometry("900x640")
        self.minsize(800, 560)
        self.configure(bg="#f3fbff")

        # try load logo
        self.logo_photo = None
        if PIL_AVAILABLE and os.path.exists(LOGO_PATH):
            try:
                img = Image.open(LOGO_PATH)
                img.thumbnail((110, 110), Image.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img)
            except Exception:
                self.logo_photo = None

        # top branding area
        top = tk.Frame(self, bg="#f3fbff")
        top.pack(fill="x", pady=(10, 0))
        if self.logo_photo:
            tk.Label(top, image=self.logo_photo, bg="#f3fbff").pack(side="left", padx=(14, 12))
        else:
            tk.Label(top, text="ROUTELINK", font=("Helvetica", 26, "bold"), fg="#0b5878", bg="#f3fbff").pack(
                side="left", padx=(18, 12))
        brand = tk.Frame(top, bg="#f3fbff"); brand.pack(side="left", anchor="n")
        tk.Label(brand, text="Every Link Counts,", font=("Helvetica", 13, "italic"), fg="#1b5f73", bg="#f3fbff").pack(anchor="w")
        tk.Label(brand, text="Every Route Matters", font=("Helvetica", 16, "bold"), fg="#e85a4f", bg="#f3fbff").pack(anchor="w")
        tk.Label(self, text="A student-first travel connection platform for VIT students — plan, match, and share journeys.",
                 font=("Arial", 10), bg="#f3fbff", fg="#333").pack(pady=2)
        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=6)

        # notebook
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=("Helvetica", 11, "bold"))
        self.nb = ttk.Notebook(self); self.nb.pack(fill="both", expand=True, padx=12, pady=8)

        # initial start tab (buttons open dialogs)
        self.start_tab = StartTab(self.nb, app=self)
        self.nb.add(self.start_tab, text="Get Started")

        # placeholders
        self.calendar_tab = None
        self.route_tab = None
        self.link_tab = None

        # holidays for current year (deterministic)
        self.holidays = generate_holidays_for_year(date.today().year)

    def show_calendar_tab(self):
        # remove all tabs and show only calendar
        for t in list(self.nb.tabs()):
            self.nb.forget(t)
        self.calendar_tab = CalendarTab(self.nb, app=self, holidays=self.holidays)
        self.nb.add(self.calendar_tab, text="Calendar")
        self.nb.select(self.calendar_tab)

    def show_route_tab(self, iso_date: str):
        # add route tab if missing and select it
        if self.route_tab is None:
            self.route_tab = RouteTab(self.nb, app=self)
            self.nb.add(self.route_tab, text="Route Details")
        self.route_tab.set_current_date(iso_date)
        self.nb.select(self.route_tab)

    def show_link_tab(self, route_id: int, route_date: str):
        if self.link_tab is None:
            self.link_tab = LinkTab(self.nb, app=self)
            self.nb.add(self.link_tab, text="Link Details")
        self.link_tab.prefill_for_route(route_id, route_date)
        self.nb.select(self.link_tab)


# ---------------- Start Tab ----------------
class StartTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=18)
        self.app = app
        tk.Label(self, text="Welcome to RouteLink", font=("Georgia", 22, "bold"), fg="#0b5878").pack(pady=(12, 6))
        tk.Label(self, text="Register with your VIT email, then login to continue", font=("Arial", 11), fg="#444").pack(pady=(0, 12))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=18)
        tk.Button(btn_frame, text="Register", command=self.open_register, width=18, bg="#2a9d8f", fg="white").grid(row=0, column=0, padx=12, pady=4)
        tk.Button(btn_frame, text="Login", command=self.open_login, width=18, bg="#e76f51", fg="white").grid(row=0, column=1, padx=12, pady=4)

        tk.Label(self, text="Tip: Register first. After login you'll see the Calendar where you can add routes.", fg="#666").pack(pady=10)

    def open_register(self):
        RegisterDialog(self.app)

    def open_login(self):
        LoginDialog(self.app)


# ---------------- Register / Login Dialogs ----------------
class RegisterDialog(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.title("Register - RouteLink")
        self.geometry("420x320")
        self.resizable(False, False)
        self.grab_set()

        frame = tk.Frame(self, padx=12, pady=12)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Create an account", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(4, 12))

        tk.Label(frame, text="Full Name").grid(row=1, column=0, sticky="w", pady=6)
        self.name = tk.Entry(frame, width=36); self.name.grid(row=1, column=1, pady=6)
        tk.Label(frame, text="Email (VIT only)").grid(row=2, column=0, sticky="w", pady=6)
        self.email = tk.Entry(frame, width=36); self.email.grid(row=2, column=1, pady=6)
        tk.Label(frame, text="Password").grid(row=3, column=0, sticky="w", pady=6)
        self.pw = tk.Entry(frame, width=36, show="*"); self.pw.grid(row=3, column=1, pady=6)

        tk.Button(frame, text="Register", bg="#2a9d8f", fg="white", width=20, command=self.do_register).grid(row=4, column=0, columnspan=2, pady=12)

    def do_register(self):
        name = self.name.get().strip()
        email = self.email.get().strip().lower()
        pw = self.pw.get()
        if not name or not email or not pw:
            messagebox.showerror("Validation", "All fields required.")
            return
        if not re.match(r"^[A-Za-z0-9._%+-]+@vit\.ac\.in$", email):
            messagebox.showerror("Validation", "Please use a VIT email (example@vit.ac.in).")
            return
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", (name, email, hash_pw(pw)))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration completed. Now login.")
            self.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already registered.")


class LoginDialog(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.title("Login - RouteLink")
        self.geometry("420x240")
        self.resizable(False, False)
        self.grab_set()

        frame = tk.Frame(self, padx=12, pady=12)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Login", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(4, 12))

        tk.Label(frame, text="Email").grid(row=1, column=0, sticky="w", pady=6)
        self.email = tk.Entry(frame, width=36); self.email.grid(row=1, column=1, pady=6)
        tk.Label(frame, text="Password").grid(row=2, column=0, sticky="w", pady=6)
        self.pw = tk.Entry(frame, width=36, show="*"); self.pw.grid(row=2, column=1, pady=6)

        tk.Button(frame, text="Login", bg="#e76f51", fg="white", width=20, command=self.do_login).grid(row=3, column=0, columnspan=2, pady=12)

    def do_login(self):
        email = self.email.get().strip().lower()
        pw = self.pw.get()
        if not email or not pw:
            messagebox.showerror("Validation", "Enter email and password.")
            return
        if not user_exists(email):
            messagebox.showerror("No account", "No account found with this email. Please register first.")
            return
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id, name FROM users WHERE email=? AND password_hash=?", (email, hash_pw(pw)))
        r = c.fetchone()
        conn.close()
        if r:
            messagebox.showinfo("Welcome", f"Hello, {r[1]}! Entering the app.")
            self.destroy()
            self.app.show_calendar_tab()
        else:
            messagebox.showerror("Error", "Invalid credentials. If you don't have an account, please register.")


# ---------------- Calendar Tab ----------------
class CalendarTab(ttk.Frame):
    def __init__(self, parent, app, holidays=None):
        super().__init__(parent, padding=14)
        self.app = app
        self.holidays = set(holidays or [])
        tk.Label(self, text="📅 Calendar", font=("Georgia", 20, "bold"), fg="#0b5878").pack(pady=(6, 4))
        tk.Label(self, text="Click a date to add/view Route details.", font=("Arial", 10), fg="#444").pack(pady=(0, 8))

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=8, pady=6)

        left = tk.Frame(container, bd=0, padx=8, pady=8)
        left.pack(side="left", padx=6, pady=6)
        right = tk.Frame(container, padx=8, pady=8)
        right.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        # use tkcalendar if present, otherwise MiniCalendar
        if TKCAL_AVAILABLE:
            try:
                self.cal = TKCalendar(left, selectmode="day", date_pattern="yyyy-mm-dd")
                self.cal.pack()
                self.cal.bind("<<CalendarSelected>>", self.on_date_selected)
                # highlight holiday days using tags if possible (tkcalendar supports tags)
                # We'll mark holidays by adding a tooltip-like text in the right panel instead.
            except Exception:
                self._build_mini(left)
        else:
            self._build_mini(left)

        tk.Label(right, text="Holidays", font=("Arial", 12, "bold")).pack(anchor="nw")
        self.hol_text = tk.Text(right, height=6, width=40)
        self.hol_text.pack(pady=6)
        self._populate_holidays()

        tk.Label(right, text="Routes for selected date", font=("Arial", 12, "bold")).pack(anchor="nw")
        self.routes_text = tk.Text(right, height=12)
        self.routes_text.pack(fill="both", expand=True, pady=6)

        # show today's routes by default
        self.current_date = date.today().isoformat()
        self.display_routes_for_date(self.current_date)

    def _build_mini(self, parent):
        # build mini calendar widget with holiday highlighting
        mc = MiniCalendar(parent, on_select=self.on_mini_select, holidays=self.holidays)
        mc.pack()
        self.mini = mc

    def _populate_holidays(self):
        self.hol_text.delete("1.0", tk.END)
        if not self.holidays:
            self.hol_text.insert(tk.END, "No holiday data available.\n")
            return
        for h in sorted(self.holidays):
            pretty = datetime.strptime(h, "%Y-%m-%d").strftime("%d %b %Y")
            self.hol_text.insert(tk.END, f"• {pretty}\n")

    def on_mini_select(self, iso_date):
        self.current_date = iso_date
        self.display_routes_for_date(iso_date)
        # open route tab for that date
        self.app.show_route_tab(iso_date)

    def on_date_selected(self, event):
        try:
            iso = self.cal.selection_get().isoformat()
        except Exception:
            return
        self.current_date = iso
        self.display_routes_for_date(iso)
        self.app.show_route_tab(iso)

    def display_routes_for_date(self, iso_date):
        self.routes_text.delete("1.0", tk.END)
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
            SELECT cal.id, r.id, r.slot_no, r.end_point, r.time, r.transport_type, r.no_of_people
            FROM calendar cal
            LEFT JOIN routes r ON cal.route_id = r.id
            WHERE cal.travel_date = ?
        """, (iso_date,))
        rows = c.fetchall()
        conn.close()
        if not rows:
            self.routes_text.insert(tk.END, f"No routes on {iso_date}\n\nClick a date to add one.\n")
            return
        self.routes_text.insert(tk.END, f"Routes on {iso_date}:\n\n")
        for cal_id, r_id, slot, endp, ttime, ttype, ppl in rows:
            self.routes_text.insert(tk.END, f"Route ID: {r_id} | Slot: {slot} | {endp} | Time: {ttime or '-'} | {ttype or '-'} | People: {ppl or '-'}\n\n")


# ---------------- RouteTab ----------------
class RouteTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=14)
        self.app = app
        self.current_date = None
        tk.Label(self, text="🚌 Route Details", font=("Georgia", 20, "bold"), fg="#0b5878").pack(pady=(6, 4))
        tk.Label(self, text="Double-click a route to open Link Details (attach students to the route).", font=("Arial", 10), fg="#444").pack(pady=(0, 8))

        cols = ("ID", "Slot No", "End Point", "Major Stops", "Time", "Transport", "People")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            if c == "Major Stops":
                self.tree.column(c, width=220)
            elif c == "End Point":
                self.tree.column(c, width=140)
            elif c == "ID":
                self.tree.column(c, width=60)
            else:
                self.tree.column(c, width=100)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<Double-1>", self.on_route_double_click)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Add Route", bg="#2a9d8f", fg="white", command=self.add_route).pack(side="left", padx=8)
        

    def set_current_date(self, iso_date: str):
        self.current_date = iso_date
        self.refresh()

    def add_route(self):
        if not self.current_date:
            messagebox.showerror("Error", "No date selected.")
            return
        RouteDialog(self.app, pre_fill_date=self.current_date, after_create_callback=self._after_route_created)

    def _after_route_created(self, route_id, route_date):
        self.refresh()
        messagebox.showinfo("Created", f"Route {route_id} created for {route_date}.")

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        if not self.current_date:
            return
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("""
            SELECT r.id, r.slot_no, r.end_point, r.major_stops, r.time, r.transport_type, r.no_of_people
            FROM routes r JOIN calendar cal ON cal.route_id = r.id
            WHERE cal.travel_date = ?
            ORDER BY r.id DESC
        """, (self.current_date,))
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

    def on_route_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        vals = self.tree.item(item, "values")
        if not vals:
            return
        try:
            route_id = int(vals[0])
        except Exception:
            return
        self.app.show_link_tab(route_id, self.current_date)


# ---------------- Route Dialog ----------------
class RouteDialog(tk.Toplevel):
    def __init__(self, app, pre_fill_date=None, after_create_callback=None):
        super().__init__(app)
        self.app = app
        self.after_create_callback = after_create_callback
        self.title("Create Route")
        self.geometry("480x400")
        self.resizable(False, False)
        self.grab_set()

        frame = tk.Frame(self, padx=12, pady=12, bg="#f8ffff")
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Create Route for Date", font=("Helvetica", 12, "bold"), bg="#f8ffff").grid(row=0, column=0, columnspan=2, pady=(0, 8))
        tk.Label(frame, text="Date (YYYY-MM-DD)", bg="#f8ffff").grid(row=1, column=0, sticky="w", pady=6)
        self.date_ent = tk.Entry(frame, width=20); self.date_ent.grid(row=1, column=1, pady=6)
        if pre_fill_date:
            self.date_ent.insert(0, pre_fill_date)

        labels = ["Slot No", "End Point", "Major Stops", "Time (HH:MM)", "Transport Type", "No. of People"]
        self.entries = {}
        for i, lab in enumerate(labels, start=2):
            tk.Label(frame, text=lab, bg="#f8ffff").grid(row=i, column=0, sticky="w", pady=6)
            ent = tk.Entry(frame, width=36); ent.grid(row=i, column=1, pady=6)
            self.entries[lab] = ent

        tk.Button(frame, text="Create Route", bg="#2a9d8f", fg="white", width=18, command=self.create_route).grid(row=8, column=0, columnspan=2, pady=12)

    def create_route(self):
        d = self.date_ent.get().strip()
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Validation", "Date must be YYYY-MM-DD.")
            return
        vals = [self.entries[k].get().strip() for k in self.entries]
        if not all(vals):
            messagebox.showerror("Validation", "All route fields are required.")
            return
        try:
            ppl = int(vals[-1])
            if ppl <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Validation", "No. of People must be a positive integer.")
            return
        t = vals[3]
        if t:
            try:
                datetime.strptime(t, "%H:%M")
            except Exception:
                messagebox.showerror("Validation", "Time must be HH:MM.")
                return
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO routes (slot_no, end_point, major_stops, time, transport_type, no_of_people) VALUES (?, ?, ?, ?, ?, ?)", vals)
        conn.commit()
        route_id = c.lastrowid
        c.execute("INSERT INTO calendar (travel_date, route_id, link_id) VALUES (?, ?, NULL)", (d, route_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Route created (ID {route_id}) and assigned to {d}.")
        if callable(self.after_create_callback):
            self.after_create_callback(route_id, d)
        self.destroy()


# ---------------- Link Tab ----------------
class LinkTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=14)
        self.app = app
        self.route_id = None
        self.route_date = None

        tk.Label(self, text="👥 Link Details", font=("Georgia", 20, "bold"), fg="#0b5878").pack(pady=(6, 4))
        tk.Label(self, text="Add a student's link and attach to the selected route.", font=("Arial", 10), fg="#444").pack(pady=(0, 8))

        frame = tk.Frame(self)
        frame.pack(pady=6)
        labels = ["Name", "Drop", "Phone", "Course Year", "Branch"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(frame, text=lab).grid(row=i, column=0, sticky="w", padx=6, pady=4)
            e = tk.Entry(frame, width=32)
            e.grid(row=i, column=1, padx=6, pady=4)
            self.entries[lab] = e

        tk.Button(frame, text="Save & Attach", bg="#2a9d8f", fg="white", command=self.save_and_attach).grid(row=len(labels), column=0, columnspan=2, pady=8)

        cols = ("ID", "Name", "Drop", "Phone", "Year", "Branch")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110)
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

        self.refresh()

    def prefill_for_route(self, rid: int, rdate: str):
        self.route_id = rid
        self.route_date = rdate
        self.refresh()
        messagebox.showinfo("Attach Link", f"Preparing to attach links to Route {rid} on {rdate}.")

    def save_and_attach(self):
        vals = [self.entries[k].get().strip() for k in self.entries]
        if not all(vals):
            messagebox.showerror("Validation", "All link fields are required.")
            return
        phone = vals[2]
        if not phone.isdigit() or len(phone) < 7:
            messagebox.showerror("Validation", "Please enter a valid phone number (digits only).")
            return
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO links (name, drop_point, phone, course_year, branch) VALUES (?, ?, ?, ?, ?)", vals)
        lid = c.lastrowid
        if self.route_id and self.route_date:
            c.execute("SELECT id FROM calendar WHERE travel_date=? AND route_id=? AND link_id=?", (self.route_date, self.route_id, lid))
            if not c.fetchone():
                c.execute("INSERT INTO calendar (travel_date, route_id, link_id) VALUES (?, ?, ?)", (self.route_date, self.route_id, lid))
        conn.commit()
        conn.close()
        messagebox.showinfo("Attached", f"Link {lid} attached to route {self.route_id} on {self.route_date}.")
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.refresh()

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT id, name, drop_point, phone, course_year, branch FROM links ORDER BY id DESC")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()


# ---------------- Run ----------------
if __name__ == "__main__":
    init_db()
    app = RouteLinkApp()
    app.mainloop()
