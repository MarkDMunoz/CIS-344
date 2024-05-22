from http.server import HTTPServer, BaseHTTPRequestHandler
from restaurantDatabase import RestaurantDatabase
import cgi

class RestaurantPortalHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        self.database = RestaurantDatabase()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path == '/addReservation':
            self.handle_add_reservation()
        elif self.path == '/deleteReservation':
            self.handle_delete_reservation()
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def handle_add_reservation(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        customer_id = int(form.getvalue("customer_id"))
        reservation_time = form.getvalue("reservation_time")
        number_of_guests = int(form.getvalue("number_of_guests"))
        special_requests = form.getvalue("special_requests")

        # Call the Database Method to add a new reservation
        self.database.addReservation(customer_id, reservation_time, number_of_guests, special_requests)
        
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div><a href='/'>Home</a> | \
                         <a href='/addReservationForm'>Add Reservation</a> | \
                         <a href='/viewReservations'>View Reservations</a></div>")
        self.wfile.write(b"<hr><h3>Reservation has been added</h3>")
        self.wfile.write(b"<div><a href='/addReservationForm'>Add Another Reservation</a></div>")
        self.wfile.write(b"</center></body></html>")

    def handle_delete_reservation(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        reservation_id = int(form.getvalue("reservation_id"))

        # Call the Database Method to delete the reservation
        self.database.deleteReservation(reservation_id)
        
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div><a href='/'>Home</a> | \
                         <a href='/addReservationForm'>Add Reservation</a> | \
                         <a href='/viewReservations'>View Reservations</a></div>")
        self.wfile.write(b"<hr><h3>Reservation has been deleted</h3>")
        self.wfile.write(b"<div><a href='/viewReservations'>View Reservations</a></div>")
        self.wfile.write(b"</center></body></html>")

    def do_GET(self):
        if self.path == '/':
            self.handle_view_reservations()
        elif self.path == '/addReservationForm':
            self.handle_add_reservation_form()
        elif self.path == '/viewReservations':
            self.handle_view_reservations()
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def handle_add_reservation_form(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><head><title>Add Reservation</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Add Reservation</h1>")
        self.wfile.write(b"<form method='POST' action='/addReservation'>")
        self.wfile.write(b"Customer ID: <input type='text' name='customer_id'><br>")
        self.wfile.write(b"Reservation Time: <input type='text' name='reservation_time'><br>")
        self.wfile.write(b"Number of Guests: <input type='text' name='number_of_guests'><br>")
        self.wfile.write(b"Special Requests: <input type='text' name='special_requests'><br>")
        self.wfile.write(b"<input type='submit' value='Add Reservation'>")
        self.wfile.write(b"</form>")
        self.wfile.write(b"</center></body></html>")

    def handle_view_reservations(self):
        records = self.database.getAllReservations()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><head><title>Restaurant Portal</title></head>")
        self.wfile.write(b"<body>")
        self.wfile.write(b"<center><h1>Restaurant Portal</h1>")
        self.wfile.write(b"<hr>")
        self.wfile.write(b"<div><a href='/'>Home</a> | \
                         <a href='/addReservationForm'>Add Reservation</a> | \
                         <a href='/viewReservations'>View Reservations</a></div>")
        self.wfile.write(b"<hr><h2>All Reservations</h2>")
        self.wfile.write(b"<table border=2> \
                            <tr><th>Reservation ID</th> \
                                <th>Customer ID</th> \
                                <th>Reservation Time</th> \
                                <th>Number of Guests</th> \
                                <th>Special Requests</th> \
                                <th>Action</th></tr>")
        for row in records:
            self.wfile.write(b'<tr>')
            self.wfile.write(b''.join([b'<td>' + str(col).encode() + b'</td>' for col in row]))
            self.wfile.write(b'<td><form method="POST" action="/deleteReservation">')
            self.wfile.write(b'<input type="hidden" name="reservation_id" value="' + str(row[0]).encode() + b'">')
            self.wfile.write(b'<input type="submit" value="Delete">')
            self.wfile.write(b'</form></td>')
            self.wfile.write(b'</tr>')
        
        self.wfile.write(b"</table></center>")
        self.wfile.write(b"</body></html>")

def run(server_class=HTTPServer, handler_class=RestaurantPortalHandler, port=8000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
