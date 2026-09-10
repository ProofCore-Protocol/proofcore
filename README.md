# 🛡️ ProofCore Python SDK

[![PyPI Version](https://img.shields.io/pypi/v/proofcore.svg?color=00d2ff)](https://pypi.org/project/proofcore/)
[![Python Versions](https://img.shields.io/pypi/pyversions/proofcore.svg)](https://pypi.org/project/proofcore/)
[![License: MIT](https://img.shields.io/badge/License-MIT-00f298.svg)](https://opensource.org/licenses/MIT)
[![TON Blockchain](https://img.shields.io/badge/TON-Mainnet-blue.svg)](https://ton.org)
[![Strict Zero-Storage](https://img.shields.io/badge/Privacy-Strict%20Zero--Storage-brightgreen.svg)](#strict-zero-storage-architecture)

> **Decentralized Cryptographic Evidence Layer for Autonomous AI Agents, Developers, and DevOps.**  
> Anchor text, model inferences, and software supply chains to The Open Network (TON) Blockchain via Merkle trees.

---

## ⚡ The Problem & The Solution

In the era of autonomous AI agents, digital trust is broken:
* **Denial of Generation:** AI outputs can be secretly altered or deleted.
* **Fabricated Hallucinations:** Screenshots of LLM predictions and contract audits can easily be faked.
* **Centralized Vulnerability:** Traditional notarization APIs require manual API keys, subscriptions, and trusting a single server's timestamp.

**ProofCore** is a high-throughput, **Zero-Auth M2M Protocol** that cryptographically commits digital outputs into **The Open Network (TON) Blockchain** via Merkle Tree batching. It delivers mathematical **Proof-of-Existence (PoE)** and verifiable provenance without storing private user keys.

```text
┌────────────────┐     POST /api/v0.1/seal     ┌────────────────┐
│ Autonomous AI  │ ──────────────────────────> │   ProofCore    │
│ Agent / LLM    │ <────────────────────────── │   API Gateway  │
└────────────────┘    Instant Citation Badge   └───────┬────────┘
                                                       │
                                            SHA-256 Merkle Batching
                                                       │
                                                       ▼
                                            ┌────────────────────┐
                                            │   TON Blockchain   │
                                            │ (Immutable Anchor) │
                                            └────────────────────┘
```

## ⚡ Core Axiom

> *“Don't trust ProofCore. Verify the mathematical proof yourself.”*

ProofCore separates cryptographic trust from vendor dependency:
- **Instant Attestation (<10ms):** Server signs SHA-256 payload digests with an Ed25519 notary key.
- **Decentralized Anchor (~30s):** Aggregates thousands of hashes into a single RFC 6962 Merkle root anchored in a public TON block.
- **Strict Zero-Storage:** Raw inputs and prompts are processed in RAM and discarded. Hashes are anchored; your data never touches our disk.
- **100% Offline Verifiability:** Verify proofs locally without internet, API keys, or ProofCore servers.

---

## 🚀 Installation

```bash
pip install --upgrade proofcore
```

*Optional agent ecosystem dependencies:*
```bash
pip install proofcore[langchain]  # LangChain tools
pip install proofcore[crewai]     # CrewAI tools
pip install proofcore[gradio]     # Gradio UI components
```

---

## 🛠️ Quickstart

### 1. Atomic AI Inference Sealing (Eliminates JSON Escaping Bugs)
Best for LLM pipelines and autonomous agents. Prevents prompt/output tampering:

```python
import proofcore

proof = proofcore.seal_inference(
    prompt="Audit this Solidity contract for reentrancy vulnerabilities...",
    output="Audit complete. Severity: 0 High, 0 Critical. Safe for mainnet deployment.",
    model_id="claude-3-5-sonnet-20241022",
    title="Vault.sol Security Audit"
)

print(f"Deal ID: {proof['deal_id']}")
print(f"Explorer URL: {proof['verification_url']}")
print(f"Verification Badge: {proof['badge_markdown']}")
```

### 2. General Text / Raw JSON Sealing (WYSIWYWH)
Accepts plain text, markdown, source code, or arbitrary stringified JSON envelopes (e.g. precomputed hashes of terabyte datasets):

```python
import proofcore

# Plain text or code
proof = proofcore.seal(
    content="Bilateral Agreement Terms: Party A agrees to pay Party B $5,000 on delivery.",
    title="Freelance P2P Milestone"
)

# Or stringified JSON envelope containing offline hashes
proof_json = proofcore.seal(
    content='{"dataset": "imagenet-subset.tar.gz", "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}',
    title="ML Training Dataset Checksum"
)
```

### 3. Multi-File Artifacts & SBOM Batching
Seal multiple files or codebases into a single cryptographic batch:

```python
import proofcore

files = [
    {"filename": "main.py", "content": "print('hello world')"},
    {"filename": "requirements.txt", "content": "fastapi==0.115.0\npydantic==2.9.2"},
    {"filename": "sbom.json", "content": '{"spdxVersion": "SPDX-2.3", "packages": []}'}
]

proof = proofcore.seal_artifacts(
    files=files,
    title="Release v1.0.0 Artifacts"
)
```

---

## 🔍 Independent Verification

ProofCore gives you two independent verification workflows:

### A. 100% Offline Local Verification (The Killer Feature)
Mathematically verify that a string matches a proof manifest locally. **Zero network calls, zero vendor dependency:**

```python
import proofcore

# Fetch the proof manifest once (or load from local proof.json)
proof_data = proofcore.get_proof("b4ed4c20-7f2a-4c8d-9a81-123456789abc")

# Verify offline!
result = proofcore.verify_local(
    content="Audit complete. Severity: 0 High, 0 Critical. Safe for mainnet deployment.",
    proof_data=proof_data
)

if result["valid"]:
    print(f"✅ Cryptographically Proven! Merkle Root: {result['calculated_merkle_root']}")
    print(f"TON Transaction: {result['ton_tx_hash']}")
else:
    print(f"❌ Verification Failed: {result.get('error')}")
```

### B. Remote M2M Verification (Gateway Check)
Verify content directly against the ProofCore notary oracle:

```python
import proofcore

result = proofcore.verify(
    deal_id="b4ed4c20-7f2a-4c8d-9a81-123456789abc",
    content="Audit complete. Severity: 0 High, 0 Critical. Safe for mainnet deployment."
)

print(result["valid"])  # True / False
print(result["checks"]["signature_valid"])  # Ed25519 Notary Signature
```

---

## 🤖 Model Context Protocol (MCP) Integration

ProofCore hosts a public, zero-auth Model Context Protocol server.

### Connect to Cursor / Windsurf
Add to `.cursor/mcp.json` or Windsurf settings:

```json
{
  "mcpServers": {
    "proofcore": {
      "url": "https://mcp.proofcore.org"
    }
  }
}
```

### Connect to Claude Desktop / Claude Code
```bash
claude mcp add proofcore https://mcp.proofcore.org
```

---

## 🧩 Agent Framework Tools

### LangChain Integration
```python
from proofcore.langchain import ProofCoreSealerTool, ProofCoreVerifierTool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI

tools = [ProofCoreSealerTool(), ProofCoreVerifierTool()]
agent = initialize_agent(tools, ChatOpenAI(model="gpt-4o"), agent=AgentType.OPENAI_FUNCTIONS)

agent.run("Review this smart contract and cryptographically seal your findings.")
```

### CrewAI Integration
```python
from crewai import Agent, Task, Crew
from proofcore.crewai import ProofCoreCrewTool

auditor = Agent(
    role="Smart Contract Auditor",
    goal="Identify security vulnerabilities and anchor results to TON Blockchain",
    tools=[ProofCoreCrewTool()],
    verbose=True
)
```

---

## 🔒 Strict Zero-Storage Architecture

ProofCore operates on a strict **Zero-Knowledge, Zero-Storage** principle for developer APIs:
1. Payloads sent to `/seal` are hashed in RAM via `SHA-256`.
2. Raw payloads are **never written to disk**.
3. The database only records: `sha256_hash`, `merkle_root`, `deal_id`, timestamps, and the Ed25519 notary signature.
4. **GDPR & Enterprise Safe:** We physically cannot leak your proprietary source code, secrets, or prompts because we never retain them.

---

## ⚖️ Evidentiary & Regulatory Alignment

ProofCore Evidence Packages are architected to satisfy digital evidence standards across global jurisdictions:
- **US FRE 902(13) & 902(14):** Self-authenticating electronic records verified by a process or system producing an accurate result (hash values).
- **EU AI Act (Article 50):** Machine-readable marking and provenance of AI-generated synthetic content.
- **EU eIDAS 2.0 (Reg 2024/1183):** Electronic ledgers and timestamps legally recognized across member states.
- **SLSA Level 3 & SBOM:** Cryptographic provenance for CI/CD build pipelines using GitHub Actions OIDC tokens.
- **UK Civil Evidence Act 1995:** Section 8/9 continuous Chain of Custody validation.

---

## 🌐 Ecosystem Links

- **Interactive Sandbox & Tamper Simulator:** [demo.proofcore.org](https://demo.proofcore.org)
- **Protocol Documentation:** [docs.proofcore.org](https://docs.proofcore.org)
- **Official Website:** [proofcore.org](https://proofcore.org)
- **MCP Server Endpoint:** `https://mcp.proofcore.org`
- **GitHub Action:** [ProofCore-Protocol/proofcore-action@v1](https://github.com/ProofCore-Protocol/proofcore-action)
- **Telegram Bot:** [@ProofCoreBot](https://t.me/ProofCoreBot)

---

## 📄 License

MIT License © 2026 ProofCore Protocol Core Contributors.
