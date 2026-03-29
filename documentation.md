# Enterprise Tax Agent Documentation

The **Enterprise Tax Agent** is an autonomous, graph-based computation engine designed for professional Indian tax compliance (Income Tax & GST). It combines high-accuracy local OCR, generative AI reasoning via Amazon Bedrock, and deterministic financial logic to provide an end-to-end automation suite for accountants, CAs, and businesses.

---

## 🏗️ Architecture Overiew

The agent is built on a **LangGraph** orchestration layer, which ensures that complex tax workflows are handled deterministically rather than relying solely on probabilistic AI outputs.

### 📐 System Flow
The workflow follows a rigorous 7-stage process:

1.  **ML-Powered Data Ingestion**: Extracts text from financial documents (PDFs, Images, Excel) using local **EasyOCR** and structures it into a standard ledger using **Claude 3.5 Sonnet** (via Amazon Bedrock).
2.  **Data Normalization**: Merges unstructured OCR data with structured imports (e.g., Tally Exports, CSVs) using a unified schema.
3.  **Statutory Rules Retrieval (RAG)**: Queries a **Qdrant Vector Database** to fetch the exact section-wise tax rules (e.g., ITR-4, 44AD presumptive slabs) applicable to the specific business framework.
4.  **Web Intelligence (Taxpayer Verification)**: Connects to the **TinyFish API** to perform live verification of GSTINs and retrieve real-time regulatory updates from the GST portal.
5.  **Deterministic Computation**: Executes Python-based financial logic (using `pandas`) to calculate tax liabilities, GST set-offs, and presumptive income. **Numerics are handled outside the LLM to ensure 100% accuracy.**
6.  **Financial Analysis**: Uses **Amazon Bedrock** to perform a qualitative audit, identifying tax risks, margin trends, and optimization recommendations.
7.  **Artifact Generation**: Automatically maps results into government-ready JSON payloads (e.g., GSTR-3B) and generates a standard **Balance Sheet**.

---

## 🛠️ Technology Stack

| Component | Tool / Technology | Purpose |
| :--- | :--- | :--- |
| **Orchestration** | LangGraph | Deterministic workflow management |
| **LLM Reasoning** | Amazon Bedrock (Claude 3.5 Sonnet) | Data structuring and risk assessment |
| **OCR (Local)** | EasyOCR | Privacy-first text extraction from images |
| **Vector DB** | Qdrant / Weaviate | Statutory rule retrieval (RAG) |
| **Data Engine** | Pandas / Python | Deterministic tax calculations |
| **Web Extraction** | TinyFish API | Real-time GST portal verification |
| **API Layer** | FastAPI | Integration with external orchestrators |

---

## 💼 Use Cases & Benefits

### 👨‍💼 For CAs & Accounting Professionals
- **Automated Audits**: Generate an complete audit trail from raw document to final balance sheet in seconds.
- **Statutory Accuracy**: Every calculation is grounded in real-time rules retrieved from the vector database.
- **Scale**: Handle hundreds of clients simultaneously by automating the repetitive ingestion and reconciliation tasks.

### 🏢 For Businesses & SMEs
- **Self-Serve Tax Estimates**: Real-time visibility into tax liabilities (GST and Income Tax) throughout the year.
- **Vendor Risk Management**: Automatically verify the GSTIN status of every vendor in your ledger via the TinyFish integration.
- **Zero Data Leakage**: OCR is processed locally, and sensitive documents are analyzed within a secure enterprise environment.

---

## 🔌 Advanced Integrations

### 🤖 Orchestrators (OpenClaw, etc.)
The agent exposes a standard **FastAPI** endpoint (`/invoke`) that can be called by any orchestrator.
- **Input**: List of raw documents (URLs/Base64) or transaction text.
- **Output**: Full state object containing normalized ledger, analysis report, and government-ready payloads.

### 📥 Email & Accounting Software (MCP)
The agent is designed for **Model Context Protocol (MCP)** compatibility, allowing it to connect directly to:
- **Email Inboxes**: Monitor an `accounts@` or `tax@` email to automatically ingest document attachments.
- **Tally / QuickBooks**: Sync directly with accounting software via MCP servers to pull live ledger data for real-time compliance monitoring.

### 📊 Dashboard Access
While the agent runs as a headless engine, it emits structured state updates that power modern frontend dashboards (React/Next.js). Key dashboard widgets include:
- **GST Liability Monitor**
- **Presumptive vs. Actual Tax Comparison**
- **Audit Logs**

---

## 🛡️ Compliance & Security
- **DPDP Act 2023**: Fully compliant with Indian data protection laws through local OCR and enterprise-grade LLM deployments.
- **SOC 2 Ready**: Deterministic logic and comprehensive logging provide a clear "Chain of custody" for every financial calculation.

---

## 🚀 Getting Started
To deploy the agent in your environment:
1.  **Configure `.env`**: Add your `AWS_ACCESS_KEY`, `TINYFISH_API_KEY`, and `QDRANT_URL`.
2.  **Initialize DB**: Populate Qdrant with the latest CBDT/CBIC rulebooks.
3.  **Run Server**: `python api.py`
