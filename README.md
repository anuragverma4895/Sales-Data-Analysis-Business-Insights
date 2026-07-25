<div align="center">

# Sales Data Analysis & Business Insights

### Interactive 3D Dashboard for Sales Intelligence

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**A professional-grade, deployment-ready analytics dashboard** that transforms raw sales data into actionable business insights with stunning 3D interactive visualizations, real-time filtering, and AI-generated strategic recommendations.

---

[Features](#-features) · [Tech Stack](#-tech-stack) · [Installation](#-installation) · [Deployment](#-deployment) · [Project Structure](#-project-structure)

</div>

---

## ✨ Features

### 📊 6-Page Interactive Dashboard
- **Overview** — KPI cards, revenue trends, category breakdown, regional performance
- **Revenue & Trends** — Monthly analysis, YoY growth, seasonal patterns, 3D surface plot
- **Regional Analysis** — City-level breakdown, radar comparisons, 3D geographic visualization
- **Product Performance** — Top/bottom products, treemap, 3D scatter analysis
- **Customer Insights** — Segmentation, payment modes, discount impact analysis
- **Business Insights** — Auto-generated findings, heatmaps, strategic recommendations

### 🎯 3D Interactive Visualizations
| Chart | Dimensions | Purpose |
|-------|-----------|---------|
| Revenue Surface | Month × Category × Revenue | Seasonal & category trends |
| City Performance | City × Category × Revenue | Regional breakdown |
| Product Scatter | Quantity × Price × Profit | Price-volume-profit analysis |
| Customer Bubbles | Segment × Revenue × Profit | Customer segment analysis |

### 🎨 Premium UI/UX
- Dark theme with glass-morphism effects
- Material Design Icons (no emojis in UI)
- Gradient accents (Indigo → Purple → Pink)
- Smooth hover animations & transitions
- Fully responsive layout
- Custom Google Fonts (Inter, Outfit)

### 📈 Real Data Analysis
- **2,500+ orders** spanning 2 years (2023-2024)
- **22 Indian cities** with population-weighted distribution
- **5 product categories** with 25+ sub-categories
- Realistic seasonal patterns (Diwali, Black Friday spikes)
- Proper profit margins per category
- Real Indian product names & brands

---

## 🛠 Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.9+** | Core programming language |
| **Streamlit** | Web dashboard framework |
| **Plotly** | Interactive 2D & 3D visualizations |
| **Pandas** | Data manipulation & analysis |
| **NumPy** | Numerical computations |

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/anuragverma4895/Sales-Data-Analysis-Business-Insights.git
cd Sales-Data-Analysis-Business-Insights
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate the dataset** (if not already present)
```bash
python generate_data.py
```

4. **Launch the dashboard**
```bash
streamlit run app.py
```

5. Open your browser at `http://localhost:8501`

---

## ☁️ Deployment

### Streamlit Community Cloud (Recommended)
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repository → `app.py` → Deploy
5. Your dashboard will be live with a shareable URL

### Heroku (Alternative)
```bash
heroku create your-app-name
git push heroku main
```
The `Procfile` and `setup.sh` are already configured for Heroku deployment.

---

## 📁 Project Structure

```
Sales-Data-Analysis-Business-Insights/
├── .streamlit/
│   └── config.toml          # Streamlit theme configuration
├── analysis/
│   ├── __init__.py           # Package init
│   └── data_processor.py     # Core analytics engine
├── assets/
│   └── style.css             # Custom CSS (glass-morphism, animations)
├── data/
│   └── sales_data.csv        # Generated sales dataset
├── app.py                    # Main Streamlit dashboard
├── generate_data.py          # Realistic data generation script
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore                # Git ignore rules
├── Procfile                  # Heroku deployment
├── setup.sh                  # Server configuration
└── LICENSE                   # MIT License
```

---

## 📊 Dataset Details

| Feature | Details |
|---------|---------|
| **Records** | 2,500+ orders |
| **Time Period** | Jan 2023 — Dec 2024 |
| **Cities** | 22 Indian cities (Mumbai, Delhi, Bangalore, etc.) |
| **Categories** | Electronics, Clothing, Furniture, Office Supplies, Food & Beverages |
| **Sub-Categories** | 25+ (Smartphones, Laptops, T-Shirts, Desks, etc.) |
| **Segments** | Consumer (52%), Corporate (30%), Home Office (18%) |
| **Payment Modes** | UPI, Credit Card, Debit Card, Cash, Net Banking |

### Columns
`Order_ID` · `Order_Date` · `Customer_ID` · `Customer_Name` · `Segment` · `City` · `State` · `Region` · `Category` · `Sub_Category` · `Product_Name` · `Quantity` · `Unit_Price` · `Discount` · `Revenue` · `Profit` · `Payment_Mode` · `Ship_Mode`

---

## 🔑 Key Insights Generated

- Top revenue category and its market share
- Most profitable product segments
- Seasonal demand patterns (festive season spikes)
- Regional performance disparities
- Discount impact on profitability
- Customer segment behavior analysis
- Year-over-Year growth metrics
- Strategic business recommendations

---

## 👤 Author

**Anurag Verma**

- GitHub: [@anuragverma4895](https://github.com/anuragverma4895)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with Python, Streamlit, Plotly & Pandas**

</div>
