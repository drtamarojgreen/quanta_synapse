# Quanta Ecosystem Project Summaries (Expanded)

This document provides a detailed summary of each project within the Quanta ecosystem, based on a review of their individual repositories. The summaries include each project's purpose, key features, technology stack, and its specific role within the broader architecture.

---

## Core Architectural Components

These projects form the central nervous system of the Quanta ecosystem, responsible for strategy, execution, and governance.

### 1. `quanta_ethos` (The Orchestrator & Conscience)

*   **Purpose:** The central, philosophical repository for the entire ecosystem. It defines the guiding principles (local-first, modular, ethical), high-level architecture, and contains the core ethical documents. It also holds the top-level scripts for building and running the entire system.
*   **Key Features:**
    *   Contains core documentation on the project's vision, ethics, and architecture.
    *   Provides top-level `build_all.sh`, `start_system.sh`, and `test_all.sh` scripts.
    *   Defines the high-level roles of other components (`QuantaLista`, `QuantaPorto`, etc.).
*   **Technology:** C++ and Shell.
*   **Data Format:** Uses a file-based queue for inter-component communication.
*   **Dependencies:** `g++`, `cmake`, `make`, `python3`, `Rscript`, `git`.
*   **Role in Ecosystem:** `quanta_ethos` is the heart of the ecosystem. It is not a runtime component itself, but rather the source of truth for the project's philosophy and the master orchestrator for building and launching all other components.

### 2. `quanta_porto` (The LLM Commander)

*   **Purpose:** A philosophical and technical framework for interacting with a local Large Language Model (LLM). It acts as the tactical controller that translates high-level tasks into a structured, XML-based language for the LLM.
*   **Key Features:**
    *   **PQL (QuantaPorto Language):** An XML-defined intermediate language for issuing tasks, constraints, and reflections to the LLM.
    *   **Rule System:** XML-defined rules that encode behavioral expectations for the model.
    *   **Local Autonomy:** Runs entirely offline and uses shell scripts to interact with a local LLM.
*   **Technology:** Shell and C++.
*   **Data Format:** XML (for PQL and rules).
*   **Dependencies:** `bash`, `xmlstarlet`.
*   **Role in Ecosystem:** `quanta_porto` is the "Commander". It receives tasks from the scheduler (`QuantaLista`) and translates them into precise, structured commands (PQL) that the execution agent (`QuantaSensa`) can understand and act upon. It is the bridge between high-level strategy and low-level LLM interaction.

### 3. `quanta_lista` (The Task Scheduler)

*   **Purpose:** An intelligent coordination and management layer for the multi-agent system. It acts as a central scheduler, managing a queue of tasks, handling dependencies, and assigning work to available agents.
*   **Key Features:**
    *   Dynamic task scheduling with dependency resolution.
    *   Manages agent states (IDLE, BUSY, OFFLINE).
    *   Provides a C++ `Coordinator` engine to orchestrate the workflow.
*   **Technology:** C++.
*   **Data Format:** Internal C++ objects. The format for receiving tasks is not specified but would likely be a simple text or structured format.
*   **Dependencies:** `g++`.
*   **Role in Ecosystem:** `quanta_lista` is the "Strategist" or "Project Manager". It holds the master plan and ensures that the right tasks are sent to `QuantaPorto` in the correct order.

### 4. `quanta_sensa` (The Field Agent)

*   **Purpose:** The autonomous agent framework that actually executes tasks. It is designed for resilient, self-aware operation in a constrained, offline Linux environment.
*   **Key Features:**
    *   A C++ parent controller that schedules and monitors the agent.
    *   A Python agent that executes a single, discrete action per invocation.
    *   Learns exclusively from local Linux `man` pages to improve its capabilities.
    *   Designed with no `while(true)` loops for stability.
*   **Technology:** C++ (parent controller) and Python (agent).
*   **Data Format:** Consumes commands (likely PQL from `QuantaPorto`) and uses a YAML file for its own action configuration.
*   **Dependencies:** `g++`, `python3`, `psutil` (Python package).
*   **Role in Ecosystem:** `quanta_sensa` is the "Field Agent" or the "hands" of the system. It is the component that interacts with the operating system to carry out the commands issued by `QuantaPorto`.

