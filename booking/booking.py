import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingInfo(userid=booking["userid"], dates=booking["dates"])

    def GetBookingsByUserID(self, request, context):
        userid = request.userid
        for booking in self.db:
            if booking["userid"] == userid:
                return booking_pb2.BookingInfo(userid=userid, dates=booking["dates"])
        return booking_pb2.BookingInfo(userid="", dates=[])

    def AddBooking(self, request, context):
        with grpc.insecure_channel('localhost:3002') as channel:
            stub = showtime_pb2_grpc.ShowtimeStub(channel)
            userid, date, movieid = request.userid, request.date, request.movieid
            movies_by_date = stub.GetMoviesByDate(date)
            if movieid not in movies_by_date.movies:
                return booking_pb2.BookingInfo(userid="", dates=[])
            for booking in self.db:
                if booking["userid"] == userid:
                    for day in booking["dates"]:
                        if day["date"] == date:
                            for movie in day["movies"]:
                                if movie == movieid:
                                    return booking_pb2.BookingInfo(userid="", dates=[])
                            day["movies"].append(movieid)
                            with open('{}/data/bookings.json'.format("."), "w") as wfile:
                                json.dump({"bookings": self.db}, wfile)
                            return booking_pb2.BookingInfo(userid=userid, dates=booking["dates"])
                    booking["dates"].append({"date": date, "movies": [movieid]})
                    with open('{}/data/bookings.json'.format("."), "w") as wfile:
                        json.dump({"bookings": self.db}, wfile)
                    return booking_pb2.BookingInfo(userid=userid, dates=booking["dates"])
            booking.append({"userid": userid, "dates": [{"date": date, "movies": [movieid]}]})
            with open('{}/data/bookings.json'.format("."), "w") as wfile:
                json.dump({"bookings": self.db}, wfile)
            return booking_pb2.BookingInfo(userid=userid, dates=booking["dates"])


def get_schedule(stub):
    schedule = stub.GetSchedule(showtime_pb2.Empty())
    for timeslot in schedule:
        print(f"Timeslot: {timeslot.date}")
        for movie in timeslot.movies:
            print(f"movie: {movie}")


def get_movies_by_date(stub, date):
    movies = stub.GetMoviesByDate(date)
    print(f"Movies in {date}: {movies}")


def run():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetSchedule --------------")
        get_schedule(stub)
        print("-------------- GetMoviesByDate 20151203 --------------")
        date = showtime_pb2.DateSlot(date="20151203")
        get_movies_by_date(stub, date)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    #run()
    serve()
