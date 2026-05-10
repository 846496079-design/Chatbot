from typing import TypedDict, Annotated, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    session_id: str
    current_intent: Optional[Dict[str, Any]]
    current_emotion: Optional[Dict[str, Any]]
    current_flow: Optional[str]
    current_step: Optional[str]
    business_slots: Dict[str, Any]
    user_profile: Dict[str, Any]
    token_usage: Dict[str, int]
    fallback_count: int
    negative_emotion_count: int
    snapshot_stack: List[Dict[str, Any]]
    need_escalation: bool
    need_comfort: bool
    quick_actions: List[str]
    error: Optional[str]
    cards: Optional[List[Dict[str, Any]]]
    card_type: Optional[str]
