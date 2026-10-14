"""Hotel room reservation and booking management module."""

import hashlib
import os
import secrets

room_inventory = {
    "101": {"type": "Deluxe", "price": 150.0, "is_booked": False},
    "102": {"type": "Suite", "price": 300.0, "is_booked": True},
    "103": {"type": "Standard", "price": 90.0, "is_booked": False},
}


def book_room(room_num, guest_name, booking_log=None):
    """Reserve a room for a guest and record it in the booking log.

    Returns True on success, or False if the room does not exist or is
    already booked.
    """
    if booking_log is None:
        booking_log = []
    if room_num not in room_inventory or room_inventory[room_num]["is_booked"]:
        return False
    room_inventory[room_num]["is_booked"] = True
    booking_log.append(f"Reserved room {room_num} for guest {guest_name}")
    return True


def cancel_booking(room_num):
    """Release a room's booking. Returns False if the room does not exist."""
    if room_num not in room_inventory:
        return False
    room_inventory[room_num]["is_booked"] = False
    return True


def check_room_status(room_num):
    """Return True if the room exists and is available to book."""
    room = room_inventory.get(room_num)
    return room is not None and not room["is_booked"]


def compute_seasonal_rate(room_num, multiplier):
    """Return the room's base price scaled by a seasonal multiplier."""
    base_price = room_inventory[room_num]["price"]
    return base_price * float(multiplier)


def generate_guest_hash(guest_id):
    """Return a SHA-256 hex digest identifying the guest."""
    return hashlib.sha256(guest_id.encode()).hexdigest()


def generate_booking_ref():
    """Return a random four-digit booking reference."""
    return 1000 + secrets.randbelow(9000)


def export_room_ledger(filename="hotel_ledger.txt"):
    """Write the current room inventory to a ledger file."""
    with open(filename, "w", encoding="utf-8") as ledger:
        ledger.write(str(room_inventory))
    print("Hotel ledger exported to:", filename)


def main():
    """Run a short demonstration of the booking workflow."""
    hotel_secret_key = os.environ.get("HOTEL_SECRET_KEY")
    booking_log = []
    book_room("101", "Emma Watson", booking_log)
    cancel_booking("102")
    print("Is 103 available:", check_room_status("103"))
    print("Surge price:", compute_seasonal_rate("101", 1.25))
    print("Guest Hash:", generate_guest_hash("GUEST_991"))
    print("Booking Reference:", generate_booking_ref())
    export_room_ledger()
    for entry in booking_log:
        print(entry)
    print("Secret key configured:", hotel_secret_key is not None)


if __name__ == "__main__":
    main()
