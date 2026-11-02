# Triagent – Technical Decision Log

This document records the technical and architectural decisions made during the development of Triagent, including the rationale, alternatives considered, and trade-offs.

## 1. Custom RAG Implementation

**Status:** Accepted

**Decision:** Implemented a custom Retrieval-Augmented Generation (RAG) pipeline using Python without LangChain or LlamaIndex.

**Rationale:**

- Understand the underlying RAG workflow.
- Gain practical experience with embeddings, vector retrieval, context preparation, and LLM inference.
- Maintain control over individual components.

**Alternatives:** LangChain, LlamaIndex.

**Trade-off:** Requires more manual implementation but provides greater control and understanding of the RAG pipeline.

## 2. LLM Migration – Gemini to Ollama

**Status:** Accepted

**Decision:** Initially used Google Gemini API for LLM inference and embedding generation. Later migrated to local inference and embedding models.

**Initial implementation:**

- Google Gemini API.
- Gemini embedding model.

**Current implementation:**

- Ollama – Qwen3 1.7B.
- Sentence Transformers – all-MiniLM-L6-v2.

**Rationale:**

- Gemini free-tier quota limitations affected development.
- Local inference reduced dependency on external API quotas.
- Local embeddings enabled independent experimentation.

**Trade-off:** Local inference requires computational resources and model installation.

## 3. Local Embedding Model

**Status:** Accepted

**Decision:** Selected `sentence-transformers/all-MiniLM-L6-v2` for generating text embeddings.

**Rationale:**

- Lightweight model.
- Local embedding generation.
- Suitable for semantic similarity search.
- Easy integration with ChromaDB.

**Alternative:** Google Gemini embedding model.

**Trade-off:** Retrieval relevance and embedding quality require further evaluation.

## 4. ChromaDB as Vector Database

**Status:** Accepted

**Decision:** Selected ChromaDB with persistent storage for vector storage and similarity-based retrieval.

**Rationale:**

- Integrates with Sentence Transformers.
- Supports persistent local storage.
- Suitable for the current knowledge base.

**Trade-off:** Larger-scale applications may require more advanced storage infrastructure.

## 5. JSON-Based Knowledge Base and Ticket Memory

**Status:** Accepted

**Decision:** Used JSON files to manage the knowledge base and previously analysed tickets.

**Implementation:**

- `knowledge_base.json` – 45 ERP support ticket examples.
- `memory.json` – Previously analysed tickets and generated diagnoses.

**Rationale:**

- Simple and readable data structure.
- Easy to maintain and modify.
- Avoids unnecessary database infrastructure during initial development.

**Trade-off:** JSON has limitations for concurrent access and large-scale querying.

## 6. Pydantic for Structured Output Validation

**Status:** Accepted

**Decision:** Used Pydantic models to validate structured LLM responses.

**Rationale:**

- Enforces the expected response structure.
- Validates fields such as module, category, complexity, root cause, and troubleshooting steps.
- Helps handle inconsistent LLM outputs.

**Alternative:** Manual JSON parsing and validation.

**Trade-off:** Requires predefined schemas and validation error handling.

## 7. LLM-Based Input Guardrail

**Status:** Accepted

**Decision:** Implemented an LLM-based input validation mechanism to identify ERP-related requests before processing.

**Rationale:**

- Keeps the application focused on ERP support.
- Rejects unrelated requests.
- Avoids unnecessary processing of unsupported inputs.

**Implementation:** Ollama with a Pydantic-defined response schema.

**Trade-off:** Adds an additional inference step and may misclassify ambiguous inputs. It is not a complete security mechanism.

## 8. Streamlit for User Interface

**Status:** Accepted

**Decision:** Selected Streamlit for the application interface.

**Rationale:**

- Native Python integration.
- Rapid development.
- Built-in components for forms, navigation, and ticket history.
- Avoids a separate frontend implementation.

**Alternatives:** Flask, FastAPI with a separate frontend.

**Trade-off:** Less frontend customisation than dedicated web frameworks.

## 9. Project Documentation

**Status:** Accepted

**Decision:** Organised project documentation through README.md, requirements.txt, and DECISION_LOG.md.

**Rationale:**

- Improve maintainability.
- Simplify project setup.
- Explain architectural choices and trade-offs.
- Make the repository easier for developers and recruiters to understand.

## Future Technical Decisions

| Area            | Planned Improvement                               | Status  |
| --------------- | ------------------------------------------------- | ------- |
| RAG Evaluation  | Measure retrieval relevance and diagnosis quality | Planned |
| Grounding       | Improve evidence-based diagnosis generation       | Planned |
| ERP Integration | Explore REST API integration                      | Planned |
| Testing         | Introduce automated testing with pytest           | Planned |
| Deployment      | Cloud deployment                                  | Planned |
| Database        | Explore scalable persistent storage               | Planned |
| Agentic AI      | Explore multi-step troubleshooting workflows      | Planned |

---

**Project:** Triagent  
**Document:** Technical Decision Log
