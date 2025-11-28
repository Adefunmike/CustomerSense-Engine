import random
import pandas as pd

class ExperimentAgent:
    def __init__(self, customers, variants):
        self.customers = customers
        self.variants = variants

    def run_experiment(self):
        rows = []

        for _, row in self.customers.iterrows():
            variant = random.choice(self.variants)

            impressions = random.randint(50, 200)
            clicks = random.randint(0, impressions)
            ctr = clicks / impressions

            rows.append({
                "customer_id": row["customer_id"],
                "variant": variant,
                "impressions": impressions,
                "clicks": clicks,
                "ctr": ctr
            })

        return pd.DataFrame(rows)
