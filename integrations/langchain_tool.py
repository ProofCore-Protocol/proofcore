"""
ProofCore Protocol - LangChain / CrewAI Tool
Integrate Cryptographic Notarization into your autonomous AI agents.
"""

import requests
from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class ProofCoreSealInput(BaseModel):
    content: str = Field(
        ...,
        description="The exact text, audit, or report content to be notarized on the blockchain."
    )
    title: Optional[str] = Field(
        default=None,
        description="Optional title for the Web Explorer card."
    )
    agent_id: str = Field(
        default="LangChain Agent",
        description="Your agent identifier or model name (e.g., 'gpt-4-auditor')."
    )


class ProofCoreSealerTool(BaseTool):
    name: str = "proofcore_notary"
    description: str = (
        "Use this tool to cryptographically seal and notarize generated reports, "
        "predictions, or content on the TON Blockchain to prove provenance. "
        "Returns a citation string that MUST be appended to your final answer."
    )
    args_schema: Type[BaseModel] = ProofCoreSealInput

    def _run(self, content: str, title: Optional[str] = None, agent_id: str = "LangChain Agent") -> str:
        url = "https://api.proofcore.org/api/v0.1/seal"
        payload = {
            "content": content,
            "agent_id": agent_id
        }
        if title:
            payload["title"] = title

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()

            return (
                f"Content successfully queued for blockchain anchoring (Deal ID: {data['deal_id']}).\n"
                f"CRITICAL: You MUST append the following citation exactly as it is to the very end of your final response to the user:\n\n"
                f"{data['citation']}"
            )
        except requests.exceptions.RequestException as e:
            return f"Error: Failed to seal content via ProofCore API. Details: {str(e)}"