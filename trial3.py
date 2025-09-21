# routelink_app.py
"""
RouteLink app (works with or without tkcalendar)

If you want the prettier tkcalendar widget, install:
    pip install tkcalendar
"""

import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, date



DB_NAME = "routelink.db"

# Try to import tkcalendar; if available we'll use it for nicer UX.
try:
    from tkcalendar import Calendar as TKCalendar
    TKCAL_AVAILABLE = True
except Exception:
    TKCAL_AVAILABLE = False

# ---------------- Database ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )""")
    # Routes
    c.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_no TEXT,
        end_point TEXT,
        major_stops TEXT,
        time TEXT,
        transport_type TEXT,
        no_of_people INTEGER
    )""")
    # Links
    c.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        drop_point TEXT,
        phone TEXT,
        course_year TEXT,
        branch TEXT
    )""")
    # Calendar mapping
    c.execute("""
    CREATE TABLE IF NOT EXISTS calendar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        travel_date TEXT,
        route_id INTEGER,
        link_id INTEGER,
        FOREIGN KEY(route_id) REFERENCES routes(id),
        FOREIGN KEY(link_id) REFERENCES links(id)
    )""")
    conn.commit()
    conn.close()

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()



# ---------------- App ----------------
class RouteLinkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RouteLink - Student Travel Connector")
        self.geometry("1000x700")
        self.configure(bg="#f7fbff")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.tab_login = LoginTab(self.notebook)
        self.tab_route = RouteTab(self.notebook)
        self.tab_link = LinkTab(self.notebook)
        self.tab_calendar = CalendarTab(self.notebook)

        self.notebook.add(self.tab_login, text="Login / Register")
        self.notebook.add(self.tab_route, text="Route Details")
        self.notebook.add(self.tab_link, text="Link Details")
        self.notebook.add(self.tab_calendar, text="Calendar")


# routelink_app.py
"""
RouteLink app (works with or without tkcalendar)

If you want the prettier tkcalendar widget, install:
    pip install tkcalendar
"""

import sqlite3
import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, date

DB_NAME = "routelink.db"

# Try to import tkcalendar; if available we'll use it for nicer UX.
try:
    from tkcalendar import Calendar as TKCalendar
    TKCAL_AVAILABLE = True
except Exception:
    TKCAL_AVAILABLE = False






   # add this import at the top

class RouteLinkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RouteLink - Student Travel Connector")
        self.geometry("1000x750")
        self.configure(bg="#f7fbff")

        # --- Add Logo ---
        try:
            logo_img = Image.open("logo.png")   # make sure the file exists in same folder
            logo_img = logo_img.resize((220, 220))   # resize to fit GUI
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(self, image=self.logo_photo, bg="#f7fbff")
            logo_label.pack(pady=10)
        except Exception as e:
            print("Logo could not be loaded:", e)


