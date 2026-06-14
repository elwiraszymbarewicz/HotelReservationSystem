from datetime import date
from src.models import Reservation
class Invoice:
    """Reprezentuje fakturę wystawioną do konkretnej rezerwacji hotelowej."""
    def __init__(self, invoice_id: int, reservation: Reservation, issued_date: date):
        self.invoice_id: int = invoice_id
        self.reservation: Reservation = reservation
        self.issued_date: date = issued_date
        self.is_paid: bool = False
    def generate_summary(self) -> str:
        """Generuje czytelne, tekstowe podsumowanie faktury dla klienta."""
        total_cost = self.reservation.calculate_total_cost()
        guest_name = self.reservation.guest.name
        room_num = self.reservation.room.room_number
        return (
            f"Faktura FV/{self.invoice_id}\n"
            f"Nabywca: {guest_name}\n"
            f"Pokój nr: {room_num}\n"
            f"Kwota całkowita: {total_cost:.2f} PLN"
        )
    def mark_as_paid(self) -> None:
        """Zmienia status płatności faktury na opłaconą."""
        self.is_paid = True