# Simple placeholder for scheduled refresh logic.
# In practice, run this via cron/GitHub Actions/Airflow.
import subprocess

print("Running daily refresh...")
subprocess.run(["python", "scripts/build_funnel.py"], check=True)
print("Done.")
