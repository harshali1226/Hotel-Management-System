from Config.connection import *

"""Function to delete the roomreservation bridge entity record."""
def delete_roomreservation(reservation_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Query to delete the reservation
            delete_query = "DELETE FROM RoomReservation WHERE ReservationID = %s"
            cursor.execute(delete_query, (reservation_id,))
            connection.commit()                
        except mysql.connector.Error as err:
            print("Failed to delete record in roomreservation!\n")
        finally:
            cursor.close()
            connection.close()

"""Function to delete the a reservation based on the reservation ID."""
def delete_reservation(reservation_id):
    delete_roomreservation(reservation_id)
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Query to delete the reservation
            delete_query = "DELETE FROM Reservation WHERE ReservationID = %s"
            cursor.execute(delete_query, (reservation_id,))
            connection.commit()

            if cursor.rowcount > 0:
                print(f"Reservation with ID {reservation_id} deleted successfully!")
            else:
                print(f"No reservation found with ID {reservation_id}.")
                
        except mysql.connector.Error as err:
            print("Failed to delete reservation!\n")
        finally:
            cursor.close()
            connection.close()

"""Function to delete guest information based on the name and email of the guest."""
def delete_guest(name, email):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the guest exists before attempting to delete
            select_query = "SELECT * FROM Guest WHERE GuestName = %s AND Email = %s"
            cursor.execute(select_query, (name, email))
            guest = cursor.fetchone()

            if guest:
                # Delete query
                delete_query = "DELETE FROM Guest WHERE GuestName = %s AND Email = %s"
                cursor.execute(delete_query, (name, email))
                connection.commit()

                print(f"Guest with Name '{name}' and Email '{email}' deleted successfully.")
            else:
                print(f"No guest found with Name '{name}' and Email '{email}'.")

        except mysql.connector.Error as err:
            print("Cannot delete this guest because a reservation is present for this guest. Please delete the reservation first and then delete the user.")
        finally:
            cursor.close()
            connection.close()