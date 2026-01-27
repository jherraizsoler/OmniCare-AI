# state.py
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # Annotated + add_messages permite que los nodos "sumen" mensajes a la lista
    messages: Annotated[list, add_messages] 
    patient_data: dict
    resource_focus: str
    safety_check_passed: bool