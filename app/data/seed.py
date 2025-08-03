from app.core.database import db
from datetime import datetime, timedelta

def seed():
    print("Clearing existing data...")
    db.clients.delete_many({})
    db.orders.delete_many({})
    db.classes.delete_many({})
    db.payments.delete_many({})
    db.courses.delete_many({})
    db.attendance.delete_many({})
    print("Data cleared.")


    print("Seeding clients...")
    db.clients.insert_many([
        {"_id": 1, "name":"Priya Sharma","email":"priya@example.com","phone":"9999999999", "status": "active", "enrolled_services": ["Yoga Beginner"], "created_at": datetime.now() - timedelta(days=60), "dob": datetime(1990, 7, 1)},
        {"_id": 2, "name":"Rahul Singh","email":"rahul@example.com","phone":"8888888888", "status": "active", "enrolled_services": ["Pilates Advanced"], "created_at": datetime.now() - timedelta(days=30), "dob": datetime(1985, 12, 15)},
        {"_id": 3, "name":"Amit Kumar","email":"amit@example.com","phone":"7777777777", "status": "inactive", "enrolled_services": [], "created_at": datetime.now() - timedelta(days=90), "dob": datetime(1992, 3, 20)},
        {"_id": 4, "name":"Neha Reddy","email":"neha@example.com","phone":"6666666666", "status": "active", "enrolled_services": ["Zumba Basics", "Yoga Beginner"], "created_at": datetime.now() - timedelta(days=15), "dob": datetime(1995, 7, 5)},
        {"_id": 5, "name":"Sita Devi","email":"sita@example.com","phone":"5555555555", "status": "active", "enrolled_services": ["Yoga Beginner"], "created_at": datetime.now() - timedelta(days=5), "dob": datetime(1988, 1, 25)}, # New client this month
    ])
    print("Clients seeded.")


    print("Seeding courses...")
    db.courses.insert_many([
        {"_id": 101, "name": "Yoga Beginner", "description": "Introduction to Yoga", "price": 100},
        {"_id": 102, "name": "Pilates Advanced", "description": "Advanced Pilates techniques", "price": 150},
        {"_id": 103, "name": "Zumba Basics", "description": "Fun cardio dance", "price": 80},
        {"_id": 104, "name": "Meditation Fundamentals", "description": "Learn basic meditation techniques", "price": 70},
    ])
    print("Courses seeded.")


    print("Seeding classes...")
    db.classes.insert_many([
        {"_id": 201, "course":"Yoga Beginner", "instructor":"Anjali", "status":"upcoming", "date":"2025-07-07", "time": "10:00 AM"},
        {"_id": 202, "course":"Pilates Advanced", "instructor":"Deepa", "status":"upcoming", "date":"2025-07-08", "time": "09:00 AM"},
        {"_id": 203, "course":"Zumba Basics", "instructor":"Ravi", "status":"completed", "date":"2025-06-25", "time": "06:00 PM"},
        {"_id": 204, "course":"Yoga Beginner", "instructor":"Anjali", "status":"upcoming", "date":"2025-07-14", "time": "10:00 AM"},
        {"_id": 205, "course":"Meditation Fundamentals", "instructor":"Anjali", "status":"upcoming", "date":"2025-07-10", "time": "05:00 PM"}
    ])
    print("Classes seeded.")


    print("Seeding orders...")
    db.orders.insert_many([
        {"_id": 1, "order_id":12345, "client_id": 1, "client_name":"Priya Sharma", "course":"Yoga Beginner", "status":"pending", "amount": 100, "created_at": datetime.now() - timedelta(days=2)},
        {"_id": 2, "order_id":54321, "client_id": 2, "client_name":"Rahul Singh", "course":"Pilates Advanced", "status":"paid", "amount": 150, "created_at": datetime.now() - timedelta(days=10)},
        {"_id": 3, "order_id":98765, "client_id": 1, "client_name":"Priya Sharma", "course":"Zumba Basics", "status":"paid", "amount": 80, "created_at": datetime.now() - timedelta(days=15)},
        {"_id": 4, "order_id":11223, "client_id": 4, "client_name":"Neha Reddy", "course":"Yoga Beginner", "status":"pending", "amount": 100, "created_at": datetime.now() - timedelta(days=1)},
        {"_id": 5, "order_id":33445, "client_id": 5, "client_name":"Sita Devi", "course":"Meditation Fundamentals", "status":"paid", "amount": 70, "created_at": datetime.now() - timedelta(days=3)}, # Order for new client
    ])
    print("Orders seeded.")


    print("Seeding payments...")
    db.payments.insert_many([
        {"_id": 1, "order_id": 54321, "amount": 150, "date": datetime.now() - timedelta(days=9), "status": "completed"},
        {"_id": 2, "order_id": 98765, "amount": 80, "date": datetime.now() - timedelta(days=14), "status": "completed"},
        {"_id": 3, "order_id": 33445, "amount": 70, "date": datetime.now() - timedelta(days=2), "status": "completed"}, # Payment for new client's order
    ])
    print("Payments seeded.")


    print("Seeding attendance...")
    db.attendance.insert_many([
        {"_id": 1, "class_id": 203, "course": "Zumba Basics", "date": "2025-06-25", "client_id": 4, "client_name": "Neha Reddy", "present": True},
        {"_id": 2, "class_id": 203, "course": "Zumba Basics", "date": "2025-06-25", "client_id": 1, "client_name": "Priya Sharma", "present": False},
        {"_id": 3, "class_id": 203, "course": "Zumba Basics", "date": "2025-06-25", "client_id": 2, "client_name": "Rahul Singh", "present": True},
    ])
    print("Attendance seeded.")

    print("Mock data seeding complete!")

if __name__ == "__main__":
    seed()