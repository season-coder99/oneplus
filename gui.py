"""
PyQt5-based GUI for task and agent management system.
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QTextEdit, QTableWidget, QTableWidgetItem, QPushButton,
                             QLabel, QSpinBox, QDialog, QDialogButtonBox, QFormLayout, QLineEdit,
                             QListWidget, QFileDialog, QMessageBox, QInputDialog, QGraphicsView,
                             QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, 
                             QGraphicsTextItem, QMenu, QAction, QSplitter)
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter

from project_manager import Project
from models import ImplicitTask, Agent, Capability


class GraphView(QGraphicsView):
    """Custom graphics view for visualizing relationships."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.nodes = {}  # id -> (item, position)
        self.edges = []
        self.selected_item_id = None
        self.setDragMode(QGraphicsView.ScrollHandDrag)
    
    def clear_graph(self):
        """Clear all items from the graph."""
        self.scene.clear()
        self.nodes = {}
        self.edges = []
        self.selected_item_id = None


class TaskCapabilityGraphView(GraphView):
    """Graph view for tasks and their capability relationships."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
    
    def visualize_tasks_capabilities(self, implicit_tasks, capabilities_dict):
        """Visualize tasks and capabilities with relationships."""
        self.clear_graph()
        
        if not implicit_tasks:
            return
        
        # Layout parameters
        task_x = 100
        cap_x = 500
        y_spacing = 80
        
        # Draw capabilities on the right
        cap_positions = {}
        for i, (cap_name, cap) in enumerate(capabilities_dict.items()):
            y = 100 + i * y_spacing
            ellipse = self.scene.addEllipse(cap_x - 40, y - 20, 80, 40,
                                           QPen(Qt.black), QBrush(QColor(173, 216, 230)))
            text = self.scene.addText(cap_name[:15])
            text.setPos(cap_x - 35, y - 15)
            
            ellipse.setData(0, 'capability')
            ellipse.setData(1, cap_name)
            ellipse.setFlag(ellipse.ItemIsSelectable)
            
            self.nodes[f"cap_{cap_name}"] = (ellipse, QPointF(cap_x, y))
            cap_positions[cap_name] = (cap_x, y)
        
        # Draw tasks on the left
        for i, task in enumerate(implicit_tasks):
            y = 100 + i * y_spacing
            rect = self.scene.addRect(task_x - 50, y - 25, 100, 50,
                                     QPen(Qt.black), QBrush(QColor(144, 238, 144)))
            text = self.scene.addText(task.name[:15])
            text.setPos(task_x - 45, y - 20)
            
            rect.setData(0, 'task')
            rect.setData(1, task.id)
            rect.setFlag(rect.ItemIsSelectable)
            
            self.nodes[f"task_{task.id}"] = (rect, QPointF(task_x, y))
            
            # Draw edges to capabilities
            for cap_name in task.required_capabilities:
                if cap_name in cap_positions:
                    cap_pos = cap_positions[cap_name]
                    line = self.scene.addLine(task_x + 50, y, cap_pos[0] - 40, cap_pos[1],
                                             QPen(Qt.gray, 2))
                    line.setData(0, 'edge')
                    line.setData(1, f"{task.id}:{cap_name}")
                    line.setFlag(line.ItemIsSelectable)
                    self.edges.append(line)
    
    def mousePressEvent(self, event):
        """Handle mouse press to select items."""
        super().mousePressEvent(event)
        
        item = self.itemAt(event.pos())
        if item and hasattr(item, 'data'):
            item_type = item.data(0)
            
            if item_type == 'task':
                task_id = item.data(1)
                self.highlight_task_capabilities(task_id)
            elif item_type == 'capability':
                cap_name = item.data(1)
                self.highlight_capability_tasks(cap_name)
            elif item_type == 'edge':
                edge_info = item.data(1)
                if self.main_window:
                    task_id, cap_name = edge_info.split(':')
                    self.main_window.show_link_info(task_id, cap_name)
    
    def highlight_task_capabilities(self, task_id):
        """Highlight capabilities required by selected task."""
        # Reset all colors
        for node_id, (node_item, pos) in self.nodes.items():
            if node_id.startswith('cap_'):
                node_item.setBrush(QBrush(QColor(173, 216, 230)))
            elif node_id.startswith('task_'):
                node_item.setBrush(QBrush(QColor(144, 238, 144)))
        
        # Find and highlight task
        if f"task_{task_id}" in self.nodes:
            task_item, _ = self.nodes[f"task_{task_id}"]
            task_item.setBrush(QBrush(QColor(255, 255, 0)))  # Yellow
        
        # Find task and highlight its capabilities
        if self.main_window and self.main_window.project:
            for task in self.main_window.project.implicit_tasks:
                if task.id == task_id:
                    for cap_name in task.required_capabilities:
                        if f"cap_{cap_name}" in self.nodes:
                            cap_item, _ = self.nodes[f"cap_{cap_name}"]
                            cap_item.setBrush(QBrush(QColor(255, 165, 0)))  # Orange
                    break
    
    def highlight_capability_tasks(self, cap_name):
        """Highlight tasks that require selected capability."""
        # Reset all colors
        for node_id, (node_item, pos) in self.nodes.items():
            if node_id.startswith('cap_'):
                node_item.setBrush(QBrush(QColor(173, 216, 230)))
            elif node_id.startswith('task_'):
                node_item.setBrush(QBrush(QColor(144, 238, 144)))
        
        # Highlight capability
        if f"cap_{cap_name}" in self.nodes:
            cap_item, _ = self.nodes[f"cap_{cap_name}"]
            cap_item.setBrush(QBrush(QColor(255, 255, 0)))  # Yellow
        
        # Highlight tasks that use this capability
        if self.main_window and self.main_window.project:
            for task in self.main_window.project.implicit_tasks:
                if cap_name in task.required_capabilities:
                    if f"task_{task.id}" in self.nodes:
                        task_item, _ = self.nodes[f"task_{task.id}"]
                        task_item.setBrush(QBrush(QColor(255, 165, 0)))  # Orange


class AgentCapabilityGraphView(GraphView):
    """Graph view for agents and their capability relationships."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
    
    def visualize_agents_capabilities(self, agents, capabilities_dict):
        """Visualize agents and capabilities with relationships."""
        self.clear_graph()
        
        if not agents:
            return
        
        # Layout parameters
        agent_x = 100
        cap_x = 500
        y_spacing = 80
        
        # Draw capabilities on the right
        cap_positions = {}
        for i, (cap_name, cap) in enumerate(capabilities_dict.items()):
            y = 100 + i * y_spacing
            ellipse = self.scene.addEllipse(cap_x - 40, y - 20, 80, 40,
                                           QPen(Qt.black), QBrush(QColor(173, 216, 230)))
            text = self.scene.addText(cap_name[:15])
            text.setPos(cap_x - 35, y - 15)
            
            ellipse.setData(0, 'capability')
            ellipse.setData(1, cap_name)
            ellipse.setFlag(ellipse.ItemIsSelectable)
            
            self.nodes[f"cap_{cap_name}"] = (ellipse, QPointF(cap_x, y))
            cap_positions[cap_name] = (cap_x, y)
        
        # Draw agents on the left
        for i, agent in enumerate(agents):
            y = 100 + i * y_spacing
            ellipse = self.scene.addEllipse(agent_x - 40, y - 20, 80, 40,
                                           QPen(Qt.black), QBrush(QColor(255, 182, 193)))
            text = self.scene.addText(agent.name[:15])
            text.setPos(agent_x - 35, y - 15)
            
            ellipse.setData(0, 'agent')
            ellipse.setData(1, agent.id)
            ellipse.setFlag(ellipse.ItemIsSelectable)
            
            self.nodes[f"agent_{agent.id}"] = (ellipse, QPointF(agent_x, y))
            
            # Draw edges to capabilities
            for cap in agent.capabilities:
                if cap.name in cap_positions:
                    cap_pos = cap_positions[cap.name]
                    line = self.scene.addLine(agent_x + 40, y, cap_pos[0] - 40, cap_pos[1],
                                             QPen(Qt.gray, 2))
                    line.setData(0, 'edge')
                    line.setData(1, f"{agent.id}:{cap.name}")
                    self.edges.append(line)
    
    def mousePressEvent(self, event):
        """Handle mouse press to select items."""
        super().mousePressEvent(event)
        
        item = self.itemAt(event.pos())
        if item and hasattr(item, 'data'):
            item_type = item.data(0)
            
            if item_type == 'agent':
                agent_id = item.data(1)
                self.highlight_agent_capabilities(agent_id)
            elif item_type == 'capability':
                cap_name = item.data(1)
                self.highlight_capability_agents(cap_name)
    
    def highlight_agent_capabilities(self, agent_id):
        """Highlight capabilities provided by selected agent."""
        # Reset all colors
        for node_id, (node_item, pos) in self.nodes.items():
            if node_id.startswith('cap_'):
                node_item.setBrush(QBrush(QColor(173, 216, 230)))
            elif node_id.startswith('agent_'):
                node_item.setBrush(QBrush(QColor(255, 182, 193)))
        
        # Highlight agent
        if f"agent_{agent_id}" in self.nodes:
            agent_item, _ = self.nodes[f"agent_{agent_id}"]
            agent_item.setBrush(QBrush(QColor(255, 255, 0)))  # Yellow
        
        # Highlight agent's capabilities
        if self.main_window and self.main_window.project:
            for agent in self.main_window.project.agents:
                if agent.id == agent_id:
                    for cap in agent.capabilities:
                        if f"cap_{cap.name}" in self.nodes:
                            cap_item, _ = self.nodes[f"cap_{cap.name}"]
                            cap_item.setBrush(QBrush(QColor(255, 165, 0)))  # Orange
                    break
    
    def highlight_capability_agents(self, cap_name):
        """Highlight agents that provide selected capability."""
        # Reset all colors
        for node_id, (node_item, pos) in self.nodes.items():
            if node_id.startswith('cap_'):
                node_item.setBrush(QBrush(QColor(173, 216, 230)))
            elif node_id.startswith('agent_'):
                node_item.setBrush(QBrush(QColor(255, 182, 193)))
        
        # Highlight capability
        if f"cap_{cap_name}" in self.nodes:
            cap_item, _ = self.nodes[f"cap_{cap_name}"]
            cap_item.setBrush(QBrush(QColor(255, 255, 0)))  # Yellow
        
        # Highlight agents that provide this capability
        if self.main_window and self.main_window.project:
            for agent in self.main_window.project.agents:
                if any(cap.name == cap_name for cap in agent.capabilities):
                    if f"agent_{agent.id}" in self.nodes:
                        agent_item, _ = self.nodes[f"agent_{agent.id}"]
                        agent_item.setBrush(QBrush(QColor(255, 165, 0)))  # Orange


