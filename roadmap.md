# 🗺️ CloudLab - Detailed Project Roadmap

This document outlines the comprehensive development phases for the **CloudLab – Virtual Cloud Experiment Simulator**.

---

## ✅ Phase 1: Project Conception & UI/UX Design
*Objective: Solidify the project requirements, design the layout, and establish the technical stack.*

- [x] **Requirement Analysis**
  - [x] Define specific simulation rules (Cost per VM, Load Balancer traffic limits, Database storage costs).
  - [x] Outline the Pre-built Lab scenarios (e.g., "High Availability Web App", "Cost-Optimized Backend").
- [x] **UI/UX Mockups & Prototyping**
  - [x] Design the slick, minimalistic UI aesthetic with color accents.
  - [x] Design the boxy left-side navigation bar layout.
  - [x] Prototype the Drag-and-Drop canvas interface.
  - [x] Design the Cost and Performance dashboard overlay.
- [x] **Repository Setup**
  - [x] Initialize Git repository.
  - [x] Create `README.md` with proprietary styling.
  - [x] Create this `roadmap.md` file.

---

## ✅ Phase 2: Backend Development (Python + MongoDB)
*Objective: Build the logic-based simulation engine and the API layer.*

- [x] **Environment Setup**
  - [x] Initialize Python virtual environment.
  - [x] Install framework (FastAPI) and PyMongo.
- [x] **Database Schema Design (MongoDB)**
  - [x] Create `Architectures` collection (to save drag-and-drop states).
  - [x] Create `Components` collection (catalogue of VMs, LBs, DBs with base stats).
  - [x] Create `Labs` collection (pre-built scenarios).
- [x] **Core Simulation Engine**
  - [x] Develop cost calculation algorithm based on active nodes.
  - [x] Develop performance calculation algorithm (throughput, latency bottlenecks).
  - [x] Implement validation logic (e.g., Load Balancer must connect to VMs, VMs to DB).
- [x] **REST API Development**
  - [x] `GET /api/components` - Fetch available drag-and-drop items.
  - [x] `POST /api/simulate` - Send architecture JSON, return estimated cost/performance.
  - [x] `POST /api/architectures/save` - Save user design.
  - [x] `GET /api/labs` - Fetch pre-built labs.

---

## ✅ Phase 3: Frontend Development (React + Tailwind CSS)
*Objective: Construct the user interface and implement the core interactive features.*

- [x] **Frontend Initialization**
  - [x] Initialize React App (Vite or Create React App).
  - [x] Install and configure Tailwind CSS.
  - [x] Set up routing (`react-router-dom`).
- [x] **Layout Construction**
  - [x] Build the boxy left-side navigation bar.
  - [x] Create base page layouts (Canvas Page, Labs Page, Saved Architectures Page).
- [x] **Drag-and-Drop Implementation**
  - [x] Integrate a drag-and-drop library (`reactflow`).
  - [x] Create draggable UI components:
    - [x] 🖥️ Virtual Machine Node
    - [x] ⚖️ Load Balancer Node
    - [x] 🗄️ Database Node
  - [x] Implement connection logic (drawing lines between nodes).
- [x] **Simulation Dashboard UI**
  - [x] Build the dynamic Cost Estimator panel.
  - [x] Build the Performance Metrics panel (Speed, Uptime, Bottlenecks).
  - [x] Connect the frontend state to the Python backend via Axios/Fetch.
- [x] **Pre-Built Labs UI**
  - [x] Create the lab selection menu.
  - [x] Implement the interactive "Mission Objective" tracker on the canvas.

---

## ✅ Phase 4: Integration & Polish
*Objective: Connect the frontend and backend, test the algorithms, and refine the aesthetic.*

- [x] **End-to-End Testing**
  - [x] Verify that adding a VM updates the cost in real-time.
  - [x] Ensure saved architectures load correctly from MongoDB.
  - [x] Test edge cases (e.g., connecting a DB directly to a user input node).
- [x] **UI/UX Polish**
  - [x] Add smooth animations for node drops and panel transitions.
  - [x] Ensure Tailwind color accents (e.g., vibrant blue for connections, neon green for successful simulations) pop correctly against the minimalistic background.
  - [x] Implement empty states and loading spinners.
- [x] **Performance Optimization**
  - [x] Debounce the simulation API calls during rapid drag-and-drop actions.
  - [x] Ensure the React canvas remains performant with 50+ nodes.

---

## ✅ Phase 5: Documentation & Deployment Prep (Viva Ready)
*Objective: Prepare the project for final presentation and demo.*

- [x] **Viva Demo Preparations**
  - [x] Create 3 highly polished pre-built labs demonstrating specific cloud concepts (Scalable Web Service, Two-Tier Application, Cost-Effective Batch Processor).
  - [x] Seed the MongoDB database with initial lab data.
- [x] **Final Code Cleanup**
  - [x] Remove console logs and unused code.
  - [x] Add inline comments to complex cost calculation algorithms.
- [x] **Final Documentation**
  - [x] Update `README.md` with final screenshots of the UI.
  - [x] Add an "Architecture Guide" section for the viva examiner.

---
*Status: Project Completed!*