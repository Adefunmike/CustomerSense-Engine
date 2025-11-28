from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

class RetrievalAgent:
    def __init__(self, search_index, api_key, endpoint):
        self.client = SearchClient(
            endpoint=endpoint,
            index_name=search_index,
            credential=AzureKeyCredential(api_key)
        )

    def get_content(self, query):
        results = self.client.search(query, top=5)
        retrieved = []
        for r in results:
            retrieved.append({
                "text": r["content"],
                "source": r["@search.highlights"],
                "doc_id": r["id"]
            })
        return retrieved
