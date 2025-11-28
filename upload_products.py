import os
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
)

# -----------------------------
# CONFIG
# -----------------------------
SEARCH_SERVICE_NAME = "marketing-agent-search"   # your service name
SEARCH_ADMIN_KEY = "kgSj5DZRK9cpAGIX9Nn6la9Kb5vi3yrtoJVGUcPyQiAzSeAdm4Ao"  # your key
SEARCH_ENDPOINT = f"https://marketing-agent-search.search.windows.net"
INDEX_NAME = "product-index"

PRODUCT_CSV_PATH = "data/product_content.csv"   # where your CSV is

# -----------------------------
# CREATE INDEX
# -----------------------------
def create_index():
    index_client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT,
        credential=AzureKeyCredential(SEARCH_ADMIN_KEY)
    )

    fields = [
        SimpleField(name="product_id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="name", type=SearchFieldDataType.String),
        SearchableField(name="description", type=SearchFieldDataType.String),
        SearchableField(name="category", type=SearchFieldDataType.String),
        SimpleField(name="price", type=SearchFieldDataType.Double),
    ]

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
    )

    index_client.create_or_update_index(index)
    print(f"✅ Index '{INDEX_NAME}' created successfully.")

# -----------------------------
# UPLOAD CSV DOCUMENTS
# -----------------------------
def upload_products():
    df = pd.read_csv(PRODUCT_CSV_PATH)

    # Convert rows to dictionaries
    docs = df.to_dict(orient="records")

    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=AzureKeyCredential(SEARCH_ADMIN_KEY)
    )

    result = search_client.upload_documents(documents=docs)
    print(f"📌 Uploaded {len(result)} products successfully.")


if __name__ == "__main__":
    create_index()
    upload_products()