# ---------------- Database ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )""")
    # Routes
    c.execute("""
    CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_no TEXT,
        end_point TEXT,
        major_stops TEXT,
        time TEXT,
        transport_type TEXT,
        no_of_people INTEGER
    )""")
    # Links
    c.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        drop_point TEXT,
        phone TEXT,
        course_year TEXT,
        branch TEXT
    )""")
    # Calendar mapping
    c.execute("""
    CREATE TABLE IF NOT EXISTS calendar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        travel_date TEXT,
        route_id INTEGER,
        link_id INTEGER,
        FOREIGN KEY(route_id) REFERENCES routes(id),
        FOREIGN KEY(link_id) REFERENCES links(id)
    )""")
    conn.commit()
    conn.close()

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

# ---------------- App ----------------
class RouteLinkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RouteLink - Student Travel Connector")
        self.geometry("1000x700")
        self.configure(bg="#f7fbff")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.tab_login = LoginTab(self.notebook)
        self.tab_route = RouteTab(self.notebook)
        self.tab_link = LinkTab(self.notebook)
        self.tab_calendar = CalendarTab(self.notebook)

        self.notebook.add(self.tab_login, text="Login / Register")
        self.notebook.add(self.tab_route, text="Route Details")
        self.notebook.add(self.tab_link, text="Link Details")
        self.notebook.add(self.tab_calendar, text="Calendar")

# ---------------- Login / Register ----------------
class LoginTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        heading = tk.Label(self, text="Welcome to RouteLink", font=("Georgia", 26, "bold"), fg="#1b4965", bg="#f7fbff")
        heading.pack(pady=(10,6))

        sub = tk.Label(self, text="A student-focused travel connection platform", font=("Arial", 12), bg="#f7fbff")
        sub.pack(pady=(0,20))

        btn_frame = tk.Frame(self, bg="#f7fbff")
        btn_frame.pack(pady=10)

        reg_btn = tk.Button(btn_frame, text="Register", width=16, bg="#2a9d8f", fg="white", font=("Arial", 12, "bold"), command=self.open_register)
        reg_btn.grid(row=0, column=0, padx=12)

        login_btn = tk.Button(btn_frame, text="Login", width=16, bg="#e76f51", fg="white", font=("Arial", 12, "bold"), command=self.open_login)
        login_btn.grid(row=0, column=1, padx=12)

        hint = tk.Label(self, text="Use Register to create an account. Login if already registered.", bg="#f7fbff", font=("Arial", 10, "italic"))
        hint.pack(pady=10)

    def open_register(self):
        win = tk.Toplevel(self)
        win.title("Register")
        win.geometry("420x380")
        win.resizable(False, False)

        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        labels = ["Full name", "Email", "Password", "Confirm password"]
        entries = {}
        for i, lab in enumerate(labels):
            tk.Label(frame, text=lab, anchor="w").grid(row=i, column=0, sticky="w", pady=8)
            ent = tk.Entry(frame, width=36, show="*" if "Password" in lab else "")
            ent.grid(row=i, column=1, pady=8)
            entries[lab] = ent

        def do_register():
            name = entries["Full name"].get().strip()
            email = entries["Email"].get().strip().lower()
            pw = entries["Password"].get()
            cpw = entries["Confirm password"].get()
            if not name or not email or not pw:
                messagebox.showerror("Validation", "All fields are required.")
                return
            if "@" not in email or "." not in email:
                messagebox.showerror("Validation", "Please enter a valid email.")
                return
            if pw != cpw:
                messagebox.showerror("Validation", "Passwords do not match.")
                return
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO users (name, email, password_hash) VALUES (?,?,?)", (name, email, hash_password(pw)))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registered! You can login now.")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already registered.")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}")

        tk.Button(frame, text="Register", bg="#2a9d8f", fg="white", width=18, command=do_register).grid(row=len(labels), column=0, columnspan=2, pady=16)

    def open_login(self):
        win = tk.Toplevel(self)
        win.title("Login")
        win.geometry("420x260")
        win.resizable(False, False)

        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Email", anchor="w").grid(row=0, column=0, sticky="w", pady=8)
        email_ent = tk.Entry(frame, width=36)
        email_ent.grid(row=0, column=1, pady=8)

        tk.Label(frame, text="Password", anchor="w").grid(row=1, column=0, sticky="w", pady=8)
        pw_ent = tk.Entry(frame, width=36, show="*")
        pw_ent.grid(row=1, column=1, pady=8)

        def do_login():
            e = email_ent.get().strip().lower()
            p = pw_ent.get()
            if not e or not p:
                messagebox.showerror("Validation", "Please enter email and password.")
                return
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT id, name FROM users WHERE email=? AND password_hash=?", (e, hash_password(p)))
            row = c.fetchone()
            conn.close()
            if row:
                messagebox.showinfo("Welcome", f"Hello, {row[1]}!")
                win.destroy()
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(frame, text="Login", bg="#e76f51", fg="white", width=18, command=do_login).grid(row=3, column=0, columnspan=2, pady=14)

# ---------------- Route Details Tab ----------------
class RouteTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        head = tk.Label(self, text="Route Details", font=("Georgia", 20, "bold"), fg="#1b4965", bg="#f7fbff")
        head.pack(anchor="w", pady=(6,12))

        form = tk.Frame(self, bg="#f7fbff")
        form.pack(anchor="nw")

        labels = ["Slot No", "End Point", "Major Stops", "Time (HH:MM)", "Transport Type", "No. of People"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(form, text=lab, width=18, anchor="e", bg="#f7fbff").grid(row=i, column=0, padx=6, pady=6)
            ent = tk.Entry(form, width=38)
            ent.grid(row=i, column=1, padx=6, pady=6)
            self.entries[lab] = ent

        add_btn = tk.Button(form, text="Add Slot", bg="#2a9d8f", fg="white", command=self.add_slot, width=16)
        add_btn.grid(row=len(labels), column=0, columnspan=2, pady=12)

        # Treeview to show existing slots
        cols = ("Slot No", "End Point", "Major Stops", "Time", "Transport", "People")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130 if c == "Major Stops" else 100)
        self.tree.pack(fill="both", expand=True, padx=8, pady=12)

        self.refresh()

    def add_slot(self):
        vals = [self.entries[k].get().strip() for k in self.entries]
        if not all(vals):
            messagebox.showerror("Validation", "All fields are required for a route slot.")
            return
        # ensure people is integer
        try:
            ppl = int(vals[-1])
            if ppl < 1:
                raise ValueError
        except Exception:
            messagebox.showerror("Validation", "No. of People must be a positive integer.")
            return
        # time basic check
        t = vals[3]
        if t:
            try:
                datetime.strptime(t, "%H:%M")
            except Exception:
                messagebox.showerror("Validation", "Time must be HH:MM format.")
                return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            INSERT INTO routes (slot_no, end_point, major_stops, time, transport_type, no_of_people)
            VALUES (?, ?, ?, ?, ?, ?)
        """, vals)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Route slot added.")
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.refresh()
        # update calendar tab in case needed
        try:
            self.master.master.tab_calendar.refresh()
        except Exception:
            pass

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT slot_no, end_point, major_stops, time, transport_type, no_of_people FROM routes ORDER BY id DESC")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

