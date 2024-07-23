import pymongo
import google.generativeai as genai
from IPython.display import Markdown
import textwrap
from embeddings import SentenceTransformerEmbedding, EmbeddingConfig

class RAG():
    def __init__(self, 
            mongodbUri: str,
            dbName: str,
            dbCollection: str,
            llm,
            embeddingName: str ='sentence-transformers/all-MiniLM-L12-v2',
        ):
        self.client = pymongo.MongoClient(mongodbUri)
        self.db = self.client[dbName] 
        self.collection = self.db[dbCollection]
        self.embedding_model = SentenceTransformerEmbedding(
            EmbeddingConfig(name=embeddingName)
        )
        self.llm = llm

    def get_embedding(self, text):
        if not text.strip():
            return []

        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def vector_search(
            self, 
            user_query: str, 
            limit=4):
        """
        Perform a vector search in the MongoDB collection based on the user query.

        Args:
        user_query (str): The user's query string.

        Returns:
        list: A list of matching documents.
        """

        # Generate embedding for the user query
        query_embedding = self.get_embedding(user_query)

        if query_embedding is None:
            return "Invalid query or embedding generation failed."

        # Define the vector search pipeline
        vector_search_stage = {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 400,
                "limit": limit,
            }
        }

        unset_stage = {
            "$unset": "embedding"
        }

        project_stage = {
            "$project": {
                "_id": 0,
                "name": 1,
                "description": 1,
                "price": 1,
                "rating": 1,
                "score": {
                    "$meta": "vectorSearchScore"
                }
            }
        }

        pipeline = [vector_search_stage, unset_stage, project_stage]

        # Execute the search
        results = self.collection.aggregate(pipeline)

        return list(results)

    def enhance_prompt(self, query):
        get_knowledge = self.vector_search(query, 10)
        enhanced_prompt = ""
        i = 0
        for result in get_knowledge:
            print(result)
            if result.get('name'):
                i += 1
                enhanced_prompt += f"\n {i}) Name: {result.get('name')}"

                if result.get('price'):
                    enhanced_prompt += f", Price: {result.get('price')}"
                else:
                    # Mock up data
                    # Retrieval model pricing from the internet.
                    enhanced_prompt += f", Price: Contact for more information"

                if result.get('rating'):
                    enhanced_prompt += f", Rating: {result.get('rating')}"
        print('---enhanced_prompt', enhanced_prompt)
        return enhanced_prompt

    def generate_content(self, prompt):
        return self.llm.generate_content(prompt)

    def _to_markdown(text):
        text = text.replace('•', '  *')
        return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
