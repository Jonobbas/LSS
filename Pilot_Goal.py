import pandas as pd
import matplotlib.pyplot as plt

# Baseline data for Indian Oil Sardine - replace with your actual lab values later
baseline = {
    "Parameter": [
        "Oil Yield (%)",
        "EPA (%)",
        "DHA (%)",
        "Peroxide Value (meq/kg)",
        "Anisidine Value",
        "TOTOX",
        "Free Fatty Acid (%)",
        "Moisture (%)",
        "Lead Pb (mg/kg)",
        "Cadmium Cd (mg/kg)",
        "Mercury Hg (mg/kg)"
    ],
    "Current_Value": [
        12, 8, 10, 12, 20, 44, 3.5, 0.8, 0.25, 0.08, 0.12
    ],
    "Target_Value": [
        18, 10, 12, 5, 10, 20, 1.5, 0.2, 0.10, 0.05, 0.05
    ],
    "Direction": [
        "Higher Better",
        "Higher Better",
        "Higher Better",
        "Lower Better",
        "Lower Better",
        "Lower Better",
        "Lower Better",
        "Lower Better",
        "Lower Better",
        "Lower Better",
        "Lower Better"
    ]
}

df = pd.DataFrame(baseline)

def gap_status(row):
    current = row["Current_Value"]
    target = row["Target_Value"]
    
    if row["Direction"] == "Higher Better":
        gap = current - target
        status = "Pass" if current >= target else "Gap"
    else:
        gap = target - current
        status = "Pass" if current <= target else "Gap"
        
    return pd.Series([gap, status])

df[["Gap_Value", "Status"]] = df.apply(gap_status, axis=1)

print("Indian Oil Sardine Baseline Quality Gap Analysis")
display(df)

# Count pass and gap
summary = df["Status"].value_counts()
print("\nSummary:")
print(summary)

# Bar chart
plt.figure(figsize=(12, 6))
plt.bar(df["Parameter"], df["Current_Value"], label="Current Value")
plt.bar(df["Parameter"], df["Target_Value"], alpha=0.5, label="Target Value")
plt.xticks(rotation=75, ha="right")
plt.ylabel("Value")
plt.title("Indian Oil Sardine: Current Quality vs Target Quality")
plt.legend()
plt.tight_layout()
plt.show()

# Final interpretation
print("\nProject Interpretation:")
for _, row in df.iterrows():
    if row["Status"] == "Gap":
        print(f"- {row['Parameter']}: Gap identified. Current = {row['Current_Value']}, Target = {row['Target_Value']}")
