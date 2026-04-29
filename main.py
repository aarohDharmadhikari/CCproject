from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
import subprocess
import time
import webbrowser
import os
from multiprocessing import Process

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
    client = None

# --- Database Seeding and Initialization ---
def seed_database():
    if not client: return
    # Clear existing labs to avoid duplicates on restart during development
    labs_collection.delete_many({})
    
    # Seed Components if the collection is empty
    if components_collection.count_documents({}) == 0:
        print("Seeding 'components' collection...")
        default_components = [
            {"type": "VM", "name": "Virtual Machine", "cost": 20, "performance": 10},
            {"type": "LoadBalancer", "name": "Load Balancer", "cost": 15, "performance": 30},
            {"type": "Database", "name": "Database", "cost": 30, "performance": 15}
        ]
        components_collection.insert_many(default_components)

    # Seed Labs with predefined scenarios
    print("Seeding 'labs' collection...")
    default_labs = [
        {
            "id": "lab_1", 
            "title": "Scalable Web Service", 
            "description": "Build a web service that can handle high traffic. Requires at least one Load Balancer and two VMs.", 
            "target_cost": 100
        },
        {
            "id": "lab_2", 
            "title": "Two-Tier Application", 
            "description": "Create a standard two-tier application with a VM and a Database. Performance is key.", 
            "target_cost": 60
        },
        {
            "id": "lab_3", 
            "title": "Cost-Effective Batch Processor", 
            "description": "Design a simple, low-cost architecture for batch processing. Must stay under $40.", 
            "target_cost": 40
        }
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
    """Fetches the list of available drag-and-drop components from the database."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    components = list(components_collection.find({}, {'_id': 0})) # Exclude MongoDB's default _id field
    return components

@app.post("/api/simulate")
def simulate_architecture(architecture: dict):
    """
    Logic-based simulation endpoint.
    Calculates estimated cost and performance based on the components present and their connections.
    Includes basic architectural validation.
    """
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    
    nodes = architecture.get("nodes", [])
    edges = architecture.get("edges", [])
    
    total_cost = 0
    performance_score = 100
    warnings = [] # Collect architectural warnings
    
    # Fetch component statistics (cost, performance) from the database
    component_stats = {comp['type']: comp for comp in components_collection.find()}
    # Create a map for quick node lookup by ID
    node_map = {node['id']: node for node in nodes}

    # --- Architectural Validation Logic ---
    lb_connected_to_vm = False
    for edge in edges:
        source_node = node_map.get(edge['source'])
        target_node = node_map.get(edge['target'])
        
        # Skip if source or target node is not found (e.g., deleted node)
        if not source_node or not target_node:
            continue

        # Check for Load Balancer to VM connection
        if source_node['type'] == 'LoadBalancer' and target_node['type'] == 'VM':
            lb_connected_to_vm = True
        
        # Example: Valid connection from VM to Database
        if source_node['type'] == 'VM' and target_node['type'] == 'Database':
            pass 
        
        # Example: Warn about unusual direct Database to VM connection
        if source_node['type'] == 'Database' and target_node['type'] == 'VM':
            warnings.append("Warning: Direct connection from Database to VM is unusual and might indicate a security risk or architectural flaw.")

    # Check if a Load Balancer exists but isn't connected to any VMs
    if any(node['type'] == 'LoadBalancer' for node in nodes) and not lb_connected_to_vm:
        warnings.append("Warning: A Load Balancer is present but not connected to any Virtual Machines. It might not be effectively distributing traffic.")

    # --- Cost and Performance Calculation ---
    # Calculate cost and performance based on individual nodes
    for node in nodes:
        node_type = node.get("type")
        if node_type in component_stats:
            total_cost += component_stats[node_type]['cost']
            performance_score += component_stats[node_type]['performance']
    
    # Add a small cost and performance bonus for each connection (representing network traffic/data flow)
    total_cost += len(edges) * 0.5 
    performance_score += len(edges) * 1

    # Construct the simulation message, including any warnings
    message = f"Simulation completed. {len(nodes)} nodes and {len(edges)} edges processed."
    if warnings:
        message += " " + " ".join(warnings)

    return {
        "status": "success",
        "estimated_cost_usd": total_cost,
        "performance_score": performance_score,
        "message": message
    }

@app.get("/api/labs")
def get_labs():
    """Returns pre-built training labs for users to experiment with, fetched from the database."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    labs = list(labs_collection.find({}, {'_id': 0}))
    return labs

@app.post("/api/architectures/save", status_code=201)
def save_architecture(arch_data: Architecture):
    """Saves a user's architecture design to the database."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    
    # Convert Pydantic model to dictionary and insert into MongoDB
    inserted_id = architectures_collection.insert_one(arch_data.dict(by_alias=True, exclude={'id'})).inserted_id
    return {"status": "success", "inserted_id": str(inserted_id)}

@app.get("/api/architectures", response_model=List[Architecture])
def get_saved_architectures():
    """Retrieves all saved architectures from the database."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    # Convert MongoDB documents to Pydantic models for response
    architectures = list(architectures_collection.find())
    return architectures

@app.get("/api/architectures/{architecture_id}", response_model=Architecture)
def get_architecture_by_id(architecture_id: str):
    """Retrieves a specific architecture by its ID from the database."""
    if not client: raise HTTPException(status_code=503, detail="Database not connected")
    
    # Validate ObjectId format
    if not ObjectId.is_valid(architecture_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
    architecture = architectures_collection.find_one({"_id": ObjectId(architecture_id)})
    if architecture:
        return architecture
    raise HTTPException(status_code=404, detail="Architecture not found")

# Function to run the FastAPI backend
def run_backend():
    print("Starting CloudLab Backend Server on port 8000...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# Function to run the React frontend
def run_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
    print(f"Starting CloudLab Frontend from: {frontend_path}")
    try:
        # Use shell=True for Windows compatibility with npm commands
        # and start a new process group to allow killing it later
        subprocess.run("npm start", cwd=frontend_path, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting frontend: {e}")
    except FileNotFoundError:
        print("npm command not found. Please ensure Node.js and npm are installed and in your PATH.")

if __name__ == "__main__":
    # Start backend in a separate process
    backend_process = Process(target=run_backend)
    backend_process.start()

    # Give the backend a moment to start up
    time.sleep(5) 

    # Open the frontend in a web browser
    frontend_url = "http://localhost:3000"
    print(f"\nFrontend GUI available at: {frontend_url}\n") # Explicitly print clickable URL
    webbrowser.open(frontend_url)

    # Start frontend in the main process (or another process if preferred)
    # Note: npm start will block this process. If you want to keep the main Python script interactive,
    # you might run this in another Process as well, but then managing its lifecycle becomes more complex.
    run_frontend()

    # To ensure the backend process is terminated when the main script exits (e.g., Ctrl+C)
    # You might need more sophisticated process management for production.
    # For development, simply killing the main script will often leave the backend running,
    # which can be useful for quick restarts of the frontend.
    # backend_process.join() # Uncomment if you want the main script to wait for backend to finish
