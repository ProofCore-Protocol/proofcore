import json
import hashlib
import requests
from typing import Optional, Dict, Any, List, Union

API_BASE_URL = "https://api.proofcore.org/api/v0.1"


def sha256_node(left: str, right: str) -> str:
    """RFC 6962 Domain Separation Hashing (0x01 prefix)"""
    return hashlib.sha256(b"\x01" + (left + right).encode("utf-8")).hexdigest()


class ProofCoreClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')

    def seal(
        self,
        content: Optional[str] = None,
        title: Optional[str] = None,
        agent_id: str = "Python Client",
        payload: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cryptographically seal text, code, or arbitrary JSON-envelope string.
        """
        url = f"{self.base_url}/seal"
        body: Dict[str, Any] = {"agent_id": agent_id}
        if title:
            body["title"] = title
        if webhook_url:
            body["webhook_url"] = webhook_url

        if payload:
            body["payload"] = payload
        elif content is not None:
            body["content"] = content
        else:
            raise ValueError("Either 'content' or 'payload' must be provided.")

        res = requests.post(url, json=body, timeout=10)
        res.raise_for_status()
        return res.json()

    def seal_inference(
        self,
        prompt: str,
        output: str,
        model_id: str,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Atomic AI Inference Provenance (Eliminates JSON escaping bugs).
        """
        payload = {
            "mode": "inference",
            "prompt": prompt,
            "output": output,
            "model_id": model_id
        }
        clean_title = title or f"AI Inference ({model_id})"
        return self.seal(title=clean_title, agent_id=model_id, payload=payload)

    def seal_artifacts(
        self,
        files: List[Dict[str, str]],
        title: Optional[str] = None,
        agent_id: str = "DevOps Client"
    ) -> Dict[str, Any]:
        """
        Seal multiple files/codebase artifacts into a single Merkle batch.
        files format: [{"filename": "main.py", "content": "print('hello')"}]
        """
        payload = {
            "mode": "artifacts",
            "files": files
        }
        clean_title = title or f"Artifacts Bundle ({len(files)} files)"
        return self.seal(title=clean_title, agent_id=agent_id, payload=payload)

    def get_proof(self, deal_id: str) -> Dict[str, Any]:
        """Fetch cryptographic manifest and TON on-chain confirmation."""
        url = f"{self.base_url}/proof/{deal_id}"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()

    def verify(self, deal_id: str, content: str) -> Dict[str, Any]:
        """
        M2M API Verification via ProofCore Notary Gateway.
        """
        url = f"{self.base_url}/verify"
        res = requests.post(url, json={"deal_id": deal_id, "content": content}, timeout=10)
        res.raise_for_status()
        return res.json()

    def verify_local(self, content: str, proof_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        100% Offline Cryptographic Verification (Zero-Trust, Zero-Network).
        Reconstructs SHA-256 and Merkle Path locally against expected on-chain root.
        """
        expected_root = proof_data.get("merkle_root") or proof_data.get("onchain", {}).get("merkle_root")
        if not expected_root or expected_root == "pending":
            return {
                "valid": False,
                "error": "Proof does not contain finalized on-chain Merkle Root."
            }

        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        
        assets = proof_data.get("assets", [])
        expected_hashes = [a.get("sha256_hash") for a in assets]
        
        hash_match = content_hash in expected_hashes
        if not hash_match:
            return {
                "valid": False,
                "error": "Local content SHA-256 does not match any asset in manifest.",
                "calculated_hash": content_hash,
                "expected_hashes": expected_hashes
            }

        current_hash = content_hash
        merkle_path = proof_data.get("merkle_path") or proof_data.get("onchain", {}).get("merkle_path", [])
        
        for node in merkle_path:
            sibling = node["hash"]
            if node.get("direction") == "left":
                current_hash = sha256_node(sibling, current_hash)
            else:
                current_hash = sha256_node(current_hash, sibling)

        root_match = (current_hash == expected_root)

        return {
            "valid": root_match,
            "checks": {
                "hash_match": True,
                "merkle_path_valid": root_match
            },
            "calculated_merkle_root": current_hash,
            "expected_merkle_root": expected_root,
            "ton_tx_hash": proof_data.get("ton_tx_hash") or proof_data.get("onchain", {}).get("ton_tx_hash")
        }

    def get_pubkey(self) -> Dict[str, Any]:
        """Fetch the notary's Ed25519 public key."""
        url = f"{self.base_url}/pubkey"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()


_default_client = ProofCoreClient()

def seal(
    content: Optional[str] = None,
    title: Optional[str] = None,
    agent_id: str = "Python Client",
    payload: Optional[Dict[str, Any]] = None,
    webhook_url: Optional[str] = None
) -> Dict[str, Any]:
    return _default_client.seal(content=content, title=title, agent_id=agent_id, payload=payload, webhook_url=webhook_url)

def seal_inference(prompt: str, output: str, model_id: str, title: Optional[str] = None) -> Dict[str, Any]:
    return _default_client.seal_inference(prompt, output, model_id, title=title)

def seal_artifacts(files: List[Dict[str, str]], title: Optional[str] = None, agent_id: str = "DevOps Client") -> Dict[str, Any]:
    return _default_client.seal_artifacts(files, title=title, agent_id=agent_id)

def get_proof(deal_id: str) -> Dict[str, Any]:
    return _default_client.get_proof(deal_id)

def verify(deal_id: str, content: str) -> Dict[str, Any]:
    return _default_client.verify(deal_id, content)

def verify_local(content: str, proof_data: Dict[str, Any]) -> Dict[str, Any]:
    return _default_client.verify_local(content, proof_data)

def get_pubkey() -> Dict[str, Any]:
    return _default_client.get_pubkey()
