from Config.connection import *

def get_guests_with_payments_or_reservations():
    try:
        # Connect to the database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL UNION query
        query = """
            SELECT GuestID, GuestName
            FROM Guest
            WHERE GuestID IN (SELECT GuestID FROM Reservation)
            UNION
            SELECT GuestID, GuestName
            FROM Guest
            WHERE GuestID IN (
                SELECT res.GuestID
                FROM Reservation res
                JOIN Payment p ON res.ReservationID = p.ReservationID
            );
        """
        
        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestID   GuestName")
        print("-------------------")
        for guest_id, guest_name in results:
            print(f"{guest_id:<8} {guest_name}")

        
    except mysql.connector.Error as error:
        print("Failed to get the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_guests_with_reservation_and_payment():
    """
    Executes a SQL query to find guests who have both a reservation and a payment.
    
    Returns:
    - list of tuples: Guests with (GuestID, GuestName) who have both a reservation and a payment.
    """
    try:
        # Connect to the database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query using EXISTS
        query = """
            SELECT GuestID, GuestName
            FROM Guest
            WHERE EXISTS (
                SELECT 1
                FROM Reservation
                JOIN Payment ON Reservation.ReservationID = Payment.ReservationID
                WHERE Reservation.GuestID = Guest.GuestID
            );
        """
        
        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestID   GuestName")
        print("-------------------")
        for guest_id, guest_name in results:
            print(f"{guest_id:<8} {guest_name}")
    
    except mysql.connector.Error as error:
        print("Failed to execute the query:", error)
    
    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_rooms_less_than_suite_price():
    try:
        # Connect to the database
        connection = create_connection()
        cursor = connection.cursor()
        
        roomtype = input("Enter the room type(Single,  Deluxe, Queen, King, Suite): ")
        # SQL query to find rooms with a price lower than any room of type 'Suite'
        query = f"""
            SELECT RoomNumber, RoomType, Price
            FROM Room
            WHERE Price < ANY (
                SELECT Price
                FROM Room
                WHERE RoomType = '{roomtype}'
            );
        """
        
        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("RoomNumber   RoomType   Price")
        print("-----------------------------")
        for room_number, room_type, price in results:
            print(f"{room_number:<12} {room_type:<10} {price:<10.2f}")
        
    except mysql.connector.Error as error:
        print("Failed to execute the query:", error)
        
    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
