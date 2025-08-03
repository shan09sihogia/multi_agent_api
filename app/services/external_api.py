from app.core.database import db
from app.models.common import ClientCreate, OrderCreate
from datetime import datetime
from typing import Dict, Any

class ExternalAPI:
    def create_client(self, data: ClientCreate) -> Dict[str, Any]:
        """Creates a new client entry. [cite: 32]"""
        last_client = db.clients.find_one(sort=[("_id", -1)])
        new_id = (last_client["_id"] + 1) if last_client else 1
        client_data = data.dict()
        client_data["_id"] = new_id
        client_data["status"] = "active"
        client_data["enrolled_services"] = []
        client_data["created_at"] = datetime.now() 
        client_data["dob"] = None 
        result = db.clients.insert_one(client_data)
        return {"id": str(result.inserted_id), "client_id": new_id, "name": client_data["name"]}

    def create_order(self, data: OrderCreate) -> Dict[str, Any]:
        """Creates a new order entry. [cite: 33]"""
        last_order = db.orders.find_one(sort=[("_id", -1)])
        new_id = (last_order["_id"] + 1) if last_order else 1
        last_order_id_doc = db.orders.find_one(sort=[("order_id", -1)])
        new_order_id = (last_order_id_doc["order_id"] + 1) if last_order_id_doc else 12346 

        # Find client to link by ID
        client = db.clients.find_one({"name": {"$regex": data.client_name, "$options": "i"}})
        if not client:
            return {"error": "Client not found. Please create client first."}

        order_data = data.dict()
        order_data["_id"] = new_id
        order_data["order_id"] = new_order_id
        order_data["client_id"] = client["_id"]
        order_data["status"] = "pending" 

       
        course = db.courses.find_one({"name": {"$regex": data.course_name, "$options": "i"}})
        order_data["amount"] = course.get("price", 0) if course else 0
        order_data["created_at"] = datetime.now()

        result = db.orders.insert_one(order_data)
        
      
        if data.course_name not in client.get("enrolled_services", []):
            db.clients.update_one(
                {"_id": client["_id"]},
                {"$addToSet": {"enrolled_services": data.course_name}}
            )

        return {"id": str(result.inserted_id), "order_id": new_order_id, "client_name": client["name"], "course": data.course_name, "status": order_data["status"], "amount": order_data["amount"]}