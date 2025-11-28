from agents.experiment_agent import ExperimentAgent
from agents.reporting_agent import ReportingAgent
import pandas as pd

customers = pd.read_csv("data/customers.csv")

agent = ExperimentAgent(customers, ["A", "B", "C"])
results_df = agent.run_experiment()

report_agent = ReportingAgent()
report = report_agent.generate_report(results_df)

print(report)
