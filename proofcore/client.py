import requests
from typing import Optional, Dict, Any

API_BASE_URL = "https://api.proofcore.org/api/v0.1"


class ProofCoreClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')

    def seal(self, content: str, title: Optional[str] = None, agent_id: str = "Python Client") -> Dict[str, Any]:
        """Cryptographically seals text and queues it for TON Blockchain anchoring."""
        url = f"{self.base_url}/seal"
        payload = {"content": content, "agent_id": agent_id}
        if title:
            payload["title"] = title

        res = requests.post(url, json=payload, timeout=10)
        res.raise_for_status()
        return res.json()

    def get_proof(self, deal_id: str) -> Dict[str, Any]:
        """Retrieves the cryptographic manifest, Merkle path, and TON transaction status."""
        url = f"{self.base_url}/proof/{deal_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()


# Singleton-методы для быстрого импорта
_default_client = ProofCoreClient()


def seal(content: str, title: Optional[str] = None, agent_id: str = "Python Client") -> Dict[str, Any]:
    return _default_client.seal(content, title=title, agent_id=agent_id)


def get_proof(deal_id: str) -> Dict[str, Any]:
    return _default_client.get_proof(deal_id)