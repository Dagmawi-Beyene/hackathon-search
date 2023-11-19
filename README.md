---
# Hackathon Submission: Fast Keyword Search in Large Datasets

## Introduction:
I am excited to present my solution for the challenge of *Fast Keyword Search in Large Datasets*. My goal was to design a fast, robust, and ready-for-production system to quickly retrieve information from the vast amount of transcript data stored on Amazon S3. The solution utilises the open-source tool MeiliSearch to perform both the keyword and vector based searches.

## Solution Overview:
I decided to incorporate a *Hybrid Search Approach* with both keyword and vector search methods:

- For the keyword search, I use it for the first 2 words and if that doesn't yield satisfactory results, the vector search is used as a fallback.
- For more complex searches with more words, the system defaults to vector search.
  
This approach simplifies the indexing stage for documents and provides the users with real-time instant search results.

## Implementation:
For the implemenation, I chose MeiliSearch, a fast open-source search engine famed for its clean, streamlined and powerful full-text search capabilities with a notably low memory footprint. Its recent upgrade to support vector storage aligns perfectly with my hybrid search approach.

## Demo:
[Live Demo Link](https://search-pyjwrsrc3q-uc.a.run.app/)

![Image1](https://firebasestorage.googleapis.com/v0/b/gpt3-app.appspot.com/o/Screenshot%202023-11-19%20at%2010.02.07.png?alt=media&token=2414aa32-c89b-4293-b4a3-ef8800ac4454)
![Image2](https://firebasestorage.googleapis.com/v0/b/gpt3-app.appspot.com/o/Screenshot%202023-11-19%20at%2010.03.24.png?alt=media&token=bd7132f3-a59c-48b0-9a5f-5b8ddbc12589)

## Why I chose MeiliSearch:
1. Open-source: This gives the flexibility to host it anywhere ensuring adaptability to varied needs and changing requirements.
2. Speed: Meilisearch is recognised for its speed, presenting nearly real-time returns on search results.
3. Vector Search: With the recent introduction of vector storage, MeiliSearch perfectly fits my hybrid search idea.

## Comparison with ElasticSearch & Closed source solutions:
While Elasticsearch is popular, I found it to be highly demanding in terms of resources and it lacks native support for vector search. Closed source solutions offer less flexibility and control.

In contrast, MeiliSearch proved to be a winning combination of simple setup, minimal resource usage, quick data processing and open-source flexibility. With the newly-added capability of vector search, it is my preferred solution for this challenge.

## Conclusion:
I am confident that my solution leveraging the features of MeiliSearch meets all the requirements for this challenge and beyond. This system is designed to be efficient, very fast and ready for production deployment, providing room for future changes and updates.

The solution I've developed is nimble, efficient, and ready to be implemented. I am excited for what it could possibly bring to the table as a significant upgrade to the way transcript data is searched.

---

## How to run the code:
cd into the directory:
```
cd backend
```
install the dependencies:
```
pip3 install -r requirements.txt
```
start the server:
```
python3 main.py
```

## How to run the frontend:
cd into the directory:
```
cd frontend
```
install the dependencies:
```
pnpm install
```
start the server:
```
pnpm run dev
```

