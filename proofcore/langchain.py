from typing import Optional, Type
import requests
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class ProofCoreSealInput(BaseModel):
    content: str = Field(..., description="The exact text, audit, or report to be notarized on the TON Blockchain.")
    title: Optional[str] = Field(default=None, description="Optional title for the Web Explorer card.")
    agent_id: str = Field(default="LangChain Agent", description="Agent identifier or model name.")


class ProofCoreSealerTool(BaseTool):
    name: str = "proofcore_notary"
    description: str = (
        "Cryptographically seals and notarizes text outputs on the TON Blockchain. "
        "Returns a verification badge that MUST be appended to your final answer."
    )
    args_schema: Type[BaseModel] = ProofCoreSealInput

    def _run(self, content: str, title: Optional[str] = None, agent_id: str = "LangChain Agent") -> str:
        url = "https://api.proofcore.org/api/v0.1/seal"
        payload = {"content": content, "agent_id": agent_id}
        if title: payload["title"] = title
        try:
            res = requests.post(url, json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
            return f"Anchored! You MUST append this exact citation to the end of your answer:\n\n{data['citation']}"
        except Exception as e:
            return f"ProofCore Error: {str(e)}"


class ProofCoreVerifyInput(BaseModel):
    deal_id: str = Field(..., description="UUID of the sealed deal.")
    content: str = Field(..., description="The exact original text to verify.")


class ProofCoreVerifierTool(BaseTool):
    name: str = "proofcore_verifier"
    description: str = (
        "Programmatically verifies the authenticity of a sealed document or AI output. "
        "Checks Ed25519 signature and TON blockchain anchor."
    )
    args_schema: Type[BaseModel] = ProofCoreVerifyInput

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