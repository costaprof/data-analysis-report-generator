import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def generate_summary(analysis_results):
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    prompt = f"""
    You are a professional data analyst. Below are the results of an analysis performed on an Amazon product dataset.
    Write a comprehensive, professional, plain-English summary of these findings.
    Cover the overall picture, ratings, pricing and discounts, category insights, and data quality.
    Be specific — use the actual numbers from the data.

    Here is the analysis data:

    Overview:
    - Total Products: {analysis_results['overview']['total_products']}
    - Total Categories: {analysis_results['overview']['total_categories']}
    - Total Reviews: {analysis_results['overview']['total_reviews']}

    Ratings:
    - Average Rating: {analysis_results['ratings']['average_rating']}
    - Top 5 Rated Products: {analysis_results['ratings']['top_5_products']}

    Pricing:
    - Average Discount: {analysis_results['pricing']['average_discount']}%
    - Average Actual Price: ₹{analysis_results['pricing']['average_actual_price']}
    - Price Range: ₹{analysis_results['pricing']['min_price']} - ₹{analysis_results['pricing']['max_price']}
    - Top 5 Most Discounted: {analysis_results['pricing']['top_5_discounted']}

    Categories:
    - Top 10 by Product Count: {analysis_results['categories']['top_10_by_count']}
    - Average Rating by Category: {analysis_results['categories']['avg_rating_by_category']}

    Data Quality:
    - Missing Values per Column: {analysis_results['data_quality']['missing_values']}
    - Total Missing Values: {analysis_results['data_quality']['total_missing']}

    Write the summary in a professional tone suitable for a business report.
    """

    response = model.generate_content(prompt)
    return response.text