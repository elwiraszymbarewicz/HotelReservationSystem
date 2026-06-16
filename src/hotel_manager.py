from datetime import date
from typing import Optional
from src.models import Room, Guest, Reservation


class HotelManager:
    """Główna klasa zarządzająca systemem (Fasada).
    Odpowiada za rejestrację danych oraz kluczową logikę dostępności pokoi.
    """

    def __init__(self, hotel_name: str):
        self.hotel_name: str = hotel_name
        self.rooms: list[Room] = []
        self.guests: list[Guest] = []
        self.reservations: list[Reservation] = []

    def add_room(self, room: Room) -> None:
        """Dodaje nowy pokój do oferty hotelu."""
        self.rooms.append(room)

    def register_guest(self, guest: Guest) -> None:
        """Rejestruje nowego gościa w systemie hotelowym."""
        self.guests.append(guest)

    def check_availability(
        self,
        room_number: int,
        start_date: date,
        end_date: date
    ) -> bool:
        """Sprawdza, czy pokój o danym numerze jest wolny w wybranym przedziale czasowym.

        Zwraca False, jeśli termin nachodzi na jakąkolwiek aktywną rezerwację tego pokoju.
        """
        for res in self.reservations:
            if res.room.room_number == room_number and res.is_active:
                if not (end_date <= res.start_date or start_date >= res.end_date):
                    return False
        return True

    def create_reservation(
        self,
        res_id: int,
        guest: Guest,
        room: Room,
        start: date,
        end: date
    ) -> Optional[Reservation]:
        """Tworzy i zapisuje rezerwację, o ile wybrany pokój jest dostępny."""
        if self.check_availability(room.room_number, start, end):
            new_res = Reservation(res_id, guest, room, start, end)
            self.reservations.append(new_res)
            return new_res
        return None