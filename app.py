# Streamlit Cost Comparison App

This app allows users to input estimated and actual cost data for composite manufacturing projects. It automatically calculates and compares costs by labor, office work, machinery, and material. Pricing is fixed and displayed for transparency.

## 💰 Fixed Unit Prices (USD)
| Category        | Unit Price (USD/hour) |
|----------------|------------------------|
| Labor          | 10                     |
| Office         | 15                     |
| CNC            | 25                     |
| Robot          | 30                     |
| Autoclave      | 35                     |

## 🧮 Sections

### 1. Input Estimated Cost (Estimate Sheet)
Input estimated values for each component:
- Labor hours
- Office hours
- CNC hours
- Robot hours
- Autoclave hours
- Material cost (USD)
- Margin (%)

**Example Input Table:**
| Category     | Unit      | Value (Estimated) |
|--------------|-----------|-------------------|
| Labor Hours  | hr        | 200               |
| Office Hours | hr        | 50                |
| CNC Hours    | hr        | 30                |
| Robot Hours  | hr        | 10                |
| Autoclave    | hr        | 15                |
| Material     | USD       | 5,000             |
| Margin       | %         | 15                |

### 2. Input Actual Cost (Actual Sheet)
Input actual values similarly:
- Labor hours
- Office hours
- CNC hours
- Robot hours
- Autoclave hours
- Material cost (USD)

**Example Input Table:**
| Category     | Unit      | Value (Actual)    |
|--------------|-----------|-------------------|
| Labor Hours  | hr        | 220               |
| Office Hours | hr        | 40                |
| CNC Hours    | hr        | 35                |
| Robot Hours  | hr        | 12                |
| Autoclave    | hr        | 10                |
| Material     | USD       | 5,200             |

### 3. Output Comparison Table
Automatically compute:
- Cost by category (Estimated)
- Cost by category (Actual)
- Total cost (Estimated)
- Selling Price = Total Estimate × (1 + Margin)
- Total Actual Cost
- Comparison between:
  - Estimated vs Actual
  - Estimated vs Selling Price
  - Selling Price vs Actual

**Example Output Table:**
| Category     | Estimated Cost | Actual Cost | Difference |
|--------------|----------------|-------------|------------|
| Labor        | $2,000         | $2,200      | $200       |
| Office       | $750           | $600        | -$150      |
| CNC          | $750           | $875        | $125       |
| Robot        | $300           | $360        | $60        |
| Autoclave    | $525           | $350        | -$175      |
| Material     | $5,000         | $5,200      | $200       |
| **Total**    | **$9,325**     | **$9,585**  | **$260**   |
| Margin       | 15%            | N/A         | N/A        |
| **Selling Price** | **$10,724**    |             |            |

## 📌 Notes
- Unit prices are **fixed** and **not editable** via UI.
- All inputs support decimal numbers (e.g., `10.5`).
- All currency is in **USD** only.

---

Next steps:
- Create a `streamlit_app.py` file implementing this UI logic.
- Layout: Two columns side-by-side for Estimate vs Actual input.
- Output section below for computed comparison table.
- Optional export to Excel or PDF.

Let me know if you'd like the full Python/Streamlit code for this logic!
