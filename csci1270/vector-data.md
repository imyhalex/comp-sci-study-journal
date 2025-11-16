# Vector Data

- Unstructured data
    - Text
    - Images
    - Audio
    - Video
- Store __unstructured data__ along with their vector embeddings
    - Dense Vector (Not many zeros)
    - Large # dimension (100s to 1000s)
    - Capture semantic features of underlying data that enable content-based processing

__Vector Embedding__
- What is it
    - Is simply a list of numbers that represents meaning
    - Example: "cat" -> `[0.12, -0.89, ..., 1.44]`
- Key Property:
    - Distance in vector space roughly equals to semantics similarity
        - “king” close to “queen”
        - “dog” close to “puppy”
        - “Paris” close to “France”
- Embeddings capture semantics relationships
- Embeddings that are close in vector space correspond to semantically similar items
- Allows sophisticated search of unstructured data

__How To Genrate Embeddings__
- Static embeddings = Every word has ONE fixed vector, no matter where it appears
    - Classic models
        - GloVe
        - Word2Vec
        - FastText
        - etc..
    - How they work:
        - Train on a huge text corpus
        - For each word, learn a fixed-length vector
        - Publish the embedding table (like a lookup dictionary)
- Problem: Static Embedding have no context
    - Example:
        - Sentence #1: “Convert this data into a table in Excel.” -> “table” here = data grid
        - Sentence #2: “Put this bottle on the table.” -> “table” here = furniture
        - But Word2Vec/Glove/FastText give the SAME vector for “table”
    - So this leads to no context

__Transformer__
- Contextualized embedding models
- BERT → Bidirectional Encoder Representations from Transformers
- BERT reads a sentence left → right AND right → left at the same time.
- It uses:
    - Masked Language Modeling (MLM)
        > “An apple a day keeps the doctor away”
        > → Randomly mask some words
        > → “An [MASK] a day [MASK] the doctor away”

        BERT’s job:
        **Predict the masked words** using information from both sides.

        This forces the model to understand:

        * grammar
        * semantics
        * context
        * relationships between words

        This is how it builds powerful contextual embeddings.
    - Next Sentence Prediction (NSP)
        The model gets:

        * Sentence A
        * Sentence B

        And it must predict:

        > “Is B really the next sentence after A?”

        Example from slide:

        A:

        > “An apple a day keeps the doctor away.”

        B:

        > “It highlights the health benefits of eating apples regularly.”

        NSP → “Yes, this is logically consecutive.”

        Randomly paired sentences → “No.”

        This trains BERT to understand:

        * topic flow
        * discourse
        * sentence relationships

        Useful for search, question answering, and document understanding.

__Vector Database Storage__
- Store both the raw and corresponding vectors

__Querying a Vector Database__
- Search for vectors that are similar to the query vector
- Example: Search for the nearest neighbors
- Simiar metries
    - Euclidian distance
    - Cosine Similarity
- Concerns:
    1. Expensive distance computations
        - Proportional to the # dimensions
        - Brute force approach does not scale well
    2. Vector can get large -> large memory footprint
- Big problems:
    - Computing distance requires looping over all D dimensions.
    - Doing this for all N vectors = too slow.
    - Vectors can be huge (384, 768, 1024 dims) → memory + time problems.

__Flat Index__
- Flat Index = brute force
- You compute the distance between the query vector and every single vector.
- Search Cost
    - `O(N⋅D)`
    - Where:
        - `N` = number of stored vectors
        - `D` = number of dimensions
- f N = 10 million and D = 768 → that’s 7.68 billion operations per query.
- Why this is bad
    - If you double the number of dimensions, what happens to the search time for Flat Index?

__Inverted File Index__
- Now the slides introduce IVF — this is exactly what FAISS, pgvector, and Pinecone use.
- Goal: Search only a small subset of vectors instead of all N.
- Example:
    - Green cluster
    - Yellow cluster
    - Red cluster
    - Gray cluster
