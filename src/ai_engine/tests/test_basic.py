# ai_engine\tests\test_basic.py  

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from ai_engine.main import app

client = TestClient(app)

def test_health_check():
    """Verifica que la app carga con el título correcto."""
    assert app.title == "OmniCare AI Engine"

async def test_analyze_endpoint_structure():
    payload = {
        "patientId": "PAC-123",
        "symptoms": "Dolor de cabeza leve",
        "urgencyLevel": 1,
        "consentProvided": True
    }

    # Creamos un objeto que simule el mensaje de LangChain
    mock_message = AsyncMock()
    mock_message.content = "Análisis simulado: Reposo y mucha agua."

    mock_response = {
        "messages": [mock_message],
        "safety_check_passed": True
    }

    # Patch a la instancia del grafo en main.py
    with patch("ai_engine.main.medical_graph.ainvoke", new_callable=AsyncMock) as mock_graph:
        mock_graph.return_value = mock_response
        
        response = client.post("/analyze", json=payload)
        
        # Validaciones de respuesta
        assert response.status_code == 200
        data = response.json()
        
        # Verificamos la estructura definida en tu AiResponse (Pydantic)
        assert data["analysis"] == "Análisis simulado: Reposo y mucha agua."
        assert "agent_in_charge" in data
        assert isinstance(data["recommended_actions"], list)

def test_agent_state_logic():
    """Verifica que el AgentState se puede instanciar correctamente."""
    from ai_engine.state import AgentState
    state: AgentState = {
        "messages": [],
        "patient_data": {"id": "PAC-001"},
        "resource_focus": "Triage",
        "safety_check_passed": False
    }
    assert state["patient_data"]["id"] == "PAC-001"