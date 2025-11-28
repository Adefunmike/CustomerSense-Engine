# app.py
import os
import asyncio
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import pandas as pd
from orchestrator import Orchestrator, build_config_from_env

app = FastAPI(title="Marketing Agent Orchestrator")

class RunRequest(BaseModel):
    customers_csv_path: str = "data/customers.csv"  # optional

@app.post("/run")
async def run_pipeline(req: RunRequest, background: BackgroundTasks):
    # run in background so HTTP returns quickly (optional)
    customers = pd.read_csv(req.customers_csv_path)
    orch = Orchestrator(build_config_from_env())
    result = await orch.run_pipeline(customers)
    return {"status": "completed", "report": result["report"], "safe_variants_count": {k: len(v) for k, v in result["safe_variants"].items()}}
