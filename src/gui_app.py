import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
from src.models import Guest, Room
from src.invoices import Invoice
from src.hotel_manager import HotelManager

class FullHotelManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Zarządzania Hotelem v1.2 Premium")
        self.root.geometry("950x620")
        self.root.configure(bg="#1e1e24")
        
        self.manager = HotelManager("Hotel Premium")
        self.next_guest_id = 1
        self.next_res_id = 100
        self.next_inv_id = 500

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        self.notebook = ttk.Notebook(root, style="Modern.TNotebook")
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_guests = tk.Frame(self.notebook, bg="#1e1e24")
        self.tab_rooms = tk.Frame(self.notebook, bg="#1e1e24")
        self.tab_reservations = tk.Frame(self.notebook, bg="#1e1e24")
        self.tab_invoices = tk.Frame(self.notebook, bg="#1e1e24")

        self.notebook.add(self.tab_guests, text="  Goście  ")
        self.notebook.add(self.tab_rooms, text="  Pokoje  ")
        self.notebook.add(self.tab_reservations, text="  Rezerwacje  ")
        self.notebook.add(self.tab_invoices, text="  Finanse i Faktury  ")

        self.setup_guests_tab()
        self.setup_rooms_tab()
        self.setup_reservations_tab()
        self.setup_invoices_tab()

    def configure_styles(self):
        self.style.configure("Modern.TNotebook", background="#1e1e24", borderwidth=0)
        self.style.configure("Modern.TNotebook.Tab", background="#2a2a35", foreground="#a0a0b0", font=("Segoe UI", 10, "bold"), padding=[18, 10], borderwidth=0)
        self.style.map("Modern.TNotebook.Tab", background=[("selected", "#00b4d8")], foreground=[("selected", "#ffffff")])
        
        self.style.configure("Treeview", background="#2a2a35", fieldbackground="#2a2a35", foreground="#ffffff", rowheight=32, font=("Segoe UI", 10), borderwidth=0)
        self.style.configure("Treeview.Heading", background="#3a3a4c", foreground="#ffffff", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=6)
        self.style.map("Treeview", background=[("selected", "#0077b6")])

    def create_modern_sidebar(self, parent, title):
        frame = tk.Frame(parent, bg="#2a2a35", padx=20, pady=20)
        frame.pack(side="left", fill="y", padx=(0, 15), pady=10)
        
        lbl = tk.Label(frame, text=title, font=("Segoe UI", 14, "bold"), bg="#2a2a35", fg="#00b4d8")
        lbl.pack(anchor="w", pady=(0, 15))
        return frame

    def create_modern_table_frame(self, parent, title):
        frame = tk.Frame(parent, bg="#2a2a35", padx=20, pady=20)
        frame.pack(side="right", fill="both", expand=True, pady=10)
        
        header_frame = tk.Frame(frame, bg="#2a2a35")
        header_frame.pack(fill="x", pady=(0, 10))
        
        lbl = tk.Label(header_frame, text=title, font=("Segoe UI", 14, "bold"), bg="#2a2a35", fg="#ffffff")
        lbl.pack(side="left")
        
        hint_lbl = tk.Label(header_frame, text="", font=("Segoe UI", 9, "italic"), bg="#2a2a35", fg="#00b4d8")
        hint_lbl.pack(side="right")
        
        return frame, hint_lbl

    def create_label_entry(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 9, "bold"), bg="#2a2a35", fg="#a0a0b0")
        lbl.pack(anchor="w", pady=(6, 2))
        entry = tk.Entry(parent, font=("Segoe UI", 10), bg="#1e1e24", fg="#ffffff", insertbackground="white", bd=0, highlightthickness=1, highlightbackground="#3a3a4c", highlightcolor="#00b4d8")
        entry.pack(fill="x", pady=(0, 6), ipady=5)
        return entry

    def create_modern_button(self, parent, text, bg_color, command):
        btn = tk.Button(parent, text=text, command=command, font=("Segoe UI", 10, "bold"), bg=bg_color, fg="white", activebackground=bg_color, activeforeground="white", bd=0, cursor="hand2", relief="flat")
        btn.pack(fill="x", pady=(18, 0), ipady=7)
        
        def on_enter(e): btn.config(bg=self.lighten_color(bg_color))
        def on_leave(e): btn.config(bg=bg_color)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def lighten_color(self, hex_color):
        if hex_color == "#00b4d8": return "#00c4e8"
        if hex_color == "#2a9d8f": return "#32b3a2"
        if hex_color == "#e76f51": return "#f47c60"
        if hex_color == "#9b5de5": return "#a875ec"
        return hex_color

    def setup_guests_tab(self):
        sb = self.create_modern_sidebar(self.tab_guests, "Rejestracja Gościa")
        self.ent_g_name = self.create_label_entry(sb, "Imię i Nazwisko")
        self.ent_g_email = self.create_label_entry(sb, "Adres Email")
        self.ent_g_phone = self.create_label_entry(sb, "Numer Telefonu")
        self.ent_g_doc = self.create_label_entry(sb, "Numer Dokumentu")
        self.create_modern_button(sb, "Zarejestruj gościa", "#2a9d8f", self.ui_add_guest)

        tf, self.hint_guests = self.create_modern_table_frame(self.tab_guests, "Księga Gości")
        cols = ("id", "name", "email", "phone", "doc")
        self.tree_guests = ttk.Treeview(tf, columns=cols, show="headings")
        for col, head in [("id", "ID"), ("name", "Imię i Nazwisko"), ("email", "Email"), ("phone", "Telefon"), ("doc", "Dokument")]:
            self.tree_guests.heading(col, text=head)
            self.tree_guests.column(col, width=100, anchor="center" if col=="id" else "w")
        self.tree_guests.pack(fill="both", expand=True)

    def ui_add_guest(self):
        guest = Guest(self.next_guest_id, self.ent_g_name.get(), self.ent_g_email.get(), self.ent_g_phone.get(), self.ent_g_doc.get())
        if not guest.is_data_complete() or not guest.is_email_valid():
            messagebox.showerror("Błąd", "Niepoprawne lub niekompletne dane gościa!")
            return
        self.manager.register_guest(guest)
        self.tree_guests.insert("", "end", values=(guest.guest_id, guest.name, guest.email, guest.phone, guest.document_id))
        self.hint_guests.config(text=f"Ostatnio dodane ID: {self.next_guest_id}")
        self.next_guest_id += 1
        self.clear_fields([self.ent_g_name, self.ent_g_email, self.ent_g_phone, self.ent_g_doc])

    def setup_rooms_tab(self):
        sb = self.create_modern_sidebar(self.tab_rooms, "Zasoby Hotelu")
        self.ent_r_num = self.create_label_entry(sb, "Numer Pokoju")
        
        tk.Label(sb, text="Standard Pokoju", font=("Segoe UI", 9, "bold"), bg="#2a2a35", fg="#a0a0b0").pack(anchor="w", pady=(5, 2))
        self.cb_r_type = ttk.Combobox(sb, values=["Standard", "Deluxe", "Suite"], font=("Segoe UI", 10), state="readonly")
        self.cb_r_type.pack(fill="x", pady=(0, 5))
        self.cb_r_type.current(0)
        
        self.ent_r_price = self.create_label_entry(sb, "Cena za jedną noc")
        self.create_modern_button(sb, "Dodaj nowy pokój", "#00b4d8", self.ui_add_room)

        tf, help_lbl = self.create_modern_table_frame(self.tab_rooms, "Wykaz Pokoi")
        help_lbl.config(text="Kliknij 2x w wiersz, aby zmienić stan czystości", fg="#a0a0b0")
        
        cols = ("num", "type", "price", "clean")
        self.tree_rooms = ttk.Treeview(tf, columns=cols, show="headings")
        for col, head in [("num", "Nr pokoju"), ("type", "Klasa pokoju"), ("price", "Cena za noc"), ("clean", "Stan czystości")]:
            self.tree_rooms.heading(col, text=head)
            self.tree_rooms.column(col, width=100, anchor="center")
        self.tree_rooms.pack(fill="both", expand=True)
        
        self.tree_rooms.tag_configure("dirty", background="#3d2a2a", foreground="#ff6b6b")
        self.tree_rooms.tag_configure("clean", background="#2a3d30", foreground="#2ec4b6")
        self.tree_rooms.bind("<Double-1>", self.ui_toggle_room_cleanliness)

    def ui_add_room(self):
        try:
            room = Room(int(self.ent_r_num.get()), self.cb_r_type.get(), float(self.ent_r_price.get()))
            self.manager.add_room(room)
            tag = "clean" if room.is_clean else "dirty"
            self.tree_rooms.insert("", "end", values=(room.room_number, room.room_type, f"{room.price_per_night:.2f} PLN", "Czysty" if room.is_clean else "Wymaga sprzątania"), tags=(tag,))
            self.clear_fields([self.ent_r_num, self.ent_r_price])
        except ValueError:
            messagebox.showerror("Błąd", "Numer oraz cena muszą mieć format liczbowy!")

    def ui_toggle_room_cleanliness(self, event):
        selected_item = self.tree_rooms.selection()
        if not selected_item: return
        item_values = self.tree_rooms.item(selected_item, "values")
        r_num = int(item_values[0])
        
        room = next((r for r in self.manager.rooms if r.room_number == r_num), None)
        if room:
            if room.is_clean:
                room.mark_as_dirty()
                self.tree_rooms.item(selected_item, values=(room.room_number, room.room_type, item_values[2], "Wymaga sprzątania"), tags=("dirty",))
            else:
                room.mark_as_clean()
                self.tree_rooms.item(selected_item, values=(room.room_number, room.room_type, item_values[2], "Czysty"), tags=("clean",))

    def setup_reservations_tab(self):
        sb = self.create_modern_sidebar(self.tab_reservations, "Terminarz")
        self.ent_res_gid = self.create_label_entry(sb, "ID Gościa")
        self.ent_res_rnum = self.create_label_entry(sb, "Numer Pokoju")
        self.ent_res_start = self.create_label_entry(sb, "Meldunek (RRRR-MM-DD)")
        self.ent_res_start.insert(0, "2026-07-01")
        self.ent_res_end = self.create_label_entry(sb, "Wymeldowanie (RRRR-MM-DD)")
        self.ent_res_end.insert(0, "2026-07-05")
        self.create_modern_button(sb, "Utwórz rezerwację", "#e76f51", self.ui_create_reservation)

        tf, self.hint_res = self.create_modern_table_frame(self.tab_reservations, "Grafik Rezerwacji")
        cols = ("id", "guest", "room", "dates", "cost", "status")
        self.tree_res = ttk.Treeview(tf, columns=cols, show="headings")
        for col, head in [("id", "ID"), ("guest", "Gość"), ("room", "Pokój"), ("dates", "Okres pobytu"), ("cost", "Koszt całkowity"), ("status", "Status")]:
            self.tree_res.heading(col, text=head)
            self.tree_res.column(col, width=100, anchor="center" if col in ["id", "room", "status"] else "w")
        self.tree_res.pack(fill="both", expand=True)
        self.tree_res.tag_configure("active", background="#3d342a", foreground="#f4a261")

    def ui_create_reservation(self):
        try:
            g_id = int(self.ent_res_gid.get())
            r_num = int(self.ent_res_rnum.get())
            d1 = datetime.strptime(self.ent_res_start.get(), "%Y-%m-%d").date()
            d2 = datetime.strptime(self.ent_res_end.get(), "%Y-%m-%d").date()

            selected_guest = next((g for g in self.manager.guests if g.guest_id == g_id), None)
            selected_room = next((r for r in self.manager.rooms if r.room_number == r_num), None)

            if not selected_guest or not selected_room:
                messagebox.showerror("Błąd", "Wskazany gość lub pokój nie figuruje w systemie!")
                return

            res = self.manager.create_reservation(self.next_res_id, selected_guest, selected_room, d1, d2)
            if res:
                self.tree_res.insert("", "end", values=(res.reservation_id, res.guest.name, res.room.room_number, f"{res.start_date} do {res.end_date}", f"{res.calculate_total_cost():.2f} PLN", "Zatwierdzona"), tags=("active",))
                self.hint_res.config(text=f"Ostatnia rezerwacja ID: {self.next_res_id}")
                self.next_res_id += 1
                self.clear_fields([self.ent_res_gid, self.ent_res_rnum])
            else:
                messagebox.showerror("Błąd", "Pokój jest zajęty w wybranym przedziale czasowym!")
        except Exception:
            messagebox.showerror("Błąd", "Nieprawidłowy format wprowadzonych danych lub dat!")

    def setup_invoices_tab(self):
        sb = self.create_modern_sidebar(self.tab_invoices, "Księgowość")
        self.ent_inv_resid = self.create_label_entry(sb, "ID Rezerwacji")
        self.create_modern_button(sb, "Wystaw fakturę", "#9b5de5", self.ui_create_invoice)

        tf, help_lbl = self.create_modern_table_frame(self.tab_invoices, "Rejestr Dokumentów Finansowych")
        help_lbl.config(text="Kliknij 2x w wiersz, aby oznaczyć jako OPŁACONA", fg="#a0a0b0")
        
        cols = ("id", "client", "total", "status")
        self.tree_inv = ttk.Treeview(tf, columns=cols, show="headings")
        for col, head in [("id", "Numer Faktury"), ("client", "Kontrahent"), ("total", "Należność"), ("status", "Status płatności")]:
            self.tree_inv.heading(col, text=head)
            self.tree_inv.column(col, width=120, anchor="center" if col in ["id", "total", "status"] else "w")
        self.tree_inv.pack(fill="both", expand=True)
        
        self.tree_inv.tag_configure("unpaid", background="#3d2a2a", foreground="#ff6b6b")
        self.tree_inv.tag_configure("paid", background="#2a3d30", foreground="#2ec4b6")
        self.tree_inv.bind("<Double-1>", self.ui_pay_invoice)

    def ui_create_invoice(self):
        try:
            res_id = int(self.ent_inv_resid.get())
            reservation = next((r for r in self.manager.reservations if r.reservation_id == res_id), None)

            if not reservation:
                messagebox.showerror("Błąd", "Brak rezerwacji o podanym identyfikatorze!")
                return

            inv = Invoice(self.next_inv_id, reservation, date.today())
            self.tree_inv.insert("", "end", values=(f"FV/{inv.invoice_id}", inv.reservation.guest.name, f"{inv.reservation.calculate_total_cost():.2f} PLN", "Nieopłacona"), tags=("unpaid",))
            self.next_inv_id += 1
            self.clear_fields([self.ent_inv_resid])
        except ValueError:
            messagebox.showerror("Błąd", "Identyfikator rezerwacji musi być liczbą!")

    def ui_pay_invoice(self, event):
        selected_item = self.tree_inv.selection()
        if not selected_item: return
        item_values = self.tree_inv.item(selected_item, "values")
        
        inv_id = int(item_values[0].replace("FV/", ""))
        self.tree_inv.item(selected_item, values=(item_values[0], item_values[1], item_values[2], "OPŁACONA"), tags=("paid",))

    def clear_fields(self, entries):
        for entry in entries:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = FullHotelManagementGUI(root)
    root.mainloop()