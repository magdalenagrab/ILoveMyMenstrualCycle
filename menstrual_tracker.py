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

# --- Aggregate mood by phase ---
phase_mood_summary = {}

for month in months_data:
    month_name = month["month"]
    phase_mood_summary[month_name] = {}
    for phase, days_range in CYCLE_PHASES.items():
        # Collect moods in phase
        moods = [day["mood"] for day in month["days"] if day["day"] in days_range]
        if moods:
            avg_mood = sum(moods) / len(moods)
        else:
            avg_mood = None
        phase_mood_summary[month_name][phase] = avg_mood

# --- Print summary table ---
print("Mood Summary by Month and Phase:")
print("{:<10} {:<12} {:<12} {:<12} {:<12}".format("Month", "Menstruation", "Follicular", "Ovulation", "Luteal"))
for month, phases in phase_mood_summary.items():
    print("{:<10} {:<12} {:<12} {:<12} {:<12}".format(
        month,
        phases["Menstruation"] if phases["Menstruation"] is not None else "-",
        phases["Follicular"] if phases["Follicular"] is not None else "-",
        phases["Ovulation"] if phases["Ovulation"] is not None else "-",
        phases["Luteal"] if phases["Luteal"] is not None else "-"
    ))

# --- Plot mood per phase across months ---
phases_list = list(CYCLE_PHASES.keys())
for month, phases in phase_mood_summary.items():
    moods = [phases[phase] if phases[phase] is not None else 0 for phase in phases_list]
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
