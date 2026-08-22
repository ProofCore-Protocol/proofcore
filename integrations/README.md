# 🛡️ ProofCore Protocol

**The Cryptographic Notarization & Evidence Layer for the AI & M2M Economy**

[![TON Blockchain](https://img.shields.io/badge/Blockchain-TON%20Testnet%2FMainnet-0098EA?logo=ton&logoColor=white)](https://ton.org)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![OpenAPI 3.1](https://img.shields.io/badge/OpenAPI-3.1.0-6BA539?logo=openapi-initiative&logoColor=white)](https://proofcore.org/openapi.json)
[![llms.txt](https://img.shields.io/badge/llms.txt-Standard%20Compliant-purple)](https://proofcore.org/llms.txt)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> *"Don't trust ProofCore. Verify the proof yourself."*

[🌐 Website](https://proofcore.org) • [📖 OpenAPI Spec](https://proofcore.org/openapi.json) • [🤖 llms.txt](https://proofcore.org/llms.txt) • [📱 Telegram Bot](https://t.me/ProofCoreBot)

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

---

## 🚀 Quickstart: Developer Integrations

Welcome to the ProofCore Integrations. Here you will find drop-in tools for popular AI frameworks and pure Python examples to quickly seal and verify data.

### 🤖 1. LangChain Agent Integration

Just drop the `langchain_tool.py` file from the `integrations/` folder into your project and pass it to your agent. The agent will automatically seal its reports and append the required citation badge for the user.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from integrations.langchain_tool import ProofCoreSealerTool

# 1. Init LLM and our drop-in tool
llm = ChatOpenAI(model="gpt-4o")
tools = [ProofCoreSealerTool()]

# 2. Run the agent
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# The agent will write the audit, call the tool, and give you the verification link!
response = agent.run("Write a short security audit for an ERC-20 token and notarize it.")
print(response)
```

---

### 🐍 2. Pure Python (The Lazy Way)

No frameworks? No problem. ProofCore is a Zero-Auth API. You don't need API keys or registration.

**Step 1: Create a Proof (`POST`)**
Send the text you want to anchor. The API will hash it in-memory, queue it for batching, and return a `deal_id`.

```python
import requests

seal_url = "https://api.proofcore.org/api/v0.1/seal"
payload = {
    "content": "Autonomous System Prediction: BTC > $150k before Q4 2026.",
    "agent_id": "python-script-v1",
    "title": "Market Forecast"
}

response = requests.post(seal_url, json=payload).json()

print(f"Deal ID: {response['deal_id']}")
print(f"Badge to show user: {response['citation']}")
```

**Step 2: Check Blockchain Status (`GET`)**
Blockchains take a few minutes to confirm blocks. Use the `deal_id` to poll the status and get the full mathematical manifest (Merkle Path, TON Transaction Hash).

```python
import requests
import time

deal_id = response['deal_id']  # From Step 1
status_url = f"https://api.proofcore.org/api/v0.1/proof/{deal_id}"

while True:
    proof_data = requests.get(status_url).json()
    status = proof_data.get("status")
    
    if status == "anchored_onchain":
        print("✅ SUCCESS! Anchored to TON Blockchain.")
        print(f"Merkle Root: {proof_data['merkle_root']}")
        print(f"TON TX Hash: {proof_data['ton_tx_hash']}")
        print(f"Explorer URL: {proof_data['ton_explorer_url']}")
        break
        
    elif status == "cancelled":
        print("❌ Proof generation was cancelled.")
        break
        
    print("⏳ Still in queue. Checking again in 60 seconds...")
    time.sleep(60)
```

---

## 🛡️ How to Verify the Proof Offline?

ProofCore is built on the philosophy: *"Don't trust us. Verify it yourself."* 

The `GET` endpoint returns all the data required for independent verification. You can easily reconstruct the Merkle Tree and compare the resulting root against the public TON Blockchain without ever trusting our servers. 

Check out the full **OpenAPI Specification** and **Mathematical Algorithm** at [proofcore.org/openapi.json](https://proofcore.org/openapi.json).
