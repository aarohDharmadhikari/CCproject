from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# --- Pydantic Models for Data Validation ---
class Architecture(BaseModel):
    id: Optional[str] = Field(alias='_id')
    name: str
    description: str
    architecture_data: dict

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# --- FastAPI App Initialization ---
app = FastAPI(
    title="CloudLab Backend",
    description="Backend API for CloudLab - Virtual Cloud Experiment Simulator",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Connection ---
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cloudlab_db"]
    components_collection = db["components"]
    architectures_collection = db["architectures"]
    labs_collection = db["labs"]
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    # In a real app, you might want to exit or handle this more gracefully
    client = None

# --- Database Seeding and Initialization ---
def seed_database():
    if not client: return
    # Seed Components
    if components_collection.count_documents({}) == 0:
        print("Seeding 'components' collection...")
        default_components = [
            {"type": "VM", "name": "Virtual Machine", "cost": 20, "performance": 10},
            {"type": "LoadBalancer", "name": "Load Balancer", "cost": 15, "performance": 30},
            {"type": "Database", "name": "Database", "cost": 30, "performance": 15}
        ]
        components_collection.insert_many(default_components)

    # Seed Labs
    if labs_collection.count_documents({}) == 0:
        print("Seeding 'labs' collection...")
        default_labs = [
            {"id": "lab_1", "title": "High Availability Web App", "description": "Design an architecture that survives a single VM failure.", "target_cost": 75},
            {"id": "lab_2", "title": "Cost-Optimized Backend", "description": "Reduce infrastructure cost below $50 while maintaining basic performance.", "target_cost": 50}
        ]
        labs_collection.insert_many(default_labs)

# --- API Endpoints ---
@app.on_event("startup")
def on_startup():
    seed_database()

@app.get("/")
def read_root():
    return {"message": "Welcome to the CloudLab Backend API! Now with MongoDB integration."}

@app.get("/api/components")
def get_components():
    """Fetches the list of available drag-and-drop components."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    components = list(components_collection.find({}, {'_id': 0}))
    return components

@app.post("/api/simulate")
def simulate_architecture(architecture: dict):
    """
    Logic-based simulation endpoint.
    Calculates cost and performance based on the components present.
    """
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    
    nodes = architecture.get("nodes", [])
    total_cost = 0
    performance_score = 100
    
    component_stats = {comp['type']: comp for comp in components_collection.find()}

    for node in nodes:
        node_type = node.get("type")
        if node_type in component_stats:
            total_cost += component_stats[node_type]['cost']
            performance_score += component_stats[node_type]['performance']
            
    return {
        "status": "success",
        "estimated_cost_usd": total_cost,
        "performance_score": performance_score,
        "message": "Simulation completed using dynamic data from MongoDB."
    }

@app.get("/api/labs")
def get_labs():
    """Returns pre-built training labs for users to experiment with."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    labs = list(labs_collection.find({}, {'_id': 0}))
    return labs

@app.post("/api/architectures/save", status_code=201)
def save_architecture(arch_data: Architecture):
    """Saves a user's architecture design to the database."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    
    inserted_id = architectures_collection.insert_one(arch_data.dict(by_alias=True, exclude={'id'})).inserted_id
    return {"status": "success", "inserted_id": str(inserted_id)}

@app.get("/api/architectures", response_model=List[Architecture])
def get_saved_architectures():
    """Retrieves all saved architectures."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    architectures = list(architectures_collection.find())
    return architectures

@app.get("/api/architectures/{architecture_id}", response_model=Architecture)
def get_architecture_by_id(architecture_id: str):
    """Retrieves a specific architecture by its ID."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    
    if not ObjectId.is_valid(architecture_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
    architecture = architectures_collection.find_one({"_id": ObjectId(architecture_id)})
    if architecture:
        return architecture
    raise HTTPException(status_code=404, detail="Architecture not found")

if __name__ == "__main__":
    print("Starting CloudLab Backend Server on port 8000...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)