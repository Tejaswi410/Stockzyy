
# 📈 Stockzyy  

**Stockzyy** is a Streamlit-powered web application for finance and stock price prediction. It allows you to explore historical stock data and visualize trends using an intuitive interface. The application also includes a predictive analytics feature powered by machine learning models.
Check out the live application: [Stockzyy](https://stockzyy.streamlit.app)

---

## ✨ Features  

* **Interactive Homepage**: An easy-to-use dashboard to search for companies and view stock details.
* **Historical Data**: View the last 3 months of historical stock data in a table.
* **Real-time Charts**: Visualize historical data with interactive line charts.
* **Predictive Analytics**: Forecast future stock prices using a Prophet machine learning model.
* **Model Accuracy**: Use cross-validation to evaluate the model's past performance and accuracy metrics like MAPE, MAE, and RMSE.
* **Fast & Simple UI**: Built with the Streamlit framework for quick interactions.

---

## ⚙️ Installation  

1.  **Clone this repository**
    ```bash
    git clone [https://github.com/Tejaswi410/Stockzyy.git](https://github.com/Tejaswi410/Stockzyy.git)
    cd Stockzyy
    ```

3.  **(Optional) Create a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # For Windows: venv\Scripts\activate
    ```

5.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Usage  

Run the Streamlit app:  

```bash
streamlit run 1_🏠_Homepage.py
````

Open the local server (usually `http://localhost:8501`) and:

  * **Search for a company** from the provided `tickers.csv` list.
  * **View historical price charts** and company summaries.
  * **Explore model-based predictions** on the "Stock Prediction" page.

## 🔧 Configuration

  * `requirements.txt`: Lists all the required Python libraries, including `streamlit`, `yfinance`, `prophet`, and `pandas`.
  * `tickers.csv`: Contains a list of company names and their corresponding stock ticker symbols.
  * **Data Source**: The application uses the `yfinance` library to fetch stock data.


## 🤝 Contributing

Contributions are welcome\! Please fork the repo and submit pull requests with improvements. Make sure to test new features locally and update documentation as needed.


