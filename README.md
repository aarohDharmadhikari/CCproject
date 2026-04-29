<div align="center">
  <h1>CloudLab – Virtual Cloud Experiment Simulator</h1>
  <p>An exclusive, interactive cloud deployment simulator designed to test architectures without real cloud billing, built with a Python backend, MongoDB, and a modern, minimalistic React frontend.</p>
</div>

<br><br>

> [!CAUTION]
> **PROPRIETARY AND CONFIDENTIAL**
>
> This project, along with the associated codebase, constitutes the proprietary and strictly confidential intellectual property of the originating developer.
>
> **UNAUTHORIZED USE IS STRICTLY PROHIBITED.**
> You may not copy, distribute, transmit, reproduce, publish, modify, or create derivative works from this source material without the explicit, documented authorization of the chief developer. Any unauthorized replication, reverse engineering, or dissemination of these proprietary systems will be subject to immediate legal action and aggressive prosecution under applicable intellectual property laws.
>
> *This repository does NOT grant an open-source license. All rights are explicitly reserved.*

<br><br>

---

### Status & Tech
<p align="center">
  <a href="#"><img alt="Maintained" src="https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg?style=for-the-badge"></a>
  <a href="#"><img alt="License" src="https://img.shields.io/badge/License-Proprietary-red.svg?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"></a>
  <a href="#"><img alt="React" src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB"></a>
  <a href="#"><img alt="Tailwind CSS" src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white"></a>
  <a href="#"><img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white"></a>
</p>

---

## About This Project

CloudLab is a state-of-the-art Virtual Cloud Experiment Simulator designed specifically for academic environments, vivas, and cloud training without the fear of accumulating real cloud billing costs. It unifies a high-performance Python backend backed by a MongoDB database with a breathtaking, modern React frontend.

The software acts as a personalized sandbox. It allows users to visually assemble infrastructure using a sleek drag-and-drop interface, complete with VMs, Load Balancers, and Databases. The system dynamically evaluates the proposed architecture to provide immediate feedback on estimated cost and expected performance, creating a highly advanced yet entirely logic-based simulation environment.

---

## Architectural Philosophy

*   **Logic-Based Simulation Engine**: Computes estimated costs, performance metrics, and bottlenecks natively without relying on real cloud provider APIs, perfect for safe experimentation.
*   **High-Fidelity UI/UX**: Designed with a slick, minimalistic aesthetic featuring bright color accents to highlight interactive components.
    *   A prominent, boxy left-side navigation bar seamlessly manages transitions between simulation labs and dashboards.
    *   Curviness/Border-Radius is strictly limited to an elegant `5px` for a smooth but defined aesthetic.
    *   Fully fluid and seamlessly animated (fade-ins, drag-and-drop transitions) ensuring an intuitive user experience.
*   **Modular Node Graph Interface**: The core canvas where users physically connect Load Balancers to VMs and Databases, instantly visualizing the architecture's data flow.
*   **Pre-Built Training Labs**: Offers structured, gamified challenges (akin to AWS training) guiding the user to solve specific infrastructure problems.

---

## Current Features

*   **Interactive Drag-and-Drop Canvas**: Easily drop VMs, Load Balancers, and Databases onto a grid and connect them.
*   **Real-time Cost & Performance Estimation**: Instant mathematical breakdown of the architecture's monthly cost and handling capacity.
*   **Boxy Left-Side Navigation**: Clean, accessible side-menu for navigating between the main canvas, lab scenarios, and saved architectures.
*   **Pre-built Learning Labs**: Structured missions requiring the user to build specific architectures to achieve performance/cost goals.
*   **MongoDB Architecture Persistence**: Users can save their complex architectures to the database and retrieve them seamlessly later.
*   **Python Simulation Backend**: Handles all the complex routing logic, cost algorithms, and performance bottleneck calculations via REST APIs.
*   **Modern Minimalist Aesthetics**: A clean interface with high-contrast color accents to make logical components stand out.

---

## Architecture Guide for Viva Examiners

CloudLab is structured as a modern full-stack application, adhering to a clear separation of concerns between its frontend and backend components.

### Frontend (React.js with Tailwind CSS)
The user interface is built with **React.js**, providing a dynamic and responsive single-page application experience.
-   **Component-Based Structure**: The UI is composed of reusable React components (e.g., `Canvas`, `Sidebar`, `Labs`, `Dashboard`).
-   **State Management**: React's `useState` and `useEffect` hooks manage local component state and side effects, including data fetching and UI updates.
-   **Routing**: `react-router-dom` handles navigation between different views (Canvas, Labs, Saved Architectures).
-   **Drag-and-Drop Canvas**: The core simulation area leverages `reactflow` for interactive node-based diagramming, enabling users to visually construct cloud architectures.
-   **Styling**: **Tailwind CSS** is used for utility-first styling, ensuring a consistent, slick, and minimalistic aesthetic with defined color accents.
-   **API Communication**: `axios` is used to make asynchronous HTTP requests to the Python backend.
-   **Performance**: Implemented debouncing for simulation calls to optimize API usage during rapid UI interactions.

### Backend (FastAPI with MongoDB)
The backend is developed in **Python** using the **FastAPI** framework, chosen for its high performance and ease of use for building APIs.
-   **RESTful API**: Provides a clear set of endpoints for frontend-backend communication.
-   **MongoDB Database**: Used for data persistence, storing:
    -   `components`: A catalog of available cloud resources (VMs, Load Balancers, Databases) with their base cost and performance metrics.
    -   `labs`: Pre-defined simulation scenarios with specific objectives (e.g., target cost).
    -   `architectures`: User-saved cloud designs, allowing for persistence and retrieval.
-   **Simulation Logic**: The `/api/simulate` endpoint is the heart of the backend. It receives the current architecture (nodes and edges) from the frontend and:
    -   Calculates estimated costs and performance scores based on component data from MongoDB.
    -   Includes basic architectural validation (e.g., checking if Load Balancers are connected to VMs) to provide intelligent feedback and warnings.
-   **CORS Middleware**: Configured to allow cross-origin requests from the React frontend during development.
-   **Pydantic**: Ensures robust data validation for incoming API requests and outgoing responses.

### Data Flow
1.  **Frontend Initialization**: On load, the React app fetches available `components` and `labs` from the FastAPI backend.
2.  **User Interaction**: Users drag and drop components onto the `reactflow` canvas and connect them.
3.  **Simulation Trigger**: When the user clicks "Simulate" (or automatically via debouncing), the current `nodes` and `edges` data is sent to the `/api/simulate` endpoint.
4.  **Backend Processing**: The FastAPI backend processes this data, calculates costs/performance, performs validation, and returns the results.
5.  **Frontend Display**: The `Dashboard` component in React displays the simulation results and any warnings.
6.  **Lab Integration**: If a lab is active, the simulation results are checked against the lab's objectives, and the user is notified of their progress.
7.  **Persistence**: Users can save their current canvas architecture via a dedicated API endpoint, and retrieve previously saved designs.

This architecture ensures a scalable, maintainable, and interactive simulation environment, perfectly suited for educational demonstrations and experimentation.

---

## Setup & Execution

### Prerequisites
-   Python 3.x
-   Node.js (for React frontend)
-   MongoDB instance (local or Atlas)

### Launching the Backend
Navigate to the backend directory, install requirements, and run the Python server.

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Launching the Frontend
Navigate to the frontend directory, install dependencies, and start the React app.

```bash
cd frontend
npm install
npm start
```

---

## Project Roadmap & Task Tracking

See `roadmap.md` for detailed task tracking and phase completion checklists.
