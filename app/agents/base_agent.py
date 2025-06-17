# ===== app/agents/base_agent.py =====
from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import Dict, Any, List

class BaseAgent(ABC):
    """Base class for all AI agents in ASTHA system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "idle"
        self.last_execution = None
        self.execution_history = []
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the agent's main functionality"""
        pass
    
    def start_execution(self):
        """Mark agent as active"""
        self.status = "active"
        self.last_execution = datetime.now()
        self.logger.info(f"Agent {self.name} started execution")
    
    def complete_execution(self, result: Dict[str, Any]):
        """Mark agent execution as complete"""
        self.status = "completed"
        self.execution_history.append({
            'timestamp': self.last_execution,
            'result': result,
            'success': True
        })
        self.logger.info(f"Agent {self.name} completed execution")
    
    def fail_execution(self, error: str):
        """Mark agent execution as failed"""
        self.status = "failed"
        self.execution_history.append({
            'timestamp': self.last_execution,
            'error': error,
            'success': False
        })
        self.logger.error(f"Agent {self.name} failed: {error}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'last_execution': self.last_execution,
            'execution_count': len(self.execution_history)
        }