# ---------------- Link Details Tab ----------------
class LinkTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        head = tk.Label(self, text="Link Details", font=("Georgia", 20, "bold"), fg="#1b4965", bg="#f7fbff")
        head.pack(anchor="w", pady=(6,12))

        form = tk.Frame(self, bg="#f7fbff")
        form.pack(anchor="nw")

        labels = ["Name", "Drop", "Phone", "Course Year", "Branch"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(form, text=lab, width=18, anchor="e", bg="#f7fbff").grid(row=i, column=0, padx=6, pady=6)
            ent = tk.Entry(form, width=38)
            ent.grid(row=i, column=1, padx=6, pady=6)
            self.entries[lab] = ent

        add_btn = tk.Button(form, text="Add Link", bg="#2a9d8f", fg="white", command=self.add_link, width=16)
        add_btn.grid(row=len(labels), column=0, columnspan=2, pady=12)

        cols = ("Name", "Drop", "Phone", "Year", "Branch")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130)
        self.tree.pack(fill="both", expand=True, padx=8, pady=12)

        self.refresh()

    def add_link(self):
        vals = [self.entries[k].get().strip() for k in self.entries]
        if not all(vals):
            messagebox.showerror("Validation", "All fields are required.")
            return
        # phone basic check
        phone = vals[2]
        if not phone.isdigit() or len(phone) < 7:
            messagebox.showerror("Validation", "Please enter a valid phone number digits only.")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO links (name, drop_point, phone, course_year, branch) VALUES (?, ?, ?, ?, ?)", vals)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Link added.")
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.refresh()
        try:
            self.master.master.tab_calendar.refresh()
        except Exception:
            pass

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name, drop_point, phone, course_year, branch FROM links ORDER BY id DESC")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

# ---------------- Simple fallback Calendar Widget ----------------
class MiniCalendar(tk.Frame):
    def __init__(self, parent, year=None, month=None, on_date_selected=None):
        super().__init__(parent, bg="#f7fbff")
        self.on_date_selected = on_date_selected
        today = date.today()
        self.year = year or today.year
        self.month = month or today.month
        self._build()

    def _build(self):
        # header with month/year and prev/next
        hdr = tk.Frame(self, bg="#f7fbff")
        hdr.pack(fill="x", pady=(4,8))
        tk.Button(hdr, text="<", command=self.prev_month, width=3).pack(side="left", padx=6)
        self.month_lbl = tk.Label(hdr, text=f"{calendar.month_name[self.month]} {self.year}", font=("Helvetica", 12, "bold"), bg="#f7fbff")
        self.month_lbl.pack(side="left", padx=8)
        tk.Button(hdr, text=">", command=self.next_month, width=3).pack(side="left", padx=6)

        # days header
        days = tk.Frame(self, bg="#f7fbff")
        days.pack()
        for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
            tk.Label(days, text=d, width=6, bg="#dfeaf2").pack(side="left", padx=1, pady=2)

        self.grid_frame = tk.Frame(self, bg="#f7fbff")
        self.grid_frame.pack()

        self._draw_month()

    def _draw_month(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.year, self.month)  # weeks lists
        for week in month_days:
            row = tk.Frame(self.grid_frame, bg="#f7fbff")
            row.pack()
            for day in week:
                if day == 0:
                    lbl = tk.Label(row, text="", width=6, height=2, bg="#f7fbff", relief="flat")
                    lbl.pack(side="left", padx=1, pady=1)
                else:
                    btn = tk.Button(row, text=str(day), width=6, height=2,
                                    command=lambda d=day: self._on_click(d))
                    btn.pack(side="left", padx=1, pady=1)

    def _on_click(self, day):
        sel = date(self.year, self.month, day).isoformat()
        if callable(self.on_date_selected):
            self.on_date_selected(sel)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.month_lbl.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self._draw_month()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.month_lbl.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self._draw_month()

