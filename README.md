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
  ## 🚀 Developer Integrations & SDK

  **Zero-Auth Cryptographic Notarization API for AI Agents & Autonomous Systems** The easiest way to interact with the TON Blockchain and seal your data is to use our official Python package.

## 📦 Installation

```bash
pip install proofcore
```
*(For specific AI frameworks, use `pip install proofcore[langchain]` or `pip install proofcore[crewai]`)*

---

## 🤖 1. LangChain Agent Integration

```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from proofcore.langchain import ProofCoreSealerTool

# 1. Init LLM and our official drop-in tool
llm = ChatOpenAI(model="gpt-4o")
tools = [ProofCoreSealerTool()]

# 2. Run the agent
agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# The agent will write the audit, call the tool, and give you the verification link!
response = agent.run("Write a short security audit for an ERC-20 token and notarize it.")
print(response)
```

---

## 🕵️ 2. CrewAI Integration

```python
from crewai import Agent, Task, Crew
from proofcore.crewai import ProofCoreCrewTool

notary_tool = ProofCoreCrewTool()

auditor = Agent(
    role="Smart Contract Security Auditor",
    goal="Audit contract code and cryptographically seal the final verdict on-chain.",
    backstory="You are an autonomous auditor specializing in Web3 security.",
    tools=[notary_tool]
)

# CrewAI agent will automatically use the tool to anchor the report
```

---

## 🐍 3. Pure Python (The Lazy Way)

No frameworks? No problem. ProofCore is a Zero-Auth API. You don't need API keys or registration.

```python
import proofcore
import time

# Step 1: Create a Proof
print("Sealing data...")
deal = proofcore.seal(
    content="Autonomous System Prediction: BTC > $150k before Q4 2026.",
    agent_id="python-script-v1",
    title="Market Forecast"
)

print(f"Deal ID: {deal['deal_id']}")
print(f"Badge: {deal['citation']}")

# Step 2: Check Blockchain Status
while True:
    status_data = proofcore.get_proof(deal['deal_id'])

    if status_data.get("status") == "anchored_onchain":
        print("✅ SUCCESS! Anchored to TON Blockchain.")
        print(f"Merkle Root: {status_data['merkle_root']}")
        print(f"TON TX Hash: {status_data['ton_tx_hash']}")
        break

    print("⏳ Still in queue. Checking again in 60 seconds...")
    time.sleep(60)
```

---

## 🛡️ How to Verify the Proof Offline?

ProofCore is built on the philosophy: *"Don't trust us. Verify it yourself."*

The `get_proof()` method returns all the data required for independent verification. You can easily reconstruct the Merkle Tree and compare the resulting root against the public TON Blockchain without ever trusting our servers.

Check out the full **OpenAPI Specification** and **Mathematical Algorithm** at [proofcore.org/openapi.json](https://proofcore.org/openapi.json).
