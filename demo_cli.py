"""
Command-line demonstration of the task and agent management system.
"""
from project_manager import Project
from models import ImplicitTask, Agent, Capability
import json


def print_separator():
    print("\n" + "=" * 80 + "\n")


def demo():
    """Run a demo of the system."""
    print("🎯 Task and Agent Management System - Demo")
    print_separator()
    
    # Create a new project
    print("1. Creating a new project...")
    project = Project("Demo Project")
    print(f"✓ Created project: {project.name}")
    print_separator()
    
    # Generate tasks
    print("2. Generating 5 random tasks...")
    project.generate_random_tasks(5)
    print(f"✓ Generated {len(project.implicit_tasks)} implicit tasks")
    print(f"✓ Automatically converted to {len(project.explicit_tasks)} explicit tasks")
    print(f"✓ Identified {len(project.capabilities)} unique capabilities")
    print_separator()
    
    # Show implicit tasks
    print("3. Viewing implicit tasks (textual format):")
    for i, task in enumerate(project.implicit_tasks[:3], 1):
        print(f"\nTask {i}: {task.name}")
        print(f"  ID: {task.id[:8]}...")
        print(f"  Description: {task.description}")
        print(f"  Duration: {task.duration} time units")
        print(f"  Required Capabilities: {', '.join(task.required_capabilities)}")
    print(f"\n... and {len(project.implicit_tasks) - 3} more tasks")
    print_separator()
    
    # Show explicit tasks
    print("4. Viewing explicit tasks (with resolved capability objects):")
    for i, task in enumerate(project.explicit_tasks[:2], 1):
        print(f"\nTask {i}: {task.name}")
        print(f"  Capabilities:")
        for cap in task.required_capabilities:
            print(f"    - {cap.name}: {cap.description}")
    print_separator()
    
    # Generate agents
    print("5. Generating 3 random agents...")
    project.generate_random_agents(3)
    print(f"✓ Generated {len(project.agents)} agents")
    print_separator()
    
    # Show agents
    print("6. Viewing agents:")
    for i, agent in enumerate(project.agents, 1):
        print(f"\nAgent {i}: {agent.name}")
        print(f"  ID: {agent.id[:8]}...")
        caps = ', '.join([c.name for c in agent.capabilities])
        print(f"  Capabilities: {caps}")
    print_separator()
    
    # Show capabilities
    print("7. All identified capabilities:")
    for i, (name, cap) in enumerate(project.capabilities.items(), 1):
        print(f"  {i}. {name} - {cap.description}")
    print_separator()
    
    # Edit a task
    print("8. Editing a task (demonstrating auto-sync)...")
    original_task = project.implicit_tasks[0]
    print(f"Original task: {original_task.name}")
    print(f"  Capabilities: {', '.join(original_task.required_capabilities)}")
    
    updated_task = ImplicitTask(
        id=original_task.id,
        name="Updated Development Task",
        description="This task was edited via the GUI",
        required_capabilities=["Python", "Testing", "NewCapability"],
        duration=8
    )
    
    project.update_implicit_task(original_task.id, updated_task)
    print(f"\nUpdated task: {updated_task.name}")
    print(f"  Capabilities: {', '.join(updated_task.required_capabilities)}")
    print(f"  Duration: {updated_task.duration}")
    
    # Verify explicit task was updated
    explicit = None
    for task in project.explicit_tasks:
        if task.id == original_task.id:
            explicit = task
            break
    
    print(f"\n✓ Explicit task automatically updated:")
    print(f"  Name: {explicit.name}")
    print(f"  Capabilities: {', '.join([c.name for c in explicit.required_capabilities])}")
    print_separator()
    
    # Show task-capability relationships
    print("9. Task-Capability Relationships (Graph View):")
    print("\n  Tasks (left) → Capabilities (right)\n")
    for task in project.implicit_tasks[:3]:
        print(f"  [{task.name[:20]}]", end="")
        for cap_name in task.required_capabilities:
            print(f" ──→ ({cap_name})", end="")
        print()
    print_separator()
    
    # Show agent-capability relationships
    print("10. Agent-Capability Relationships (Graph View):")
    print("\n  Agents (left) → Capabilities (right)\n")
    for agent in project.agents:
        print(f"  ({agent.name})", end="")
        for cap in agent.capabilities:
            print(f" ──→ [{cap.name}]", end="")
        print()
    print_separator()
    
    # Export to JSON
    print("11. Exporting project...")
    import tempfile
    import os
    
    with tempfile.TemporaryDirectory() as tmpdir:
        json_dir = os.path.join(tmpdir, "json_export")
        project.export_json(json_dir)
        
        print(f"✓ Exported to JSON format:")
        for filename in os.listdir(json_dir):
            filepath = os.path.join(json_dir, filename)
            size = os.path.getsize(filepath)
            print(f"  - {filename} ({size} bytes)")
        
        # Show sample JSON
        with open(os.path.join(json_dir, "implicit_tasks.json"), 'r') as f:
            data = json.load(f)
            print(f"\nSample JSON (first task):")
            print(json.dumps(data[0], indent=2))
    
    print_separator()
    
    # Summary
    print("12. Summary:")
    print(f"  ✓ Project: {project.name}")
    print(f"  ✓ Implicit Tasks: {len(project.implicit_tasks)}")
    print(f"  ✓ Explicit Tasks: {len(project.explicit_tasks)}")
    print(f"  ✓ Agents: {len(project.agents)}")
    print(f"  ✓ Capabilities: {len(project.capabilities)}")
    print(f"  ✓ All tasks automatically converted from implicit to explicit format")
    print(f"  ✓ Task edits automatically synchronized between formats")
    print_separator()
    
    print("✅ Demo complete!")
    print("\nTo use the GUI application, run: python gui.py")


if __name__ == "__main__":
    demo()
