#!/usr/bin/env python3
"""
Example: Creating a real-world project using the Task and Agent Management System.

This example demonstrates creating a software development project with
realistic tasks and agents.
"""
from project_manager import Project
from models import ImplicitTask, Agent, Capability
import json


def create_software_project():
    """Create a sample software development project."""
    
    print("Creating Software Development Project...")
    print("=" * 70)
    
    # Create project
    project = Project("Web Application Development")
    
    # Define capabilities
    capabilities = [
        Capability("Frontend", "React and modern web development"),
        Capability("Backend", "Python/Django backend development"),
        Capability("Database", "PostgreSQL database design and optimization"),
        Capability("DevOps", "CI/CD, Docker, Kubernetes"),
        Capability("Testing", "Unit and integration testing"),
        Capability("UI/UX", "User interface and experience design"),
        Capability("Security", "Application security and authentication"),
        Capability("API", "RESTful API design and implementation"),
    ]
    
    for cap in capabilities:
        project.capabilities[cap.name] = cap
    
    # Create implicit tasks
    tasks_data = [
        {
            "name": "Design User Interface",
            "description": "Create mockups and design system for the application",
            "capabilities": ["UI/UX", "Frontend"],
            "duration": 5
        },
        {
            "name": "Implement Authentication",
            "description": "Build user authentication and authorization system",
            "capabilities": ["Backend", "Security", "Database"],
            "duration": 8
        },
        {
            "name": "Create REST API",
            "description": "Develop RESTful API endpoints for the application",
            "capabilities": ["Backend", "API", "Database"],
            "duration": 10
        },
        {
            "name": "Build Frontend Components",
            "description": "Implement React components based on designs",
            "capabilities": ["Frontend", "UI/UX"],
            "duration": 12
        },
        {
            "name": "Setup CI/CD Pipeline",
            "description": "Configure automated testing and deployment",
            "capabilities": ["DevOps", "Testing"],
            "duration": 6
        },
        {
            "name": "Database Schema Design",
            "description": "Design and implement database schema",
            "capabilities": ["Database", "Backend"],
            "duration": 4
        },
        {
            "name": "Write Unit Tests",
            "description": "Create comprehensive unit test suite",
            "capabilities": ["Testing", "Backend", "Frontend"],
            "duration": 7
        },
        {
            "name": "Security Audit",
            "description": "Review and improve application security",
            "capabilities": ["Security", "Backend", "Frontend"],
            "duration": 5
        },
    ]
    
    # Create tasks
    for task_data in tasks_data:
        task = ImplicitTask(
            name=task_data["name"],
            description=task_data["description"],
            required_capabilities=task_data["capabilities"],
            duration=task_data["duration"]
        )
        project.implicit_tasks.append(task)
        
        # Convert to explicit
        from models import implicit_to_explicit
        explicit = implicit_to_explicit(task, project.capabilities)
        project.explicit_tasks.append(explicit)
    
    print(f"✓ Created {len(project.implicit_tasks)} tasks")
    
    # Create agents
    agents_data = [
        {
            "name": "Alice (Senior Frontend Developer)",
            "capabilities": ["Frontend", "UI/UX", "Testing"]
        },
        {
            "name": "Bob (Backend Engineer)",
            "capabilities": ["Backend", "Database", "API", "Testing"]
        },
        {
            "name": "Charlie (DevOps Engineer)",
            "capabilities": ["DevOps", "Backend", "Database"]
        },
        {
            "name": "Diana (Full Stack Developer)",
            "capabilities": ["Frontend", "Backend", "API"]
        },
        {
            "name": "Eve (Security Specialist)",
            "capabilities": ["Security", "Backend", "Testing"]
        },
    ]
    
    for agent_data in agents_data:
        caps = [project.capabilities[cap_name] for cap_name in agent_data["capabilities"]]
        agent = Agent(name=agent_data["name"], capabilities=caps)
        project.agents.append(agent)
    
    print(f"✓ Created {len(project.agents)} agents")
    print()
    
    return project


