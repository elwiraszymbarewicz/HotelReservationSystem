import tkinter as tk
from tkinter import messagebox, ttk
from src.models import Guest

class HotelManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Rezerwacji Hotelowych v1.0")
        self.root.geometry("700x450")
        
        self.guests_list: list[Guest] = []
        self.next_guest_id = 1

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_guests = ttk.Frame(self.notebook)
        self.tab_rooms = ttk.Frame(self.notebook)
        self.tab_reservations = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_guests, text="👤 Goście")
        self.notebook.add(self.tab_rooms, text="🛏️ Pokoje (Do zrobienia)")
        self.notebook.add(self.tab_reservations, text="📅 Rezerwacje (Do zrobienia)")

        self.setup_guests_tab()

    def setup_guests_tab(self):
        """Projektuje wygląd pierwszej zakładki zarządzania gośćmi."""
        form_frame = tk.LabelFrame(self.tab_guests, text=" Dane nowego gościa (Check-in) ", padx=10, pady=10)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form_frame, text="Imię i Nazwisko:").pack(anchor="w")
        self.entry_name = tk.Entry(form_frame, width=25)
        self.entry_name.pack(pady=2, anchor="w")

        tk.Label(form_frame, text="Email:").pack(anchor="w")
        self.entry_email = tk.Entry(form_frame, width=25)
        self.entry_email.pack(pady=2, anchor="w")

        tk.Label(form_frame, text="Numer telefonu:").pack(anchor="w")
        self.entry_phone = tk.Entry(form_frame, width=25)
        self.entry_phone.pack(pady=2, anchor="w")

        tk.Label(form_frame, text="Dowód/Paszport:").pack(anchor="w")
        self.entry_doc = tk.Entry(form_frame, width=25)
        self.entry_doc.pack(pady=2, anchor="w")

        self.btn_add = tk.Button(form_frame, text="Zarejestruj gościa", command=self.add_guest_action, bg="#4CAF50", fg="white")
        self.btn_add.pack(pady=15, fill="x")

        table_frame = tk.LabelFrame(self.tab_guests, text=" Zarejestrowani goście w systemie ", padx=10, pady=10)
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "name", "email", "phone", "doc")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Imię i Nazwisko")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Telefon")
        self.tree.heading("doc", text="Dokument")

        self.tree.column("id", width=30, anchor="center")
        self.tree.column("name", width=130)
        self.tree.column("email", width=130)
        self.tree.column("phone", width=100)
        self.tree.column("doc", width=90)

        self.tree.pack(fill="both", expand=True)

    def add_guest_action(self):
        """Pobiera dane z pól, tworzy obiekt Guest i wrzuca do tabeli."""
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        doc = self.entry_doc.get()

        new_guest = Guest(self.next_guest_id, name, email, phone, doc)

        if not new_guest.is_data_complete():
            messagebox.showwarning("Błąd", "Wszystkie pola formularza muszą być wypełnione!")
            return
        
        if not new_guest.is_email_valid():
            messagebox.showerror("Błąd walidacji", "Adres email musi zawierać znak '@'!")
            return

        self.guests_list.append(new_guest)

        self.tree.insert("", "end", values=(new_guest.guest_id, new_guest.name, new_guest.email, new_guest.phone, new_guest.document_id))

        # Czyścimy formularz po sukcesie
        self.entry_name.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_doc.delete(0, tk.END)

        self.next_guest_id += 1
        messagebox.showinfo("Sukces", "Gość został pomyślnie zarejestrowany!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementGUI(root)
    root.mainloop()