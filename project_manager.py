"""
Project management module for handling task and agent projects.
"""
import json
import yaml
import random
import zipfile
import os
from typing import List, Dict, Optional
from pathlib import Path
from models import ImplicitTask, ExplicitTask, Agent, Capability, implicit_to_explicit, explicit_to_implicit


class Project:
    """Manages a collection of tasks, agents, and capabilities."""
    
    def __init__(self, name: str = "Untitled Project"):
        self.name = name
        self.implicit_tasks: List[ImplicitTask] = []
        self.explicit_tasks: List[ExplicitTask] = []
        self.agents: List[Agent] = []
        self.capabilities: Dict[str, Capability] = {}  # name -> Capability
    
    def generate_random_tasks(self, count: int) -> None:
        """Generate random implicit tasks and convert them to explicit format."""
        task_names = ["Development", "Testing", "Deployment", "Documentation", "Review", 
                     "Planning", "Design", "Implementation", "Maintenance", "Monitoring"]
        capability_names = ["Python", "JavaScript", "Testing", "DevOps", "UI/UX", 
                          "Database", "API", "Security", "Performance", "Documentation"]
        
        for i in range(count):
            # Generate random implicit task
            num_caps = random.randint(1, 4)
            required_caps = random.sample(capability_names, num_caps)
            
            task = ImplicitTask(
                name=f"{random.choice(task_names)} Task {i+1}",
                description=f"Auto-generated task {i+1}",
                required_capabilities=required_caps,
                duration=random.randint(1, 10)
            )
            
            self.implicit_tasks.append(task)
            
            # Ensure capabilities exist
            for cap_name in required_caps:
                if cap_name not in self.capabilities:
                    self.capabilities[cap_name] = Capability(
                        name=cap_name,
                        description=f"{cap_name} capability"
                    )
            
            # Convert to explicit format immediately
            explicit_task = implicit_to_explicit(task, self.capabilities)
            self.explicit_tasks.append(explicit_task)
    
    def generate_random_agents(self, count: int) -> None:
        """Generate random agents with capabilities."""
        agent_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", 
                      "Frank", "Grace", "Henry", "Ivy", "Jack"]
        capability_names = list(self.capabilities.keys())
        
        if not capability_names:
            # Generate default capabilities if none exist
            capability_names = ["Python", "JavaScript", "Testing", "DevOps", "UI/UX"]
            for cap_name in capability_names:
                self.capabilities[cap_name] = Capability(
                    name=cap_name,
                    description=f"{cap_name} capability"
                )
        
        for i in range(count):
            num_caps = random.randint(1, min(5, len(capability_names)))
            agent_caps_names = random.sample(capability_names, num_caps)
            agent_caps = [self.capabilities[name] for name in agent_caps_names]
            
            agent = Agent(
                name=f"{random.choice(agent_names)}{i+1}",
                capabilities=agent_caps
            )
            self.agents.append(agent)
    
    def update_implicit_task(self, task_id: str, updated_task: ImplicitTask) -> None:
        """Update an implicit task and synchronize with explicit task."""
        for i, task in enumerate(self.implicit_tasks):
            if task.id == task_id:
                self.implicit_tasks[i] = updated_task
                
                # Update capabilities dict
                for cap_name in updated_task.required_capabilities:
                    if cap_name not in self.capabilities:
                        self.capabilities[cap_name] = Capability(
                            name=cap_name,
                            description=f"{cap_name} capability"
                        )
                
                # Update corresponding explicit task
                explicit_task = implicit_to_explicit(updated_task, self.capabilities)
                for j, exp_task in enumerate(self.explicit_tasks):
                    if exp_task.id == task_id:
                        self.explicit_tasks[j] = explicit_task
                        break
                break
    
    def update_agent(self, agent_id: str, updated_agent: Agent) -> None:
        """Update an agent."""
        for i, agent in enumerate(self.agents):
            if agent.id == agent_id:
                self.agents[i] = updated_agent
                
                # Update capabilities dict
                for cap in updated_agent.capabilities:
                    if cap.name not in self.capabilities:
                        self.capabilities[cap.name] = cap
                break
    
    def to_dict(self) -> Dict:
        """Convert project to dictionary for serialization."""
        return {
            'name': self.name,
            'implicit_tasks': [task.to_dict() for task in self.implicit_tasks],
            'explicit_tasks': [task.to_dict() for task in self.explicit_tasks],
            'agents': [agent.to_dict() for agent in self.agents],
            'capabilities': {name: {'name': cap.name, 'description': cap.description} 
                           for name, cap in self.capabilities.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        """Create project from dictionary."""
        project = cls(name=data.get('name', 'Untitled Project'))
        
        # Load capabilities first
        for cap_data in data.get('capabilities', {}).values():
            cap = Capability(**cap_data)
            project.capabilities[cap.name] = cap
        
        # Load tasks
        project.implicit_tasks = [ImplicitTask.from_dict(t) for t in data.get('implicit_tasks', [])]
        project.explicit_tasks = [ExplicitTask.from_dict(t) for t in data.get('explicit_tasks', [])]
        
        # Load agents
        project.agents = [Agent.from_dict(a) for a in data.get('agents', [])]
        
        return project
    
    def export_json(self, directory: str) -> None:
        """Export project data as JSON files."""
        os.makedirs(directory, exist_ok=True)
        
        data = self.to_dict()
        
        # Export implicit tasks
        with open(os.path.join(directory, 'implicit_tasks.json'), 'w') as f:
            json.dump(data['implicit_tasks'], f, indent=2)
        
        # Export explicit tasks
        with open(os.path.join(directory, 'explicit_tasks.json'), 'w') as f:
            json.dump(data['explicit_tasks'], f, indent=2)
        
        # Export agents
        with open(os.path.join(directory, 'agents.json'), 'w') as f:
            json.dump(data['agents'], f, indent=2)
        
        # Export capabilities
        with open(os.path.join(directory, 'capabilities.json'), 'w') as f:
            json.dump(data['capabilities'], f, indent=2)
    
    def export_yaml(self, directory: str) -> None:
        """Export project data as YAML files."""
        os.makedirs(directory, exist_ok=True)
        
        data = self.to_dict()
        
        # Export implicit tasks
        with open(os.path.join(directory, 'implicit_tasks.yaml'), 'w') as f:
            yaml.dump(data['implicit_tasks'], f, default_flow_style=False)
        
        # Export explicit tasks
        with open(os.path.join(directory, 'explicit_tasks.yaml'), 'w') as f:
            yaml.dump(data['explicit_tasks'], f, default_flow_style=False)
        
        # Export agents
        with open(os.path.join(directory, 'agents.yaml'), 'w') as f:
            yaml.dump(data['agents'], f, default_flow_style=False)
        
        # Export capabilities
        with open(os.path.join(directory, 'capabilities.yaml'), 'w') as f:
            yaml.dump(data['capabilities'], f, default_flow_style=False)
    
    def export_archive(self, archive_path: str) -> None:
        """Export project as a ZIP archive containing JSON and YAML files."""
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Export both formats
            json_dir = os.path.join(tmpdir, 'json')
            yaml_dir = os.path.join(tmpdir, 'yaml')
            
            self.export_json(json_dir)
            self.export_yaml(yaml_dir)
            
            # Create archive
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(tmpdir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, tmpdir)
                        zipf.write(file_path, arcname)
    
    @classmethod
    def load_from_json(cls, directory: str) -> 'Project':
        """Load project from JSON files."""
        project = cls()
        
        # Load capabilities
        caps_path = os.path.join(directory, 'capabilities.json')
        if os.path.exists(caps_path):
            with open(caps_path, 'r') as f:
                caps_data = json.load(f)
                for cap_data in caps_data.values():
                    cap = Capability(**cap_data)
                    project.capabilities[cap.name] = cap
        
        # Load implicit tasks
        impl_path = os.path.join(directory, 'implicit_tasks.json')
        if os.path.exists(impl_path):
            with open(impl_path, 'r') as f:
                tasks_data = json.load(f)
                project.implicit_tasks = [ImplicitTask.from_dict(t) for t in tasks_data]
        
        # Load explicit tasks
        expl_path = os.path.join(directory, 'explicit_tasks.json')
        if os.path.exists(expl_path):
            with open(expl_path, 'r') as f:
                tasks_data = json.load(f)
                project.explicit_tasks = [ExplicitTask.from_dict(t) for t in tasks_data]
        
        # Load agents
        agents_path = os.path.join(directory, 'agents.json')
        if os.path.exists(agents_path):
            with open(agents_path, 'r') as f:
                agents_data = json.load(f)
                project.agents = [Agent.from_dict(a) for a in agents_data]
        
        return project
