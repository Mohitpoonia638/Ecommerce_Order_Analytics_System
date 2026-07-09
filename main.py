import os

while True:

    print("\n" + "=" * 60)
    print("      E-COMMERCE ORDER ANALYTICS SYSTEM")
    print("=" * 60)

    print("1. Generate Synthetic Data")
    print("2. Inject Data Quality Issues")
    print("3. Clean Data")
    print("4. Load SQLite Database")
    print("5. Run Basic & Intermediate SQL Queries")
    print("6. Run Advanced SQL Queries")
    print("7. Generate Business Report")
    print("8. Run Edge Case Tests")
    print("9. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        os.system("python src/generate_data.py")

    elif choice == "2":
        os.system("python src/inject_data_quality_issues.py")

    elif choice == "3":
        os.system("python src/clean_data.py")

    elif choice == "4":
        os.system("python src/database_loader.py")

    elif choice == "5":
        os.system("python src/basic_intermediate_queries.py")

    elif choice == "6":
        os.system("python src/advanced_queries.py")

    elif choice == "7":
        os.system("python src/report_tool.py")

    elif choice == "8":
        os.system("python src/edge_cases.py")

    elif choice == "9":
        print("\nThank you for using the project.")
        break

    else:
        print("\nInvalid Choice.")