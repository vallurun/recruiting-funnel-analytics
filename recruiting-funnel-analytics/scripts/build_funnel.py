import pandas as pd
from pathlib import Path

RAW = Path("data/raw")
DER = Path("data/derived")
DER.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW / "candidates.csv", parse_dates=["stage_entered_at"])

# Conversion rates by source
last_stage = df.groupby("candidate_id")["stage"].max().rename("last_stage")
joined = df.drop_duplicates(subset=["candidate_id","source"]).merge(last_stage, left_on="candidate_id", right_index=True)

def conv_rate(end_stage):
    reached = joined["last_stage"].isin([end_stage, "Hired"]) if end_stage != "Hired" else (joined["last_stage"] == "Hired")
    return (reached.mean())

conv = (joined.groupby("source")
    .apply(lambda g: pd.Series({
        "applied": len(g),
        "to_phone_screen": (g["last_stage"].isin(["Phone Screen","Hiring Manager","Onsite","Offer","Hired"]).mean()),
        "to_onsite": (g["last_stage"].isin(["Onsite","Offer","Hired"]).mean()),
        "to_offer": (g["last_stage"].isin(["Offer","Hired"]).mean()),
        "to_hired": (g["last_stage"].eq("Hired").mean())
    }))
    .reset_index())
conv.to_csv(DER / "funnel_conversions.csv", index=False)

# Time to fill by job_id
stage_order = {"Applied":0,"Phone Screen":1,"Hiring Manager":2,"Onsite":3,"Offer":4,"Hired":5}
df["stage_num"] = df["stage"].map(stage_order)
hired = df[df["stage"]=="Hired"]
first_applied = df.groupby("job_id")["stage_entered_at"].min().rename("first_applied_at")
hired_join = hired.groupby("job_id")["stage_entered_at"].max().rename("hired_at").to_frame().join(first_applied, how="left")
hired_join["time_to_fill_days"] = (hired_join["hired_at"] - hired_join["first_applied_at"]).dt.days
hired_join.reset_index().to_csv(DER / "time_to_fill.csv", index=False)

# Source effectiveness (hired share by source)
hired_by_source = joined[joined["last_stage"]=="Hired"].groupby("source").size().rename("hired").reset_index()
apps_by_source = joined.groupby("source").size().rename("applied").reset_index()
src_eff = apps_by_source.merge(hired_by_source, on="source", how="left").fillna({"hired":0})
src_eff["hire_rate"] = (src_eff["hired"] / src_eff["applied"]).round(3)
src_eff.to_csv(DER / "source_effectiveness.csv", index=False)

print("Wrote funnel_conversions.csv, time_to_fill.csv, source_effectiveness.csv")
