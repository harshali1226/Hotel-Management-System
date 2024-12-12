from Config.connection import *

""""""
def average_total_cost_by_room_type():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to calculate the average total cost of reservations for each room type
        query = """
            WITH RoomReservationCounts AS (
                SELECT 
                    r.RoomType,
                    COUNT(res.ReservationID) AS ReservationCount,
                    SUM(res.TotalCost) AS TotalRevenue
                FROM 
                    Reservation res
                JOIN 
                    Room r ON res.RoomNumber = r.RoomNumber
                GROUP BY 
                    r.RoomType
                HAVING 
                    COUNT(res.ReservationID) > 0
            )

            SELECT 
                rrc.RoomType,
                rrc.ReservationCount,
                rrc.TotalRevenue,
                rrc.TotalRevenue / rrc.ReservationCount AS AvgTotalCost 
            FROM 
                RoomReservationCounts rrc
            ORDER BY 
                rrc.RoomType;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("RoomType       ReservationCount  TotalRevenue  AvgTotalCost")
        print("-----------------------------------------------------------")
        for row in results:
            room_type, reservation_count, total_revenue, avg_total_cost = row
            print(f"{room_type:<15} {reservation_count:<17} {total_revenue:<12} {avg_total_cost:<12.2f}")
    
    except mysql.connector.Error as error:
        print("Failed to get the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

""""""
def average_cost_with_rollup():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to calculate the average total cost using the ROLLUP function
        query = """
            SELECT 
                g.GuestName,
                res.ReservationStatus,
                AVG(res.TotalCost) AS AvgTotalCost
            FROM 
                Reservation res
            JOIN 
                Guest g ON res.GuestID = g.GuestID
            GROUP BY 
                g.GuestName, res.ReservationStatus WITH ROLLUP;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestName       ReservationStatus   AvgTotalCost")
        print("-------------------------------------------------")
        for row in results:
            guest_name, reservation_status, avg_total_cost = row
            
            # Handle None values for guest_name or reservation_status
            guest_name_display = guest_name if guest_name else "Overall"
            reservation_status_display = reservation_status if reservation_status else "Overall"
            
            print(f"{guest_name_display:<15} {reservation_status_display:<20} {avg_total_cost:<12.2f}")
    
    except mysql.connector.Error as error:
        print("Failed to get the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

""""""
def top_three_guests_by_spending():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to calculate the top three guests by total spending
        query = """
            WITH TotalSpending AS (
                SELECT 
                    g.GuestName,
                    SUM(res.TotalCost) AS TotalCost,
                    RANK() OVER (ORDER BY SUM(res.TotalCost) DESC) AS SpendingRank
                FROM 
                    Reservation res
                JOIN 
                    Guest g ON res.GuestID = g.GuestID
                GROUP BY 
                    g.GuestName
            )
            SELECT 
                GuestName, TotalCost
            FROM 
                TotalSpending
            WHERE 
                SpendingRank <= 3;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestName       TotalCost")
        print("---------------------------")
        for row in results:
            guest_name, total_cost = row
            print(f"{guest_name:<15} {total_cost:<10.2f}")
    
    except mysql.connector.Error as error:
        print("Failed to get the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()