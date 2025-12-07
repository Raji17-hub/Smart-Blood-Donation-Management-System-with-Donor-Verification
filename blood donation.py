# blood_donation_app_v2.py
import csv
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
import re

# -------------------------
# Config / File paths
# -------------------------
DATA_DIR = Path("data")
DONOR_FILE = DATA_DIR / "donors.csv"
REQUEST_FILE = DATA_DIR / "requests.csv"
BLOCKCHAIN_FILE = DATA_DIR / "blockchain.txt"

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
URGENCY_LEVELS = ["Low", "Medium", "High", "Critical"]

# Colors
COLOR_BG_ROOT = "#F7F7F9"
COLOR_PRIMARY = "#FF6F61"
COLOR_FRAME_LIGHT = "#FFF7F3"
COLOR_FRAME_ACCENT = "#FFE8E4"
TEXT_DARK = "#222"

# -------------------------
# Utilities
# -------------------------
def ensure_data_files():
    DATA_DIR.mkdir(exist_ok=True)
    if not DONOR_FILE.exists():
        with DONOR_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name","age","blood","location","contact"])
    if not REQUEST_FILE.exists():
        with REQUEST_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name","blood","location","urgency"])
    if not BLOCKCHAIN_FILE.exists():
        with BLOCKCHAIN_FILE.open("w", encoding="utf-8") as f:
            f.write("Alice\nBob\n")

def append_donor_to_blockchain(name: str):
    try:
        with BLOCKCHAIN_FILE.open("a", encoding="utf-8") as f:
            f.write(f"{name}\n")
    except IOError:
        messagebox.showwarning("Blockchain", "Could not write to blockchain simulation file.")

def validate_name(name):
    return bool(re.fullmatch(r"[A-Za-z ]+", name))

def validate_contact(contact):
    return bool(re.fullmatch(r"\d{10}", contact)) or bool(re.fullmatch(r"[A-Za-z0-9._%+-]+@gmail\.com", contact))

# -------------------------
# Main Application
# -------------------------
class BloodDonationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blood Donation Management System")
        self.geometry("900x650")
        self.configure(bg=COLOR_BG_ROOT)
        self.minsize(820, 560)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configure_styles()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self, style="Card.TFrame")
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.frames = {}
        for F, title in [(DonorFrame, "Register Donor"),
                         (RequestFrame, "Request Blood"),
                         (MatchFrame, "Find Match"),
                         (VerifyFrame, "Verify Donor")]:
            frame = F(parent=self.notebook, controller=self)
            self.frames[F.__name__] = frame
            self.notebook.add(frame, text=title)

    def _configure_styles(self):
        self.style.configure("Card.TFrame", background=COLOR_FRAME_LIGHT, relief="flat")
        self.style.configure("Accent.TFrame", background=COLOR_FRAME_ACCENT)
        self.style.configure("Title.TLabel", font=("Helvetica",16,"bold"), background=COLOR_FRAME_LIGHT, foreground=TEXT_DARK)
        self.style.configure("TLabel", background=COLOR_FRAME_LIGHT, foreground=TEXT_DARK)
        self.style.configure("TEntry", padding=6)
        self.style.configure("TCombobox", padding=6)
        self.style.configure("Primary.TButton", background=COLOR_PRIMARY, foreground="white", font=("Helvetica",10,"bold"), padding=6)
        self.style.map("Primary.TButton", background=[("active","#ff8b7f")])
        self.style.configure("Treeview", rowheight=24, font=("Helvetica",10))
        self.style.configure("Treeview.Heading", font=("Helvetica",10,"bold"))

