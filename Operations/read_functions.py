from Config.connection import *

"""Dynamic query fetch all records from the database for a mentioned table."""
def fetch_records(table_name):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM {table_name}"
            cursor.execute(query)
            result = cursor.fetchall()

            for row in result:
                print(row)
        except Exception as e:
            print("Failed to fetch the information")

"""Fetch the information of a particular staff member by the staff ID"""
def fetch_particular_staff_member(staff_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM Staff WHERE StaffID = %s"
            cursor.execute(query, (staff_id,))
            result = cursor.fetchone()
            
            if result:
                print("**************Staff Details**************")
                print(f"StaffID: {result[0]}")
                print(f"StaffName: {result[1]}")
                print(f"Role: {result[2]}")
                print(f"Contact Info: {result[3]}")
            else:
                print("Staff not found!")
        except Exception as e:
            print("Failed to retrieve staff details!\n")
        finally:
            cursor.close()
            connection.close()

"""Fetch the information of a reservation using the reservation ID"""
def get_reservation_details(id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM reservation WHERE reservationID = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone() 

            if result:
                print("**************Reservation Details**************")
                print(f"ReservationID: {result[0]}")
                print(f"Check-in Date: {result[1]}")
                print(f"Check-out-Date: {result[2]}")
                print(f"Reservation Status: {result[3]}")
                print(f"RoomNumber: {result[7]}")
        except Exception as e:
            print("Failed to retrieve reservation details!\n")
        finally:
            cursor.close()
            connection.close()

"""Fetch the total cost incurred for a reservation using the reservation ID."""
def get_reservation_cost(id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT TotalCost FROM reservation WHERE reservationID = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone() 

            if result:
                total_cost = result[0]
                print(f"The total cost for this reservation is: ${total_cost:.2f}")
            else:
                print(f"No reservation found with ID {id}.")
        except Exception as e:
            print("Failed to retrieve reservation details!\n")
        finally:
            cursor.close()
            connection.close()

"""Function to fetch the guest information based on the name and email."""
def get_guest_information(name,email):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM guest WHERE GuestName = %s and Email = %s"
            cursor.execute(query, (name,email))
            result = cursor.fetchone() 

            if result:
                print("**************Guest Details**************")
                print(f"Guest Name: {result[1]}")
                print(f"Guest Email: {result[6]}")
                print(f"Guest city: {result[2]}")
                print(f"Guest state: {result[3]}")
                print(f"Guest street: {result[4]}")
                print(f"Guest zipcode: {result[5]}")
            else:
                print(f"No guest found with name {name} and email {email}.")
        except Exception as e:
            print("Failed to retrieve guest details!\n")
        finally:
            cursor.close()
            connection.close()