# Task and Agent Management System

A PyQt5-based GUI application for managing tasks and agents with their capabilities.

## Features

- **Project Management**: Create new projects or load existing ones
- **Task Generation**: Generate random tasks in implicit format (automatically converted to explicit format)
- **Agent Generation**: Generate random agents with capabilities
- **Multiple Visualization Modes**:
  - Textual view of all tasks, agents, and capabilities
  - Tabular view with organized tables
  - Graphical view of task-capability relationships
  - Graphical view of agent-capability relationships
- **Interactive Graph Features**:
  - Click on tasks to highlight their required capabilities
  - Click on capabilities to highlight related tasks/agents
  - Click on links to see relationship information
- **Edit Functionality**: Edit tasks and agents (implicit task changes auto-update explicit tasks)
- **Export/Import**: Export projects as ZIP archives containing JSON and YAML representations

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python gui.py
```

### Creating a New Project

1. Go to File → New Project
2. Enter a project name
3. Click OK

### Generating Tasks and Agents

1. Click "Generate Tasks" and specify the number of tasks
2. Click "Generate Agents" and specify the number of agents
3. Click "Refresh Views" to update all visualizations

### Viewing Data

- **Textual View**: Shows detailed text representation of all data
- **Tabular View**: Shows tasks and agents in organized tables
- **Task-Capability Graph**: Shows tasks (green rectangles) connected to capabilities (blue circles)
- **Agent-Capability Graph**: Shows agents (pink circles) connected to capabilities (blue circles)

### Interactive Graph Features

- Click on a task/agent to highlight its capabilities (orange)
- Click on a capability to highlight related tasks/agents (orange)
- Click on a link (in Task-Capability graph) to see relationship details

### Editing

1. Click "Edit Task" or "Edit Agent"
2. Select the item to edit
3. Modify the fields
4. Click OK to save changes

### Exporting Projects

1. Go to File → Export Project
2. Choose a location for the ZIP file
3. The archive will contain JSON and YAML representations

### Loading Projects

1. Go to File → Load Project
2. Select a directory containing project JSON files
3. The project will be loaded with all its data

## Architecture

- `models.py`: Core data models (Task, Agent, Capability)
- `project_manager.py`: Project management and serialization
- `gui.py`: PyQt5-based GUI application
