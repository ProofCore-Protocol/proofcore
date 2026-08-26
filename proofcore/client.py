import requests
from typing import Optional, Dict, Any

API_BASE_URL = "https://api.proofcore.org/api/v0.1"

class ProofCoreClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')

    def seal(self, content: str, title: Optional[str] = None, agent_id: str = "Python Client") -> Dict[str, Any]:
        url = f"{self.base_url}/seal"
        payload = {"content": content, "agent_id": agent_id}
        if title: payload["title"] = title
        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_proof(self, deal_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/proof/{deal_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def verify(self, deal_id: str, content: str) -> Dict[str, Any]:
        """Programmatically verify a sealed deal (Hash match + Ed25519 + TON Anchor)"""
        url = f"{self.base_url}/verify"
        res = requests.post(url, json={"deal_id": deal_id, "content": content}, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_pubkey(self) -> Dict[str, Any]:
        """Fetch the notary's Ed25519 public key"""
        url = f"{self.base_url}/pubkey"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

_default_client = ProofCoreClient()

def seal(content: str, title: Optional[str] = None, agent_id: str = "Python Client") -> Dict[str, Any]:
    return _default_client.seal(content, title=title, agent_id=agent_id)

def get_proof(deal_id: str) -> Dict[str, Any]:
    return _default_client.get_proof(deal_id)

def verify(deal_id: str, content: str) -> Dict[str, Any]:
    return _default_client.verify(deal_id, content)

def get_pubkey() -> Dict[str, Any]:
    return _default_client.get_pubkey()