from langchain.schema import BaseRetriever, Document
from typing import List, Any


class MongoDBKeywordRetriever(BaseRetriever):
    collection: Any
    top_k: int
    def get_relevant_documents(self, query: str) -> List[Document]:
        self.collection.create_index([("text", "text")])
        # Perform keyword search and include relevance score
        mongo_results = self.collection.find(
            {'$text': {'$search': query}},
            {'score': {'$meta': 'textScore'}}
        ).sort([('score', {'$meta': 'textScore'})])

        # Limit results to top_k
        results = mongo_results[0:self.top_k]

        # Convert MongoDB documents to LangChain Documents
        documents = []
        for result in results:
            documents.append(Document(
                page_content=result['text'],
                metadata={
                    **result.get('metadata', {}),
                    'score': result.get('score', 0)
                }
            ))

        return documents