# ---------------- Calendar Tab ----------------
class CalendarTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        head = tk.Label(self, text="Travel Calendar", font=("Georgia", 20, "bold"), fg="#1b4965", bg="#f7fbff")
        head.pack(anchor="w", pady=(6,12))

        container = tk.Frame(self, bg="#f7fbff")
        container.pack(fill="both", expand=True)

        left = tk.Frame(container, bg="#f7fbff")
        left.pack(side="left", padx=12, pady=6, anchor="n")

        right = tk.Frame(container, bg="#f7fbff")
        right.pack(side="left", padx=12, pady=6, fill="both", expand=True)

        # Use tkcalendar if available
        if TKCAL_AVAILABLE:
            self.cal = TKCalendar(left, selectmode="day", date_pattern="yyyy-mm-dd")
            self.cal.pack()
            sel_btn = tk.Button(left, text="Show Details", bg="#e76f51", fg="white", command=self.show_for_selected)
            sel_btn.pack(pady=8)
            tk.Label(left, text="(tkcalendar present - click a date)", bg="#f7fbff").pack(pady=6)
        else:
            # fallback mini calendar
            tk.Label(left, text="Select a date to view trips", bg="#f7fbff").pack(pady=6)
            self.mini = MiniCalendar(left, on_date_selected=self.on_date_selected)
            self.mini.pack()
            tk.Label(left, text="Click a day on the calendar.", bg="#f7fbff", font=("Arial", 9, "italic")).pack(pady=6)

        # right: details text + actions
        info_lbl = tk.Label(right, text="Trips & Links on selected date:", bg="#f7fbff", font=("Arial", 12, "bold"))
        info_lbl.pack(anchor="nw", pady=(6,4))

        self.text = tk.Text(right, height=22, width=70)
        self.text.pack(fill="both", expand=True, padx=6, pady=6)

        # small form to assign route+link to a date
        assign_frame = tk.LabelFrame(right, text="Assign route & link to a date", padx=8, pady=8)
        assign_frame.pack(fill="x", padx=6, pady=6)

        tk.Label(assign_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=6, pady=6)
        self.assign_date = tk.Entry(assign_frame, width=18)
        self.assign_date.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(assign_frame, text="Route ID").grid(row=0, column=2, padx=6, pady=6)
        self.assign_route = tk.Entry(assign_frame, width=10)
        self.assign_route.grid(row=0, column=3, padx=6, pady=6)
        tk.Label(assign_frame, text="Link ID").grid(row=0, column=4, padx=6, pady=6)
        self.assign_link = tk.Entry(assign_frame, width=10)
        self.assign_link.grid(row=0, column=5, padx=6, pady=6)
        tk.Button(assign_frame, text="Assign", bg="#2a9d8f", fg="white", command=self.assign_to_date).grid(row=0, column=6, padx=8)

        # small helper to list routes and links IDs for user convenience
        quick = tk.Frame(right, bg="#f7fbff")
        quick.pack(fill="x", padx=6, pady=6)
        tk.Button(quick, text="Refresh Lists", command=self.refresh_lists).pack(side="left", padx=6)
        self.routes_list_lbl = tk.Label(quick, text="Routes: (refresh)", bg="#f7fbff")
        self.routes_list_lbl.pack(side="left", padx=12)
        self.links_list_lbl = tk.Label(quick, text="Links: (refresh)", bg="#f7fbff")
        self.links_list_lbl.pack(side="left", padx=12)

        # init
        self.refresh()

    def refresh(self):
        self.refresh_lists()
        # default show today's date
        if TKCAL_AVAILABLE:
            sel = self.cal.selection_get().isoformat()
            self._display_for_date(sel)
        else:
            today_iso = date.today().isoformat()
            self._display_for_date(today_iso)

    def refresh_lists(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, slot_no, end_point FROM routes ORDER BY id DESC LIMIT 10")
        routes = c.fetchall()
        c.execute("SELECT id, name, drop_point FROM links ORDER BY id DESC LIMIT 10")
        links = c.fetchall()
        conn.close()
        routes_text = "Routes: " + ", ".join([f"{r[0]}({r[1]}->{r[2]})" for r in routes]) if routes else "Routes: none"
        links_text = "Links: " + ", ".join([f"{l[0]}({l[1]})" for l in links]) if links else "Links: none"
        self.routes_list_lbl.config(text=routes_text)
        self.links_list_lbl.config(text=links_text)

    def show_for_selected(self):
        if TKCAL_AVAILABLE:
            sel = self.cal.selection_get().isoformat()
            self._display_for_date(sel)
        else:
            messagebox.showinfo("Info", "Click a date on the calendar (left) to view details.")

    def on_date_selected(self, iso_date):
        # update small entry for assign convenience
        self.assign_date.delete(0, tk.END)
        self.assign_date.insert(0, iso_date)
        self._display_for_date(iso_date)

    def _display_for_date(self, iso_date):
        self.text.delete("1.0", tk.END)
        try:
            # validate date string
            datetime.strptime(iso_date, "%Y-%m-%d")
        except Exception:
            self.text.insert(tk.END, f"Invalid date format: {iso_date}\n")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT cal.id, r.slot_no, r.end_point, r.major_stops, r.time, r.transport_type, r.no_of_people,
                   l.name, l.drop_point, l.phone, l.course_year, l.branch
            FROM calendar cal
            LEFT JOIN routes r ON cal.route_id = r.id
            LEFT JOIN links l ON cal.link_id = l.id
            WHERE cal.travel_date = ?
        """, (iso_date,))
        rows = c.fetchall()
        conn.close()
        if not rows:
            self.text.insert(tk.END, f"No trips found on {iso_date}\n")
            return
        self.text.insert(tk.END, f"Trips on {iso_date}:\n\n")
        for idx, row in enumerate(rows, start=1):
            (cal_id, slot_no, end_point, major_stops, ttime, ttype, ppl, name, drop_point, phone, year, branch) = row
            self.text.insert(tk.END, f"{idx}. Route: Slot {slot_no} | {end_point} | Stops: {major_stops} | Time: {ttime or '-'} | Transport: {ttype or '-'} | People: {ppl or '-'}\n")
            self.text.insert(tk.END, f"   Link: {name or '-'} | Drop: {drop_point or '-'} | Phone: {phone or '-'} | Year: {year or '-'} | Branch: {branch or '-'}\n\n")

    def assign_to_date(self):
        d = self.assign_date.get().strip()
        r = self.assign_route.get().strip()
        l = self.assign_link.get().strip()
        # basic validation
        if not d or not r or not l:
            messagebox.showerror("Validation", "Date, Route ID and Link ID are required.")
            return
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Validation", "Date must be YYYY-MM-DD.")
            return
        if not r.isdigit() or not l.isdigit():
            messagebox.showerror("Validation", "Route ID and Link ID must be numeric.")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # ensure route and link exist
        c.execute("SELECT id FROM routes WHERE id=?", (int(r),))
        if not c.fetchone():
            conn.close()
            messagebox.showerror("Error", "Route ID not found.")
            return
        c.execute("SELECT id FROM links WHERE id=?", (int(l),))
        if not c.fetchone():
            conn.close()
            messagebox.showerror("Error", "Link ID not found.")
            return
        # insert mapping
        c.execute("INSERT INTO calendar (travel_date, route_id, link_id) VALUES (?, ?, ?)", (d, int(r), int(l)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Assigned route {r} + link {l} to {d}.")
        # refresh view
        self.refresh_lists()
        self._display_for_date(d)

# ---------------- Run ----------------
if __name__ == "__main__":
    init_db()
    app = RouteLinkApp()
    app.mainloop()


# ---------------- Login / Register ----------------
class LoginTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        heading = tk.Label(self, text="Welcome to RouteLink", font=("Georgia", 26, "bold"), fg="#1b4965", bg="#f7fbff")
        heading.pack(pady=(10,6))

        sub = tk.Label(self, text="A student-focused travel connection platform", font=("Arial", 12), bg="#f7fbff")
        sub.pack(pady=(0,20))

        btn_frame = tk.Frame(self, bg="#f7fbff")
        btn_frame.pack(pady=10)

        reg_btn = tk.Button(btn_frame, text="Register", width=16, bg="#2a9d8f", fg="white", font=("Arial", 12, "bold"), command=self.open_register)
        reg_btn.grid(row=0, column=0, padx=12)

        login_btn = tk.Button(btn_frame, text="Login", width=16, bg="#e76f51", fg="white", font=("Arial", 12, "bold"), command=self.open_login)
        login_btn.grid(row=0, column=1, padx=12)

        hint = tk.Label(self, text="Use Register to create an account. Login if already registered.", bg="#f7fbff", font=("Arial", 10, "italic"))
        hint.pack(pady=10)

    def open_register(self):
        win = tk.Toplevel(self)
        win.title("Register")
        win.geometry("420x380")
        win.resizable(False, False)

        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        labels = ["Full name", "Email", "Password", "Confirm password"]
        entries = {}
        for i, lab in enumerate(labels):
            tk.Label(frame, text=lab, anchor="w").grid(row=i, column=0, sticky="w", pady=8)
            ent = tk.Entry(frame, width=36, show="*" if "Password" in lab else "")
            ent.grid(row=i, column=1, pady=8)
            entries[lab] = ent

        def do_register():
            name = entries["Full name"].get().strip()
            email = entries["Email"].get().strip().lower()
            pw = entries["Password"].get()
            cpw = entries["Confirm password"].get()
            if not name or not email or not pw:
                messagebox.showerror("Validation", "All fields are required.")
                return
            if "@" not in email or "." not in email:
                messagebox.showerror("Validation", "Please enter a valid email.")
                return
            if pw != cpw:
                messagebox.showerror("Validation", "Passwords do not match.")
                return
            try:
                conn = sqlite3.connect(DB_NAME)
                c = conn.cursor()
                c.execute("INSERT INTO users (name, email, password_hash) VALUES (?,?,?)", (name, email, hash_password(pw)))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Registered! You can login now.")
                win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Email already registered.")
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}")

        tk.Button(frame, text="Register", bg="#2a9d8f", fg="white", width=18, command=do_register).grid(row=len(labels), column=0, columnspan=2, pady=16)

    def open_login(self):
        win = tk.Toplevel(self)
        win.title("Login")
        win.geometry("420x260")
        win.resizable(False, False)

        frame = tk.Frame(win, padx=12, pady=12)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="Email", anchor="w").grid(row=0, column=0, sticky="w", pady=8)
        email_ent = tk.Entry(frame, width=36)
        email_ent.grid(row=0, column=1, pady=8)

        tk.Label(frame, text="Password", anchor="w").grid(row=1, column=0, sticky="w", pady=8)
        pw_ent = tk.Entry(frame, width=36, show="*")
        pw_ent.grid(row=1, column=1, pady=8)

        def do_login():
            e = email_ent.get().strip().lower()
            p = pw_ent.get()
            if not e or not p:
                messagebox.showerror("Validation", "Please enter email and password.")
                return
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("SELECT id, name FROM users WHERE email=? AND password_hash=?", (e, hash_password(p)))
            row = c.fetchone()
            conn.close()
            if row:
                messagebox.showinfo("Welcome", f"Hello, {row[1]}!")
                win.destroy()
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(frame, text="Login", bg="#e76f51", fg="white", width=18, command=do_login).grid(row=3, column=0, columnspan=2, pady=14)

# ---------------- Route Details Tab ----------------
class RouteTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        head = tk.Label(self, text="Route Details", font=("Georgia", 20, "bold"), fg="#1b4965", bg="#f7fbff")
        head.pack(anchor="w", pady=(6,12))

        form = tk.Frame(self, bg="#f7fbff")
        form.pack(anchor="nw")

        labels = ["Slot No", "End Point", "Major Stops", "Time (HH:MM)", "Transport Type", "No. of People"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(form, text=lab, width=18, anchor="e", bg="#f7fbff").grid(row=i, column=0, padx=6, pady=6)
            ent = tk.Entry(form, width=38)
            ent.grid(row=i, column=1, padx=6, pady=6)
            self.entries[lab] = ent

        add_btn = tk.Button(form, text="Add Slot", bg="#2a9d8f", fg="white", command=self.add_slot, width=16)
        add_btn.grid(row=len(labels), column=0, columnspan=2, pady=12)

        # Treeview to show existing slots
        cols = ("Slot No", "End Point", "Major Stops", "Time", "Transport", "People")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130 if c == "Major Stops" else 100)
        self.tree.pack(fill="both", expand=True, padx=8, pady=12)

        self.refresh()

    def add_slot(self):
        vals = [self.entries[k].get().strip() for k in self.entries]
        if not all(vals):
            messagebox.showerror("Validation", "All fields are required for a route slot.")
            return
        # ensure people is integer
        try:
            ppl = int(vals[-1])
            if ppl < 1:
                raise ValueError
        except Exception:
            messagebox.showerror("Validation", "No. of People must be a positive integer.")
            return
        # time basic check
        t = vals[3]
        if t:
            try:
                datetime.strptime(t, "%H:%M")
            except Exception:
                messagebox.showerror("Validation", "Time must be HH:MM format.")
                return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            INSERT INTO routes (slot_no, end_point, major_stops, time, transport_type, no_of_people)
            VALUES (?, ?, ?, ?, ?, ?)
        """, vals)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Route slot added.")
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.refresh()
        # update calendar tab in case needed
        try:
            self.master.master.tab_calendar.refresh()
        except Exception:
            pass

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT slot_no, end_point, major_stops, time, transport_type, no_of_people FROM routes ORDER BY id DESC")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

