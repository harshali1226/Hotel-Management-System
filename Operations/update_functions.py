from Config.connection import *
from datetime import datetime
from Operations import read_functions

"""Function to update the guest information using guest email and name."""
def update_guest(name, email):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the guest exists
            select_query = "SELECT * FROM Guest WHERE GuestName = %s AND Email = %s"
            cursor.execute(select_query, (name, email))
            guest = cursor.fetchone()

            if guest:
                # Take the input to update the guest information
                updated_name = input("Enter new Guest Name (leave blank to keep current): ").strip()
                updated_email = input("Enter new Email (leave blank to keep current): ").strip()

                updated_city = input("Enter new Address City (leave blank to keep current): ").strip()
                updated_state = input("Enter new Address State (leave blank to keep current): ").strip()
                updated_street = input("Enter new Address Street (leave blank to keep current): ").strip()
                updated_zipcode = input("Enter new Address Zipcode (leave blank to keep current): ").strip()

                # Prepare update query
                update_query = "UPDATE Guest SET "
                update_values = []

                if updated_name:
                    update_query += "GuestName = %s, "
                    update_values.append(updated_name)

                if updated_email:
                    update_query += "Email = %s, "
                    update_values.append(updated_email)

                if updated_city:
                    update_query += "Address_City = %s, "
                    update_values.append(updated_city)

                if updated_state:
                    update_query += "Address_State = %s, "
                    update_values.append(updated_state)

                if updated_street:
                    update_query += "Address_Street = %s, "
                    update_values.append(updated_street)

                if updated_zipcode:
                    update_query += "Address_Zipcode = %s, "
                    update_values.append(updated_zipcode)

                # Remove the last comma and space
                update_query = update_query.rstrip(", ")
                update_query += " WHERE GuestName = %s AND Email = %s"
                update_values.append(name) 
                update_values.append(email)

                cursor.execute(update_query, tuple(update_values))
                connection.commit()

                print(f"Guest information updated successfully.")
            else:
                print(f"No guest found with Name '{name}' and Email '{email}'.")

        except mysql.connector.Error as err:
            print("Could not update the guest information! try again.")
        finally:
            cursor.close()
            connection.close()

"""Function to update the reservation information using reservation ID."""
def update_reservation(reservation_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the reservation exists
            select_query = "SELECT * FROM reservation WHERE ReservationID = %s"
            cursor.execute(select_query, (reservation_id,))
            reservation = cursor.fetchone()

            if reservation:
                read_functions.get_reservation_details(reservation_id)
                
                # Take the input to update the guest information
                updated_check_in = input("Enter new CheckInDate (YYYY-MM-DD) (leave blank to keep current): ").strip()
                updated_check_out = input("Enter new CheckOutDate (YYYY-MM-DD) (leave blank to keep current): ").strip()
                updated_status = input("Enter new ReservationStatus (leave blank to keep current): ").strip()
                updated_total_cost = input("Enter new TotalCost (leave blank to keep current): ").strip()

                # Prepare update query
                update_query = "UPDATE reservation SET "
                update_values = []

                if updated_check_in:
                    try:
                        datetime.strptime(updated_check_in, '%Y-%m-%d')
                        update_query += "CheckInDate = %s, "
                        update_values.append(updated_check_in)
                    except ValueError:
                        print("Invalid date format for the check-in-date. Skipping update.")

                if updated_check_out:
                    try:
                        datetime.strptime(updated_check_out, '%Y-%m-%d')
                        update_query += "CheckOutDate = %s, "
                        update_values.append(updated_check_out)
                    except ValueError:
                        print("Invalid date format for check-out-date. Skipping update.")

                if updated_status:
                    update_query += "ReservationStatus = %s, "
                    update_values.append(updated_status)


                # Remove the last comma and space
                update_query = update_query.rstrip(", ")
                update_query += " WHERE ReservationID = %s"
                update_values.append(reservation_id)

                # Execute the update query
                if update_values:
                    cursor.execute(update_query, tuple(update_values))
                    connection.commit()
                    print(f"Reservation with ID {reservation_id} updated successfully.")
                else:
                    print("No valid updates were provided.")
            else:
                print(f"No reservation found with ID '{reservation_id}'.")

        except mysql.connector.Error as err:
            print("Could not update the reservation! try again")
        finally:
            cursor.close()
            connection.close()

"""Function to fetch the information of all the services available."""
def get_all_services():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Query to fetch all services from the view
            cursor.execute("SELECT * FROM all_services")
            services = cursor.fetchall()
            
            print("Available Services:\n")
            print(f"{'ServiceID':<10} {'ServiceType':<20} {'Description':<50} {'Cost':<10}")
            print("-" * 90)

            for service in services:
                service_id, service_type, description, cost = service
                print(f"{service_id:<10} {service_type:<20} {description:<50} ${cost:<10.2f}")
        except mysql.connector.Error as e:
            print("No services present")
        finally:
            cursor.close()
            connection.close()

"""Function to update the service information using service name."""
def update_service_by_name(service_name):
    # Take input for updating service information
    new_type = input(f"Enter new service type for {service_name} (or press Enter to skip): ").strip()
    new_description = input(f"Enter new description for {service_name} (or press Enter to skip): ").strip()
    new_cost = input(f"Enter new cost for {service_name} (or press Enter to skip): ").strip()

    # Build the query dynamically based on the inputs provided
    updates = []
    if new_type:
        updates.append(f"ServiceType = '{new_type}'")
    if new_description:
        updates.append(f"Description = '{new_description}'")
    if new_cost:
        updates.append(f"Cost = {new_cost}")

    if not updates:
        print("No updates provided.")
        return

    update_query = f"UPDATE service SET {', '.join(updates)} WHERE ServiceType = %s"

    # Execute the update query
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(update_query, (service_name,))
            connection.commit()
            print(f"Service '{service_name}' updated successfully!")
        except mysql.connector.Error as e:
            print("Could not update the service! Try again")
        finally:
            cursor.close()
            connection.close()

"""Function to update the staff information using staff id."""
def update_staff_information(staff_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Display the current staff details for the given staff_id
            cursor.execute("SELECT * FROM Staff WHERE StaffID = %s", (staff_id,))
            staff = cursor.fetchone()
            
            if staff:
                print(f"Current Staff Details: ID = {staff[0]}, Name = {staff[1]}, Role = {staff[2]}, Contact = {staff[3]}")
                
                # Get updated details from the user
                new_name = input(f"Enter new name (or press Enter to keep '{staff[1]}'): ").strip()
                new_role = input(f"Enter new role (or press Enter to keep '{staff[2]}'): ").strip()
                new_contact_info = input(f"Enter new contact info (or press Enter to keep '{staff[3]}'): ").strip()

                # Use the old value if the user doesn't input new data
                updated_name = new_name if new_name else staff[1]
                updated_role = new_role if new_role else staff[2]
                updated_contact_info = new_contact_info if new_contact_info else staff[3]

                # Update query
                update_query = """
                UPDATE Staff 
                SET StaffName = %s, Role = %s, ContactInfo = %s 
                WHERE StaffID = %s
                """
                cursor.execute(update_query, (updated_name, updated_role, updated_contact_info, staff_id))
                connection.commit()

                print(f"Staff information updated successfully for StaffID {staff_id}.")

            else:
                print(f"No staff found with ID {staff_id}.")

        except Exception as e:
            print("Failed to update staff information! Please try again.")
        finally:
            cursor.close()
            connection.close()