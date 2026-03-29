# Enterprise Tax Agent (India)

A deterministic, graph-based computation engine for autonomous Indian tax compliance (ITR, GST). Built with LangGraph, Amazon Bedrock, and high-performance OCR for enterprise-grade tax automation.

## Features

- **Autonomous Workflows**: LangGraph-powered deterministic graph for handling complex tax calculations and document processing.
- **Enterprise Reasoning**: Integrated with **Amazon Bedrock** for sophisticated data extraction and reasoning.
- **Local OCR**: High-accuracy document parsing using local models for data privacy and speed.
- **Vector Intelligence**: Hybrid search capabilities for RAG using Qdrant/Weaviate.
- **Compliance Focused**: Designed to adhere to SOC 2 and the Indian DPDP Act 2023.

## Project Structure

```bash
├── api.py              # FastAPI server and agent interface
├── graph.py            # LangGraph workflow and node definitions
├── state.py            # System state schema
├── vector_db.py        # Vector database (Qdrant/Weaviate) integration
├── bedrock_client.py   # Amazon Bedrock AI integration
├── nodes/             # Core computation and reasoning modules
│   ├── computation.py  # Tax calculation logic
│   ├── ml_ingestion.py # OCR and document processing
│   ├── analyst.py     # Data analysis and reasoning
│   ├── rag.py         # Knowledge retrieval
│   └── normalizer.py  # Data standardisation
├── Dockerfile          # Production-ready deployment
└── docker-compose.yml   # Local development environment
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional, for local services)
- Amazon Bedrock access

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/atnahm/TAX-AGENT_V2.git
   cd TAX-AGENT_V2
   ```

2. Install dependencies:
   ```bash
   pip install .
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

### Running Locally

To start the API server:
```bash
python api.py
```

To run with local dependencies (Qdrant, etc.):
```bash
docker-compose up -d
```

## Security & Compliance

The system implements strict data segregation and encryption at rest/transit to ensure compliance with the **Digital Personal Data Protection (DPDP) Act 2023**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
