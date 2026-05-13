import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO


def save_chart(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)
    return image_base64


def create_rating_chart(analysis_results):
    categories = list(analysis_results['categories']['avg_rating_by_category'].keys())
    ratings = list(analysis_results['categories']['avg_rating_by_category'].values())

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(categories, ratings, color='#4f8ef7')
    ax.set_xlabel('Average Rating')
    ax.set_title('Average Rating by Category')
    ax.set_xlim(0, 5)
    fig.tight_layout()
    return save_chart(fig)


def create_discount_chart(analysis_results):
    categories = list(analysis_results['categories']['top_10_by_count'].keys())
    counts = list(analysis_results['categories']['top_10_by_count'].values())

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(categories, counts, color='#34c98a')
    ax.set_ylabel('Number of Products')
    ax.set_title('Top 10 Categories by Product Count')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    return save_chart(fig)


def generate_report(analysis_results, ai_summary):
    rating_chart = create_rating_chart(analysis_results)
    discount_chart = create_discount_chart(analysis_results)

    top_5_products_rows = ""
    for product in analysis_results['ratings']['top_5_products']:
        top_5_products_rows += f"""
        <tr>
            <td>{product['product_name'][:80]}...</td>
            <td>{product['rating']}</td>
            <td>{int(product['rating_count'])}</td>
        </tr>"""

    top_5_discounted_rows = ""
    for product in analysis_results['pricing']['top_5_discounted']:
        top_5_discounted_rows += f"""
        <tr>
            <td>{product['product_name'][:80]}...</td>
            <td>{product['discount_percentage']}%</td>
        </tr>"""

    missing_values_rows = ""
    for column, count in analysis_results['data_quality']['missing_values'].items():
        if count > 0:
            missing_values_rows += f"""
        <tr>
            <td>{column}</td>
            <td>{count}</td>
        </tr>"""

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            color: #333;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #4f8ef7;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #4f8ef7;
            margin-top: 40px;
        }}
        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8f9ff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 1px solid #e0e7ff;
        }}
        .stat-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #4f8ef7;
        }}
        .stat-card .label {{
            color: #666;
            margin-top: 5px;
        }}
        .summary-box {{
            background: #f8f9ff;
            border-left: 4px solid #4f8ef7;
            padding: 20px;
            border-radius: 0 10px 10px 0;
            line-height: 1.8;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        th {{
            background: #4f8ef7;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f8f9ff;
        }}
        .chart {{
            width: 100%;
            margin: 20px 0;
            border-radius: 10px;
        }}
        .pricing-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
<div class="container">
    <h1>📊 Automated Data Analysis Report</h1>
    <p style="color:#888;">Amazon Products Dataset</p>

    <h2>🤖 AI Summary</h2>
    <div class="summary-box">{ai_summary}</div>

    <h2>📈 Overview</h2>
    <div class="overview-grid">
        <div class="stat-card">
            <div class="value">{analysis_results['overview']['total_products']:,}</div>
            <div class="label">Total Products</div>
        </div>
        <div class="stat-card">
            <div class="value">{analysis_results['overview']['total_categories']}</div>
            <div class="label">Categories</div>
        </div>
        <div class="stat-card">
            <div class="value">{analysis_results['overview']['total_reviews']:,}</div>
            <div class="label">Total Reviews</div>
        </div>
    </div>

    <h2>⭐ Ratings</h2>
    <div class="stat-card" style="display:inline-block; margin-bottom:20px;">
        <div class="value">{analysis_results['ratings']['average_rating']}</div>
        <div class="label">Average Rating</div>
    </div>
    <table>
        <tr><th>Product</th><th>Rating</th><th>Review Count</th></tr>
        {top_5_products_rows}
    </table>
    <img class="chart" src="data:image/png;base64,{rating_chart}" alt="Rating Chart"/>

    <h2>💰 Pricing & Discounts</h2>
    <div class="pricing-grid">
        <div class="stat-card">
            <div class="value">{analysis_results['pricing']['average_discount']}%</div>
            <div class="label">Average Discount</div>
        </div>
        <div class="stat-card">
            <div class="value">₹{analysis_results['pricing']['average_actual_price']:,}</div>
            <div class="label">Average Price</div>
        </div>
        <div class="stat-card">
            <div class="value">₹{analysis_results['pricing']['min_price']} - ₹{analysis_results['pricing']['max_price']}</div>
            <div class="label">Price Range</div>
        </div>
    </div>
    <table>
        <tr><th>Product</th><th>Discount</th></tr>
        {top_5_discounted_rows}
    </table>

    <h2>🗂️ Categories</h2>
    <img class="chart" src="data:image/png;base64,{discount_chart}" alt="Categories Chart"/>

    <h2>🔍 Data Quality</h2>
    <div class="stat-card" style="display:inline-block; margin-bottom:20px;">
        <div class="value">{analysis_results['data_quality']['total_missing']}</div>
        <div class="label">Total Missing Values</div>
    </div>
    <table>
        <tr><th>Column</th><th>Missing Values</th></tr>
        {missing_values_rows}
    </table>

</div>
</body>
</html>"""

    os.makedirs('output', exist_ok=True)
    output_path = os.path.join('output', 'report.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report saved to {output_path}")
    return output_path