# ---------------- Link Details Tab ----------------
class LinkTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        head = tk.Label(self, text="Link Details", font=("Georgia", 20, "bold"), fg="#1b4965", bg="#f7fbff")
        head.pack(anchor="w", pady=(6,12))

        form = tk.Frame(self, bg="#f7fbff")
        form.pack(anchor="nw")

        labels = ["Name", "Drop", "Phone", "Course Year", "Branch"]
        self.entries = {}
        for i, lab in enumerate(labels):
            tk.Label(form, text=lab, width=18, anchor="e", bg="#f7fbff").grid(row=i, column=0, padx=6, pady=6)
            ent = tk.Entry(form, width=38)
            ent.grid(row=i, column=1, padx=6, pady=6)
            self.entries[lab] = ent

        add_btn = tk.Button(form, text="Add Link", bg="#2a9d8f", fg="white", command=self.add_link, width=16)
        add_btn.grid(row=len(labels), column=0, columnspan=2, pady=12)

        cols = ("Name", "Drop", "Phone", "Year", "Branch")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130)
        self.tree.pack(fill="both", expand=True, padx=8, pady=12)

        self.refresh()

    def add_link(self):
        vals = [self.entries[k].get().strip() for k in self.entries]
        if not all(vals):
            messagebox.showerror("Validation", "All fields are required.")
            return
        # phone basic check
        phone = vals[2]
        if not phone.isdigit() or len(phone) < 7:
            messagebox.showerror("Validation", "Please enter a valid phone number digits only.")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO links (name, drop_point, phone, course_year, branch) VALUES (?, ?, ?, ?, ?)", vals)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Link added.")
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.refresh()
        try:
            self.master.master.tab_calendar.refresh()
        except Exception:
            pass

    def refresh(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT name, drop_point, phone, course_year, branch FROM links ORDER BY id DESC")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

# ---------------- Simple fallback Calendar Widget ----------------
class MiniCalendar(tk.Frame):
    def __init__(self, parent, year=None, month=None, on_date_selected=None):
        super().__init__(parent, bg="#f7fbff")
        self.on_date_selected = on_date_selected
        today = date.today()
        self.year = year or today.year
        self.month = month or today.month
        self._build()

    def _build(self):
        # header with month/year and prev/next
        hdr = tk.Frame(self, bg="#f7fbff")
        hdr.pack(fill="x", pady=(4,8))
        tk.Button(hdr, text="<", command=self.prev_month, width=3).pack(side="left", padx=6)
        self.month_lbl = tk.Label(hdr, text=f"{calendar.month_name[self.month]} {self.year}", font=("Helvetica", 12, "bold"), bg="#f7fbff")
        self.month_lbl.pack(side="left", padx=8)
        tk.Button(hdr, text=">", command=self.next_month, width=3).pack(side="left", padx=6)

        # days header
        days = tk.Frame(self, bg="#f7fbff")
        days.pack()
        for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]:
            tk.Label(days, text=d, width=6, bg="#dfeaf2").pack(side="left", padx=1, pady=2)

        self.grid_frame = tk.Frame(self, bg="#f7fbff")
        self.grid_frame.pack()

        self._draw_month()

    def _draw_month(self):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.year, self.month)  # weeks lists
        for week in month_days:
            row = tk.Frame(self.grid_frame, bg="#f7fbff")
            row.pack()
            for day in week:
                if day == 0:
                    lbl = tk.Label(row, text="", width=6, height=2, bg="#f7fbff", relief="flat")
                    lbl.pack(side="left", padx=1, pady=1)
                else:
                    btn = tk.Button(row, text=str(day), width=6, height=2,
                                    command=lambda d=day: self._on_click(d))
                    btn.pack(side="left", padx=1, pady=1)

    def _on_click(self, day):
        sel = date(self.year, self.month, day).isoformat()
        if callable(self.on_date_selected):
            self.on_date_selected(sel)

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.month_lbl.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self._draw_month()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.month_lbl.config(text=f"{calendar.month_name[self.month]} {self.year}")
        self._draw_month()

