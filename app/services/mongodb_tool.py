from app.core.database import db
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

class MongoDBTool:
    def get_client(self, query: str) -> Dict[str, Any] | None:
        """Searches for a client by name, email, or phone."""
        client = db.clients.find_one({
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"email": {"$regex": query, "$options": "i"}},
                {"phone": {"$regex": query, "$options": "i"}}
            ]
        })
        if client:
            if 'dob' in client and isinstance(client['dob'], datetime):
                client['dob'] = client['dob'].strftime("%Y-%m-%d") 
        return client

    def get_client_enrolled_services(self, client_query: str) -> List[Dict[str, Any]]:
        """Retrieves enrolled services and their status for a given client query (name, email, or phone)."""
        client = self.get_client(client_query)
        if client:
            return [{"client_name": client.get("name"), "enrolled_services": client.get("enrolled_services", []), "status": client.get("status")}]
        return []

    def get_order_status(self, order_id: int) -> str:
        """Fetches status by order ID."""
        order = db.orders.find_one({"order_id": order_id})
        return order["status"] if order else "Not found"

    def get_order_details_by_client(self, client_query: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Gets order details for a client, optionally filtered by status."""
        client = self.get_client(client_query)
        if not client:
            return []

      
        query = {"client_id": client["_id"]} 
    
        
        if status:
            query["status"] = {"$regex": status, "$options": "i"}
        
        orders = list(db.orders.find(query, {"_id": 0, "order_id": 1, "course": 1, "status": 1, "amount": 1}))
        return orders

    def get_payment_details_for_order(self, order_id: int) -> Dict[str, Any] | None:
        """Retrieves payment details for a specific order."""
        payment = db.payments.find_one({"order_id": order_id})
        if payment:
            payment['_id'] = str(payment['_id']) 
            if 'date' in payment and isinstance(payment['date'], datetime):
                payment['date'] = payment['date'].isoformat()
        return payment

    def calculate_pending_dues(self, client_query: str) -> str:
        """Calculates total pending dues for a client."""
        client = self.get_client(client_query)
        if not client:
            return f"Client '{client_query}' not found."

      
        pending_orders = list(db.orders.find({"client_id": client["_id"], "status": "pending"}))


        total_pending = sum(order.get("amount", 0) for order in pending_orders)
        return f"Client: {client['name']}, Total Pending Dues: ${total_pending:.2f}"

    def list_upcoming_classes(self) -> List[Dict[str, Any]]:
        """Lists all upcoming services/classes."""
        classes = list(db.classes.find({"status": "upcoming"}, {"_id": 0}))
        return classes

    def filter_classes(self, query: str) -> List[Dict[str, Any]]:
        """Filters classes by instructor or course."""
        classes = list(db.classes.find({
            "$and": [
                {"status": {"$regex": "upcoming", "$options": "i"}},
                {"$or": [
                    {"instructor": {"$regex": query, "$options": "i"}},
                    {"course": {"$regex": query, "$options": "i"}}
                ]}
            ]
        }, {"_id": 0}))
        return classes


    def get_total_revenue_this_month(self) -> float:
        """Calculates total revenue from paid orders this current month."""
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        pipeline = [
            {"$match": {"status": "completed", "date": {"$gte": start_of_month}}}, 
            {"$group": {"_id": None, "total_revenue": {"$sum": "$amount"}}}
        ]
        result = list(db.payments.aggregate(pipeline))
        return result[0]["total_revenue"] if result else 0.0

    def get_outstanding_payments(self) -> List[Dict[str, Any]]:
        """Lists orders with pending status and their amounts."""
        outstanding = list(db.orders.find({"status": "pending"}, {"_id": 0, "order_id": 1, "client_name": 1, "amount": 1, "course": 1}))
        return outstanding

    def get_active_inactive_clients_count(self) -> Dict[str, int]:
        """Counts active and inactive clients."""
        active_count = db.clients.count_documents({"status": "active"})
        inactive_count = db.clients.count_documents({"status": "inactive"})
        return {"active_clients": active_count, "inactive_clients": inactive_count}

    def get_new_clients_this_month(self) -> int:
        """Counts new clients added this month."""
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_clients_count = db.clients.count_documents({"created_at": {"$gte": start_of_month}})
        return new_clients_count

    def get_enrollment_trends(self) -> List[Dict[str, Any]]:
        """Provides enrollment trends by course."""
        pipeline = [
            {"$group": {"_id": "$course", "enrollment_count": {"$sum": 1}}},
            {"$sort": {"enrollment_count": -1}}
        ]
        trends = list(db.orders.aggregate(pipeline))
        return trends

    def get_top_services(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Identifies top courses based on enrollment count."""
        pipeline = [
            {"$group": {"_id": "$course", "enrollment_count": {"$sum": 1}}},
            {"$sort": {"enrollment_count": -1}},
            {"$limit": limit}
        ]
        top_services = list(db.orders.aggregate(pipeline))
        return top_services

    def get_course_completion_rates(self) -> List[Dict[str, Any]]:
        """Calculates approximate course completion rates (requires 'completed' status in orders or specific attendance for a course)."""
        pipeline = [
            {"$group": {"_id": "$course",
                                "total_orders": {"$sum": 1},
                                "completed_orders": {"$sum": {"$cond": [{"$eq": ["$status", "paid"]}, 1, 0]}} # Using 'paid' as proxy
                               }},
            {"$project": {"_id": 0, "course": "$_id",
                                "completion_rate": {"$cond": [{"$eq": ["$total_orders", 0]}, 0, {"$multiply": [{"$divide": ["$completed_orders", "$total_orders"]}, 100]}]}}}
        ]
        completion_rates = list(db.orders.aggregate(pipeline))
        return completion_rates

    def get_attendance_percentage_by_class(self, course_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Calculates attendance percentage for classes, optionally by course."""
        query = {}
        if course_name:
            query["course"] = {"$regex": course_name, "$options": "i"}

        classes = list(db.classes.find(query))
        attendance_reports = []

        for cls in classes:
            
            total_attended = db.attendance.count_documents({"class_id": cls["_id"], "present": True})
            total_students_enrolled_in_class = db.attendance.count_documents({"class_id": cls["_id"]}) 
            
            percentage = (total_attended / total_students_enrolled_in_class * 100) if total_students_enrolled_in_class > 0 else 0
            attendance_reports.append({
                "class_id": str(cls["_id"]), 
                "course": cls.get("course", "N/A"),
                "instructor": cls.get("instructor", "N/A"),
                "date": cls.get("date", "N/A"),
                "attendance_percentage": round(percentage, 2)
            })
        return attendance_reports