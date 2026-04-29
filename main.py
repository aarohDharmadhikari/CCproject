from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# from pymongo import MongoClient

app = FastAPI(
    title="CloudLab Backend",
    description="Backend API for CloudLab - Virtual Cloud Experiment Simulator",
    version="1.0.0"
)

# CORS configuration to allow your React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection Setup (uncomment when MongoDB is running)
# client = MongoClient("mongodb://localhost:27017/")
# db = client["cloudlab_db"]

@app.get("/")
def read_root():
    return {"message": "Welcome to the CloudLab Backend API!"}

@app.post("/api/simulate")
def simulate_architecture(architecture: dict):
    """
    Logic-based simulation endpoint.
    Calculates cost and performance based on the components present.
    """
    nodes = architecture.get("nodes", [])
    
    total_cost = 0
    performance_score = 100
    
    for node in nodes:
        node_type = node.get("type")
        if node_type == "VM":
            total_cost += 20
            performance_score += 10
        elif node_type == "LoadBalancer":
            total_cost += 15
            performance_score += 30
        elif node_type == "Database":
            total_cost += 30
            performance_score += 15
            
    return {
        "status": "success",
        "estimated_cost_usd": total_cost,
        "performance_score": performance_score,
        "message": "Simulation completed without actual cloud billing."
    }

@app.get("/api/labs")
def get_labs():
    """Returns pre-built training labs for users to experiment with."""
    return [
        {
            "id": "lab_1",
            "title": "High Availability Web App",
            "description": "Design an architecture that survives a single VM failure.",
            "target_cost": 75
        },
        {
            "id": "lab_2", 
            "title": "Cost-Optimized Backend",
            "description": "Reduce infrastructure cost below $50 while maintaining basic performance.",
            "target_cost": 50
        }
    ]

if __name__ == "__main__":
    print("Starting CloudLab Backend Server on port 8000...")
    # Run with: uvicorn main:app --reload
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)