# -------------------------
# Frames
# -------------------------
class DonorFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Donor Registration", style="Title.TLabel").grid(row=0,column=0,columnspan=2,sticky="w", pady=(2,14))

        # Name
        ttk.Label(self, text="Name:").grid(row=1,column=0, sticky="w", padx=6,pady=6)
        self.name = ttk.Entry(self)
        self.name.grid(row=1,column=1, sticky="ew", padx=6,pady=6)

        # Age
        ttk.Label(self, text="Age:").grid(row=2,column=0, sticky="w", padx=6,pady=6)
        self.age = ttk.Entry(self)
        self.age.grid(row=2,column=1, sticky="w", padx=6,pady=6)

        # Blood
        ttk.Label(self, text="Blood Type:").grid(row=3,column=0, sticky="w", padx=6,pady=6)
        self.blood = ttk.Combobox(self, values=BLOOD_TYPES, state="readonly")
        self.blood.grid(row=3,column=1, sticky="w", padx=6,pady=6)

        # Location
        ttk.Label(self, text="Location:").grid(row=4,column=0, sticky="w", padx=6,pady=6)
        self.location = ttk.Entry(self)
        self.location.grid(row=4,column=1, sticky="ew", padx=6,pady=6)

        # Contact
        ttk.Label(self, text="Contact (Phone or Gmail):").grid(row=5,column=0, sticky="w", padx=6,pady=6)
        self.contact = ttk.Entry(self)
        self.contact.grid(row=5,column=1, sticky="ew", padx=6,pady=6)

        btn = ttk.Button(self, text="Register Donor", style="Primary.TButton", command=self.register_donor)
        btn.grid(row=6,column=0,columnspan=2,pady=(14,6), padx=6, sticky="ew")

    def register_donor(self):
        name = self.name.get().strip()
        age = self.age.get().strip()
        blood = self.blood.get().strip()
        location = self.location.get().strip()
        contact = self.contact.get().strip()

        if not all([name, age, blood, location, contact]):
            messagebox.showwarning("Missing data","Please fill all fields.")
            return

        if not validate_name(name):
            messagebox.showwarning("Invalid Name","Name must contain alphabets and spaces only.")
            return

        if not age.isdigit() or not (16 <= int(age) <= 100):
            messagebox.showwarning("Invalid Age","Age must be a number between 16 and 100.")
            return

        if not validate_contact(contact):
            messagebox.showwarning("Invalid Contact","Enter 10-digit phone number or Gmail ending with @gmail.com")
            return

        try:
            with DONOR_FILE.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([name, age, blood, location, contact])
            append_donor_to_blockchain(name)
            messagebox.showinfo("Success", f"Donor '{name}' registered successfully.")
            self.name.delete(0,"end")
            self.age.delete(0,"end")
            self.blood.set("")
            self.location.delete(0,"end")
            self.contact.delete(0,"end")
        except IOError:
            messagebox.showerror("File error","Could not save donor data.")

# --- RequestFrame ---
class RequestFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Request Blood", style="Title.TLabel").grid(row=0,column=0,columnspan=2,sticky="w", pady=(2,14))

        ttk.Label(self, text="Patient Name:").grid(row=1,column=0, sticky="w", padx=6,pady=6)
        self.name = ttk.Entry(self)
        self.name.grid(row=1,column=1, sticky="ew", padx=6,pady=6)

        ttk.Label(self, text="Blood Type Needed:").grid(row=2,column=0, sticky="w", padx=6,pady=6)
        self.blood = ttk.Combobox(self, values=BLOOD_TYPES, state="readonly")
        self.blood.grid(row=2,column=1, sticky="w", padx=6,pady=6)

        ttk.Label(self, text="Location (Hospital/City):").grid(row=3,column=0, sticky="w", padx=6,pady=6)
        self.location = ttk.Entry(self)
        self.location.grid(row=3,column=1, sticky="ew", padx=6,pady=6)

        ttk.Label(self, text="Urgency Level:").grid(row=4,column=0, sticky="w", padx=6,pady=6)
        self.urgency = ttk.Combobox(self, values=URGENCY_LEVELS, state="readonly")
        self.urgency.grid(row=4,column=1, sticky="w", padx=6,pady=6)

        btn = ttk.Button(self, text="Submit Request", style="Primary.TButton", command=self.submit_request)
        btn.grid(row=5,column=0,columnspan=2, pady=(14,6), padx=6, sticky="ew")

    def submit_request(self):
        name = self.name.get().strip()
        blood = self.blood.get().strip()
        location = self.location.get().strip()
        urgency = self.urgency.get().strip()

        if not all([name,blood,location,urgency]):
            messagebox.showwarning("Missing data","Please fill all fields.")
            return

        try:
            with REQUEST_FILE.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([name,blood,location,urgency])
            messagebox.showinfo("Success","Request submitted successfully.")
            self.name.delete(0,"end")
            self.blood.set("")
            self.location.delete(0,"end")
            self.urgency.set("")
        except IOError:
            messagebox.showerror("File error","Could not save request.")

