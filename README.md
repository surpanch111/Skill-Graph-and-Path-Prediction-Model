# ⚡ SkillGraph: Graph-Based Skill Path & Role Prediction

> An interactive web app that uses a **graph database (CognoDB)** to trace multi-hop prerequisite skill paths and match your skills to the best-fit engineering role.

![Status](https://img.shields.io/badge/status-live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Graph DB](https://img.shields.io/badge/Graph%20DB-CognoDB-00b4f0)
![Deployed on](https://img.shields.io/badge/deployed%20on-Render-46E3B7)

🔗 **Live Demo:** https://skillgraphpredictor-app.onrender.com
*(Hosted on Render. The first load may take ~30–60 seconds if the service has been idle.)*

<img width="1558" height="787" alt="2026-09-30 (1)" src="https://github.com/user-attachments/assets/6dfbf1b2-1bc8-4a75-968a-84ed2f241345" />


---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Roles & Skills Covered](#-roles--skills-covered)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🔍 Overview

Job requirements are a web of dependencies. To become an *Autonomous Drone Engineer*, you need PID control, which needs multivariable calculus, which needs linear algebra, and so on. Flat skill lists hide these relationships.

**SkillGraph** models careers as a **graph**:

- 🔴 **Role nodes** are job roles (e.g. Computer Vision Engineer)
- 🔵 **Skill nodes** are individual skills (e.g. OpenCV, C++, Linear Algebra)
- **Edges** are prerequisite and requirement relationships

Because the data is stored as a graph, the app can **traverse multiple hops** to reveal the full chain of skills behind any role, and run **graph pattern matching** to find which roles fit the skills you already have.

---

## ✨ Features

### 1️⃣ Multi-Hop Prerequisite Finder
Select a target role and click **Trace Path** to traverse 2+ hops of transitive prerequisite skills, showing not only what a role needs directly but everything you must learn *before* that.

### 2️⃣ Skill-Based Role Matcher
Tick the skills you already have and click **Calculate Matches**. The app uses graph pattern matching to score your compatibility with each role.

### 3️⃣ Live Graph Topology Visualization
An interactive force-directed graph of the entire knowledge base, rendered live from CognoDB. Role nodes are shown in red and skill nodes in blue.

---

## 🎯 Roles & Skills Covered

**Roles**

| Role |
|------|
| Autonomous Drone Engineer |
| Embedded Robotics Engineer |
| Computer Vision Engineer |
| Backend Systems Engineer |
| Wireless Communications Engineer |

**Skills**

`Python` · `C++` · `Linear Algebra` · `Calculus` · `DSA` · `ML Basics` · `Deep Learning` · `OpenCV` · `ROS2` · `RTOS` · `PID Control` · `DSP` · `RF Comms` · `Docker` · `Cloud`

---

## ⚙️ How It Works

```
   ┌──────────────┐      ┌───────────────┐      ┌─────────────────────┐
   │  Web UI      │ ───► │  Backend API  │ ───► │  CognoDB (graph)    │
   │  (select     │      │  (query       │      │  Roles ⇄ Skills     │
   │  role/skills)│ ◄─── │  logic)       │ ◄─── │  prerequisite edges │
   └──────────────┘      └───────────────┘      └─────────────────────┘
          │
          ▼
   Live topology visualization
```

1. **Prerequisite tracing:** starting from a role node, the backend walks outward through prerequisite edges 2+ hops deep and returns the ordered skill chain.
2. **Role matching:** the selected skill set is compared against each role's required-skill subgraph, producing a compatibility score per role.
3. **Visualization:** nodes and edges are streamed to the frontend and drawn as an interactive graph.

---

## 📁 Project Structure

```
Skill-Graph-and-Path-Prediction-Model/
├── skillgraph/        # Core application (graph logic, API, frontend)
├── docs/
│   └── screenshot.png # App screenshot used in this README
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python |
| Graph Database | CognoDB |
| Visualization | Interactive force-directed graph (browser) |
| Deployment | Render |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip
- Access to a CognoDB instance

### Installation

```bash
# Clone the repository
git clone https://github.com/surpanch111/Skill-Graph-and-Path-Prediction-Model.git
cd Skill-Graph-and-Path-Prediction-Model

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run locally

```bash
python skillgraph/app.py
```

Then open **http://localhost:5000** in your browser.

---

## ▶️ Usage

**Find prerequisites for a role**
1. Choose a role from the dropdown (e.g. *Autonomous Drone Engineer*)
2. Click **Trace Path**
3. View the transitive chain of skills required to reach that role

**Find roles that match your skills**
1. Tick the skills you already know
2. Click **Calculate Matches**
3. See your compatibility with each role

---

## 🗺️ Roadmap

- [ ] Expand the graph with more roles and skills
- [ ] Weighted edges (skill importance and difficulty)
- [ ] Personalized learning-path ordering with time estimates
- [ ] Course and resource recommendations per skill
- [ ] Skill-gap report export (PDF)
- [ ] Unit tests and CI with GitHub Actions

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**surpanch111**
GitHub: [@surpanch111](https://github.com/surpanch111)

⭐ If you found this project useful, please give it a star!
