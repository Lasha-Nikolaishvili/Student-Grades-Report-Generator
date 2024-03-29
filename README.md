# Student Grades Report Generator

This Python program generates a report in PDF format containing information about student grades. It analyzes the grades of students in various subjects and provides insights such as the highest and lowest average grades, the highest and lowest grades in mathematics, and students with above and below average grades in English.

## Features

- Calculates the highest and lowest average grades among students.
- Identifies the students with the highest and lowest grades in mathematics.
- Lists students with grades above and below the average in English.
- Generates a detailed table displaying all student grades.
- Adds all of this data to a pdf file.

## How to Use

1. Install the required dependencies:
   ```bash
   pip install requirements.txt
   ```

2. Run the program:
   ```bash
   python main.py
   ```

3. View the generated report PDF file named `report.pdf` for detailed insights into student grades.

## Dependencies

- [NumPy](https://numpy.org/): For numerical operations and data manipulation.
- [Tabulate](https://pypi.org/project/tabulate/): For formatting data into a table.
- [ReportLab](https://www.reportlab.com/opensource/): For generating PDF documents programmatically.