# --- MatchFrame ---
class MatchFrame(ttk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

        ttk.Label(self, text="Find Donor Match", style="Title.TLabel").grid(row=0,column=0,columnspan=3,sticky="w", pady=(2,14))

        ttk.Label(self, text="Blood Type Needed:").grid(row=1,column=0, sticky="w", padx=6,pady=6)
        self.blood = ttk.Combobox(self, values=BLOOD_TYPES, state="readonly")
        self.blood.grid(row=1,column=1, sticky="w", padx=6,pady=6)

        ttk.Label(self, text="Location (optional):").grid(row=2,column=0, sticky="w", padx=6,pady=6)
        self.location = ttk.Entry(self)
        self.location.grid(row=2,column=1, sticky="ew", padx=6,pady=6)

        btn = ttk.Button(self, text="Find Matches", style="Primary.TButton", command=self.find_matches)
        btn.grid(row=1,column=2,rowspan=2,padx=8,pady=6, sticky="ns")

        cols = ("Name","Blood","Location","Contact","Age")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w", width=140 if c!="Age" else 60)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=4,column=0,columnspan=3,sticky="nsew", padx=6,pady=(10,6))
        vsb.grid(row=4,column=3,sticky="ns", pady=(10,6))

    def find_matches(self):
        blood_needed = self.blood.get().strip()
        loc = self.location.get().strip().lower()

        if not blood_needed:
            messagebox.showwarning("Select blood","Please select a blood type.")
            return

        for r in self.tree.get_children():
            self.tree.delete(r)

        try:
            with DONOR_FILE.open("r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                found=False
                for row in reader:
                    donor_blood = row["blood"].strip()
                    donor_loc = row["location"].strip().lower()
                    if donor_blood==blood_needed and (not loc or loc in donor_loc):
                        self.tree.insert("", "end", values=(row["name"], donor_blood, row["location"], row["contact"], row["age"]))
                        found=True
                if not found:
                    messagebox.showinfo("No matches","No donors found matching criteria.")
        except IOError:
            messagebox.showerror("File error","Could not read donor data.")

# --- VerifyFrame ---
class VerifyFrame(ttk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent, style="Card.TFrame")
        self.controller = controller
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Verify Donor Identity", style="Title.TLabel").grid(row=0,column=0,columnspan=2,sticky="w", pady=(2,14))
        ttk.Label(self, text="Donor Name:").grid(row=1,column=0, sticky="w", padx=6,pady=6)
        self.name = ttk.Entry(self)
        self.name.grid(row=1,column=1, sticky="ew", padx=6,pady=6)

        btn = ttk.Button(self, text="Verify", style="Primary.TButton", command=self.verify)
        btn.grid(row=2,column=0,columnspan=2,pady=(12,6), padx=6, sticky="ew")

    def verify(self):
        target = self.name.get().strip()
        if not target:
            messagebox.showwarning("Missing","Enter a name to verify.")
            return
        try:
            with BLOCKCHAIN_FILE.open("r", encoding="utf-8") as f:
                names = [line.strip().lower() for line in f if line.strip()]
            if target.lower() in names:
                messagebox.showinfo("Verified", f"'{target}' is verified and registered as donor.")
            else:
                res = messagebox.askyesno("Not Found", f"'{target}' not found. Add to blockchain simulation?")
                if res:
                    append_donor_to_blockchain(target)
                    messagebox.showinfo("Added", f"'{target}' added to blockchain simulation.")
            self.name.delete(0,"end")
        except IOError:
            messagebox.showerror("File error","Could not read blockchain data.")

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    ensure_data_files()
    app = BloodDonationApp()
    app.mainloop()
