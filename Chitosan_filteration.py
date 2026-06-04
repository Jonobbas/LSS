import pandas as pd
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches

# -----------------------------
# Baseline Data
# -----------------------------

data = {
    "Parameter": [
        "Oil Yield (%)", "EPA (%)", "DHA (%)",
        "Peroxide Value (meq/kg)", "Anisidine Value", "TOTOX",
        "Free Fatty Acid (%)", "Moisture (%)",
        "Lead Pb (mg/kg)", "Cadmium Cd (mg/kg)", "Mercury Hg (mg/kg)"
    ],
    "Current_Value": [12, 8, 10, 12, 20, 44, 3.5, 0.8, 0.25, 0.08, 0.12],
    "Target_Value": [18, 10, 12, 5, 10, 20, 1.5, 0.2, 0.10, 0.05, 0.05],
    "Direction": [
        "Higher Better", "Higher Better", "Higher Better",
        "Lower Better", "Lower Better", "Lower Better",
        "Lower Better", "Lower Better", "Lower Better",
        "Lower Better", "Lower Better"
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# Pure Chitosan Treatment Assumptions
# -----------------------------
# Note: Chitosan is treated here as a bio-based adsorbent/purification material,
# not as an enzyme.

chitosan_effect = {
    "Oil Yield (%)": 0.00,
    "EPA (%)": 0.02,
    "DHA (%)": 0.02,
    "Peroxide Value (meq/kg)": -0.35,
    "Anisidine Value": -0.30,
    "TOTOX": -0.32,
    "Free Fatty Acid (%)": -0.40,
    "Moisture (%)": -0.25,
    "Lead Pb (mg/kg)": -0.45,
    "Cadmium Cd (mg/kg)": -0.40,
    "Mercury Hg (mg/kg)": -0.50
}

def apply_chitosan(row):
    effect = chitosan_effect[row["Parameter"]]
    return round(row["Current_Value"] * (1 + effect), 3)

df["After_Chitosan_Treatment"] = df.apply(apply_chitosan, axis=1)

def check_status(row, value_column):
    value = row[value_column]
    target = row["Target_Value"]

    if row["Direction"] == "Higher Better":
        return "Achieved" if value >= target else "Gap"
    else:
        return "Achieved" if value <= target else "Gap"

df["Baseline_Status"] = df.apply(lambda row: check_status(row, "Current_Value"), axis=1)
df["After_Chitosan_Status"] = df.apply(lambda row: check_status(row, "After_Chitosan_Treatment"), axis=1)

# -----------------------------
# Export CSV
# -----------------------------

csv_file = "chitosan_gap_analysis_report.csv"
df.to_csv(csv_file, index=False)

# -----------------------------
# Generate Chart
# -----------------------------

plt.figure(figsize=(14, 7))
plt.plot(df["Parameter"], df["Current_Value"], marker="o", label="Current Value")
plt.plot(df["Parameter"], df["After_Chitosan_Treatment"], marker="o", label="After Chitosan Treatment")
plt.plot(df["Parameter"], df["Target_Value"], marker="o", label="Target Value")

plt.xticks(rotation=75, ha="right")
plt.ylabel("Value")
plt.title("Indian Oil Sardine Quality Gap: Pure Chitosan Treatment Simulation")
plt.legend()
plt.tight_layout()

chart_file = "chitosan_treatment_chart.png"
plt.savefig(chart_file, dpi=300)
plt.close()

# -----------------------------
# Generate Word Report
# -----------------------------

doc = Document()

doc.add_heading("Indian Oil Sardine Quality Gap Analysis Report", level=1)

doc.add_paragraph(
    "This report presents a preliminary simulation of quality improvement in Indian Oil Sardine marine lipid "
    "intermediate after treatment with pure chitosan. Chitosan is considered here as a bio-based purification "
    "adsorbent and not as an enzyme."
)

doc.add_heading("1. Objective", level=2)
doc.add_paragraph(
    "The objective of this simulation is to evaluate whether pure chitosan treatment can reduce key quality gaps "
    "in crude marine lipid parameters such as oxidation value, free fatty acid content, moisture, and heavy metals."
)

doc.add_heading("2. Simulation Assumption", level=2)
doc.add_paragraph(
    "The percentage improvement values used in this model are assumed values for early-stage hypothesis testing. "
    "These values must be replaced with actual laboratory data after experimental validation."
)

doc.add_heading("3. Quality Gap Table", level=2)

table = doc.add_table(rows=1, cols=len(df.columns))
table.style = "Table Grid"

hdr_cells = table.rows[0].cells
for i, col in enumerate(df.columns):
    hdr_cells[i].text = col

for _, row in df.iterrows():
    row_cells = table.add_row().cells
    for i, value in enumerate(row):
        row_cells[i].text = str(value)

doc.add_heading("4. Comparative Chart", level=2)
doc.add_picture(chart_file, width=Inches(6.5))

doc.add_heading("5. Interpretation", level=2)

for _, row in df.iterrows():
    if row["After_Chitosan_Status"] == "Achieved":
        doc.add_paragraph(f"{row['Parameter']}: Target achieved after chitosan treatment.")
    else:
        doc.add_paragraph(f"{row['Parameter']}: Gap remains after chitosan treatment.")

doc.add_heading("6. Key Conclusion", level=2)
doc.add_paragraph(
    "Pure chitosan treatment may support improvement in free fatty acid reduction, moisture reduction, oxidation "
    "control, and heavy-metal reduction. However, pure chitosan alone is unlikely to significantly improve oil yield, "
    "EPA, and DHA levels. Therefore, the complete proposed architecture should include low-temperature extraction, "
    "enzymatic liquefaction, chitosan-assisted purification, and oxidation-controlled stabilization."
)

word_file = "Indian_Oil_Sardine_Chitosan_Report.docx"
doc.save(word_file)

print("Report generated successfully.")
print("Word file:", word_file)
print("Chart file:", chart_file)
print("CSV file:", csv_file)
