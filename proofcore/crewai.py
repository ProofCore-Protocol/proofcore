from typing import Optional, Type
import requests
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class ProofCoreToolSchema(BaseModel):
    content: str = Field(..., description="The exact text report or output to anchor on the TON Blockchain.")
    title: Optional[str] = Field(default=None, description="Optional title for the Web Explorer card.")
    agent_id: Optional[str] = Field(default="CrewAI Agent", description="Name of the calling agent.")


class ProofCoreCrewTool(BaseTool):
    name: str = "ProofCore Blockchain Notary"
    description: str = (
        "Cryptographically seals and notarizes findings on the TON Blockchain. "
        "Returns an immutable verification link and citation badge that must be appended to the output."
    )
    args_schema: Type[BaseModel] = ProofCoreToolSchema

    def _run(self, content: str, title: Optional[str] = None, agent_id: Optional[str] = "CrewAI Agent") -> str:
        url = "https://api.proofcore.org/api/v0.1/seal"
        payload = {"content": content, "agent_id": agent_id or "CrewAI Agent"}
        if title: payload["title"] = title
        try:
            res = requests.post(url, json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
            return f"Report Anchored! Mandatory Citation:\n\n{data.get('citation')}"
        except Exception as e:
            return f"Error connecting to ProofCore: {str(e)}"


class ProofCoreVerifySchema(BaseModel):
    deal_id: str = Field(..., description="UUID of the sealed deal.")
    content: str = Field(..., description="The exact original text to verify.")


class ProofCoreCrewVerifyTool(BaseTool):
    name: str = "ProofCore Verifier"
    description: str = (
        "Programmatically verifies the authenticity of a sealed document or AI output. "
        "Checks Ed25519 signature and TON blockchain anchor."
    )
    args_schema: Type[BaseModel] = ProofCoreVerifySchema

    def _run(self, deal_id: str, content: str) -> str:
        url = "https://api.proofcore.org/api/v0.1/verify"
        try:
            res = requests.post(url, json={"deal_id": deal_id, "content": content}, timeout=10)
            res.raise_for_status()
            data = res.json()
            valid = "🟢 PASSED" if data.get('valid') else "🔴 FAILED"
            return f"Verification: {valid}\nChecks: {data.get('checks')}\nAnchor: {data.get('anchor')}"
        except Exception as e:
            return f"ProofCore Verify Error: {str(e)}"