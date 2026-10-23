import csv
import matplotlib.pyplot as plt

drift_rates = set()
boundaries = set()
results = []

with open("ddm_results.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        row["drift_rate"] = float(row["drift_rate"])
        row["boundary"] = float(row["boundary"])
        row["accuracy_percent"] = float(row["accuracy_percent"])
        row["mean_decision_time_seconds"] = float(
            row["mean_decision_time_seconds"]
        )
        results.append(row)
        drift_rates.add(row["drift_rate"])
        boundaries.add(row["boundary"])

drift_rates = sorted(drift_rates)
boundaries = sorted(boundaries)

plt.figure(figsize=(8, 5))
for boundary in boundaries:
    selected = [
        row for row in results
        if row["boundary"] == boundary
    ]
    selected.sort(key=lambda row: row["drift_rate"])
    x = [row["drift_rate"] for row in selected]
    y = [row["accuracy_percent"] for row in selected]
    plt.plot(x, y, marker="o", label=f"Boundary = {boundary}")

plt.xlabel("Evidence Strength (Drift Rate)")
plt.ylabel("Choice Accuracy (%)")
plt.title("Evidence Strength and  Choice Accuracy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("accuracy_by_drift.png", dpi=300)
plt.show()

plt.figure(figsize=(8, 5))
for drift in drift_rates:
    selected = [
        row for row in results
         if row["drift_rate"] == drift
    ]
    selected.sort(key=lambda row: row["boundary"])
    x = [row["boundary"] for row in selected]
    y = [
        row["mean_decision_time_seconds"]
        for row in selected
    ]
    plt.plot(x, y, marker="o", label=f"Drift = {drift}")

plt.xlabel("Decision Boundary Separation")
plt.ylabel("Mean Decision Time (seconds)")
plt.title("Decision Boundary Separation and Decision Tme")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("decision_time_by_boundary.png", dpi=300)
plt.show()
print("Both graphs have been saved successfully!")
