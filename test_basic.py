"""
Basic tests for the task and agent management system.
"""
import os
import sys
import tempfile
import shutil
from models import ImplicitTask, ExplicitTask, Agent, Capability, implicit_to_explicit, explicit_to_implicit
from project_manager import Project


def test_models():
    """Test basic model functionality."""
    print("Testing models...")
    
    # Test Capability
    cap = Capability(name="Python", description="Python programming")
    assert cap.name == "Python"
    
    # Test ImplicitTask
    task = ImplicitTask(name="Test Task", required_capabilities=["Python", "Testing"])
    assert len(task.required_capabilities) == 2
    
    # Test Agent
    agent = Agent(name="Alice", capabilities=[cap])
    assert len(agent.capabilities) == 1
    
    print("✓ Models test passed")


def test_conversion():
    """Test implicit to explicit conversion."""
    print("Testing conversion...")
    
    cap_dict = {
        "Python": Capability(name="Python", description="Python programming"),
        "Testing": Capability(name="Testing", description="Software testing")
    }
    
    implicit = ImplicitTask(name="Test Task", required_capabilities=["Python", "Testing"])
    explicit = implicit_to_explicit(implicit, cap_dict)
    
    assert len(explicit.required_capabilities) == 2
    assert explicit.name == implicit.name
    
    # Convert back
    back_to_implicit = explicit_to_implicit(explicit)
    assert back_to_implicit.required_capabilities == implicit.required_capabilities
    
    print("✓ Conversion test passed")


def test_project():
    """Test project management."""
    print("Testing project management...")
    
    project = Project("Test Project")
    
    # Generate tasks
    project.generate_random_tasks(5)
    assert len(project.implicit_tasks) == 5
    assert len(project.explicit_tasks) == 5
    assert len(project.capabilities) > 0
    
    # Generate agents
    project.generate_random_agents(3)
    assert len(project.agents) == 3
    
    # Test serialization
    data = project.to_dict()
    assert data['name'] == "Test Project"
    assert len(data['implicit_tasks']) == 5
    
    # Test loading from dict
    project2 = Project.from_dict(data)
    assert project2.name == "Test Project"
    assert len(project2.implicit_tasks) == 5
    assert len(project2.agents) == 3
    
    print("✓ Project test passed")


def test_export_import():
    """Test project export and import."""
    print("Testing export/import...")
    
    project = Project("Export Test")
    project.generate_random_tasks(3)
    project.generate_random_agents(2)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test JSON export
        json_dir = os.path.join(tmpdir, "json_export")
        project.export_json(json_dir)
        assert os.path.exists(os.path.join(json_dir, "implicit_tasks.json"))
        assert os.path.exists(os.path.join(json_dir, "agents.json"))
        
        # Test YAML export
        yaml_dir = os.path.join(tmpdir, "yaml_export")
        project.export_yaml(yaml_dir)
        assert os.path.exists(os.path.join(yaml_dir, "implicit_tasks.yaml"))
        assert os.path.exists(os.path.join(yaml_dir, "agents.yaml"))
        
        # Test archive export
        archive_path = os.path.join(tmpdir, "project.zip")
        project.export_archive(archive_path)
        assert os.path.exists(archive_path)
        
        # Test loading from JSON
        project2 = Project.load_from_json(json_dir)
        assert len(project2.implicit_tasks) == 3
        assert len(project2.agents) == 2
    
    print("✓ Export/import test passed")


def test_task_update():
    """Test task update with auto-sync to explicit format."""
    print("Testing task update...")
    
    project = Project("Update Test")
    project.generate_random_tasks(2)
    
    task_id = project.implicit_tasks[0].id
    updated_task = ImplicitTask(
        id=task_id,
        name="Updated Task",
        description="Updated description",
        required_capabilities=["NewCap1", "NewCap2"],
        duration=5
    )
    
    project.update_implicit_task(task_id, updated_task)
    
    # Check implicit task was updated
    assert project.implicit_tasks[0].name == "Updated Task"
    
    # Check explicit task was also updated
    explicit = None
    for task in project.explicit_tasks:
        if task.id == task_id:
            explicit = task
            break
    
    assert explicit is not None
    assert explicit.name == "Updated Task"
    assert len(explicit.required_capabilities) == 2
    
    # Check capabilities were added
    assert "NewCap1" in project.capabilities
    assert "NewCap2" in project.capabilities
    
    print("✓ Task update test passed")


def main():
    """Run all tests."""
    print("Running tests...\n")
    
    try:
        test_models()
        test_conversion()
        test_project()
        test_export_import()
        test_task_update()
        
        print("\n✅ All tests passed!")
        return 0
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
