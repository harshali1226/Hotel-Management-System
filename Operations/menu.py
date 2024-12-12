from Operations import create_functions,read_functions,delete_functions,update_functions
from Advanced_Queries import ranking_functions,window_functions,olap_functions,set_operations

def menu():
    while True:
        print("\n===== Hotel Management System =====")
        print("0. Exit")
        print("1. Create new Guest")
        print("2. Create new Reservation")
        print("3. Create new Staff member")
        print("4. Create new service")
        print("5. Create new room")
        print("6. Get the Information about a reservation")
        print("7. Get the information of a particular staff member")
        print("8. Get Information of all the staff members")
        print("9. Get the details of all the rooms")
        print("10. Get the total cost for all a particular resrvation")
        print("11. Update guest information")
        print("12. Update reservation information")
        print("13. Update Staff information")
        print("14. Update service information")
        print("15. Delete reservation information")
        print("16. Delete guest Information")

        print("\n===== Advanced Analytics =====")
        print("17. Rank the reservations by Total Cost")
        print("18. Rank Guests by Number of Reservations")
        print("19. Rank the staff members based on the number of reservations handled")
        print("20. Rank the guests into quartiles based on their spendings")
        print("21. Rank reservations based on their duration")
        print("22. Analyse the price trends of each room by price")
        print("23. Compute Moving Average of Total Costs for Completed Reservations")
        print("24. Calculate Cumulative Total of Payments (Credit Card)")
        print("25. Calculate Average Total Cost of Reservations by Room Type")
        print("26. Calculate Average Cost of Reservations Using ROLLUP")
        print("27. Calculate Top Three Guests by Total Spending")
        print("28. Get All Guests Who Have Made Payments or Made Reservations")
        print("29. Find All Guests Who Have Made a Reservation With Any Payment")
        print("30. Find rooms with a capacity higher than any room")
        
        choice = input("\nEnter your choice: ")

        if choice == '0':
            print("Exiting the system. Goodbye!")
            break
        elif choice == '1':
            print("\nPlease enter the following guest details:")

            # Guest Name input (Cannot be NULL)
            guest_name = input("Guest Name (required): ").strip()
            while not guest_name:
                print("Guest Name cannot be empty!")
                guest_name = input("Guest Name (required): ").strip()

            # Email input (Cannot be NULL)
            email = input("Email (required): ").strip()
            while not email or not create_functions.is_valid_email(email):
                if not email:
                    print("Email cannot be empty!")
                else:
                    print("Invalid email format. Please provide a valid email address.")
                email = input("Email (required): ").strip()

            # Address information
            city = input("City: ").strip()
            state = input("State: ").strip()
            street = input("Street: ").strip()
            zipcode = input("Zipcode: ").strip()

            # Phone numbers input (allow multiple phone numbers)
            phone_numbers = []
            while True:
                phone = input("Enter phone number (or press Enter to finish): ").strip()
                if phone:
                    phone_numbers.append(phone)
                else:
                    break
            # Call the insert_new_guest function with the user's input
            create_functions.insert_new_guest(guest_name, city, state, street, zipcode, email, phone_numbers)
        elif choice == '2':
            create_functions.insert_new_reservation()
        elif choice == '3':
            print("\nPlease enter the following staff details:")

            staff_name = input("Staff Name (required): ").strip()
            while not staff_name:
                print("Staff Name cannot be empty!")
                staff_name= input("Staff Name (required): ").strip()


            role = input("Role: ").strip()
            contactInfo = input("Enter phone number: ").strip()
            print(contactInfo)
            # Call the staff function with the user's input
            create_functions.insert_new_staff_member(staff_name,role,contactInfo)
        elif choice == '4':
            create_functions.insert_new_service()        
        elif choice == '5':
            create_functions.insert_new_room()
        elif choice == '6':
            reservationID = input("Enter the resrvation ID: ").strip()
            read_functions.get_reservation_details(reservationID)
        elif choice == '7':
            staffID = input("Enter the staff ID: ").strip()
            read_functions.fetch_particular_staff_member(staff_id=staffID)
        elif choice == '8':
            read_functions.fetch_records('Staff')
        elif choice == '9':
            read_functions.fetch_records('room')
        elif choice == '10':
            reservationID = input("Enter the reservation ID: ").strip()
            read_functions.get_reservation_cost(reservationID)
        elif choice == '11':
            guest_name = input("Enter Guest Name: ").strip()

            email = input("Email (required): ").strip()
            while not email or not create_functions.is_valid_email(email):
                if not email:
                    print("Email cannot be empty!")
                else:
                    print("Invalid email format. Please provide a valid email address.")
                email = input("Email (required): ").strip()
            read_functions.get_guest_information(guest_name,email)
            update_functions.update_guest(guest_name, email)
        elif choice == '12':
            reservation_id = input("Enter Reservation ID to update: ").strip()
            update_functions.update_reservation(reservation_id)
        elif choice == '13':
            read_functions.fetch_records('Staff')
            staff_id = input("Enter the Staff ID to update: ").strip()
            update_functions.update_staff_information(staff_id)
        elif choice == '14':
            update_functions.get_all_services()
            service_name = input("\nEnter the service name to update: ").strip()
            update_functions.update_service_by_name(service_name)
        elif choice == '15':
            reservationID = input("Enter the reservation ID: ").strip()
            delete_functions.delete_reservation(reservationID)
        elif choice == '16':
            name = input("Enter the name of the guest: ").strip()
            email = input("Enter the email of the guest: ").strip()
            delete_functions.delete_guest(name,email)
        elif choice == '17':
            ranking_functions.get_reservation_cost_ranking()
        elif choice == '18':
            ranking_functions.rank_guests_by_reservation_count()
        elif choice == '19':
            ranking_functions.cumulative_distribution_of_staff_by_reservations()
        elif choice == '20':
            ranking_functions.distribute_guests_into_quartiles()
        elif choice == '21':
            ranking_functions.rank_reservations_by_duration()
        elif choice == '22':
            window_functions.rank_rooms_by_price_and_trend()
        elif choice == '23':
            window_functions.moving_average_of_costs()
        elif choice == '24':
            window_functions.moving_total_of_payments()
        elif choice == '25':
            olap_functions.average_total_cost_by_room_type()
        elif choice == '26':
            olap_functions.average_cost_with_rollup()
        elif choice == '27':
            olap_functions.top_three_guests_by_spending()
        elif choice == '28':
            set_operations.get_guests_with_payments_or_reservations()
        elif choice == '29':
            set_operations.get_guests_with_reservation_and_payment()
        elif choice == '30':
            set_operations.get_rooms_less_than_suite_price()
        else:
            print("Invalid choice! Please enter a number.")