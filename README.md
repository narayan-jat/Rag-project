# YouTube Video Search with RAG

This project showcases a **Retrieval-Augmented Generation (RAG) pipeline** designed to help users find specific YouTube videos or video segments based on natural language prompts. By leveraging video metadata (title, description) and transcript data, the pipeline performs semantic search, enabling accurate retrieval of relevant video content.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Creation](#dataset-creation)
3. [RAG Pipeline](#rag-pipeline)
4. [Methodology](#methodology)
5. [Experimentation and Challenges](#experimentation-and-challenges)
6. [Technologies Used](#technologies-used)
7. [Future Improvements](#future-improvements)

---

## Project Overview

The **YouTube Video Search with RAG** project is designed to:
- Help users locate videos or segments using a natural language search.
- Handle lengthy YouTube video transcripts by dividing them into manageable, meaningful chunks.
- Use combined techniques of keyword and semantic search to achieve accurate results.

## Dataset Creation

We created a custom dataset for this project:
1. **Data Sources**: Video title, description, and transcript.
2. **Sample Sizes**: Tested on datasets of various sizes: 10, 100, and over 1000 videos.
3. **Chunking**: Long transcripts were divided into contextually coherent segments using timestamps, enhancing response relevance.

## RAG Pipeline

The RAG pipeline is designed with the following key steps:

### 1. Embedding Generation
   - **Metadata Vectors**: Created from video titles and descriptions to capture basic video content.
   - **Transcript Vectors**: Generated from transcript chunks to capture in-depth context.

### 2. Storage
   - **Pgvector Extension**: All vectors are stored in a PostgreSQL database with the Pgvector extension for efficient similarity search.

### 3. Retrieval Process
   - **Query Processing**: Converts user queries to vectors, which are compared to metadata vectors for initial ranking.
   - **Clustering and Ranking**: Clusters top-ranked videos and performs fine-grained transcript search within clusters.
   - **Re-Ranking with Cross-Encoder**: Re-ranks relevant chunks to prioritize contextually accurate segments.

### 4. Answer Generation
   - **LLaMA Model**: The model receives the top segments and generates a response, synthesizing relevant information.

## Methodology

1. **Query Vectorization**: User prompts are vectorized using SBERT embeddings.
2. **Top-K Retrieval**: Metadata vectors are used for quick initial filtering of relevant videos.
3. **Clustering for Refinement**: Videos are grouped by similarity to focus the search within clusters.
4. **Transcript Search**: Transcript chunks within the clusters are matched to refine results.
5. **Cross-Encoder Re-Ranking**: Improves chunk relevance by re-evaluating top results.
6. **Final Answer Generation**: LLaMA synthesizes context into a coherent response.

## Experimentation and Challenges

1. **Threshold Tuning**: Set similarity thresholds to balance precision and recall, improving retrieval accuracy.
2. **Short Query Handling**: Used both BM25 and SBERT for metadata to capture keyword and semantic matches, enhancing search quality.
3. **Chunking Strategy**: Experimented with sentence-level and context-based chunking, opting for timestamp-based segmentation for better coherence.

## Technologies Used
- **SBERT (Sentence-BERT)**: Embedding generation for semantic understanding.
- **BM25**: Keyword-based matching, particularly effective for short queries.
- **Pgvector (PostgreSQL)**: Vector database for efficient storage and retrieval.
- **LLaMA**: Large language model for contextual response generation.

## Future Improvements
1. **Dynamic Thresholds**: Fine-tune thresholds based on query type or complexity.
2. **Improved Re-Ranking**: Incorporate more advanced cross-encoder models for better response accuracy.
3. **User Feedback Integration**: Capture user feedback to refine search and improve responses over time.
