from analyser import analyze_file
from ai_summary import generate_summary
from report_generator import generate_report


def main():
    file_path = "sample_data/amazon.csv"

    print("Analysing data...")
    analysis_results = analyze_file(file_path)

    print("Generating AI summary...")
    ai_summary = generate_summary(analysis_results)

    print("Building report...")
    output_path = generate_report(analysis_results, ai_summary)

    print(f"Done! Open {output_path} in your browser to view the report.")


if __name__ == "__main__":
    main()