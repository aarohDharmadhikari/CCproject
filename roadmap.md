# 🗺️ CloudLab - Detailed Project Roadmap

This document outlines the comprehensive development phases for the **CloudLab – Virtual Cloud Experiment Simulator**.

---

## 🟢 Phase 1: Project Conception & UI/UX Design
*Objective: Solidify the project requirements, design the layout, and establish the technical stack.*

- [x] **Requirement Analysis**
  - [x] Define specific simulation rules (Cost per VM, Load Balancer traffic limits, Database storage costs).
  - [x] Outline the Pre-built Lab scenarios (e.g., "High Availability Web App", "Cost-Optimized Backend").
- [ ] **UI/UX Mockups & Prototyping**
  - [ ] Design the slick, minimalistic UI aesthetic with color accents.
  - [ ] Design the boxy left-side navigation bar layout.
  - [ ] Prototype the Drag-and-Drop canvas interface.
  - [ ] Design the Cost and Performance dashboard overlay.
- [ ] **Repository Setup**
  - [x] Initialize Git repository.
  - [x] Create `README.md` with proprietary styling.
  - [x] Create this `roadmap.md` file.

---

## 🟡 Phase 2: Backend Development (Python + MongoDB)
*Objective: Build the logic-based simulation engine and the API layer.*

- [ ] **Environment Setup**
  - [ ] Initialize Python virtual environment.
  - [ ] Install framework (FastAPI or Flask) and PyMongo.
- [ ] **Database Schema Design (MongoDB)**
  - [ ] Create `Users` collection (optional if no auth, or simplified).
  - [ ] Create `Architectures` collection (to save drag-and-drop states).
  - [ ] Create `Components` collection (catalogue of VMs, LBs, DBs with base stats).
  - [ ] Create `Labs` collection (pre-built scenarios).
- [ ] **Core Simulation Engine**
  - [ ] Develop cost calculation algorithm based on active nodes.
  - [ ] Develop performance calculation algorithm (throughput, latency bottlenecks).
  - [ ] Implement validation logic (e.g., Load Balancer must connect to VMs, VMs to DB).
- [ ] **REST API Development**
  - [ ] `GET /api/components` - Fetch available drag-and-drop items.
  - [ ] `POST /api/simulate` - Send architecture JSON, return estimated cost/performance.
  - [ ] `POST /api/architectures/save` - Save user design.
  - [ ] `GET /api/labs` - Fetch pre-built labs.

---

## 🟠 Phase 3: Frontend Development (React + Tailwind CSS)
*Objective: Construct the user interface and implement the core interactive features.*

- [ ] **Frontend Initialization**
  - [ ] Initialize React App (Vite or Create React App).
  - [ ] Install and configure Tailwind CSS.
  - [ ] Set up routing (`react-router-dom`).
- [ ] **Layout Construction**
  - [ ] Build the boxy left-side navigation bar.
  - [ ] Create base page layouts (Canvas Page, Labs Page, Saved Architectures Page).
- [ ] **Drag-and-Drop Implementation**
  - [ ] Integrate a drag-and-drop library (e.g., `reactflow` or `@hello-pangea/dnd`).
  - [ ] Create draggable UI components:
    - [ ] 🖥️ Virtual Machine Node
    - [ ] ⚖️ Load Balancer Node
    - [ ] 🗄️ Database Node
  - [ ] Implement connection logic (drawing lines between nodes).
- [ ] **Simulation Dashboard UI**
  - [ ] Build the dynamic Cost Estimator panel.
  - [ ] Build the Performance Metrics panel (Speed, Uptime, Bottlenecks).
  - [ ] Connect the frontend state to the Python backend via Axios/Fetch.
- [ ] **Pre-Built Labs UI**
  - [ ] Create the lab selection menu.
  - [ ] Implement the interactive "Mission Objective" tracker on the canvas.

---

## 🔵 Phase 4: Integration & Polish
*Objective: Connect the frontend and backend, test the algorithms, and refine the aesthetic.*

- [ ] **End-to-End Testing**
  - [ ] Verify that adding a VM updates the cost in real-time.
  - [ ] Ensure saved architectures load correctly from MongoDB.
  - [ ] Test edge cases (e.g., connecting a DB directly to a user input node).
- [ ] **UI/UX Polish**
  - [ ] Add smooth animations for node drops and panel transitions.
  - [ ] Ensure Tailwind color accents (e.g., vibrant blue for connections, neon green for successful simulations) pop correctly against the minimalistic background.
  - [ ] Implement empty states and loading spinners.
- [ ] **Performance Optimization**
  - [ ] Debounce the simulation API calls during rapid drag-and-drop actions.
  - [ ] Ensure the React canvas remains performant with 50+ nodes.

---

## 🟣 Phase 5: Documentation & Deployment Prep (Viva Ready)
*Objective: Prepare the project for final presentation and demo.*

- [ ] **Viva Demo Preparations**
  - [ ] Create 3 highly polished pre-built labs demonstrating specific cloud concepts (Scaling, Redundancy, Cost-Saving).
  - [ ] Seed the MongoDB database with initial lab data.
- [ ] **Final Code Cleanup**
  - [ ] Remove console logs and unused code.
  - [ ] Add inline comments to complex cost calculation algorithms.
- [ ] **Final Documentation**
  - [ ] Update `README.md` with final screenshots of the UI.
  - [ ] Add an "Architecture Guide" section for the viva examiner.

---
*Status: In Progress...*