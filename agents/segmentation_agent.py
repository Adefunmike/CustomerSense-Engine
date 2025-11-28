import pandas as pd
from sklearn.cluster import KMeans

class SegmentationAgent:
    def __init__(self, kernel):
        self.kernel = kernel

    def segment_customers(self, df):
        # Simple clustering for demo
        features = df[["recency", "frequency", "monetary"]]
        kmeans = KMeans(n_clusters=3, random_state=0).fit(features)

        df["segment"] = kmeans.labels_

        return df
