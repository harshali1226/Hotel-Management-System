from Config.connection import *

"""Window function query to rank rooms by price and show price trends"""
def rank_rooms_by_price_and_trend():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to rank rooms by price and show price trends
        query = """
            SELECT 
                RoomNumber,
                RoomType,
                Price,
                RANK() OVER (ORDER BY Price DESC) AS PriceRank,
                LAG(Price) OVER (ORDER BY Price) AS PreviousPrice,
                LEAD(Price) OVER (ORDER BY Price) AS NextPrice
            FROM Room;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("RoomNumber  RoomType          Price      PriceRank  PreviousPrice  NextPrice")
        print("--------------------------------------------------------------------------")
        for row in results:
            room_number, room_type, price, price_rank, prev_price, next_price = row
            print(f"{room_number:<11} {room_type:<16} {price:<10} {price_rank:<10} {prev_price if prev_price is not None else 'N/A':<13} {next_price if next_price is not None else 'N/A'}")
    
    except mysql.connector.Error as error:
        print("Unable to fetch the results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def moving_average_of_costs():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to compute the moving average of total costs of completed reservations
        query = """
            SELECT 
                g.GuestID,
                g.GuestName,
                res.ReservationID, 
                res.TotalCost, 
                AVG(res.TotalCost) OVER (PARTITION BY g.GuestID ORDER BY res.ReservationID ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS Moving_Average
            FROM 
                Reservation res
            JOIN 
                Guest g ON res.GuestID = g.GuestID
            WHERE 
                res.ReservationStatus = 'Confirmed';
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("GuestID  GuestName       ReservationID  TotalCost  Moving_Average")
        print("--------------------------------------------------------------")
        for row in results:
            guest_id, guest_name, reservation_id, total_cost, moving_average = row
            print(f"{guest_id:<8} {guest_name:<15} {reservation_id:<13} {total_cost:<10} {moving_average:<15}")
    
    except mysql.connector.Error as error:
        print("Failed to get results! Please try again")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

""""""
def moving_total_of_payments():
    try:
        # Connect to your database
        connection = create_connection()
        cursor = connection.cursor()
        
        # SQL query to calculate the cumulative total of payments made with a specified payment method
        query = """
            SELECT 
                PaymentID, 
                Amount, 
                PaymentMethod,
                SUM(Amount) OVER (ORDER BY PaymentDate) AS Cumulative_Total
            FROM 
                Payment
            WHERE 
                PaymentMethod = 'Credit Card';
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Print results
        print("PaymentID  Amount  PaymentMethod  Cumulative_Total")
        print("----------------------------------------------------")
        for row in results:
            payment_id, amount, payment_method, cumulative_total = row
            print(f"{payment_id:<10} {amount:<7} {payment_method:<14} {cumulative_total:<15}")
    
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()