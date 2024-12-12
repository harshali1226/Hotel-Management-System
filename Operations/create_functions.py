from Config.connection import *
from Operations import update_functions
import re, random
from datetime import datetime

"""Validation function for email."""
def is_valid_email(email):
    # Regular expression for validating an Email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

"""Function to add a new guest to the database."""
def insert_new_guest(guest_name, city, state, street, zipcode, email, phone_numbers):
    connection = create_connection()
    if connection:
        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Insert guest query
            guest_query = """
                INSERT INTO Guest (GuestName, Address_City, Address_State, Address_Street, Address_Zipcode, Email)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            guest_data = (guest_name, city, state, street, zipcode, email)

            # Execute the guest insert query
            cursor.execute(guest_query, guest_data)
            connection.commit()

            guest_id = cursor.lastrowid  # Fetch the newly inserted GuestID

            # Insert phone numbers
            print("Running the phone_query now")
            phone_query = "INSERT INTO guest_phone (GuestID, Phone) VALUES (%s, %s)"
            for phone in phone_numbers:
                cursor.execute(phone_query, (guest_id, phone))
            
            connection.commit()

            print(f"Guest '{guest_name}' added successfully!")
        except mysql.connector.Error as err:
            print("Failed to insert a new guest in the database! Please try again")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

"""Function to add a new staff member in the database."""
def insert_new_staff_member(staff_name, role, contact_info):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"""
            INSERT INTO Staff (StaffName, Role, ContactInfo)
            VALUES (%s, %s, %s)
            """
            data = (staff_name, role, contact_info)
            cursor.execute(query, data)
            connection.commit()  # Commit the transaction
            print("Staff created successfully!\n")
        except Exception as e:
            print("Failed to create a new staffmember!\n")
        finally:
            cursor.close()
            connection.close()

"""Function to add new room based on room type."""
def insert_new_room():
    roomtype = input("Enter room type (Single, Deluxe, Suite, Queen, King): ").strip()
    
    # Set default values based on room type
    if roomtype.lower() == 'single':
        price, capacity, status = 100, 1, 'Available'
    elif roomtype.lower() == 'deluxe':
        price, capacity, status = 150, 2, 'Available'
    elif roomtype.lower() == 'suite':
        price, capacity, status = 250, 6, 'Available'
    elif roomtype.lower() == 'queen':
        price, capacity, status = 120, 3, 'Available'
    elif roomtype.lower() == 'king':
        price, capacity, status = 180, 4, 'Available'
    else:
        print("Invalid room type! Please enter a valid room type.")
        return
    
    room_data = (roomtype, price, capacity, status)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO room (roomtype, price, capacity, status)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, room_data)
            connection.commit()
            print(f"{roomtype.capitalize()} room added successfully!")
        except Exception as e:
            print("Failed to add room.")
        finally:
            cursor.close()
            connection.close()

"""Function to add a new service to the database."""
def insert_new_service():
    update_functions.get_all_services()
    # Get user input
    while True:
        try:
            serviceID = input("Enter the id of the service: ").strip()
            break
        except ValueError:
            print("Invalid input. Please enter a valid id as a number.")

    service_type = input("Enter the service type: ").strip()
    description = input("Enter the description: ").strip()

    # Ensure cost is a valid number
    while True:
        try:
            cost = float(input("Enter the cost of the service: ").strip())
            break
        except ValueError:
            print("Invalid input. Please enter a valid cost as a number.")
    
        # Establish connection to the database
    connection = create_connection()  # Assume create_connection function is already defined
    if connection:
        try:
            cursor = connection.cursor()

            # Insert data into the Service table
            insert_query = """
            INSERT INTO Service (ServiceID, ServiceType, Description, Cost)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (serviceID,service_type, description, cost))
            connection.commit()

            print("New service added successfully!")

        except mysql.connector.Error as err:
            print("Failed to add the new service to the database! Please try again")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

