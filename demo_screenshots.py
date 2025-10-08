"""
Create demonstration screenshots of the GUI.
Since we can't run PyQt5 in a headless environment easily, 
this script creates an HTML demo page showing the features.
"""

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Task and Agent Management System - Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        h2 {
            color: #555;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        .feature {
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .screenshot-placeholder {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px;
            text-align: center;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 18px;
        }
        .code {
            background-color: #f4f4f4;
            padding: 15px;
            border-left: 4px solid #4CAF50;
            margin: 10px 0;
            font-family: monospace;
        }
        .graph-demo {
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
        }
        .node {
            padding: 10px 20px;
            border-radius: 20px;
            margin: 5px;
            text-align: center;
            font-weight: bold;
        }
        .task-node {
            background-color: #90EE90;
            border: 2px solid #228B22;
        }
        .agent-node {
            background-color: #FFB6C1;
            border: 2px solid #FF1493;
        }
        .capability-node {
            background-color: #ADD8E6;
            border: 2px solid #4682B4;
        }
        .arrow {
            font-size: 24px;
            color: #888;
        }
    </style>
</head>
<body>
    <h1>🎯 Task and Agent Management System</h1>
    
    <div class="feature">
        <h2>Overview</h2>
        <p>A comprehensive PyQt5-based GUI application for managing tasks, agents, and their capabilities.</p>
        <ul>
            <li>Create and manage projects</li>
            <li>Generate random tasks and agents</li>
            <li>Multiple visualization modes (textual, tabular, graphical)</li>
            <li>Interactive graph views with highlighting</li>
            <li>Edit tasks and agents</li>
            <li>Export/import projects in JSON and YAML formats</li>
        </ul>
    </div>

    <div class="feature">
        <h2>Main Window</h2>
        <div class="screenshot-placeholder">
            Main Application Window<br/>
            Menu Bar: File (New Project, Load Project, Export Project, Exit)<br/>
            Control Panel: Generate Tasks | Generate Agents | Edit Task | Edit Agent | Refresh Views<br/>
            Tabs: Textual View | Tabular View | Task-Capability Graph | Agent-Capability Graph
        </div>
    </div>

    <div class="feature">
        <h2>Textual View</h2>
        <div class="code">
            Project: My Project<br/><br/>
            === IMPLICIT TASKS ===<br/><br/>
            Task: Development Task 1 (ID: a1b2c3d4)<br/>
            &nbsp;&nbsp;Description: Auto-generated task 1<br/>
            &nbsp;&nbsp;Duration: 5<br/>
            &nbsp;&nbsp;Required Capabilities: Python, Testing, DevOps<br/><br/>
            === AGENTS ===<br/><br/>
            Agent: Alice1 (ID: e5f6g7h8)<br/>
            &nbsp;&nbsp;Capabilities: Python, JavaScript, Testing<br/>
        </div>
    </div>

    <div class="feature">
        <h2>Tabular View</h2>
        <table border="1" cellpadding="10" style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #4CAF50; color: white;">
                <th>Name</th>
                <th>Description</th>
                <th>Capabilities</th>
                <th>Duration</th>
            </tr>
            <tr>
                <td>Development Task 1</td>
                <td>Auto-generated task 1</td>
                <td>Python, Testing, DevOps</td>
                <td>5</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td>Testing Task 2</td>
                <td>Auto-generated task 2</td>
                <td>JavaScript, UI/UX</td>
                <td>3</td>
            </tr>
        </table>
        <br/>
        <table border="1" cellpadding="10" style="width:100%; border-collapse: collapse;">
            <tr style="background-color: #2196F3; color: white;">
                <th>Name</th>
                <th>Capabilities</th>
            </tr>
            <tr>
                <td>Alice1</td>
                <td>Python, JavaScript, Testing</td>
            </tr>
            <tr style="background-color: #f9f9f9;">
                <td>Bob2</td>
                <td>DevOps, Database, API</td>
            </tr>
        </table>
    </div>

    <div class="feature">
        <h2>Task-Capability Graph View</h2>
        <p>Interactive graph showing relationships between tasks and capabilities:</p>
        <div class="graph-demo">
            <div>
                <div class="node task-node">Task 1</div>
                <div class="node task-node">Task 2</div>
                <div class="node task-node">Task 3</div>
            </div>
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <span class="arrow">→</span>
                <span class="arrow">→</span>
                <span class="arrow">→</span>
            </div>
            <div>
                <div class="node capability-node">Python</div>
                <div class="node capability-node">Testing</div>
                <div class="node capability-node">DevOps</div>
            </div>
        </div>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Click a task (green rectangle) to highlight its capabilities (orange)</li>
            <li>Click a capability (blue circle) to highlight tasks that require it (orange)</li>
            <li>Click a link to see relationship details</li>
        </ul>
    </div>

    <div class="feature">
        <h2>Agent-Capability Graph View</h2>
        <p>Interactive graph showing relationships between agents and capabilities:</p>
        <div class="graph-demo">
            <div>
                <div class="node agent-node">Alice1</div>
                <div class="node agent-node">Bob2</div>
                <div class="node agent-node">Charlie3</div>
            </div>
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <span class="arrow">→</span>
                <span class="arrow">→</span>
                <span class="arrow">→</span>
            </div>
            <div>
                <div class="node capability-node">Python</div>
                <div class="node capability-node">JavaScript</div>
                <div class="node capability-node">Testing</div>
            </div>
        </div>
        <p><strong>Features:</strong></p>
        <ul>
            <li>Click an agent (pink circle) to highlight its capabilities (orange)</li>
            <li>Click a capability (blue circle) to highlight agents that provide it (orange)</li>
        </ul>
    </div>

    <div class="feature">
        <h2>Edit Dialogs</h2>
        <div style="display: flex; justify-content: space-around;">
            <div style="border: 2px solid #ccc; padding: 20px; border-radius: 8px;">
                <h3>Edit Task</h3>
                <div style="text-align: left;">
                    <strong>Name:</strong> [Development Task 1]<br/>
                    <strong>Description:</strong> [Auto-generated task 1]<br/>
                    <strong>Capabilities:</strong> [Python, Testing, DevOps]<br/>
                    <strong>Duration:</strong> [5]<br/><br/>
                    <button style="padding: 5px 15px;">OK</button>
                    <button style="padding: 5px 15px;">Cancel</button>
                </div>
            </div>
            <div style="border: 2px solid #ccc; padding: 20px; border-radius: 8px;">
                <h3>Edit Agent</h3>
                <div style="text-align: left;">
                    <strong>Name:</strong> [Alice1]<br/>
                    <strong>Capabilities:</strong><br/>
                    ☑ Python<br/>
                    ☑ JavaScript<br/>
                    ☐ Testing<br/>
                    ☐ DevOps<br/><br/>
                    <button style="padding: 5px 15px;">OK</button>
                    <button style="padding: 5px 15px;">Cancel</button>
                </div>
            </div>
        </div>
    </div>

    <div class="feature">
        <h2>Key Features</h2>
        <ol>
            <li><strong>Automatic Conversion:</strong> When generating or editing implicit tasks, they are automatically converted to explicit format</li>
            <li><strong>Synchronized Updates:</strong> Editing an implicit task automatically updates the corresponding explicit task</li>
            <li><strong>Interactive Graphs:</strong> Click elements to see relationships, with visual highlighting</li>
            <li><strong>Export/Import:</strong> Save projects as ZIP archives containing both JSON and YAML formats</li>
            <li><strong>Multiple Visualizations:</strong> View the same data in different formats for different insights</li>
        </ol>
    </div>

    <div class="feature">
        <h2>Getting Started</h2>
        <ol>
            <li>Launch the application: <code>python gui.py</code></li>
            <li>Create a new project: File → New Project</li>
            <li>Generate sample data: Click "Generate Tasks" and "Generate Agents"</li>
            <li>Explore different views by clicking the tabs</li>
            <li>Edit data using the "Edit Task" and "Edit Agent" buttons</li>
            <li>Export your project: File → Export Project</li>
        </ol>
    </div>

</body>
</html>
"""

# Write the HTML file
with open('/home/runner/work/oneplus/oneplus/demo.html', 'w') as f:
    f.write(html_content)

print("Demo HTML created successfully!")
print("Open demo.html in a browser to see the feature overview.")
