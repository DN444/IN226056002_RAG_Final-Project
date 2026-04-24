from rank_bm25 import BM25Okapi


class HybridRetriever:
    def __init__(self, vectordb, documents):
        self.vectordb = vectordb
        self.docs = [d.page_content for d in documents]
        self.tokenized = [doc.split() for doc in self.docs]
        self.bm25 = BM25Okapi(self.tokenized)

    def retrieve(self, query, k=3):
        semantic = self.vectordb.similarity_search(query, k=k)

        scores = self.bm25.get_scores(query.split())
        keyword_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

        keyword_docs = [self.docs[i] for i in keyword_idx]

        combined = list(set(
            [d.page_content for d in semantic] + keyword_docs
        ))

        return combined[:k]