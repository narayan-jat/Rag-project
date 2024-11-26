## **YouTube Video Search with RAG**

[Code](https://github.com/narayan-jat/Rag-project/)

### **Introduction**

In this project, we aimed to build a RAG pipeline to help users find relevant videos or segments of videos using natural language prompts. We utilized a YouTube video dataset, extracting metadata like titles, descriptions, and transcripts.

---

### **Dataset**

We did not use a pre-existing dataset but created our own. The dataset consists of:
1. Video metadata such as title and description.
2. YouTube video transcripts.

We tested the pipeline on datasets of three sizes:
- 10 videos.
- 100 videos.
- More than 1000 videos.

---

### **RAG Pipeline**

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.001.png)

---

### **Converting Documents to Vectors**

1. **Types of Vectors**:
   - **Document Metadata Vectors**: Based on video titles and descriptions.
   - **Transcript Vectors**: Based on video transcripts for deeper content analysis.

2. **Handling Long Transcripts**:
   - For lengthy transcripts (e.g., 5-10 hours), we applied **chunking**:
     - **Contextual Chunking**: Divided transcripts into coherent segments based on timestamps.
     - Initially tried treating each sentence as a chunk but found it ineffective.

3. **Embedding**:
   - Metadata and transcript chunks were embedded using **SBERT** embeddings.
   - Experimented with **BM25** as a comparison.

4. **Storage**:
   - Stored vectors in a PostgreSQL database using the Pgvector extension for efficient retrieval.

---

### **Retrieving Documents Based on Query**

1. **Query Processing**:
   - Converted user queries into vectors.
   - Compared query vectors with metadata vectors for initial ranking.

2. **Metadata-Based Ranking**:
   - Videos were ranked based on metadata relevance.

3. **Clustering**:
   - Clustered top-ranked videos to refine search and focus on more relevant ones.

---

### **Fine-Grained Retrieval within Clusters**

1. **Transcript Chunk Embedding**:
   - Embedded transcript chunks of relevant videos within clusters.

2. **Chunk Retrieval**:
   - Used similarity calculations to retrieve the most relevant chunks.

3. **Chunking Improvements**:
   - Larger, contextually meaningful chunks using start times improved coherence.

---

### **Re-Ranking Results with a Cross-Encoder**

1. **Purpose**:
   - Re-ranked retrieved chunks to prioritize relevance.

2. **Cross-Encoder Model**:
   - Assigned relevance scores to chunks for final ranking.

3. **Results**:
   - Enhanced relevance for complex queries.

---

### **Generating the Final Answer with LLaMA**

1. **Contextual Input for LLM**:
   - Concatenated top-ranked chunks for input to the LLaMA model.

2. **Answer Generation**:
   - Generated a response by synthesizing information from relevant video segments.

3. **Handling Insufficient Context**:
   - If retrieved context was insufficient, the model prompted for clarification.

---

### **Problems We Faced**

#### **Threshold Tuning**

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.002.jpeg)

1. At a threshold of **0.3**, natural language prompts retrieved no content as documents failed to pass the threshold.

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.003.jpeg)

2. At a threshold of **0.1**, natural language prompts returned good results.

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.004.jpeg)

3. When the content was not in the database, a threshold of **0.1** still retrieved some results due to partial matches.

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.005.jpeg)

4. At a threshold of **0.3**, irrelevant queries returned appropriate "no result" messages.

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.006.jpeg)

- **Final Threshold**: Set to **0.25** to balance relevance and accuracy.

---

#### **Short Query Problem**

1. Used a hybrid approach combining **BM25** and **SBERT** embeddings for metadata.
2. Retrieved top 5 results from both methods and merged them for ranking.
3. This approach addressed short, keyword-based queries (e.g., "What is RNN?") and natural language prompts (e.g., "What is the best time to sell stocks?").

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.007.jpeg)

---

### **Quantitative Analysis**

#### **Success Rate vs. Threshold**

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.008.jpeg)

- A threshold of **0.1** returned too many irrelevant chunks.
- A threshold of **0.3** missed relevant chunks.
- **Optimal Threshold**: **0.25**.

#### **Chunk Distribution with Dataset Growth**

![](Youtube%20video%20search(RAG)/media/Aspose.Words.39d9ae32-589e-409b-b690-aa16d4d14a26.009.jpeg)

---

### **Conclusion**

In this project, we developed a RAG pipeline to help users find relevant YouTube videos or segments through natural language prompts. By combining **BM25** for keyword matching and **SBERT** for semantic understanding, we effectively handled both short and complex queries. Contextual chunking and careful tuning of the retrieval threshold significantly improved accuracy. Finally, we used the **LLaMA** model to generate comprehensive responses, making the system scalable and effective for large video datasets.

---

### **Authors**
1. Narayan Jat
2. Kirtan Khichi
3. Sonal Kumari
