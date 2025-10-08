# GUI Features Documentation

## Main Window Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ Task and Agent Management System                          [_][□][X] │
├─────────────────────────────────────────────────────────────────┤
│ File                                                            │
│  ├─ New Project                                                 │
│  ├─ Load Project                                                │
│  ├─ Export Project                                              │
│  └─ Exit                                                        │
├─────────────────────────────────────────────────────────────────┤
│ Project: My Project                                             │
├─────────────────────────────────────────────────────────────────┤
│ [Generate Tasks] [Generate Agents] [Edit Task] [Edit Agent] [Refresh] │
├─────────────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────────────┐   │
│ │ Textual View | Tabular View | Task-Capability | Agent-Cap │   │
│ ├───────────────────────────────────────────────────────────┤   │
│ │                                                           │   │
│ │              ACTIVE TAB CONTENT AREA                      │   │
│ │                                                           │   │
│ │                                                           │   │
│ │                                                           │   │
│ │                                                           │   │
│ └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Tab 1: Textual View

```
┌───────────────────────────────────────────────────────────────┐
│ Project: My Project                                           │
│                                                               │
│ === IMPLICIT TASKS ===                                        │
│                                                               │
│ Task: Development Task 1 (ID: a1b2c3d4)                       │
│   Description: Auto-generated task 1                          │
│   Duration: 5                                                 │
│   Required Capabilities: Python, Testing, DevOps              │
│                                                               │
│ Task: Planning Task 2 (ID: e5f6g7h8)                          │
│   Description: Auto-generated task 2                          │
│   Duration: 3                                                 │
│   Required Capabilities: JavaScript, UI/UX                    │
│                                                               │
│ === EXPLICIT TASKS ===                                        │
│ [Similar format but with full capability objects]            │
│                                                               │
│ === AGENTS ===                                                │
│                                                               │
│ Agent: Alice1 (ID: i9j0k1l2)                                  │
│   Capabilities: Python, JavaScript, Testing                   │
│                                                               │
│ === CAPABILITIES ===                                          │
│ [List of all capabilities]                                    │
└───────────────────────────────────────────────────────────────┘
```

## Tab 2: Tabular View

```
┌───────────────────────────────────────────────────────────────┐
│ Tasks                                                         │
│ ┌─────────────┬───────────────┬──────────────────┬─────────┐ │
│ │ Name        │ Description   │ Capabilities     │ Duration│ │
│ ├─────────────┼───────────────┼──────────────────┼─────────┤ │
│ │Development 1│Auto-gen task 1│Python, Testing   │    5    │ │
│ │Planning 2   │Auto-gen task 2│JavaScript, UI/UX │    3    │ │
│ └─────────────┴───────────────┴──────────────────┴─────────┘ │
│                                                               │
│ Agents                                                        │
│ ┌─────────────┬───────────────────────────────────────────┐  │
│ │ Name        │ Capabilities                              │  │
│ ├─────────────┼───────────────────────────────────────────┤  │
│ │Alice1       │Python, JavaScript, Testing                │  │
│ │Bob2         │DevOps, Database, API                      │  │
│ └─────────────┴───────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

## Tab 3: Task-Capability Graph View

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│   Tasks (Green Rectangles)    Capabilities (Blue Circles)    │
│                                                               │
│   ┌──────────────┐                                           │
│   │ Development  │────────────────────────┐                  │
│   │   Task 1     │                        │                  │
│   └──────────────┘                        ↓                  │
│                                      ╭─────────╮              │
│   ┌──────────────┐                  │ Python  │              │
│   │  Planning    │──────────────────│         │              │
│   │   Task 2     │                  ╰─────────╯              │
│   └──────────────┘                        ↑                  │
│                                           │                  │
│   ┌──────────────┐                        │                  │
│   │   Testing    │────────────────────────┘                  │
│   │   Task 3     │                                           │
│   └──────────────┘                  ╭─────────╮              │
│                        ┌────────────│ Testing │              │
│                        │            │         │              │
│                        │            ╰─────────╯              │
│                        │                                     │
│                        │            ╭─────────╮              │
│                        └────────────│ DevOps  │              │
│                                     │         │              │
│                                     ╰─────────╯              │
│                                                               │
│ Interactions:                                                 │
│ • Click task → Highlights its capabilities (orange)           │
│ • Click capability → Highlights related tasks (orange)        │
│ • Click link → Shows relationship details                     │
└───────────────────────────────────────────────────────────────┘
```

## Tab 4: Agent-Capability Graph View

