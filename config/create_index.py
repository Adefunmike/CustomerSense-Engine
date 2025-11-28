from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType, SearchableField


service_name = "marketing-agent-search"
admin_key = "kgSj5DZRK9cpAGIX9Nn6la9Kb5vi3yrtoJVGUcPyQiAzSeAdm4Ao"
index_name = "product-index"
endpoint = f"https://marketing-agent-search.search.windows.net"

# ---- CONNECT ----
client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(admin_key))

# ---- DEFINE INDEX ----
index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(name="product_id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="name", type=SearchFieldDataType.String),
        SearchableField(name="description", type=SearchFieldDataType.String),
        SimpleField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SimpleField(name="price", type=SearchFieldDataType.Double, filterable=True, sortable=True)
    ]
)

# ---- CREATE INDEX ----
client.create_index(index)
print("Index created successfully!")
