# Power BI Dashboard Setup & Architecture Guide
## Cycle-Based Women's Productivity Analysis

This document provides step-by-step instructions to create a 3-page interactive Power BI report matching **Phase 9** requirements using the generated dataset `womens_cycle_productivity_dataset.csv`.

---

## 1. Data Source & Import Setup
1. Open **Power BI Desktop**.
2. Click **Get Data** $\to$ **Text/CSV**.
3. Select `data/womens_cycle_productivity_dataset.csv`.
4. Click **Transform Data** (Power Query):
   - Change `Cycle_Phase` to Text data type.
   - Change `Sleep_Hours` and `Productivity_Score` to Decimal Number.
   - Change `Stress_Level`, `Pain_Level`, `Mood_Score`, `Energy_Level`, `Age` to Whole Number.
5. Click **Close & Apply**.

---

## 2. DAX Measures Library
Create a dedicated measure table `_Measures` and add the following DAX calculations:

```dax
// 1. Executive KPIs
Average Productivity = AVERAGE(womens_cycle_productivity_dataset[Productivity_Score])

Average Sleep = AVERAGE(womens_cycle_productivity_dataset[Sleep_Hours])

Average Stress = AVERAGE(womens_cycle_productivity_dataset[Stress_Level])

Average Mood = AVERAGE(womens_cycle_productivity_dataset[Mood_Score])

Average Energy = AVERAGE(womens_cycle_productivity_dataset[Energy_Level])

// 2. Advanced Performance Metrics
Productivity Delta vs Baseline = 
VAR OverallAvg = CALCULATE([Average Productivity], ALL(womens_cycle_productivity_dataset))
RETURN [Average Productivity] - OverallAvg

High Stress Employee Count = 
CALCULATE(
    COUNTROWS(womens_cycle_productivity_dataset),
    womens_cycle_productivity_dataset[Stress_Level] >= 7
)

Sleep Deficiency Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(womens_cycle_productivity_dataset), womens_cycle_productivity_dataset[Sleep_Hours] < 7.0),
    COUNTROWS(womens_cycle_productivity_dataset),
    0
)
```

---

## 3. Page Layouts & Visual Configurations

### Page 1: Executive Dashboard
- **Header**: Title Banner ("Cycle-Based Women's Productivity Overview") + Slicers (Age Range, Work Mode).
- **KPI Cards Row** (4 Cards):
  1. `[Average Productivity]` (Formatted: 0.0)
  2. `[Average Sleep]` (Formatted: 0.0 hrs)
  3. `[Average Stress]` (Formatted: 0.0 / 10)
  4. `[Average Mood]` (Formatted: 0.0 / 10)
- **Main Bar Chart**: `Cycle_Phase` vs `[Average Productivity]` sorted by phase order (Menstrual, Follicular, Ovulation, Luteal).
- **Donut Chart**: `Work_Mode` distribution (Remote vs Hybrid vs In-Office).

---

### Page 2: Cycle Phase Dashboard
- **Slicer**: `Cycle_Phase` Single-select Pills.
- **Visual 1 (Bar Chart)**: `[Average Productivity]` by `Cycle_Phase` with Data Labels.
- **Visual 2 (Grouped Bar Chart)**: `[Average Stress]` by `Cycle_Phase` vs `[Average Mood]`.
- **Visual 3 (Clustered Column Chart)**: `[Average Energy]` vs `[Average Pain]` per Phase.
- **Matrix Visual**: Summary Table detailing Count of Women, Avg Sleep, Avg Stress, Avg Pain, Avg Energy, and Avg Productivity for each phase.

---

### Page 3: Productivity Drivers & Factor Impact
- **Scatter Plot 1**: X-Axis = `Sleep_Hours`, Y-Axis = `Productivity_Score`, Legend = `Cycle_Phase`, Trendline = Linear Regression.
- **Scatter Plot 2**: X-Axis = `Stress_Level`, Y-Axis = `Productivity_Score`, Trendline = Negative Exponential.
- **Box Plot**: Category = `Pain_Level` (1-10), Y-Axis = `Productivity_Score`.
- **Decomposition Tree Visual**: Analyzes drivers of low productivity scores (< 50) split by `Cycle_Phase` $\to$ `Stress_Level` $\to$ `Sleep_Hours`.

---

## 4. Theme & Color Palette Specification
- **Background**: Dark Navy (`#0B0F19`)
- **Card Fill**: Translucent Glass Slate (`#161C2D`)
- **Accent Palette**:
  - Menstrual Phase: Coral Red (`#E63946`)
  - Follicular Phase: Soft Teal (`#457B9D`)
  - Ovulation Phase: Vibrant Green (`#2A9D8F`)
  - Luteal Phase: Deep Orange (`#E76F51`)