# ---------------- Calendar Tab ----------------
class CalendarTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        head = tk.Label(self, text="Travel Calendar", font=("Georgia", 20, "bold"), fg="#1b4965", bg="#f7fbff")
        head.pack(anchor="w", pady=(6,12))

        container = tk.Frame(self, bg="#f7fbff")
        container.pack(fill="both", expand=True)

        left = tk.Frame(container, bg="#f7fbff")
        left.pack(side="left", padx=12, pady=6, anchor="n")

        right = tk.Frame(container, bg="#f7fbff")
        right.pack(side="left", padx=12, pady=6, fill="both", expand=True)

        # Use tkcalendar if available
        if TKCAL_AVAILABLE:
            self.cal = TKCalendar(left, selectmode="day", date_pattern="yyyy-mm-dd")
            self.cal.pack()
            sel_btn = tk.Button(left, text="Show Details", bg="#e76f51", fg="white", command=self.show_for_selected)
            sel_btn.pack(pady=8)
            tk.Label(left, text="(tkcalendar present - click a date)", bg="#f7fbff").pack(pady=6)
        else:
            # fallback mini calendar
            tk.Label(left, text="Select a date to view trips", bg="#f7fbff").pack(pady=6)
            self.mini = MiniCalendar(left, on_date_selected=self.on_date_selected)
            self.mini.pack()
            tk.Label(left, text="Click a day on the calendar.", bg="#f7fbff", font=("Arial", 9, "italic")).pack(pady=6)

        # right: details text + actions
        info_lbl = tk.Label(right, text="Trips & Links on selected date:", bg="#f7fbff", font=("Arial", 12, "bold"))
        info_lbl.pack(anchor="nw", pady=(6,4))

        self.text = tk.Text(right, height=22, width=70)
        self.text.pack(fill="both", expand=True, padx=6, pady=6)

        # small form to assign route+link to a date
        assign_frame = tk.LabelFrame(right, text="Assign route & link to a date", padx=8, pady=8)
        assign_frame.pack(fill="x", padx=6, pady=6)

        tk.Label(assign_frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=6, pady=6)
        self.assign_date = tk.Entry(assign_frame, width=18)
        self.assign_date.grid(row=0, column=1, padx=6, pady=6)
        tk.Label(assign_frame, text="Route ID").grid(row=0, column=2, padx=6, pady=6)
        self.assign_route = tk.Entry(assign_frame, width=10)
        self.assign_route.grid(row=0, column=3, padx=6, pady=6)
        tk.Label(assign_frame, text="Link ID").grid(row=0, column=4, padx=6, pady=6)
        self.assign_link = tk.Entry(assign_frame, width=10)
        self.assign_link.grid(row=0, column=5, padx=6, pady=6)
        tk.Button(assign_frame, text="Assign", bg="#2a9d8f", fg="white", command=self.assign_to_date).grid(row=0, column=6, padx=8)

        # small helper to list routes and links IDs for user convenience
        quick = tk.Frame(right, bg="#f7fbff")
        quick.pack(fill="x", padx=6, pady=6)
        tk.Button(quick, text="Refresh Lists", command=self.refresh_lists).pack(side="left", padx=6)
        self.routes_list_lbl = tk.Label(quick, text="Routes: (refresh)", bg="#f7fbff")
        self.routes_list_lbl.pack(side="left", padx=12)
        self.links_list_lbl = tk.Label(quick, text="Links: (refresh)", bg="#f7fbff")
        self.links_list_lbl.pack(side="left", padx=12)

        # init
        self.refresh()

    def refresh(self):
        self.refresh_lists()
        # default show today's date
        if TKCAL_AVAILABLE:
            sel = self.cal.selection_get().isoformat()
            self._display_for_date(sel)
        else:
            today_iso = date.today().isoformat()
            self._display_for_date(today_iso)

    def refresh_lists(self):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT id, slot_no, end_point FROM routes ORDER BY id DESC LIMIT 10")
        routes = c.fetchall()
        c.execute("SELECT id, name, drop_point FROM links ORDER BY id DESC LIMIT 10")
        links = c.fetchall()
        conn.close()
        routes_text = "Routes: " + ", ".join([f"{r[0]}({r[1]}->{r[2]})" for r in routes]) if routes else "Routes: none"
        links_text = "Links: " + ", ".join([f"{l[0]}({l[1]})" for l in links]) if links else "Links: none"
        self.routes_list_lbl.config(text=routes_text)
        self.links_list_lbl.config(text=links_text)

    def show_for_selected(self):
        if TKCAL_AVAILABLE:
            sel = self.cal.selection_get().isoformat()
            self._display_for_date(sel)
        else:
            messagebox.showinfo("Info", "Click a date on the calendar (left) to view details.")

    def on_date_selected(self, iso_date):
        # update small entry for assign convenience
        self.assign_date.delete(0, tk.END)
        self.assign_date.insert(0, iso_date)
        self._display_for_date(iso_date)

    def _display_for_date(self, iso_date):
        self.text.delete("1.0", tk.END)
        try:
            # validate date string
            datetime.strptime(iso_date, "%Y-%m-%d")
        except Exception:
            self.text.insert(tk.END, f"Invalid date format: {iso_date}\n")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT cal.id, r.slot_no, r.end_point, r.major_stops, r.time, r.transport_type, r.no_of_people,
                   l.name, l.drop_point, l.phone, l.course_year, l.branch
            FROM calendar cal
            LEFT JOIN routes r ON cal.route_id = r.id
            LEFT JOIN links l ON cal.link_id = l.id
            WHERE cal.travel_date = ?
        """, (iso_date,))
        rows = c.fetchall()
        conn.close()
        if not rows:
            self.text.insert(tk.END, f"No trips found on {iso_date}\n")
            return
        self.text.insert(tk.END, f"Trips on {iso_date}:\n\n")
        for idx, row in enumerate(rows, start=1):
            (cal_id, slot_no, end_point, major_stops, ttime, ttype, ppl, name, drop_point, phone, year, branch) = row
            self.text.insert(tk.END, f"{idx}. Route: Slot {slot_no} | {end_point} | Stops: {major_stops} | Time: {ttime or '-'} | Transport: {ttype or '-'} | People: {ppl or '-'}\n")
            self.text.insert(tk.END, f"   Link: {name or '-'} | Drop: {drop_point or '-'} | Phone: {phone or '-'} | Year: {year or '-'} | Branch: {branch or '-'}\n\n")

    def assign_to_date(self):
        d = self.assign_date.get().strip()
        r = self.assign_route.get().strip()
        l = self.assign_link.get().strip()
        # basic validation
        if not d or not r or not l:
            messagebox.showerror("Validation", "Date, Route ID and Link ID are required.")
            return
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Validation", "Date must be YYYY-MM-DD.")
            return
        if not r.isdigit() or not l.isdigit():
            messagebox.showerror("Validation", "Route ID and Link ID must be numeric.")
            return
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        # ensure route and link exist
        c.execute("SELECT id FROM routes WHERE id=?", (int(r),))
        if not c.fetchone():
            conn.close()
            messagebox.showerror("Error", "Route ID not found.")
            return
        c.execute("SELECT id FROM links WHERE id=?", (int(l),))
        if not c.fetchone():
            conn.close()
            messagebox.showerror("Error", "Link ID not found.")
            return
        # insert mapping
        c.execute("INSERT INTO calendar (travel_date, route_id, link_id) VALUES (?, ?, ?)", (d, int(r), int(l)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Assigned route {r} + link {l} to {d}.")
        # refresh view
        self.refresh_lists()
        self._display_for_date(d)

# ---------------- Run ----------------
if __name__ == "__main__":
    init_db()
    app = RouteLinkApp()
    app.mainloop()
