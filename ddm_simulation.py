import random 
import csv

TIME_STEP = 0.01
MAX_TIME = 10.0
TRIALS_PER_CONDITION = 1000
NOISE = 1.0

DRIFT_RATES = [0.2, 0.5, 0.8]
BOUNDARIES = [0.5, 1.0, 1.5]

random.seed(42)

def simulate_trial(drift, boundary):
    """Simulate one evidence-accumulation decision."""
    position = boundary / 2
    elapsed_time = 0.0
    while elapsed_time < MAX_TIME:
        noise_change = (
            NOISE
            * (TIME_STEP ** 0.5)
            * random.gauss(0, 1)
        )

        position += drift * TIME_STEP + noise_change
        elapsed_time += TIME_STEP

        if position >= boundary:
            return "Option A", elapsed_time

        if position <= 0:
            return "Option B", elapsed_time
    return "Incomplete", elapsed_time

def run_experiment():
    """Run every combination of drift and boundary."""

    summary_results = []
    trial_results = []

    for drift in DRIFT_RATES:
        for boundary in BOUNDARIES:
            correct = 0
            incorrect = 0
            incomplete = 0
            decision_times = []

            for trial in range(1, TRIALS_PER_CONDITION + 1):
                choice, decision_time = simulate_trial(
                    drift, boundary
                )

                trial_results.append({
                    "drift_rate": drift,
                    "boundary": boundary,
                    "trial": trial,
                    "choice": choice,
                    "decision_time_seconds": round(
                        decision_time, 4
                    )
                })

                if choice == "Option A":
                    correct += 1
                    decision_times.append(decision_time)

                elif choice == "Option B":
                    incorrect += 1
                    decision_times.append(decision_time)

                else:
                    incomplete += 1

            completed = correct + incorrect

            accuracy = (
                correct / completed * 100
                if completed > 0 else 0
            )

            mean_time = (
                sum(decision_times) / len(decision_times)
                if decision_times else 0
            )

            summary_results.append({
                "drift_rate": drift,
                "boundary": boundary,
                "trials": TRIALS_PER_CONDITION,
                "correct": correct,
                "incorrect": incorrect,
                "incomplete": incomplete,
                "accuracy_percent": round(accuracy, 2),
                "mean_decision_time_seconds": round(
                    mean_time, 4
                )
            })

    return summary_results, trial_results

def save_results(results):
    """Save condition-level summary results."""
    with open("ddm_results.csv", "w", newline="") as file:
        fieldnames = [
            "drift_rate",
            "boundary",
            "trials",
            "correct",
            "incorrect",
            "incomplete",
            "accuracy_percent",
            "mean_decision_time_seconds"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def save_trial_results(results):
    """Save the results of individual trials."""
    with open("ddm_trial_results.csv", "w", newline="") as file:
        fieldnames = [
            "drift_rate",
            "boundary",
            "trial",
            "choice",
            "decision_time_seconds"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

def main():
    print("DDM RESEARCH SIMULATION")
    print("=======================")
    print("Running experiments...")
    print()
    summary_results, trial_results = run_experiment()
    for result in summary_results:
        print(
            f"Drift: {result['drift_rate']} | "
            f"Boundary: {result['boundary']} | "
            f"Accuracy: {result['accuracy_percent']}% | "
            f"Mean time: "
            f"{result['mean_decision_time_seconds']} seconds | "
            f"Incomplete: {result['incomplete']}"
        )

    save_results(summary_results)
    save_trial_results(trial_results)
    print()
    print("Experiment complete!")
    print("Summary saved to: ddm_results.csv")
    print("Individual trials saved to: ddm_trial_results.csv")
    print(f"Total individual trials: {len(trial_results)}")

if __name__ == "__main__":
    main()

                