```
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│   Agents (Pink Circles)       Capabilities (Blue Circles)    │
│                                                               │
│      ╭─────────╮                                             │
│      │ Alice1  │──────────────────────┐                      │
│      │         │                      │                      │
│      ╰─────────╯                      ↓                      │
│                                  ╭─────────╮                  │
│      ╭─────────╮                │ Python  │                  │
│      │  Bob2   │────────────────│         │                  │
│      │         │                ╰─────────╯                  │
│      ╰─────────╯                      ↑                      │
│                                       │                      │
│      ╭─────────╮                      │                      │
│      │Charlie3 │──────────────────────┘                      │
│      │         │                                             │
│      ╰─────────╯                ╭─────────╮                  │
│              ┌──────────────────│JavaScript│                 │
│              │                  │         │                  │
│              │                  ╰─────────╯                  │
│              │                                               │
│              │                  ╭─────────╮                  │
│              └──────────────────│ Testing │                  │
│                                 │         │                  │
│                                 ╰─────────╯                  │
│                                                               │
│ Interactions:                                                 │
│ • Click agent → Highlights its capabilities (orange)          │
│ • Click capability → Highlights agents that provide it        │
└───────────────────────────────────────────────────────────────┘
```

## Edit Task Dialog

```
┌─────────────────────────────────────┐
│ Edit Task                      [X]  │
├─────────────────────────────────────┤
│                                     │
│ Name:                               │
│ ┌─────────────────────────────────┐ │
│ │ Development Task 1              │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Description:                        │
│ ┌─────────────────────────────────┐ │
│ │ Auto-generated task 1           │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Capabilities (comma-separated):     │
│ ┌─────────────────────────────────┐ │
│ │ Python, Testing, DevOps         │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Duration:                           │
│ ┌────────┐                          │
│ │   5   ▲│                          │
│ │       ▼│                          │
│ └────────┘                          │
│                                     │
│        [ OK ]      [ Cancel ]       │
└─────────────────────────────────────┘
```

## Edit Agent Dialog

```
┌─────────────────────────────────────┐
│ Edit Agent                     [X]  │
├─────────────────────────────────────┤
│                                     │
│ Name:                               │
│ ┌─────────────────────────────────┐ │
│ │ Alice1                          │ │
│ └─────────────────────────────────┘ │
│                                     │
│ Capabilities:                       │
│ ┌─────────────────────────────────┐ │
│ │ ☑ Python                        │ │
│ │ ☑ JavaScript                    │ │
│ │ ☑ Testing                       │ │
│ │ ☐ DevOps                        │ │
│ │ ☐ UI/UX                         │ │
│ │ ☐ Database                      │ │
│ │ ☐ API                           │ │
│ └─────────────────────────────────┘ │
│                                     │
│        [ OK ]      [ Cancel ]       │
└─────────────────────────────────────┘
```

## Color Scheme

### Task-Capability Graph
- **Tasks**: Light green rectangles (`#90EE90`)
- **Capabilities**: Light blue circles (`#ADD8E6`)
- **Selected item**: Yellow (`#FFFF00`)
- **Related items**: Orange (`#FFA500`)
- **Connections**: Gray lines

### Agent-Capability Graph
- **Agents**: Light pink circles (`#FFB6C1`)
- **Capabilities**: Light blue circles (`#ADD8E6`)
- **Selected item**: Yellow (`#FFFF00`)
- **Related items**: Orange (`#FFA500`)
- **Connections**: Gray lines

## Interactive Features

### Selection Behavior

1. **Task Selection** (Task-Capability Graph):
   - Task background → Yellow
   - All capabilities required by task → Orange
   
2. **Capability Selection** (Task-Capability Graph):
   - Capability background → Yellow
   - All tasks requiring capability → Orange

3. **Agent Selection** (Agent-Capability Graph):
   - Agent background → Yellow
   - All capabilities provided by agent → Orange

4. **Capability Selection** (Agent-Capability Graph):
   - Capability background → Yellow
   - All agents providing capability → Orange

5. **Link Selection** (Task-Capability Graph):
   - Shows popup with:
     - Task name
     - Capability name
     - Capability description

## Data Synchronization

When editing an implicit task:
```
User edits implicit task
        ↓
Update implicit task in memory
        ↓
Add any new capabilities to registry
        ↓
Convert to explicit task
        ↓
Update corresponding explicit task
        ↓
Refresh all views
```

## Export Structure

When exporting a project, the ZIP archive contains:

```
project.zip
├── json/
│   ├── implicit_tasks.json
│   ├── explicit_tasks.json
│   ├── agents.json
│   └── capabilities.json
└── yaml/
    ├── implicit_tasks.yaml
    ├── explicit_tasks.yaml
    ├── agents.yaml
    └── capabilities.yaml
```

## Requirements

- Python 3.6+
- PyQt5 5.15+
- PyYAML 5.4+

## Launch Command

```bash
python gui.py
```
