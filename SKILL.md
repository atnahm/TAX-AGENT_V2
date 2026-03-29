---
name: Enterprise Tax Agent
description: Deterministic graph-based tax compliance engine for Indian businesses (ITR, GST) powered by hybrid Bedrock + Local AI.
---

# Enterprise Tax Agent — Skills & Capabilities

## Agent Overview

The Enterprise Tax Agent is a deterministic, graph-based computation engine built with LangGraph. It autonomously handles Indian tax compliance (ITR-4, GSTR-3B) through a 7-node workflow pipeline.

---

## Core Skills

### 1. ML-Powered Data Ingestion
- **Node**: `ML_Ingestion`
- **Model**: EasyOCR (local) + Claude 3.5 Sonnet (Bedrock)
- **Capability**: Extracts financial data from raw text, images (invoices, receipts), and PDFs. Uses local OCR for text extraction and Bedrock LLM for structured parsing into normalized ledger entries.
- **Supported Formats**: `.png`, `.jpg`, `.jpeg`, `.tiff`, and raw text

### 2. Financial Data Normalization
- **Node**: `Normalizer`
- **Model**: Rule-based (no LLM)
- **Capability**: Normalizes extracted data into a consistent schema with categorized entries (Revenue, Expense, Liability), standard date formats (YYYY-MM-DD), and GST identifiers.

### 3. Web Intelligence & GSTIN Verification
- **Node**: `Web_Intelligence`
- **Model**: TinyFish REST API (AgentQL)
- **Capability**: Live verification of GSTIN status from the GST portal (services.gst.gov.in). Extracts taxpayer status, trade name, and registration date in real-time.

### 4. Statutory Rules Retrieval (RAG)
- **Node**: `Rules_Retrieval`
- **Model**: HuggingFace `all-MiniLM-L6-v2` (local embeddings) + Qdrant
- **Capability**: Semantic search over Indian tax statutes (Income Tax Act, GST Act, CBDT circulars). Retrieves the top-5 most relevant rules for the taxpayer's filing framework (e.g., ITR-4, 44AD).

### 5. Deterministic Tax Computation
- **Node**: `Computation`
- **Model**: Rule-based (no LLM)
- **Capability**: Calculates taxable income, GST liability (CGST/SGST/IGST), Input Tax Credit (ITC), presumptive income under Section 44AD, and net tax payable. Applies exact statutory rates — no LLM hallucination risk.

### 6. Financial Analysis & Risk Assessment
- **Node**: `Financial_Analyst`
- **Model**: Claude 3.5 Sonnet (Bedrock)
- **Capability**: Generates qualitative insights including net margin analysis, presumptive vs actual income comparison, tax risk identification, and GST ITC optimization recommendations.

### 7. Government-Ready Artifact Generation
- **Node**: `Artifact_Generator`
- **Model**: Rule-based (no LLM)
- **Capability**: Produces GSTR-3B JSON payload (exact schema for government portal submission), ITR-4 formatted output, and a standard Balance Sheet with assets and liabilities.

---

## Architecture Skills

### Human-in-the-Loop (HITL) Approval
- The workflow pauses after `Financial_Analyst` and waits for `human_approval_status = "approved"` before generating final tax artifacts. This ensures compliance officers can review before submission.

### LangGraph Checkpointing
- Full workflow state is persisted to PostgreSQL via `PostgresSaver`. Supports resume-from-failure, audit trails, and multi-session workflows.

### Dual Vector Database
- **Qdrant**: Semantic RAG for statutory tax rules (384-dim, MiniLM embeddings)
- **Weaviate**: Multi-modal storage for unstructured documents and images (CLIP vectorizer)

### MCP Protocol Support
- FastAPI endpoint with Model Context Protocol compliance for integration with external agent orchestrators.

---

## Compliance & Security

| Standard | Implementation |
| :--- | :--- |
| **SOC 2** | All data encrypted in transit (TLS). No PII sent to external APIs without approval. |
| **DPDP Act 2023** | Financial data processed locally where possible (OCR, embeddings). Bedrock data stays in AWS region. |
| **Audit Trail** | Every graph execution is checkpointed with full state history in PostgreSQL. |
