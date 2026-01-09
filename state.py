"""
State schema for code review agent.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field


class CodeReviewState(BaseModel):
    """
    Simplified state schema for code review agent.
    """
    
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Chat messages")
    commit_id: str = Field(description="Git commit ID to review")

