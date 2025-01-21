## src/omega_agents/memory.py

"""
Memory management for ephemeral agent states: messages, logs, etc.
"""

from datetime import datetime
from typing import List, Dict, Any

class AgentMemory:
    """
    Stores conversation messages plus detailed logs for ephemeral usage.
    """
    def __init__(self, verbose: bool = False, debug: bool = False):
        # conversation: list of dict(role="user"/"assistant"/"system", content="...")
        self.conversation: List[Dict[str, str]] = []
        # logs: each log entry is a dict with 'timestamp', 'type', 'details'
        self.logs: List[Dict[str, Any]] = []

        self.verbose = verbose
        self.debug = debug

    def add_message(self, role: str, content: str):
        """
        Add a new message to the conversation, with optional verbose logging.
        """
        msg = {"role": role, "content": content}
        self.conversation.append(msg)
        if self.verbose or self.debug:
            print(f"[MEMORY] {role.upper()} message: {content}")

    def add_log(self, step_type: str, details: Dict[str, Any]):
        """
        Add a log entry with a timestamp, step type, and arbitrary details.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": step_type,
            "details": details
        }
        self.logs.append(entry)
        if self.debug:
            print(f"[DEBUG LOG] {step_type} - {details}")