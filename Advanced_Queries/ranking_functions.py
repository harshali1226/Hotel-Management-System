from Config.connection import *

"""Ranking query to rank the reservations by the Total Cost using Dense Rank"""
def get_reservation_cost_ranking():
    try:
        # Establish a connection and cursor
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to get the reservation cost ranking with DENSE_RANK
        query = """
            WITH ReservationCost AS (
                SELECT 
                    Reservation.ReservationID,
                    Guest.GuestName,
                    Reservation.TotalCost
                FROM Reservation
                JOIN Guest ON Reservation.GuestID = Guest.GuestID
            )
            SELECT 
                ReservationID,
                GuestName,
                TotalCost,
                DENSE_RANK() OVER (ORDER BY TotalCost DESC) AS CostRank
            FROM ReservationCost;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("ReservationID  GuestName           TotalCost      CostRank  ")
        print("------------------------------------------------------------")
        for row in results:
            print(f"{row[0]:<15}{row[1]:<20}{row[2]:<15}{row[3]:<10}")
    
    except mysql.connector.Error as error:
        print("Unable to fetch the results! Please try again")
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

"""Ranking Query to rank the guests based on the number of reservations in the hotel using Rank function"""
def rank_guests_by_reservation_count():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to rank guests by reservation count using DENSE_RANK
        query = """
            SELECT 
                Guest.GuestID,
                Guest.GuestName,
                COUNT(Reservation.ReservationID) AS ReservationCount,
                RANK() OVER (ORDER BY COUNT(Reservation.ReservationID) DESC) AS ReservationRank
            FROM Guest
            JOIN Reservation ON Guest.GuestID = Reservation.GuestID
            GROUP BY Guest.GuestID;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestID        GuestName           ReservationCount    ReservationRank")
        print("-----------------------------------------------------------------------")
        for row in results:
            print(f"{row[0]:<15}{row[1]:<20}{row[2]:<20}{row[3]:<15}")
    
    except mysql.connector.Error as error:
        print("Unable to fetch the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

"""Ranking query to rank the staff members based on the number of reservations they have handled"""
def cumulative_distribution_of_staff_by_reservations():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to calculate cumulative distribution of staff by reservations managed using CUME_DIST
        query = """
            SELECT 
                Staff.StaffID,
                Staff.StaffName,
                COUNT(Reservation.ReservationID) AS ReservationsManaged,
                CUME_DIST() OVER (ORDER BY COUNT(Reservation.ReservationID) DESC) AS ReservationDistribution
            FROM Staff
            JOIN Reservation ON Staff.StaffID = Reservation.StaffID
            GROUP BY Staff.StaffID;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("StaffID        StaffName           ReservationsManaged    ReservationDistribution")
        print("-------------------------------------------------------------------------")
        for row in results:
            print(f"{row[0]:<15}{row[1]:<20}{row[2]:<20}{row[3]:<15.2f}")
    
    except mysql.connector.Error as error:
        print("Unable to fetch the result! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

"""Ranking query to group the guests into quartiles based on their spending."""
def distribute_guests_into_quartiles():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to distribute guests into quartiles based on total spending using NTILE(4)
        query = """
            SELECT 
                Guest.GuestID,
                Guest.GuestName,
                SUM(Payment.Amount) AS TotalSpending,
                NTILE(4) OVER (ORDER BY SUM(Payment.Amount) DESC) AS SpendingQuartile
            FROM Guest
            JOIN Reservation ON Guest.GuestID = Reservation.GuestID
            JOIN Payment ON Reservation.ReservationID = Payment.ReservationID
            GROUP BY Guest.GuestID;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestID        GuestName           TotalSpending    SpendingQuartile")
        print("--------------------------------------------------------------")
        for row in results:
            print(f"{row[0]:<15}{row[1]:<20}{row[2]:<20.2f}{row[3]}")
    
    except mysql.connector.Error as error:
        print("Unable to fetch the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def rank_reservations_by_duration():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to rank reservations by duration using PERCENT_RANK
        query = """
            SELECT 
                Reservation.ReservationID,
                Guest.GuestName,
                DATEDIFF(Reservation.CheckOutDate, Reservation.CheckInDate) AS Duration,
                PERCENT_RANK() OVER (ORDER BY DATEDIFF(Reservation.CheckOutDate, Reservation.CheckInDate) DESC)*100 AS DurationRank
            FROM Reservation
            JOIN Guest ON Reservation.GuestID = Guest.GuestID;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("ReservationID  GuestName           Duration    DurationRank")
        print("-----------------------------------------------------------")
        for row in results:
            print(f"{row[0]:<15}{row[1]:<20}{row[2]:<10}{row[3]:.2f}")
    
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()