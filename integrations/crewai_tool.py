"""
ProofCore Protocol - CrewAI Custom Tool
Empowers autonomous multi-agent squads to certify findings on TON Blockchain.
"""

import requests
from typing import Type, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ProofCoreSealSchema(BaseModel):
    """Input schema for ProofCore sealing tool."""
    content: str = Field(..., description="The exact report or output text to be notarized on the blockchain.")
    title: Optional[str] = Field(default="CrewAI Notarized Report", description="Title for the Web Explorer card.")
    agent_id: Optional[str] = Field(default="CrewAI Agent", description="Name of the calling agent/role.")

class ProofCoreCrewTool(BaseTool):
    name: str = "ProofCore Blockchain Notary"
    description: str = (
        "Cryptographically seals and notarizes agent findings on the TON Blockchain. "
        "Returns an immutable verification URL and citation badge that must be appended to the final response."
    )
    args_schema: Type[BaseModel] = ProofCoreSealSchema

    def _run(self, content: str, title: str = "CrewAI Notarized Report", agent_id: str = "CrewAI Agent") -> str:
        url = "https://api.proofcore.org/api/v0.1/seal"
        payload = {
            "content": content,
            "title": title,
            "agent_id": agent_id
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return f"Report Anchored! Mandatory Citation to append:\n\n{data['citation']}"
        except Exception as e:
            return f"Failed to seal via ProofCore: {str(e)}"