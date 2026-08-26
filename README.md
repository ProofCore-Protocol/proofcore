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
from proofcore.langchain import ProofCoreSealerTool, ProofCoreVerifierTool

llm = ChatOpenAI(model="gpt-4o")
# Tools for both sealing output and verifying other agents' claims
tools = [ProofCoreSealerTool(), ProofCoreVerifierTool()]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
response = agent.run("Verify the authenticity of report for deal '4eea9784-2371-4505-8f2f-0b4c5a15a9ec' with content 'Vault audit...'")
print(response)
```

---

## 🕵️ 2. CrewAI Integration

```python
from crewai import Agent
from proofcore.crewai import ProofCoreCrewTool, ProofCoreCrewVerifyTool

# Drop-in tools for CrewAI pipelines
auditor = Agent(
    role="Smart Contract Auditor",
    goal="Audit code, seal proofs on TON, and verify counterparty claims.",
    tools=[ProofCoreCrewTool(), ProofCoreCrewVerifyTool()]
)
```

---

## 🐍 3. Pure Python (The Lazy Way)

No frameworks? ProofCore is a Zero-Auth API. No API keys or registration required.

```python
import proofcore

# Step 1: Seal content & get instant Ed25519 attestation
deal = proofcore.seal(
    content="Autonomous System Prediction: BTC > $150k before Q4 2026.",
    agent_id="python-script-v1",
    title="Market Forecast"
)
print(f"Deal ID: {deal['deal_id']}")
print(f"Badge: {deal['citation']}")

# Step 2: Programmatic M2M Verification (Agent-to-Agent)
result = proofcore.verify(
    deal_id=deal['deal_id'],
    content="Autonomous System Prediction: BTC > $150k before Q4 2026."
)
print(f"Is Authentic: {result['valid']}")
print(f"Ed25519 Signature Valid: {result['checks']['signature_valid']}")
print(f"TON Blockchain Status: {result['anchor']['status']}")
```

---

## 🎨 4. Hugging Face Spaces & Gradio (UI Component)

Building an AI demo on Hugging Face? Add our drop-in UI component to instantly give your space a Web3 verification badge. 

First, add `proofcore[ui]` to your `requirements.txt`. Then use the `NotarizedOutput` class:

```python

import gradio as gr
from proofcore.gradio import NotarizedOutput

def generate_text(prompt):
    return f"AI generated response for: {prompt}"

with gr.Blocks() as demo:
    gr.Markdown("# My Secure AI Generator")
    inp = gr.Textbox(label="Prompt")
    
    # Drop-in replacement for gr.Textbox
    out = NotarizedOutput(label="AI Output (Anchored on TON)")
    
    btn = gr.Button("Generate & Notarize")
    
    # 1. Generate text -> 2. Process and Seal
    btn.click(fn=generate_text, inputs=inp, outputs=out.textbox).then(
        fn=out.process, inputs=out.textbox, outputs=out.outputs
    )

demo.launch()
```

---

## 🛡️ How to Verify the Proof Offline?

ProofCore is built on the philosophy: *"Don't trust us. Verify it yourself."*

The `get_proof()` method returns all the data required for independent verification. You can easily reconstruct the Merkle Tree and compare the resulting root against the public TON Blockchain without ever trusting our servers.

Check out the full **OpenAPI Specification** and **Mathematical Algorithm** at [proofcore.org/openapi.json](https://proofcore.org/openapi.json).