### 5. `quanta_glia` (The Knowledge Manager)

*   **Purpose:** An autonomous system for managing the ecosystem's knowledge base. It is designed to simulate biological glial cells by pruning unused knowledge (repositories) and fostering the growth of new, productive knowledge.
*   **Key Features:**
    *   **Repository Spawner:** Can clone or fork new repositories based on identified knowledge gaps.
    *   **Pruner:** Can merge, archive, or delete repositories based on configurable rules (age, usage, etc.).
    *   Learns from agent activity to identify what new tools or documentation might be needed.
*   **Technology:** Python.
*   **Data Format:** Uses a `config.yaml` file for its configuration.
*   **Dependencies:** `python3`.
*   **Role in Ecosystem:** `quanta_glia` is the "Librarian" and the engine of self-improvement for the entire ecosystem. It observes the activity on the bus and the state of the repositories to autonomously generate new tasks for `QuantaLista`, creating a full feedback loop.

---

## Subsystems & Tools

These projects provide specialized capabilities that support the core architectural components.

### 6. Monitoring & Advisory Systems

A suite of tools to ensure the safety, reliability, and accuracy of the LLM agents.

*   **`quanta_alarma` (Risk Monitor):**
    *   **Purpose:** A planned system to proactively monitor for anomalous or *risky* LLM activities.
    *   **Status:** Pre-development.
    *   **Technology:** C++.
*   **`quanta_pulsa` (Coherence Monitor):**
    *   **Purpose:** A tool to monitor LLM response coherence and latency to detect hallucinations or "fibbing".
    *   **Status:** Defined concept.
    *   **Technology:** C++.
*   **`quanta_quilida` (Fact-Checking Monitor):**
    *   **Purpose:** A planned system to perform quality control by cross-referencing LLM outputs against trusted data sources for factual accuracy.
    *   **Status:** Planning/Design.
    *   **Technology:** C++.

### 7. Visualization Tools

*   **`quanta_cerebra` (Brain Activity Visualizer):**
    *   **Purpose:** A C++ application that generates ASCII-based video simulations of brain activity.
    *   **Data Format:** Consumes JSON input.
    *   **Dependencies:** None (self-contained C++17).
*   **`quanta_retina` (`QuantaGraph`):**
    *   **Purpose:** A C++ application that renders ASCII-based undirected network graphs in the terminal.
    *   **Dependencies:** None (self-contained C++).
*   **`quanta_dorsa` (Neuroscience Pipeline):**
    *   **Purpose:** A polyglot pipeline for end-to-end neuroscientific modeling.
    *   **Data Format:** Uses CSV as the interchange format between its C++, Python, and R scripts.
    *   **Dependencies:** `g++`, `python3`, `R`, `pandas`, `matplotlib`, `ggplot2`, `ffmpeg`.

### 8. Developer & Project Tools

*   **`quanta_memora` (C++ Template Generator):**
    *   **Purpose:** A general-purpose C++ project template generator that can create various project types (console apps, libraries, etc.) with CMake or Makefile build systems.
    *   **Technology:** C++.
*   **`quanta_occipita` (Quanta Module Bootstrapper):**
    *   **Purpose:** A specialized tool for bootstrapping new Quanta modules, ensuring they follow the specific standards of the ecosystem.
    *   **Technology:** PowerShell.
*   **`quanta_tissu` (Toy Transformer Model):**
    *   **Purpose:** An educational, from-scratch implementation of a transformer model, serving as a foundation for a future agentic coding assistant.
    *   **Technology:** Python.
    *   **Dependencies:** `NumPy`.

### 9. Data & API Modules

*   **`quanta_cogno` (Genomics API):**
    *   **Purpose:** A simulated C++ API for exploring the relationship between genomics and mental health.
    *   **Data Format:** Provides a JSON-based API.
    *   **Dependencies:** None (self-contained C++).

---

### 10. Deprecated or Unclear Projects

*   **`prismquanta`:** Appears to be the deprecated version of `quanta_porto`. The repository contains a note that it is closed and will be moved.
*   **`quanta_serene`:** A C++ task scheduler. Its purpose seems to overlap significantly with `quanta_lista`. Further clarification is needed to determine its exact role or if it is a redundant/alternative implementation.
