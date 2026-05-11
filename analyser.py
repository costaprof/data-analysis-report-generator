import pandas as pd


def analyze_file(file_path):
    df = pd.read_csv(file_path)

    # Clean price columns by removing ₹ and commas
    df['actual_price'] = df['actual_price'].str.replace('₹', '').str.replace(',', '').astype(float)
    df['discounted_price'] = df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
    df['discount_percentage'] = df['discount_percentage'].str.replace('%', '').astype(float)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_count'] = df['rating_count'].str.replace(',', '').astype(float)

    # Clean categories (take only the top-level category)
    df['main_category'] = df['category'].str.split('|').str[0]

    results = {
        'overview': {
            'total_products': len(df),
            'total_categories': df['main_category'].nunique(),
            'total_reviews': int(df['rating_count'].sum())
        },
        'ratings': {
            'average_rating': round(df['rating'].mean(), 2),
            'top_5_products': df[df['rating_count'] >= 1000].nlargest(5, 'rating')[['product_name', 'rating', 'rating_count']].to_dict('records')
        },
        'pricing': {
            'average_discount': round(df['discount_percentage'].mean(), 2),
            'average_actual_price': round(df['actual_price'].mean(), 2),
            'min_price': df['actual_price'].min(),
            'max_price': df['actual_price'].max(),
            'top_5_discounted': df.nlargest(5, 'discount_percentage')[['product_name', 'discount_percentage']].to_dict('records')
        },
        'categories': {
            'top_10_by_count': df['main_category'].value_counts().head(10).to_dict(),
            'avg_rating_by_category': df.groupby('main_category')['rating'].mean().round(2).to_dict()
        },
        'data_quality': {
            'missing_values': df.isnull().sum().to_dict(),# Without defining a column, df works on every column automatically and provides a total value per column
            'total_missing': int(df.isnull().sum().sum())
        }
    }

    return results