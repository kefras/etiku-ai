# Digital Twin AI - Word2Vec, GloVe, RAG & Gemini PDF Chat

**An end-to-end NLP and Generative AI project combining word embeddings, semantic retrieval, Retrieval-Augmented Generation (RAG), and conversational PDF question answering.**

[**Live Application**](https://digitaltwin1.streamlit.app/) | [**GitHub Repository**](https://github.com/kefras/digital-twin-word2vec-glove-embeddings)

## Project Overview

Digital Twin AI demonstrates how natural language processing techniques can evolve from traditional word embeddings into practical AI-powered knowledge retrieval systems.

The project integrates **Word2Vec, a custom GloVe implementation, semantic search, RAG, Streamlit, and Google Gemini** into an interactive application.

Users can explore knowledge-base question answering, upload PDF documents, ask contextual questions, and continue conversations using follow-up questions.

## Key Features

- **Word2Vec Embeddings:** Explore distributed word representations and semantic relationships.
- **Custom GloVe Implementation:** Learn global word co-occurrence-based embedding techniques.
- **Semantic Search:** Retrieve relevant text using vector embeddings and similarity matching.
- **Retrieval-Augmented Generation:** Chunk documents, retrieve supporting passages, and generate grounded responses.
- **Knowledge Base Q&A:** Ask questions against a predefined knowledge base, with fallback behavior for unsupported questions.
- **Gemini-Powered PDF Chat:** Upload PDFs and ask natural-language questions about their contents.
- **Conversational Context:** Ask follow-up questions that build on earlier interactions.
- **Automated Testing:** Validate core application functionality using Python tests.
- **Streamlit Deployment:** Access the application through a publicly deployed web interface.

## System Architecture

![Digital Twin AI System Architecture](diagrams/architecture1.png)

```text
                    DIGITAL TWIN AI
                           |
                   Streamlit Interface
                           |
              +------------+------------+
              |                         |
       Knowledge Base Q&A          PDF AI Chat
              |                         |
       Text Knowledge Base          PDF Upload
              |                         |
         Text Chunking             PDF Extraction
              |                         |
       Sentence Embeddings         Text Chunking
              |                         |
       Semantic Retrieval       Sentence Embeddings
              |                         |
       Grounded Q&A /             Semantic Retrieval
         Abstention                    |
              |                   Google Gemini
              |                         |
              +------------+------------+
                           |
                     User Response
```

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| NLP | Word2Vec, GloVe |
| Embeddings | Sentence Transformers |
| Retrieval | Vector similarity search |
| AI Model | Google Gemini |
| Document Processing | PDF text extraction |
| Application | Streamlit |
| Testing | Python automated tests |
| Version Control | Git and GitHub |
| Deployment | Streamlit Community Cloud |

## Example Use Cases

**Knowledge Base Q&A**

Question: What does Kubernetes do?

Answer: Kubernetes automates container deployment and scaling.

**Conversational PDF Chat**

Question: How does Kubernetes compare with Docker?

Answer: Docker packages applications into portable containers, while Kubernetes manages container deployment and scaling.

These examples illustrate how retrieval and conversational context support document-grounded question answering.

## Live Application

Try the deployed application:

**https://digitaltwin1.streamlit.app/**

The application supports both knowledge-base question answering and Gemini-powered PDF conversations.

## Testing and Validation

The project has previously passed **21 automated tests** covering its core functionality. The repository also includes a GitHub Actions CI workflow.

## Project Limitations

- Answers depend on the quality and relevance of retrieved text.
- PDF text extraction may be less reliable for scanned or image-only documents.
- Gemini API availability and quotas can affect PDF chat responses.
- The application is intended as an educational and portfolio demonstration rather than a production-grade enterprise knowledge system.

## Future Improvements

- Persistent vector database integration.
- Support for multiple uploaded documents.
- Retrieval quality evaluation and benchmarking.
- Improved source citations and document references.
- Containerized deployment using Docker.
- Cloud infrastructure deployment and CI/CD enhancements.

## Project Background

Originally developed for a Week 2 AI School embeddings challenge, this project demonstrates a progression from traditional word embeddings to practical semantic retrieval and AI-assisted document question answering.

It serves as a hands-on learning project in machine learning, natural language processing, Retrieval-Augmented Generation, generative AI integration, and cloud application deployment.

## Live Demo

Try the deployed Digital Twin AI Assistant:

**[Launch Digital Twin AI](https://digitaltwin1.streamlit.app/)**

The application includes a knowledge-base question-answering interface and an AI-powered PDF chat system using semantic retrieval and Google Gemini.

## Application Screenshots

### Knowledge Base Question Answering

![Knowledge Base Q&A](screenshots/knowledge-base/qa-demo-final.png)

### PDF AI Chat

Upload a PDF document and ask questions about its contents.

![PDF AI Chat](screenshots/pdf-chat/pdf-upload.png)

### Automated Testing

The project successfully passed 21 automated unit tests.

![21 Tests Passed](screenshots/tests/21-tests-passed.png)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
