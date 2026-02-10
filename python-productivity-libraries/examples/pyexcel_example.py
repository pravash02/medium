import pyexcel as pe
import os
import csv
from datetime import datetime


def create_sample_csv(filepath):
    rows = [
        ['employee_id', 'name', 'department', 'salary', 'start_date'],
        ['E001', 'Alice Johnson', 'Engineering', 95000, '2023-03-01'],
        ['E002', 'Bob Smith', 'Marketing', 72000, '2022-07-15'],
        ['E003', 'Carol White', 'Engineering', 88000, '2021-11-20'],
        ['E004', 'David Lee', 'HR', 65000, '2024-01-10'],
        ['E005', 'Eve Martinez', 'Engineering', 102000, '2020-06-05'],
        ['', 'INVALID ROW', '', '', ''],  # bad row
        ['E006', 'Frank Wilson', 'Finance', 78000, '2023-09-18'],
    ]
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Created {filepath}")


def process_uploaded_file(file_path):
    print(f"\n--- Processing: {file_path} ---")

    sheet = pe.get_sheet(file_name=file_path)
    data = sheet.to_array()

    if not data:
        return {'error': 'Empty file'}

    headers = [str(h).strip() for h in data[0]]
    rows = data[1:]

    print(f"  Headers   : {headers}")
    print(f"  Raw rows  : {len(rows)}")

    valid_records = []
    error_rows = []

    for idx, row in enumerate(rows, start=2):  # Row 2 = first data row
        while len(row) < len(headers):
            row.append('')

        record = dict(zip(headers, [str(v).strip() for v in row]))

        if not record.get('employee_id') or not record.get('name'):
            error_rows.append({'row': idx, 'reason': 'Missing employee_id or name', 'data': record})
            continue

        try:
            record['salary'] = float(record['salary'])
        except (ValueError, TypeError):
            error_rows.append({'row': idx, 'reason': 'Invalid salary', 'data': record})
            continue

        valid_records.append(record)

    print(f"  Valid     : {len(valid_records)}")
    print(f"  Errors    : {len(error_rows)}")

    if error_rows:
        for err in error_rows:
            print(f"    Row {err['row']}: {err['reason']}")

    return {'records': valid_records, 'errors': error_rows}


def generate_salary_report(records, output_path):
    if not records:
        print("No records to report on.")
        return

    departments = {}
    for r in records:
        dept = r.get('department', 'Unknown')
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(r)

    summary = [['Department', 'Headcount', 'Total Salary', 'Avg Salary', 'Min Salary', 'Max Salary']]

    for dept, emps in sorted(departments.items()):
        salaries = [e['salary'] for e in emps]
        total = sum(salaries)
        avg = total / len(salaries)
        summary.append([
            dept,
            len(emps),
            f"${total:,.0f}",
            f"${avg:,.0f}",
            f"${min(salaries):,.0f}",
            f"${max(salaries):,.0f}",
        ])

    pe.save_as(array=summary, dest_file_name=output_path)
    print(f"\nSaved salary report → {output_path}")

    print(f"\n{'Department':<20} {'HC':>4} {'Total':>12} {'Avg':>10}")
    print("-" * 50)
    for row in summary[1:]:
        print(f"{row[0]:<20} {row[1]:>4} {row[2]:>12} {row[3]:>10}")


def format_converter(input_path, output_format):
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_converted.{output_format}"

    sheet = pe.get_sheet(file_name=input_path)
    sheet.save_as(output_path)

    print(f"\nConverted  {input_path}  →  {output_path}")
    return output_path


def main():
    print("=" * 60)
    print("Pyexcel: Universal Spreadsheet Processing")
    print("=" * 60)

    sample_csv = 'data/employees.csv'
    report_path = 'data/salary_report.csv'
    os.makedirs('data', exist_ok=True)

    print("\n--- Step 1: Creating sample data ---")
    create_sample_csv(sample_csv)

    print("\n--- Step 2: Processing upload ---")
    result = process_uploaded_file(sample_csv)

    print("\n--- Step 3: Generating salary report ---")
    generate_salary_report(result.get('records', []), report_path)

    print("\n--- Step 4: Format conversion (CSV → XLSX) ---")
    print("Requires pyexcel-xlsx: pip install pyexcel-xlsx")
    try:
        format_converter(sample_csv, 'xlsx')
    except Exception as e:
        print(f"Skipped (install pyexcel-xlsx to enable): {e}")

    print("\nPRODUCTION NOTE:")
    print("  Pyexcel loads entire file into memory.")
    print("  For files >50 MB use openpyxl read-only mode instead.")


if __name__ == '__main__':
    main()
