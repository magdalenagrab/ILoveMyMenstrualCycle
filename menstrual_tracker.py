import json
import matplotlib.pyplot as plt

# --- Define cycle phases by day ---
CYCLE_PHASES = {
    "Menstruation": range(1, 6),
    "Follicular": range(6, 13),
    "Ovulation": range(13, 18),
    "Luteal": range(18, 29)
}

# --- Load JSON data ---
with open("sample_cycle_data.json", "r", encoding="utf-8") as f:
    months_data = json.load(f)

# --- Aggregate mood + notes by phase ---
phase_summary = {}

for month in months_data:
    month_name = month["month"]
    phase_summary[month_name] = {}
    for phase, days_range in CYCLE_PHASES.items():
        # Collect moods and notes
        moods = [day["mood"] for day in month["days"] if day["day"] in days_range]
        notes = [day["note"] for day in month["days"] if day["day"] in days_range]

        avg_mood = sum(moods) / len(moods) if moods else None
        joined_notes = " | ".join(notes) if notes else "(no notes)"

        phase_summary[month_name][phase] = {
            "avg_mood": avg_mood,
            "notes": joined_notes
        }

# --- Print summary table ---
print("\nMood Summary by Month and Phase:")
print("{:<10} {:<12} {:<12} {:<12} {:<12}".format("Month", "Menstruation", "Follicular", "Ovulation", "Luteal"))
for month, phases in phase_summary.items():
    print("{:<10} {:<12} {:<12} {:<12} {:<12}".format(
        month,
        round(phases["Menstruation"]["avg_mood"], 1) if phases["Menstruation"]["avg_mood"] else "-",
        round(phases["Follicular"]["avg_mood"], 1) if phases["Follicular"]["avg_mood"] else "-",
        round(phases["Ovulation"]["avg_mood"], 1) if phases["Ovulation"]["avg_mood"] else "-",
        round(phases["Luteal"]["avg_mood"], 1) if phases["Luteal"]["avg_mood"] else "-"
    ))

# --- Print notes grouped by phase ---
print("\nDetailed Notes per Phase:")
for month, phases in phase_summary.items():
    print(f"\n{month.upper()}")
    for phase, data in phases.items():
        print(f"  {phase}: {data['notes']}")

# --- Plot mood per phase across months ---
phases_list = list(CYCLE_PHASES.keys())
for month, phases in phase_summary.items():
    moods = [phases[p]["avg_mood"] if phases[p]["avg_mood"] is not None else 0 for p in phases_list]
    plt.plot(phases_list, moods, marker='o', label=month)

plt.title("Average Mood per Cycle Phase")
plt.xlabel("Cycle Phase")
plt.ylabel("Average Mood (1-10)")
plt.ylim(0, 10)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("mood_summary.png", dpi=300)
plt.show()
