# Task and Agent Management System - Usage Guide

## Overview

This system provides a comprehensive GUI for managing tasks, agents, and their relationships through capabilities. Tasks can be in two formats:
- **Implicit Format**: References capabilities by name (strings)
- **Explicit Format**: References capabilities as resolved objects

The system automatically converts between these formats.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python gui.py
```

## Quick Start Guide

### 1. Creating a New Project

1. Launch the application
2. Click **File → New Project**
3. Enter a project name
4. Click OK

### 2. Generating Sample Data

#### Generate Tasks
1. Click the **"Generate Tasks"** button in the control panel
2. Enter the number of tasks to generate (e.g., 5)
3. Tasks are created in implicit format and automatically converted to explicit format
4. Capabilities are automatically identified and registered

#### Generate Agents
1. Click the **"Generate Agents"** button in the control panel
2. Enter the number of agents to generate (e.g., 3)
3. Agents are created with random capabilities from the available pool

### 3. Viewing Data

The application provides four different views accessible via tabs:

#### Textual View
- Shows complete text representation of all data
- Displays both implicit and explicit task formats
- Lists all agents with their capabilities
- Shows all registered capabilities

#### Tabular View
- Presents tasks in a table with columns: Name, Description, Capabilities, Duration
- Shows agents in a separate table with columns: Name, Capabilities
- Easy to scan and compare data

#### Task-Capability Graph
- Visual representation of task-capability relationships
- **Green rectangles** represent tasks
- **Blue circles** represent capabilities
- **Gray lines** connect tasks to their required capabilities
- **Interactive features**:
  - Click a task to highlight its capabilities in orange
  - Click a capability to highlight tasks that require it in orange
  - Click a connecting line to see detailed relationship information

#### Agent-Capability Graph
- Visual representation of agent-capability relationships
- **Pink circles** represent agents
- **Blue circles** represent capabilities
- **Gray lines** connect agents to their provided capabilities
- **Interactive features**:
  - Click an agent to highlight its capabilities in orange
  - Click a capability to highlight agents that provide it in orange

### 4. Editing Data

#### Editing a Task
1. Click the **"Edit Task"** button
2. Select a task from the list
3. Modify any of the following:
   - Name
   - Description
   - Required capabilities (comma-separated list)
   - Duration
4. Click OK to save
5. **Note**: The explicit task is automatically updated to match

#### Editing an Agent
1. Click the **"Edit Agent"** button
2. Select an agent from the list
3. Modify:
   - Name
   - Select/deselect capabilities from the list
4. Click OK to save

### 5. Refreshing Views

Click the **"Refresh Views"** button to update all visualizations after making changes.

### 6. Exporting a Project

1. Click **File → Export Project**
2. Choose a location and filename for the ZIP archive
3. The archive will contain:
   - `json/implicit_tasks.json` - Tasks in implicit format
   - `json/explicit_tasks.json` - Tasks in explicit format
   - `json/agents.json` - Agent data
   - `json/capabilities.json` - Capability registry
   - `yaml/` directory with the same data in YAML format

### 7. Loading an Existing Project

1. Click **File → Load Project**
2. Select a directory containing project JSON files
3. The project data will be loaded and displayed

## Understanding the Data Formats

### Implicit Task
```json
{
  "id": "a1b2c3d4-...",
  "name": "Development Task 1",
  "description": "Auto-generated task",
  "required_capabilities": ["Python", "Testing", "DevOps"],
  "duration": 5
}
```

### Explicit Task
```json
{
  "id": "a1b2c3d4-...",
  "name": "Development Task 1",
  "description": "Auto-generated task",
  "required_capabilities": [
    {"name": "Python", "description": "Python programming"},
    {"name": "Testing", "description": "Software testing"},
    {"name": "DevOps", "description": "DevOps capability"}
  ],
  "duration": 5
}
```

### Agent
```json
{
  "id": "e5f6g7h8-...",
  "name": "Alice1",
  "capabilities": [
    {"name": "Python", "description": "Python programming"},
    {"name": "JavaScript", "description": "JavaScript programming"}
  ]
}
```

## Key Features

### Automatic Conversion
- When you generate or edit an implicit task, the system automatically:
  1. Identifies all required capabilities
  2. Creates Capability objects if they don't exist
  3. Generates the corresponding explicit task
  4. Updates the capability registry

### Synchronized Updates
- Editing an implicit task automatically updates:
  - The implicit task itself
  - The corresponding explicit task
  - The capability registry (adds new capabilities if needed)

### Graph Minimization
- The graph layouts attempt to minimize edge crossings for better readability
- Tasks and agents are arranged on the left
- Capabilities are arranged on the right
- Connections are drawn with straight lines

### Visual Feedback
- **Yellow highlighting**: Selected item
- **Orange highlighting**: Related items
- Color coding helps understand relationships quickly

## Tips

1. **Start with tasks**: Generate tasks first to establish your capability pool
2. **Then add agents**: Agents will use capabilities from the existing pool
3. **Use graphs for understanding**: The graph views are best for seeing relationships
4. **Use tables for data entry**: The tabular view is best for reviewing detailed data
5. **Export regularly**: Save your work by exporting projects
6. **Edit carefully**: Remember that editing an implicit task updates the explicit task

## Troubleshooting

### No data appears
- Make sure you've created a project first
- Click "Refresh Views" after generating or editing data

### GUI doesn't start
- Ensure PyQt5 is installed: `pip install PyQt5`
- Check Python version (requires Python 3.6+)

### Cannot export project
- Ensure you have write permissions in the target directory
- Make sure the project has been created and contains data

### Graphs are cluttered
- Generate fewer items initially to test
- Use the scroll and zoom features in the graph view
- Consider filtering by selecting specific items

## Examples

### Example Workflow 1: New Project Setup
```
1. File → New Project → "My Research Project"
2. Generate Tasks → 10
3. Generate Agents → 5
4. Switch to Task-Capability Graph
5. Click tasks to see their requirements
6. Edit Agent → Assign capabilities based on task needs
7. File → Export Project → "my_project.zip"
```

### Example Workflow 2: Loading and Editing
```
1. File → Load Project → Select directory
2. Switch to Tabular View
3. Edit Task → Select task → Modify capabilities
4. Refresh Views
5. Switch to Agent-Capability Graph
6. Verify agent assignments
7. File → Export Project → Save updated version
```

## Command-Line Demo

For a quick demonstration without the GUI:
```bash
python demo_cli.py
```

This will show all the features in action with text output.

## Running Tests

To verify the system is working correctly:
```bash
python test_basic.py
```

All tests should pass with ✅ indicators.