- Step A: Parition the vector space:
    - We choose K centroids (clusters) using something like k-means.
    - Each cluster corresponds to a list of vectors.
    - This is why it’s called an inverted file:
        - Instead of “vector → cluster”,
        - you store “cluster → list of vectors”.
            ```text
            Green:  vec1, vec5, vec7, ...
            Yellow: vec4, vec9, vec2, ...
            Red:    vec3, vec6, vec8, ...
            Gray:   vec10, vec23, vec37, ...
            ```
- Step B: Querying IVF
    - Step 1: Find nearest centroid
        - Compute distance between query and all K centroids.
        - Cost: `O(KD)`
    - Step 2: Search only that cluster
        - Say centroid #1 is closest → we search only its vectors.
        - If each partition ~ N/K vectors, cost: `O(KD/N​)`
    - Total Cost:
        - `O(KD) + O(KD/N​)`
- __What is the problem with the Inverted File Index (IVF) approach?__
    -  The nearest vectors might NOT be in the nearest cluster.
        - Your query vector might be:
            - closest to centroid #3 BUT
            - its true nearest neighbors are actually inside centroid #1 or #2.
        - Because we only search one cluster (or a few), we risk missing the correct neighbors.
        - This makes IVF an approximate method, not exact.
        - Therefore, IVF can skip the correct nearest neighbors.
            - Because clusters are imperfect
            - Boundaries between clusters are artificial
            - Real semantic vectors often lie near multiple centroids
            - Queries near the cluster border get misassigned
    - But there are more problems
        1. Still expensive for large K
        2. Cluster imbalance
        3. Sensitive to how centroids are trained

__Approximate Nearest Neighbors (ANN)__
- ANN = fast but not guaranteed exact.
- The ANN algorithm finds some neighbors within that cluster, but those neighbors might not be the true mathematically closest points.
- It searches only a small region (e.g., 1 cluster instead of all vectors), so it may:
    - return neighbors that are very close
    - but not always the exact true nearest neighbors
- ANN = umbrella term for many vector indexing techniques
    | ANN Method                    | Description                                                       |
    | ----------------------------- | ----------------------------------------------------------------- |
    | **IVF (Inverted File Index)** | Partition vectors into clusters → search only the closest cluster |
    | **IVF+PQ**                    | IVF + compress vectors                                            |
    | **HNSW**                      | Graph-based search (used in pgvector, Pinecone)                   |
    | **LSH**                       | Hashing-based similarity search                                   |
    | **ScaNN**                     | Google’s optimized algorithm                                      |
    | **FAISS Flat / IVF / HNSW**   | Meta’s vector search toolkit                                      |


__KNN vs ANN__
- k-Nearest Neighbors (kNN)
    - Exact brute-force search
    - Computes distance to every stored vector
    - Very expensive when N or D is large
- Approximate Nearest Neighbor (ANN)
    - Does not compute distance to all N vectors
    - Only looks at a subset (like IVF partition or HNSW graph neighbors)
    - May miss the mathematically closest vectors
    - But it’s MUCH faster
- Tradeoff
    - More speed → less accuracy
    - More accuracy → slower search

__Hierarchical Navigable Small World (HNSW)__
- HNSW is a graph-based ANN index used to find nearest neighbors quickly.
- Think of it like:
    - vectors = nodes in a graph
    - edges = “neighbors” (similar vectors)
    - you search through the graph to find the nearest vector
- Index strcture for scalable ANN search over vectors
- HNSW is like a multi-level skip list, but for vectors
    ```text
    Top Layer      (fast but coarse)
    Middle Layer   (medium)
    Bottom Layer   (dense, fine search)
    ```
- Small-world graph
    - Each Vertex has a small # edges
    - Avg path length between two random vertices is small
    - Hierachical version is inspired by skip lists
    - A small-world graph has 2 properties:
        - Each vertex has only a few edges
            - → keeps memory small
            - → keeps search local and fast
        - Any node is reachable from any other by a short path
            - → ensures ANN search finds good neighbors quickly
            - → you don’t have to explore the whole graph
    

__Vector Quantization__
- A technique to make vectors smaller and cheaper to store and search
- Why:
    - Embeddings can be large (384, 768, 1536 dims)
    - Stored as float32 → 4 bytes each
    - For millions or billions of vectors → very high cost
