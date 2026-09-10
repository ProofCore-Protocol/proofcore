import json
import hashlib
import requests
import base64
from typing import Optional, Dict, Any, List

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

API_BASE_URL = "https://api.proofcore.org/api/v0.1"

PINNED_NOTARY_PUBKEY = "oH96uLjPgb+M9hKBNtFqbN9zzIDWdcs79dKbMXnVIcg="


def hash_merkle_leaf(deal_hash: str) -> str:
    """RFC 6962 Leaf Hash: SHA256(0x00 || data)"""
    return hashlib.sha256(b'\x00' + bytes.fromhex(deal_hash)).hexdigest()


def hash_merkle_node(left_hex: str, right_hex: str) -> str:
    """RFC 6962 Node Hash: SHA256(0x01 || left || right)"""
    return hashlib.sha256(b'\x01' + bytes.fromhex(left_hex) + bytes.fromhex(right_hex)).hexdigest()


def build_canonical_payload(assets_list: list, forensics: dict) -> bytes:
    """Creates a deterministic JSON representation of the deal."""
    clean_assets = [
        {"filename": a.get("filename", "unknown"),
         "hash": a.get("hash") or a.get("sha256_hash", ""),
         "size": a.get("size") or a.get("file_size", 0)}
        for a in assets_list
    ]
    clean_assets = sorted(clean_assets, key=lambda x: x["filename"])
    safe_forensics = {k: v for k, v in forensics.items() if k not in ("server_signature", "signer_pubkey")}

    payload = {"assets": clean_assets, "forensics": safe_forensics}
    return json.dumps(payload, separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode('utf-8')


class ProofCoreClient:
    def __init__(self, base_url: str = API_BASE_URL, pubkey: str = PINNED_NOTARY_PUBKEY):
        self.base_url = base_url.rstrip('/')
        self.pubkey = pubkey

    def seal(self, content: Optional[str] = None, title: Optional[str] = None, agent_id: str = "Python Client",
             payload: Optional[Dict[str, Any]] = None, webhook_url: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/seal"
        body: Dict[str, Any] = {"agent_id": agent_id}
        if title: body["title"] = title
        if webhook_url: body["webhook_url"] = webhook_url

        if payload:
            body["payload"] = payload
        elif content is not None:
            body["content"] = content
        else:
            raise ValueError("Either 'content' or 'payload' must be provided.")

        res = requests.post(url, json=body, timeout=10)
        res.raise_for_status()
        return res.json()

    def seal_inference(self, prompt: str, output: str, model_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        payload = {"mode": "inference", "prompt": prompt, "output": output, "model_id": model_id}
        return self.seal(title=title or f"AI Inference ({model_id})", agent_id=model_id, payload=payload)

    def seal_artifacts(self, files: List[Dict[str, str]], title: Optional[str] = None,
                       agent_id: str = "DevOps Client") -> Dict[str, Any]:
        payload = {"mode": "artifacts", "files": files}
        return self.seal(title=title or f"Artifacts Bundle ({len(files)} files)", agent_id=agent_id, payload=payload)

    def get_proof(self, deal_id: str) -> Dict[str, Any]:
        res = requests.get(f"{self.base_url}/proof/{deal_id}", timeout=10)
        res.raise_for_status()
        return res.json()

    def verify(self, deal_id: str, content: str) -> Dict[str, Any]:
        res = requests.post(f"{self.base_url}/verify", json={"deal_id": deal_id, "content": content}, timeout=10)
        res.raise_for_status()
        return res.json()

    def verify_local(self, proof_data: Dict[str, Any], content: Optional[str] = None,
                     inference_dict: Optional[Dict[str, str]] = None, files: Optional[List[Dict[str, Any]]] = None) -> \
    Dict[str, Any]:
        """
        100% Offline Cryptographic Verification.
        Validates the Ed25519 signature and reconstructs the RFC 6962 Merkle Root locally.
        """
        expected_root = proof_data.get("merkle_root") or proof_data.get("onchain", {}).get("merkle_root")
        if not expected_root or expected_root == "pending":
            return {"valid": False, "error": "No finalized Merkle Root."}

        # 1. Hashing the provided assets
        assets_list = []
        if content:
            assets_list.append({"filename": "payload.txt", "hash": hashlib.sha256(content.encode('utf-8')).hexdigest(),
                                "size": len(content.encode('utf-8'))})
        elif inference_dict:
            canon_bytes = json.dumps(inference_dict, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
            assets_list.append({"filename": "inference.json", "hash": hashlib.sha256(canon_bytes).hexdigest(),
                                "size": len(canon_bytes)})
        elif files:
            for f in files:
                fbytes = f["content"].encode('utf-8')
                assets_list.append(
                    {"filename": f["filename"], "hash": hashlib.sha256(fbytes).hexdigest(), "size": len(fbytes)})

        # 2. Canonical Deal Hash
        forensics = proof_data.get("forensics") or proof_data.get("meta_json", {})
        canonical_bytes = build_canonical_payload(assets_list, forensics)
        deal_hash = hashlib.sha256(canonical_bytes).hexdigest()

        # 3. Signature Verification
        sig_valid = False
        server_sig = forensics.get("server_signature")
        if HAS_CRYPTO and server_sig:
            try:
                pk = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(self.pubkey))
                pk.verify(base64.b64decode(server_sig), deal_hash.encode('utf-8'))
                sig_valid = True
            except Exception:
                sig_valid = False

        # 4. Merkle Tree Traversal (RFC 6962)
        current_hash = hash_merkle_leaf(deal_hash)
        merkle_path = proof_data.get("merkle_path") or proof_data.get("onchain", {}).get("merkle_path", [])

        for node in merkle_path:
            if node.get("direction") == "left":
                current_hash = hash_merkle_node(node["hash"], current_hash)
            else:
                current_hash = hash_merkle_node(current_hash, node["hash"])

        root_match = (current_hash == expected_root)

        return {
            "valid": root_match and (not HAS_CRYPTO or sig_valid),
            "checks": {
                "merkle_path_valid": root_match,
                "signature_valid": sig_valid,
                "cryptography_installed": HAS_CRYPTO
            },
            "calculated_merkle_root": current_hash,
            "expected_merkle_root": expected_root,
            "ton_tx_hash": proof_data.get("ton_tx_hash") or proof_data.get("onchain", {}).get("ton_tx_hash")
        }

    def get_pubkey(self) -> Dict[str, Any]:
        """Fetch the notary's Ed25519 public key."""
        res = requests.get(f"{self.base_url}/pubkey", timeout=10)
        res.raise_for_status()
        return res.json()


_default_client = ProofCoreClient()


def seal(content=None, title=None, agent_id="Python Client", payload=None,
         webhook_url=None): return _default_client.seal(content, title, agent_id, payload, webhook_url)


def seal_inference(prompt: str, output: str, model_id: str, title=None): return _default_client.seal_inference(prompt,
                                                                                                               output,
                                                                                                               model_id,
                                                                                                               title)


def seal_artifacts(files: list, title=None, agent_id="DevOps"): return _default_client.seal_artifacts(files, title,
                                                                                                      agent_id)


def get_proof(deal_id: str): return _default_client.get_proof(deal_id)


def verify(deal_id: str, content: str): return _default_client.verify(deal_id, content)


def verify_local(proof_data: dict, content=None, inference_dict=None, files=None): return _default_client.verify_local(
    proof_data, content, inference_dict, files)


def get_pubkey() -> Dict[str, Any]: return _default_client.get_pubkey()