from flask import Flask, request, send_file, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)


@app.route('/welcome', methods=['GET'])
def welcome():
    return jsonify({"message": "Application running sucessfully"}), 200


def load_file(file_path):
    """
    Loading xlsx file function
    """
    try:
        df = pd.read_excel(file_path)
        required_columns = {'keyword', 'product_id', 'rank', 'rank_date'}
        if not required_columns.issubset(df.columns):
            return jsonify({"error": f"Missing required columns: {required_columns - set(df.columns)}"}), 400
        
        df['rank_date'] = pd.to_datetime(df['rank_date'])
        df.sort_values(by=["product_id", "rank_date"], inplace=True)
        return df
    
    except Exception as e:
        return jsonify({"message":"error in file reading and obtaining df"})
        
        
@app.route('/positive-trend-ids', methods=['GET'])
def find_positive_trend(tag=None, df=None):
    """
    Identify product IDs with a positive trend in ranking.
    A positive trend means rank improves over time (lower number).
    """
    if not tag:
        print("Reqeust received for finding negative trend ids...")
        print("Loading File...")
        file = "rank_trend_interview_question.xlsx"
        df = load_file(file)
        print("File loaded successfully")
        
    try:
        positive_trend = set()
        for product_id, group in df.groupby("product_id"):
            ranks = group["rank"].tolist()
            if ranks == sorted(ranks):
                positive_trend.add(product_id)
        print("List of product id's showling positive trends :: ",positive_trend)
    
        if tag:
            return positive_trend
        else:
            return jsonify({"message":"success", "data":list(positive_trend)}),200
    
    except Exception as e:
        return jsonify({"message":"error in fining positive trend ids"})


@app.route('/negative-trend-ids', methods=['GET'])
def find_negative_trend(tag=None, df=None):
    """
    Identify product IDs with a negative trend in ranking.
    A negative trend means rank worsens over time (higher number).
    """
    if not tag:
        print("Reqeust received for finding negative trend ids")
        print("Loading File...")
        file = "rank_trend_interview_question.xlsx"
        df = load_file(file)
        print("File loaded successfully")
        
    try:
        negative_trend = set()
        for product_id, group in df.groupby("product_id"):
            ranks = group["rank"].tolist()
            if ranks == sorted(ranks, reverse=True):
                negative_trend.add(product_id)
        print("List of product id's showling negative trends :: ",negative_trend)
        if tag:
            return negative_trend
        else:
            return jsonify({"message":"success", "data":list(negative_trend)}),200
    
    except Exception as e:
        return jsonify({"message":"error in fining negative trend ids"}),500


def predict_next_rank(df, common_product_ids):
    """
    Predict the next ranking for each distinct keyword and common product IDs
    using Linear Regression.
    """
    predictions = []
    for keyword, group in df[df['product_id'].isin(common_product_ids)].groupby('keyword'):
        for product_id, sub_group in group.groupby('product_id'):
            sub_group = sub_group.sort_values(by='rank_date')
            dates = (sub_group['rank_date'] - sub_group['rank_date'].min()).dt.days.values.reshape(-1, 1)
            ranks = sub_group['rank'].values

            if len(dates) > 1:  
                model = LinearRegression().fit(dates, ranks)
                next_day = (sub_group['rank_date'].max() - sub_group['rank_date'].min()).days + 1
                next_rank = model.predict([[next_day]])
                predictions.append({
                    "keyword": keyword,
                    "product_id": product_id,
                    "next_rank": round(next_rank[0], 2)
                })
    return predictions


@app.route('/predict-next-ranking', methods=['GET'])
def predict_next_ranking():
    """
    Process an uploaded Excel file to find positive/negative trends 
    and predict the next ranking for each distinct keyword.
    """
    print("Request received for predit next ranking...")
    try:
        print("Loading File...")
        file = "rank_trend_interview_question.xlsx"
        df = load_file(file)
        print("File loaded successfully")
        
        positive_trend = find_positive_trend(tag="predict-next-ranking", df=df)
        negative_trend = find_negative_trend(tag="predict-next-ranking", df=df)
            
        common_product_ids = positive_trend & negative_trend
        predictions = predict_next_rank(df, common_product_ids)
        
        return jsonify({"message":"success", "data":predictions}),200
    
    except Exception as e:
        return jsonify({"message":"error in predict next ranking"}),500

if __name__ == '__main__':
    app.run(debug=True)