class TaskEditDialog(QDialog):
    """Dialog for editing tasks."""
    
    def __init__(self, task=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Task")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.desc_edit = QLineEdit()
        self.caps_edit = QLineEdit()
        self.duration_spin = QSpinBox()
        self.duration_spin.setMinimum(1)
        self.duration_spin.setMaximum(100)
        
        if task:
            self.name_edit.setText(task.name)
            self.desc_edit.setText(task.description)
            self.caps_edit.setText(", ".join(task.required_capabilities))
            self.duration_spin.setValue(task.duration)
        
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Description:", self.desc_edit)
        layout.addRow("Capabilities (comma-separated):", self.caps_edit)
        layout.addRow("Duration:", self.duration_spin)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        
        self.setLayout(main_layout)
    
    def get_task_data(self):
        """Get task data from dialog."""
        caps_text = self.caps_edit.text()
        caps = [c.strip() for c in caps_text.split(',') if c.strip()]
        
        return {
            'name': self.name_edit.text(),
            'description': self.desc_edit.text(),
            'required_capabilities': caps,
            'duration': self.duration_spin.value()
        }


class AgentEditDialog(QDialog):
    """Dialog for editing agents."""
    
    def __init__(self, agent=None, available_capabilities=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Agent")
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.caps_list = QListWidget()
        self.caps_list.setSelectionMode(QListWidget.MultiSelection)
        
        if available_capabilities:
            for cap_name in available_capabilities:
                self.caps_list.addItem(cap_name)
        
        if agent:
            self.name_edit.setText(agent.name)
            # Select agent's capabilities
            for i in range(self.caps_list.count()):
                item = self.caps_list.item(i)
                if any(cap.name == item.text() for cap in agent.capabilities):
                    item.setSelected(True)
        
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Capabilities:", self.caps_list)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(buttons)
        
        self.setLayout(main_layout)
    
    def get_agent_data(self):
        """Get agent data from dialog."""
        selected_caps = [item.text() for item in self.caps_list.selectedItems()]
        
        return {
            'name': self.name_edit.text(),
            'capabilities': selected_caps
        }


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.project = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Task and Agent Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        load_action = QAction("Load Project", self)
        load_action.triggered.connect(self.load_project)
        file_menu.addAction(load_action)
        
        export_action = QAction("Export Project", self)
        export_action.triggered.connect(self.export_project)
        file_menu.addAction(export_action)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Project info
        self.project_label = QLabel("No project loaded")
        layout.addWidget(self.project_label)
        
        # Control panel
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel)
        
        # Tab widget for different views
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Textual view
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        self.tabs.addTab(self.text_view, "Textual View")
        
        # Tabular view
        self.table_widget = QWidget()
        self.table_layout = QVBoxLayout()
        self.table_widget.setLayout(self.table_layout)
        self.tabs.addTab(self.table_widget, "Tabular View")
        
        # Task-Capability graph
        self.task_graph = TaskCapabilityGraphView(self)
        self.tabs.addTab(self.task_graph, "Task-Capability Graph")
        
        # Agent-Capability graph
        self.agent_graph = AgentCapabilityGraphView(self)
        self.tabs.addTab(self.agent_graph, "Agent-Capability Graph")
    
    def create_control_panel(self):
        """Create control panel with buttons."""
        panel = QWidget()
        layout = QHBoxLayout()
        panel.setLayout(layout)
        
        gen_tasks_btn = QPushButton("Generate Tasks")
        gen_tasks_btn.clicked.connect(self.generate_tasks)
        layout.addWidget(gen_tasks_btn)
        
        gen_agents_btn = QPushButton("Generate Agents")
        gen_agents_btn.clicked.connect(self.generate_agents)
        layout.addWidget(gen_agents_btn)
        
        edit_task_btn = QPushButton("Edit Task")
        edit_task_btn.clicked.connect(self.edit_task)
        layout.addWidget(edit_task_btn)
        
        edit_agent_btn = QPushButton("Edit Agent")
        edit_agent_btn.clicked.connect(self.edit_agent)
        layout.addWidget(edit_agent_btn)
        
        refresh_btn = QPushButton("Refresh Views")
        refresh_btn.clicked.connect(self.refresh_views)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
        
        return panel
    
    def new_project(self):
        """Create a new project."""
        name, ok = QInputDialog.getText(self, "New Project", "Project Name:")
        if ok and name:
            self.project = Project(name)
            self.project_label.setText(f"Project: {name}")
            self.refresh_views()
            QMessageBox.information(self, "Success", f"Created new project: {name}")
    
    def load_project(self):
        """Load an existing project."""
        directory = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if directory:
            try:
                self.project = Project.load_from_json(directory)
                self.project_label.setText(f"Project: {self.project.name}")
                self.refresh_views()
                QMessageBox.information(self, "Success", "Project loaded successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")
    
    def export_project(self):
        """Export project as archive."""
        if not self.project:
            QMessageBox.warning(self, "Warning", "No project loaded")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Project", "", 
                                                    "ZIP Archive (*.zip)")
        if file_path:
            try:
                self.project.export_archive(file_path)
                QMessageBox.information(self, "Success", "Project exported successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export project: {str(e)}")
    
    def generate_tasks(self):
        """Generate random tasks."""
        if not self.project:
            QMessageBox.warning(self, "Warning", "Please create or load a project first")
            return
        
        count, ok = QInputDialog.getInt(self, "Generate Tasks", "Number of tasks:", 5, 1, 50)
        if ok:
            self.project.generate_random_tasks(count)
            self.refresh_views()
            QMessageBox.information(self, "Success", f"Generated {count} tasks")
    
    def generate_agents(self):
        """Generate random agents."""
        if not self.project:
            QMessageBox.warning(self, "Warning", "Please create or load a project first")
            return
        
        count, ok = QInputDialog.getInt(self, "Generate Agents", "Number of agents:", 3, 1, 20)
        if ok:
            self.project.generate_random_agents(count)
            self.refresh_views()
            QMessageBox.information(self, "Success", f"Generated {count} agents")
    
    def edit_task(self):
        """Edit a task."""
        if not self.project or not self.project.implicit_tasks:
            QMessageBox.warning(self, "Warning", "No tasks available")
            return
        
        # Select task
        task_names = [f"{t.name} ({t.id[:8]})" for t in self.project.implicit_tasks]
        task_name, ok = QInputDialog.getItem(self, "Select Task", "Task:", task_names, 0, False)
        
        if ok and task_name:
            # Find task
            task_idx = task_names.index(task_name)
            task = self.project.implicit_tasks[task_idx]
            
            # Show edit dialog
            dialog = TaskEditDialog(task, self)
            if dialog.exec_():
                data = dialog.get_task_data()
                updated_task = ImplicitTask(
                    id=task.id,
                    name=data['name'],
                    description=data['description'],
                    required_capabilities=data['required_capabilities'],
                    duration=data['duration']
                )
                self.project.update_implicit_task(task.id, updated_task)
                self.refresh_views()
                QMessageBox.information(self, "Success", "Task updated")
    
    def edit_agent(self):
        """Edit an agent."""
        if not self.project or not self.project.agents:
            QMessageBox.warning(self, "Warning", "No agents available")
            return
        
        # Select agent
        agent_names = [f"{a.name} ({a.id[:8]})" for a in self.project.agents]
        agent_name, ok = QInputDialog.getItem(self, "Select Agent", "Agent:", agent_names, 0, False)
        
        if ok and agent_name:
            # Find agent
            agent_idx = agent_names.index(agent_name)
            agent = self.project.agents[agent_idx]
            
            # Show edit dialog
            dialog = AgentEditDialog(agent, list(self.project.capabilities.keys()), self)
            if dialog.exec_():
                data = dialog.get_agent_data()
                caps = [self.project.capabilities[name] for name in data['capabilities'] 
                       if name in self.project.capabilities]
                updated_agent = Agent(
                    id=agent.id,
                    name=data['name'],
                    capabilities=caps
                )
                self.project.update_agent(agent.id, updated_agent)
                self.refresh_views()
                QMessageBox.information(self, "Success", "Agent updated")
    
    def refresh_views(self):
        """Refresh all views with current project data."""
        if not self.project:
            return
        
        # Update textual view
        self.update_text_view()
        
        # Update tabular view
        self.update_table_view()
        
        # Update graphs
        self.task_graph.visualize_tasks_capabilities(
            self.project.implicit_tasks, 
            self.project.capabilities
        )
        self.agent_graph.visualize_agents_capabilities(
            self.project.agents, 
            self.project.capabilities
        )
    
    def update_text_view(self):
        """Update textual view."""
        text = f"Project: {self.project.name}\n\n"
        
        text += "=== IMPLICIT TASKS ===\n"
        for task in self.project.implicit_tasks:
            text += f"\nTask: {task.name} (ID: {task.id[:8]})\n"
            text += f"  Description: {task.description}\n"
            text += f"  Duration: {task.duration}\n"
            text += f"  Required Capabilities: {', '.join(task.required_capabilities)}\n"
        
        text += "\n\n=== EXPLICIT TASKS ===\n"
        for task in self.project.explicit_tasks:
            text += f"\nTask: {task.name} (ID: {task.id[:8]})\n"
            text += f"  Description: {task.description}\n"
            text += f"  Duration: {task.duration}\n"
            text += f"  Required Capabilities: {', '.join([c.name for c in task.required_capabilities])}\n"
        
        text += "\n\n=== AGENTS ===\n"
        for agent in self.project.agents:
            text += f"\nAgent: {agent.name} (ID: {agent.id[:8]})\n"
            text += f"  Capabilities: {', '.join([c.name for c in agent.capabilities])}\n"
        
        text += "\n\n=== CAPABILITIES ===\n"
        for cap_name, cap in self.project.capabilities.items():
            text += f"\nCapability: {cap.name}\n"
            text += f"  Description: {cap.description}\n"
        
        self.text_view.setText(text)
    
    def update_table_view(self):
        """Update tabular view."""
        # Clear existing tables
        for i in reversed(range(self.table_layout.count())):
            self.table_layout.itemAt(i).widget().setParent(None)
        
        # Tasks table
        if self.project.implicit_tasks:
            tasks_label = QLabel("Tasks")
            self.table_layout.addWidget(tasks_label)
            
            tasks_table = QTableWidget()
            tasks_table.setColumnCount(4)
            tasks_table.setHorizontalHeaderLabels(["Name", "Description", "Capabilities", "Duration"])
            tasks_table.setRowCount(len(self.project.implicit_tasks))
            
            for i, task in enumerate(self.project.implicit_tasks):
                tasks_table.setItem(i, 0, QTableWidgetItem(task.name))
                tasks_table.setItem(i, 1, QTableWidgetItem(task.description))
                tasks_table.setItem(i, 2, QTableWidgetItem(", ".join(task.required_capabilities)))
                tasks_table.setItem(i, 3, QTableWidgetItem(str(task.duration)))
            
            tasks_table.resizeColumnsToContents()
            self.table_layout.addWidget(tasks_table)
        
        # Agents table
        if self.project.agents:
            agents_label = QLabel("Agents")
            self.table_layout.addWidget(agents_label)
            
            agents_table = QTableWidget()
            agents_table.setColumnCount(2)
            agents_table.setHorizontalHeaderLabels(["Name", "Capabilities"])
            agents_table.setRowCount(len(self.project.agents))
            
            for i, agent in enumerate(self.project.agents):
                agents_table.setItem(i, 0, QTableWidgetItem(agent.name))
                agents_table.setItem(i, 1, QTableWidgetItem(", ".join([c.name for c in agent.capabilities])))
            
            agents_table.resizeColumnsToContents()
            self.table_layout.addWidget(agents_table)
    
    def show_link_info(self, task_id, cap_name):
        """Show information about a task-capability link."""
        task = None
        for t in self.project.implicit_tasks:
            if t.id == task_id:
                task = t
                break
        
        if task:
            info = f"Task: {task.name}\n"
            info += f"Requires Capability: {cap_name}\n"
            if cap_name in self.project.capabilities:
                cap = self.project.capabilities[cap_name]
                info += f"Capability Description: {cap.description}"
            
            QMessageBox.information(self, "Link Information", info)


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
