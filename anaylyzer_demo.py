
from nutriscan.label_analyzer import analyze_ocr_file


try:
    report = analyze_ocr_file(
        input_path="data/processed/selected_rows_ocr.txt",
        output_path="data/processed/nutrition_results.json",
    )

    print("\n========== TATVA ANALYSIS ==========\n")

    for item in report["nutrients"]:
        print(
            f"{item['nutrient']:<16} "
            f"| Value: {item['value']} "
            f"{item['unit'] or ''} "
            f"| RDA: {item['rda_percent']}% "
            f"| Status: {item['review_status']}"
        )

    print("\n========== WARNINGS ==========\n")

    if report["warnings"]:
        for warning in report["warnings"]:
            print("-", warning)
    else:
        print("No basic quality warnings.")

    print("\nReady for scoring:", report["ready_for_scoring"])
    print("JSON saved to:", report["output_file"])

except Exception as error:
    print("TATVA analysis failed:", error)
