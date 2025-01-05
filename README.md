# Product Rank Analysis API

This Flask-based web application processes product ranking data from an Excel file to:

1. Identify product IDs with **positive trends**.
2. Identify product IDs with **negative trends**.
3. Predict the next rank for common product IDs across distinct keywords using **Linear Regression**.

---

## Features

### 1. Welcome Endpoint

- **Endpoint**: `/welcome`
- **Method**: `GET`
- **Description**: Confirms the application is running successfully.
- **Response**:
  ```json
  {
    "message": "Application running successfully"
  }
  ```

---

### 2. Identify Positive Trend IDs

- **Endpoint**: `/positive-trend-ids`
- **Method**: `GET`
- **Description**: Finds product IDs with positive trends in rank (improving rank over time).
- **Response**:
  ```json
  {
    "message": "success",
    "data": ["product_id1", "product_id2"]
  }
  ```

---

### 3. Identify Negative Trend IDs

- **Endpoint**: `/negative-trend-ids`
- **Method**: `GET`
- **Description**: Finds product IDs with negative trends in rank (worsening rank over time).
- **Response**:
  ```json
  {
    "message": "success",
    "data": ["product_id3", "product_id4"]
  }
  ```

---

### 4. Predict Next Ranking

- **Endpoint**: `/predict-next-ranking`
- **Method**: `GET`
- **Description**: Predicts the next rank for each distinct keyword and common product IDs using **Linear Regression**.
- **Response**:
  ```json
  {
    "message": "success",
    "data": [
      {
        "keyword": "keyword1",
        "product_id": "product_id1",
        "next_rank": 5.43
      },
      {
        "keyword": "keyword2",
        "product_id": "product_id2",
        "next_rank": 8.21
      }
    ]
  }
  ```

---

## How It Works

1. **File Loading**:

   - The app reads an Excel file (`rank_trend_interview_question.xlsx`) containing the following columns:
     - `keyword`: Keyword associated with the product.
     - `product_id`: Unique identifier of the product.
     - `rank`: Product's rank on a specific date.
     - `rank_date`: Date of the ranking.
   - The data is preprocessed to ensure proper formatting and sorting by `product_id` and `rank_date`.

2. **Positive and Negative Trends**:

   - A **positive trend** means ranks improve (lower number over time).
   - A **negative trend** means ranks worsen (higher number over time).
   - The app calculates these trends by analyzing the rank progression for each product ID.

3. **Prediction**:

   - For **common product IDs** (those appearing in both positive and negative trends), the app predicts the next rank using **Linear Regression**:
     - `Days` are calculated as the difference between each `rank_date` and the earliest `rank_date`.
     - A Linear Regression model is trained using `Days` as the independent variable and `Rank` as the dependent variable.
     - The next rank is predicted for one day beyond the last observed `rank_date`.

---

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Rohit-K-Gaikwad/Product-Rank-Analysis-API.git
   cd Product-Rank-Analysis-API
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   ```bash
   python main.py
   ```

4. **API Endpoints**:

   - Access the API at `http://127.0.0.1:5000`.

---

## Dependencies

The project requires the following Python packages:

- Flask
- pandas
- numpy
- scikit-learn
- openpyxl

You can install them using:

```bash
pip install flask pandas numpy scikit-learn openpyxl
```

---

## Usage

1. **Welcome Message**:

   - Access `http://127.0.0.1:5000/welcome` to confirm the server is running.

2. **Finding Trends**:

   - Use `/positive-trend-ids` or `/negative-trend-ids` to analyze product trends.

3. **Predicting Rankings**:

   - Use `/predict-next-ranking` to get the next rank predictions for common product IDs and keywords.

---

## Notes

- The input Excel file should be named `rank_trend_interview_question.xlsx` and placed in the same directory as the script.
- Ensure the file has the required columns: `keyword`, `product_id`, `rank`, `rank_date`.

---

## License

This project is licensed under the MIT License. Feel free to modify and distribute as needed.

