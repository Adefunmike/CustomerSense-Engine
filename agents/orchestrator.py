# orchestrator.py
import asyncio
import logging
from typing import List, Dict, Any

# import your agents (adjust if your filenames/classes differ)
from agents.segmentation_agent import SegmentationAgent
from agents.retrieval_agent import RetrievalAgent
from agents.generation_agent import GenerationAgent
from agents.safety_agent import SafetyAgent
from agents.experiment_agent import ExperimentAgent
from agents.reporting_agent import ReportingAgent

# configuration via env vars
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

class Orchestrator:
    def __init__(self, config: Dict[str, Any]):
        # instantiate agents using config values
        self.seg_agent = SegmentationAgent(**config.get("segmentation", {}))
        self.ret_agent = RetrievalAgent(**config.get("retrieval", {}))
        self.gen_agent = GenerationAgent(**config.get("generation", {}))
        self.safe_agent = SafetyAgent(**config.get("safety", {}))
        self.exp_agent = ExperimentAgent(**config.get("experiment", {}))
        self.rep_agent = ReportingAgent(**config.get("reporting", {}))

    async def process_segment(self, df_segment):
        segment_label = df_segment["segment"].iloc[0]
        logger.info(f"Processing segment: {segment_label}")

        # 1. retrieve product content
        query = f"products for {segment_label}"
        retrieved = self.ret_agent.get_content(query)

        # 2. generate variants (async)
        variants = await self.gen_agent.generate_variants(segment_label, retrieved)

        # variants might be a list of dicts, adjust to your GenerationAgent's return format
        safe_variants = []
        for v in variants:
            ok, reason = self.safe_agent.check_message(v["text"])
            if ok:
                safe_variants.append(v)
            else:
                logger.warning(f"Variant blocked by safety: {reason}")

        return safe_variants

    async def run_pipeline(self, customers_df):
        # 0. segmentation (sync)
        customers_df = self.seg_agent.segment_customers(customers_df)

        # collect safe variants per segment
        all_safe_variants = {}

        # process each segment concurrently
        segment_groups = [group for _, group in customers_df.groupby("segment")]
        tasks = [self.process_segment(g) for g in segment_groups]
        results = await asyncio.gather(*tasks)

        for seg_group, safe_vars in zip(segment_groups, results):
            seg_label = seg_group["segment"].iloc[0]
            all_safe_variants[seg_label] = safe_vars

        # assign variants to customers and simulate experiment
        assigned_df = self.exp_agent.assign_variants(customers_df, variants=list("ABC"))  # adapt variants list as needed
        results_df = self.exp_agent.run_experiment(assigned_df)  # run_experiment should return a DataFrame with impressions/clicks/conversions

        # generate report
        report = self.rep_agent.generate_report(results_df, variants=all_safe_variants)
        return {
            "report": report,
            "safe_variants": all_safe_variants,
            "experiment_results": results_df.to_dict(orient="records")
        }


# Helper to build config from env vars (simplified)
def build_config_from_env():
    cfg = {
        "segmentation": {},
        "retrieval": {
            "search_endpoint": os.getenv("SEARCH_ENDPOINT"),
            "search_key": os.getenv("SEARCH_ADMIN_KEY"),
            "index_name": os.getenv("SEARCH_INDEX", "product-index")
        },
        "generation": {
            "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "azure_key": os.getenv("AZURE_OPENAI_KEY"),
            "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT")
        },
        "safety": {
            "cs_endpoint": os.getenv("CONTENT_SAFETY_ENDPOINT"),
            "cs_key": os.getenv("CONTENT_SAFETY_KEY"),
            "policy_path": os.getenv("SAFETY_POLICY_PATH", "config/safety_policy.yaml")
        },
        "experiment": {},
        "reporting": {}
    }
    return cfg


# CLI entrypoint for local testing
if __name__ == "__main__":
    import pandas as pd
    import sys

    # path to customers csv by default
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/customers.csv"
    customers = pd.read_csv(csv_path)

    orch = Orchestrator(build_config_from_env())
    result = asyncio.run(orch.run_pipeline(customers))

    # Print summary
    print("=== REPORT ===")
    print(result["report"])
    print("\n=== SAFE VARIANTS ===")
    for seg, vars_ in result["safe_variants"].items():
        print(f"Segment: {seg}")
        for v in vars_:
            print("-", v["text"][:200])