"""Function to add a new reservation"""
def insert_new_reservation():
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Step 1: Get reservation details from the user
        while True:
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            check_out = input("Enter check-out date (YYYY-MM-DD): ")

            # Validate date inputs
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            # Check if check-in date is in the past
            if check_in_date < datetime.now():
                print("Check-in date cannot be in the past. Please enter a valid date.")
                continue

            # Check if check-in date is earlier than check-out date
            if check_in_date >= check_out_date:
                print("Check-in date must be earlier than check-out date. Please try again.")
                continue
            
            break  # Exit loop if date checks are passed

        room_type = input("Enter room type (Single, Deluxe, Queen, King, Suite): ").strip()

        # Fetch available rooms for the selected room type and their prices
        room_query = """
            SELECT RoomNumber, Price FROM room 
            WHERE RoomType = %s 
            AND RoomNumber NOT IN (
                SELECT RoomNumber FROM reservation 
                WHERE (CheckInDate < %s AND CheckOutDate > %s)
            );
        """
        cursor.execute(room_query, (room_type, check_out, check_in))
        available_rooms = cursor.fetchall()

        if not available_rooms:
            print("No rooms available for the selected type and dates.")
            return
        
        # Select a room and retrieve its price
        room_number, room_price = available_rooms[0]  # Pick the first available room

        # Step 2: Get or insert guest information
        guest_name = input("Guest name: ")

        # Validate email input
        while True:
            guest_email = input("Guest email: ")
            if not is_valid_email(guest_email):
                print("Invalid email format. Please enter a valid email address.")
                continue
            break

        guest_id = None
        cursor.execute("SELECT GuestID FROM guest WHERE GuestName = %s AND Email = %s", (guest_name, guest_email))
        result = cursor.fetchone()
        if result:
            guest_id = result[0]
        else:
            print("Not an existing guest. Please enter additional details to create new guest.")
            address_city = input("City: ")
            address_state = input("State: ")
            address_street = input("Street: ")
            address_zipcode = input("Zipcode: ")

            # Insert new guest
            guest_query = """
                INSERT INTO guest (GuestName, Address_City, Address_State, Address_Street, Address_Zipcode, Email) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(guest_query, (guest_name, address_city, address_state, address_street, address_zipcode, guest_email))
            guest_id = cursor.lastrowid

            # Input guest phone numbers. Since this is a multivalued attribute separate loop is created.
            while True:
                phone = input("Enter phone number (or type 'done' to finish): ").strip()
                
                # Check if input is 'done' or a valid 10-digit number
                if phone.lower() == 'done':
                    break
                elif not (phone.isdigit() and len(phone) == 10):
                    print("Invalid input. Please enter a 10-digit phone number or 'done' to finish.")
                    continue

                cursor.execute("INSERT INTO guest_phone (GuestID, Phone) VALUES (%s, %s)", (guest_id, phone))

        # Step 3: Get a random staff ID to assign to the reservation
        cursor.execute("SELECT StaffID FROM staff")
        staff_ids = [row[0] for row in cursor.fetchall()]
        if not staff_ids:
            print("No staff available to assign.")
            return
        staff_id = random.choice(staff_ids)

        # Step 4: Insert reservation with calculated TotalCost
        reservation_query = """
            INSERT INTO reservation (CheckInDate, CheckOutDate, ReservationStatus, TotalCost, StaffID, GuestID, RoomNumber) 
            VALUES (%s, %s, 'Confirmed', %s, %s, %s, %s)
        """
        cursor.execute(reservation_query, (check_in, check_out, room_price, staff_id, guest_id, room_number))
        reservation_id = cursor.lastrowid  # Get the reservation ID for the new reservation

        connection.commit()
        print(f"Reservation created successfully! Please note your reservation id: {reservation_id}")

    except Exception as e:
        print("Reservation creation failed! Please try again.")
    finally:
        cursor.close()
        connection.close()