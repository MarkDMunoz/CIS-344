import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self,
                 host="127.0.0.1",
                 port="3306",
                 database="restaurant_reservations",
                 user='root',
                 password='Blendz2002@'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addReservation(self, customer_id, reservation_time, number_of_guests, special_requests):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (customer_id, reservation_time, number_of_guests, special_requests))
                self.connection.commit()
                print("Reservation added successfully")
            except Error as e:
                print("Failed to add reservation:", e)
            finally:
                cursor.close()

    def getAllReservations(self):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = "SELECT * FROM Reservations"
                cursor.execute(query)
                return cursor.fetchall()
            except Error as e:
                print("Failed to retrieve reservations:", e)
            finally:
                cursor.close()

    def addCustomer(self, customer_name, contact_info):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO Customers (customerName, contactInfo) VALUES (%s, %s)"
                cursor.execute(query, (customer_name, contact_info))
                self.connection.commit()
                print("Customer added successfully")
            except Error as e:
                print("Failed to add customer:", e)
            finally:
                cursor.close()

    def addSpecialRequest(self, reservation_id, special_request):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = "UPDATE Reservations SET specialRequests = %s WHERE reservationId = %s"
                cursor.execute(query, (special_request, reservation_id))
                self.connection.commit()
                print("Special request added successfully")
            except Error as e:
                print("Failed to add special request:", e)
            finally:
                cursor.close()

    def findReservations(self, customer_id):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = "SELECT * FROM Reservations WHERE customerId = %s"
                cursor.execute(query, (customer_id,))
                return cursor.fetchall()
            except Error as e:
                print("Failed to find reservations:", e)
            finally:
                cursor.close()

    def deleteReservation(self, reservation_id):
        if self.connection.is_connected():
            try:
                cursor = self.connection.cursor()
                query = "DELETE FROM Reservations WHERE reservationId = %s"
                cursor.execute(query, (reservation_id,))
                self.connection.commit()
                print("Reservation deleted successfully")
            except Error as e:
                print("Failed to delete reservation:", e)
            finally:
                cursor.close()

    def viewAllReservations(self):
        return self.getAllReservations()