- Quantization reduces the memory needed by approximating the vector with a lower-precision or compressed representation.
- Types:
    - Scalar Quantization: Reduces the precision of each vector component
    - Product Quantization: Divides vectors into sub-vectors and approximates them using codebooks
    - Binary Quantization: Represents vectors using bit vectors
- Restate Tradeoff
    - Qunatized search -> fast but approximate
    - Full-percision search -> accurate but slow

__Re-Rankking with Full Embeddings__
- Goal: Balance speed of quantized search with accuracy of full-persion ranking
    - Over-retrive with quantizd embeddings -> fast but approximate
    - Re-ranking can use original, full-precision embedding to refine results
- Two-stage pipeline
    - Stage 1: Over-retrieval: coarse search w/ quantized embeddings
        - Use compressed vectors
        - Retrieve top-k ≈ 100 candidates quickly
    - Stages 2: Re-Ranking: w/ full embeddings
        - Fetch original 32-bit vectors for those k
        - Recompute exact distances
        - Output final top-N (e.g., 10)

__Integration W/ SQL__
- Goal: Combine vector and relational data in one query
    - Traditional SQL-> great for searching structured data
    - Vector embeddings → great for searching unstructured data
    - Hybrid queries blend both
- Example
    ```sql
    CREATE TABLE photos (
        image_id    SERIAL PRIMARY KEY,
        location    TEXT,
        season      TEXT,
        taken_date  DATE,
        photographer TEXT,
        embedding   VECTOR(1536)
    );

    SELECT image_id, location
    FROM photos
    WHERE season = 'winter'
    ORDER BY cosine_similarity(embedding, embed('snowy mountain landscape')) DESC
    LIMIT 5;

    CREATE INDEX photos_embedding_idx
    ON photos USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
    ```

__Using Vector Database with LLMs__
- LLM encode parametric knowledge
- Their knowledge is limited to their traning data
- Sometimes we need to use private data up-to-date data

__RAG (Retrieval-Augmented Generation)__
- RAG = LLM (Generation) + Vector Database (Retrieval)
- The model retrieves relevant information from an external knowledge base before generating an answer.
- Course slide explaination
    - Left side: Retrieval
        - User prompt: “Tell me my sales in the last 10 days”
        - Convert prompt into an embedding vector (0.2, -1.2, …, 2.3)
        - Use vector search to fetch nearest neighbors from a vector DB (chunks like “the team reported sales of…”, “the burn this month…”)
    - Right side: Augment -> Genrate
        - Combine:
            - The user prompt
            - The retrieved context
            - Into into a single combined prompt and send that to the LLM.
        - The LLM answers using:
            - your query
            - the context retrieved from vector search

__General RAG Flow__
- **Step 0 — Document preprocessing**
    * You take documents
    * Split them into chunks (paragraphs, sections, etc.)
    * Embed each chunk
    * Store embeddings + text in the vector database
- **Step 1 — Retrieval**
    - At query time:
        1. User sends query
        2. Query is embedded
        3. Vector database returns the most similar chunks
- **Step 2 — Augment the prompt**
    - You create a final prompt template:
        ```
        User query:
        "Tell me my sales in the last 10 days"

        Relevant context:
        - The team reported sales of ...
        - The burn this month was ...
        ```
- **Step 3 — Generation**
- Send the augmented prompt to the LLM.
- LLM generates the final answer using the retrieved knowledge.

__How to Embed For Retrival__
1. Chuncking
    - Break long documents into semantically coherent chunks (e.g., 100–300 words)
    - Maintain sentence boundaries to preserve context
    - Each chunk → one vector
2. Normalization: Normalize text before embedding (case, punctuation, encoding)
3. Model Selection
    - Use contextual embedding models tuned for retrieval
    - Keep the same model for both indexing and querying
4. Storage & Metadata
    - Vector + Associated raw text chunk + Metadata (e.g., title, timestamp, source)
5. Query Embedding
    - Embed full user query
    - Optionally add context prompts (“This is a search query about...”) for clarity