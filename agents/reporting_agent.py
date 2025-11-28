class ReportingAgent:
    def generate_report(self, experiment_df):
        grouped = experiment_df.groupby("variant").agg({
            "clicks": "sum",
            "impressions": "sum"
        }).reset_index()

        # compute CTR per variant
        grouped["ctr"] = grouped["clicks"] / grouped["impressions"]

        # control = first variant alphabetically
        control_ctr = grouped.iloc[0]["ctr"]

        report_lines = []
        for _, row in grouped.iterrows():
            lift = row["ctr"] - control_ctr
            if row["variant"] == grouped.iloc[0]["variant"]:
                lift_display = "N/A"
            else:
                lift_display = f"{lift:.3f}"

            report_lines.append(
                f"Variant: {row['variant']}\n"
                f"CTR: {row['ctr']:.3f}\n"
                f"Lift over control: {lift_display}\n"
            )

        return "\n".join(report_lines)