def display_project_summary(project):
    """Display a summary of the project."""
    
    print("\n" + "=" * 70)
    print("PROJECT SUMMARY")
    print("=" * 70)
    
    print(f"\nProject Name: {project.name}")
    print(f"Total Tasks: {len(project.implicit_tasks)}")
    print(f"Total Agents: {len(project.agents)}")
    print(f"Total Capabilities: {len(project.capabilities)}")
    
    # Task breakdown
    print("\n--- TASKS ---")
    total_duration = sum(task.duration for task in project.implicit_tasks)
    print(f"Total Duration: {total_duration} time units")
    print("\nTask List:")
    for i, task in enumerate(project.implicit_tasks, 1):
        caps = ", ".join(task.required_capabilities)
        print(f"  {i}. {task.name} ({task.duration} units)")
        print(f"     Requires: {caps}")
    
    # Agent breakdown
    print("\n--- AGENTS ---")
    for agent in project.agents:
        caps = ", ".join([c.name for c in agent.capabilities])
        print(f"  • {agent.name}")
        print(f"    Skills: {caps}")
    
    # Capability analysis
    print("\n--- CAPABILITY ANALYSIS ---")
    
    # Count how many tasks need each capability
    cap_usage = {}
    for task in project.implicit_tasks:
        for cap_name in task.required_capabilities:
            cap_usage[cap_name] = cap_usage.get(cap_name, 0) + 1
    
    # Count how many agents have each capability
    cap_supply = {}
    for agent in project.agents:
        for cap in agent.capabilities:
            cap_supply[cap.name] = cap_supply.get(cap.name, 0) + 1
    
    print("\nCapability Demand vs Supply:")
    print(f"{'Capability':<15} {'Tasks':<10} {'Agents':<10} {'Status':<10}")
    print("-" * 50)
    
    all_caps = set(cap_usage.keys()) | set(cap_supply.keys())
    for cap_name in sorted(all_caps):
        demand = cap_usage.get(cap_name, 0)
        supply = cap_supply.get(cap_name, 0)
        
        if supply >= demand:
            status = "✓ Good"
        elif supply > 0:
            status = "⚠ Low"
        else:
            status = "✗ None"
        
        print(f"{cap_name:<15} {demand:<10} {supply:<10} {status:<10}")
    
    # Task assignment suggestions
    print("\n--- TASK ASSIGNMENT SUGGESTIONS ---")
    for task in project.implicit_tasks:
        print(f"\n{task.name}:")
        print(f"  Required: {', '.join(task.required_capabilities)}")
        
        # Find agents that can do this task
        qualified_agents = []
        for agent in project.agents:
            agent_caps = set(c.name for c in agent.capabilities)
            task_caps = set(task.required_capabilities)
            
            matching = task_caps & agent_caps
            if matching:
                coverage = len(matching) / len(task_caps) * 100
                qualified_agents.append((agent.name, coverage, matching))
        
        if qualified_agents:
            qualified_agents.sort(key=lambda x: x[1], reverse=True)
            print("  Qualified agents:")
            for agent_name, coverage, matching in qualified_agents:
                print(f"    • {agent_name}: {coverage:.0f}% match ({', '.join(matching)})")
        else:
            print("  ⚠ No qualified agents found!")


def export_project_example(project):
    """Export the project to various formats."""
    
    print("\n" + "=" * 70)
    print("EXPORTING PROJECT")
    print("=" * 70)
    
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Export JSON
        json_dir = os.path.join(tmpdir, "json")
        project.export_json(json_dir)
        print(f"\n✓ Exported to JSON format: {json_dir}")
        
        # Show sample
        with open(os.path.join(json_dir, "implicit_tasks.json"), 'r') as f:
            data = json.load(f)
            print("\nSample task (JSON):")
            print(json.dumps(data[0], indent=2))
        
        # Export YAML
        yaml_dir = os.path.join(tmpdir, "yaml")
        project.export_yaml(yaml_dir)
        print(f"\n✓ Exported to YAML format: {yaml_dir}")
        
        # Export archive
        archive_path = os.path.join(tmpdir, "project.zip")
        project.export_archive(archive_path)
        print(f"\n✓ Created archive: project.zip")
        print(f"  Archive size: {os.path.getsize(archive_path)} bytes")


def main():
    """Main entry point."""
    
    print("\n" + "=" * 70)
    print(" TASK AND AGENT MANAGEMENT SYSTEM - EXAMPLE PROJECT")
    print("=" * 70)
    
    # Create project
    project = create_software_project()
    
    # Display summary
    display_project_summary(project)
    
    # Export project
    export_project_example(project)
    
    print("\n" + "=" * 70)
    print(" NEXT STEPS")
    print("=" * 70)
    print("\nTo visualize this project in the GUI:")
    print("  1. Run: python gui.py")
    print("  2. File → New Project")
    print("  3. Generate or manually add your tasks and agents")
    print("  4. Use the graph views to visualize relationships")
    print("  5. Edit and refine your project")
    print("  6. Export when complete")
    print("\nThis example demonstrated:")
    print("  ✓ Creating a realistic project")
    print("  ✓ Defining capabilities")
    print("  ✓ Creating tasks with requirements")
    print("  ✓ Creating agents with skills")
    print("  ✓ Analyzing capability coverage")
    print("  ✓ Suggesting task assignments")
    print("  ✓ Exporting project data")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
