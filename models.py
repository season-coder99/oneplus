"""
Core data models for task and agent management system.
"""
import uuid
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field


@dataclass
class Capability:
    """Represents a capability that can be required by tasks or provided by agents."""
    name: str
    description: str = ""
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, Capability):
            return self.name == other.name
        return False


@dataclass
class ImplicitTask:
    """
    Implicit task format: tasks reference capabilities by name/tags.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    required_capabilities: List[str] = field(default_factory=list)  # capability names
    duration: int = 1  # time units
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'required_capabilities': self.required_capabilities,
            'duration': self.duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ImplicitTask':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ExplicitTask:
    """
    Explicit task format: tasks directly reference capability objects.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    required_capabilities: List[Capability] = field(default_factory=list)  # actual capability objects
    duration: int = 1
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'required_capabilities': [{'name': cap.name, 'description': cap.description} 
                                     for cap in self.required_capabilities],
            'duration': self.duration
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ExplicitTask':
        """Create from dictionary."""
        caps = [Capability(**cap_data) for cap_data in data.get('required_capabilities', [])]
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            required_capabilities=caps,
            duration=data.get('duration', 1)
        )


@dataclass
class Agent:
    """Represents an agent with capabilities."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    capabilities: List[Capability] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'capabilities': [{'name': cap.name, 'description': cap.description} 
                           for cap in self.capabilities]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Agent':
        """Create from dictionary."""
        caps = [Capability(**cap_data) for cap_data in data.get('capabilities', [])]
        return cls(
            id=data['id'],
            name=data['name'],
            capabilities=caps
        )


def implicit_to_explicit(implicit_task: ImplicitTask, 
                        capabilities_dict: Dict[str, Capability]) -> ExplicitTask:
    """
    Convert implicit task to explicit task by resolving capability names to objects.
    
    Args:
        implicit_task: The implicit task to convert
        capabilities_dict: Dictionary mapping capability names to Capability objects
    
    Returns:
        ExplicitTask with resolved capability references
    """
    explicit_caps = []
    for cap_name in implicit_task.required_capabilities:
        if cap_name in capabilities_dict:
            explicit_caps.append(capabilities_dict[cap_name])
        else:
            # Create new capability if not found
            new_cap = Capability(name=cap_name, description=f"Auto-generated: {cap_name}")
            capabilities_dict[cap_name] = new_cap
            explicit_caps.append(new_cap)
    
    return ExplicitTask(
        id=implicit_task.id,
        name=implicit_task.name,
        description=implicit_task.description,
        required_capabilities=explicit_caps,
        duration=implicit_task.duration
    )


def explicit_to_implicit(explicit_task: ExplicitTask) -> ImplicitTask:
    """
    Convert explicit task to implicit task by extracting capability names.
    
    Args:
        explicit_task: The explicit task to convert
    
    Returns:
        ImplicitTask with capability names
    """
    return ImplicitTask(
        id=explicit_task.id,
        name=explicit_task.name,
        description=explicit_task.description,
        required_capabilities=[cap.name for cap in explicit_task.required_capabilities],
        duration=explicit_task.duration
    )
