# 🏛 ProofCore Protocol

> **Trust you can't delete.**  
> A trustless, cryptographic Proof-of-Existence (PoE) engine built on **The Open Network (TON)**. Turn ephemeral Telegram messages, E-Mails, agreements, and files into legally admissible, unalterable digital evidence.

[![TON Blockchain](https://img.shields.io/badge/Blockchain-TON-blue.svg)](https://ton.org)
[![Smart Contract](https://img.shields.io/badge/Tact-ProofRegistry-00f298.svg)](https://tact-lang.org)
[![Compliance](https://img.shields.io/badge/Legal-FRE%20902%20%7C%20eIDAS-00d2ff.svg)](https://proofcore.org/docs.html)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 💡 The Problem

In modern communications (Telegram, E-Mails, Messengers), agreements can be unilaterally erased using **"Delete for Everyone"**, or altered via DOM tools and Photoshop. Screenshots carry zero mathematical weight in court or formal arbitration.

If a partner deletes a chat after a P2P crypto swap, freelance milestone, or OTC agreement, you are left with **zero admissible proof**.

---

## 🛡 The Solution: ProofCore

**ProofCore** anchors digital fingerprints (SHA-256 hashes) directly into the TON Blockchain. Even if a scammer deletes the chat, **they cannot delete data anchored into a decentralized blockchain.**

### Key Features
* 💬 **Telegram Deep Context:** Extracts sender ID, forward origins, avatar SHA-256 hash, and raw JSON message payloads via `@ProofCoreBot`.
* 📧 **DKIM-Authenticated E-Mails:** Cloudflare Workers extract `.eml` raw payloads and verify DKIM cryptographic signatures against Google/Microsoft DNS.
* 📁 **Immutable Media & Files:** Computes SHA-256 checksums for PDFs, code, screenshots, and media up to 50MB.
* 🌳 **Merkle Tree Batching:** Groups thousands of asset hashes into a binary Merkle Tree and writes a single 64-character Merkle Root to TON via Tact Smart Contract (`ProofRegistry.tact`), keeping gas fees near zero.
* 📦 **Offline Evidence Package (ZIP):** Generates a self-authenticating ZIP package containing original raw files, JSON manifests, FRE 902 PDF certificates, and 100% offline HTML/Python verifiers.

---

## 🏛 Legal Compliance & Standards

ProofCore certificates are designed to meet international electronic evidence standards:
* **🇺🇸 US Federal Rules of Evidence (FRE 902):** Rule 902(14) governs self-authenticating electronic data authenticated by a process of digital identification (cryptographic hash value).
* **🇪🇺 EU eIDAS Regulation (910/2014):** Article 41(1) recognizes electronic time stamps as legally admissible evidence in legal proceedings across European Union member states.

---

## 📦 Evidence Package Structure (ZIP)

When an asset is sealed, ProofCore outputs a standalone, self-authenticating archive:

```
proof_package.zip
├── 📁 1_ORIGINAL_ASSET/        ← Unmodified raw file or payload
├── 📁 2_PROOF_DATA/           ← proof.json manifest + forensic_metadata.json
├── 📁 3_VERIFIERS/            ← verify.py & verify.html (100% Offline Verifiers)
├── 📁 4_LEGAL_CERTIFICATE/    <-- FRE 902 PDF Certificate with verification QR
└── 📁 5_README/               ← Verification instructions
```

---

## 🔍 Independent Offline Verification

You do **not** need ProofCore servers to verify your evidence. You can verify it offline in 2 seconds:

### Method A: Browser Verification
Open `3_VERIFIERS/verify.html` in any browser, select `proof.json` and your original file. The local JavaScript engine recalculates the SHA-256 hash and traverses the Merkle Tree to verify against TON Blockchain.

### Method B: Python Terminal
```bash
python3 3_VERIFIERS/verify.py
```

---

## ⚙️ Architecture & Smart Contracts

```
[ Telegram / E-Mail / Upload ] 
            │
            ▼
[ SHA-256 Fingerprint + Forensic Metadata ]
            │
            ▼
[ Merkle Tree Batching Engine ]
            │
            ▼
[ TON Blockchain Smart Contract ] ──► ProofRegistry.tact
```

The smart contract is written in **Tact** for TON Blockchain. It emits `BatchAnchoredEvent` containing `batch_id` and `merkle_root`.

---

## 🌐 Ecosystem Links

* **Website:** [https://proofcore.org](https://proofcore.org)
* **Documentation:** [https://docs.proofcore.org](https://docs.proofcore.org)
* **Telegram Bot:** [@ProofCoreBot](https://t.me/proofcore_bot)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
