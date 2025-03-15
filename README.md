**Big Data Analysis Project: eCommerce User Behavior Analysis**

## **1. Introduction**
This report details the end-to-end process of analyzing user behavior in an eCommerce store using Python and Power BI. The project covers data collection, cleaning, analysis, and visualization to extract meaningful insights.

---

## **2. Data Sources and Collection Methods**
### **Data Source:**
The dataset was obtained from **Kaggle**, titled "eCommerce behavior data from a multi-category store." It includes user interactions such as product views, cart additions, removals, and purchases.

### **Collection Method:**
- The dataset was **downloaded automatically** using the Kaggle API.
- A **Python script** selects and processes the latest month’s data.
- Due to system limitations, **only 10% of the original dataset** is sampled for analysis.
- The script runs **monthly using Windows Task Scheduler** to update data.

---

## **3. Data Cleaning and Transformation**
To ensure data consistency and efficiency, the following cleaning steps were performed:

### **Cleaning Steps:**
- **Converted** `event_time` to datetime format.
- **Removed duplicate records** to avoid redundant data.
- **Dropped the `category_code` column** due to missing values and redundancy.
- **Filled missing `brand` values** with "Unavailable" to maintain consistency.
- **Added an `event_id` column** to uniquely identify each event.

### **Data Reduction for Local Processing:**
- **Sampled 10%** of the dataset to keep it manageable for local execution.
- **Filtered only the latest month’s CSV file** for analysis.

---

## **4. Data Analysis and Insights**
### **Exploratory Data Analysis (EDA):**
- **Event Type Distribution:** A pie chart was created to visualize the frequency of user actions (`view`, `cart`, `remove_from_cart`, `purchase`).
- **Top 5 Brands Analysis:** A stacked column chart was used to compare the top brands by total events and purchase conversions.
- **Sales Trends:** A line chart was used to track purchases over time.

### **Key Insights:**
- **Cart abandonment is high**, indicating a need for marketing strategies to improve conversions.
- **Certain brands have high engagement but low purchases,** suggesting pricing or trust issues.
- **Peak purchase hours were identified,** which can help optimize ad placements and promotions.

---

## **5. Using the Power BI Dashboard**
The Power BI dashboard provides an interactive view of the analysis. It includes:

### **Dashboard Components:**
1. **Event Type Distribution (Pie Chart)** – Shows the frequency of different user actions.
2. **Top Brands by Events and Purchases (Stacked Column Chart)** – Displays total interactions per brand and purchase conversion rates.
3. **Sales Over Time (Line Chart)** – Trends in purchases over a given period.

### **How to Use the Dashboard:**
- **Filters:** Users can filter by date, brand, and event type.
- **Interactive Elements:** Click on any section to drill down into details.
- **Live Updates:** The dataset refreshes monthly through automated data collection and processing.

---

## **6. Conclusion and Future Work**
This project successfully analyzed eCommerce user behavior, providing insights into sales trends, brand engagement, and customer behavior. Future improvements may include:
- **Incorporating predictive analytics** for demand forecasting.
- **Enhancing customer segmentation** using clustering techniques.
- **Integrating real-time data streaming** for live business intelligence.

This structured approach allows businesses to make data-driven decisions, optimize sales strategies, and improve user engagement on eCommerce platforms.

