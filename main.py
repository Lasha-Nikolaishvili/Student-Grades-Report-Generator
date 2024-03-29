from samples import names, last_names
import numpy as np
import tabulate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from pathlib import Path


def print_full_results(students_table, header, table_format="grid"):
    print('სრული შედეგები:')
    print(tabulate.tabulate(students_table[1:], header, tablefmt=table_format))


def get_highest_avg_grade(students_table, grades):
    highest_grade = np.max(np.mean(grades, 1))
    highest_grades = students_table[np.argmax(np.mean(grades, 1)) + 1][1::]
    highest_name = students_table[np.argmax(np.mean(grades, 1)) + 1][0]
    return \
        f'სტუდენტი ყველაზე მაღალი საშუალო ქულით({highest_grade}) იყო {highest_name}, შემდეგი ქულებით: {highest_grades}.'


def get_lowest_avg_grade(students_table, grades):
    lowest_grade = np.min(np.mean(grades, 1))
    lowest_grades = students_table[np.argmin(np.mean(grades, 1)) + 1][1::]
    lowest_name = students_table[np.argmin(np.mean(grades, 1)) + 1][0]
    return f'სტუდენტი ყველაზე დაბალი საშუალო ქულით({lowest_grade}) იყო {lowest_name}, შემდეგი ქულებით: {lowest_grades}.'


def get_highest_math_grade(students_table, grades):
    highest_math_grade = np.max(grades.T[1])
    highest_math_name = students_table[np.argmax(grades.T[1]) + 1][0]
    return f'სტუდენტი, რომელსაც ყველაზე მაღალი ქულა({highest_math_grade}) აქვს მათემატიკაში არის {highest_math_name}.'


def get_lowest_math_grade(students_table, grades):
    lowest_math_grade = np.min(grades.T[1])
    lowest_math_name = students_table[np.argmin(grades.T[1]) + 1][0]
    return f'სტუდენტი, რომელსაც ყველაზე დაბალი ქულა({lowest_math_grade}) აქვს მათემატიკაში არის {lowest_math_name}.'


def get_abv_avg_eng_studs(students_table, grades):
    average_english_grade = np.mean(grades.T[3])
    studs_with_abv_avg_grds = students_table[1::][grades.T[3] > np.mean(grades.T[3])]
    text_data = \
        f"""სტუდენტები, რომელთა ინგლისურის ქულაც მეტია ინგლისურის საშუალო ქულაზე({average_english_grade}):<br/>"""
    for student in studs_with_abv_avg_grds:
        text_data += f'{student[0]} - {student[4]} ქულა.<br/>'
    return text_data


def get_bel_avg_eng_studs(students_table, grades):
    average_english_grade = np.mean(grades.T[3])
    studs_with_abv_avg_grds = students_table[1::][grades.T[3] < np.mean(grades.T[3])]
    text_data = \
        f"""სტუდენტები, რომელთა ინგლისურის ქულაც ნაკლებია ინგლისურის საშუალო ქულაზე({average_english_grade}):<br/>"""
    for student in studs_with_abv_avg_grds:
        text_data += f'{student[0]} - {student[4]} ქულა.<br/>'
    return text_data


def get_pdf_paragraph(text, header_styles):
    report_header_text = text
    report_header_style = ParagraphStyle(**header_styles)
    report_header_paragraph = Paragraph(report_header_text, report_header_style)
    return report_header_paragraph


def generate_report(students_table, grades, file_name='report.pdf'):
    font_path = Path('fonts', 'bpg_glaho_sylfaen.ttf')
    font_name = 'Sylfaen'

    # Register custom font
    if font_path:
        pdfmetrics.registerFont(TTFont(font_name, font_path))

    # create a PDF document
    pdf_document = SimpleDocTemplate(file_name)
    pdf_elements = []

    # create and add report header
    report_header_paragraph = get_pdf_paragraph(
        """<b>სტუდენტის ქულების რეპორტი</b>""",
        {
            'name': 'ReportHeaderStyle',
            'fontName': font_name,
            'fontSize': 20,
            'textColor': colors.black,
            'spaceAfter': 50,
            'alignment': 1
        })
    pdf_elements.append(report_header_paragraph)

    # write average points data
    average_points_header_paragraph = get_pdf_paragraph(
        """<b>სტუდენტების ყველაზე მაღალი/დაბალი საშუალო ქულა.</b>""",
        {
            'name': 'AveragePointsHeaderStyle',
            'fontName': font_name,
            'fontSize': 13,
            'textColor': colors.black,
            'spaceAfter': 10,
        }
    )
    pdf_elements.append(average_points_header_paragraph)

    average_points_body_paragraph = get_pdf_paragraph(
        f"""
            • {get_highest_avg_grade(students_table, grades)}<br/>
            • {get_lowest_avg_grade(students_table, grades)}<br/>
            """,
        {
            'name': 'AveragePointsBodyStyle',
            'fontName': font_name,
            'fontSize': 11,
            'textColor': colors.black,
            'spaceAfter': 10,
        }
    )
    pdf_elements.append(average_points_body_paragraph)

    # write mathematics highest/lowest points data
    maths_points_header_paragraph = get_pdf_paragraph(
        """<b>სტუდენტების ყველაზე მაღალი/დაბალი მათემატიკის ქულა.</b>""",
        {
            'name': 'MathsPointsHeaderStyle',
            'fontName': font_name,
            'fontSize': 13,
            'textColor': colors.black,
            'spaceAfter': 10,
        }
    )
    pdf_elements.append(maths_points_header_paragraph)

    maths_points_body_paragraph = get_pdf_paragraph(
        f"""
            • {get_highest_math_grade(students_table, grades)}<br/>
            • {get_lowest_math_grade(students_table, grades)}<br/>
            """,
        {
            'name': 'MathsPointsBodyStyle',
            'fontName': font_name,
            'fontSize': 11,
            'textColor': colors.black,
            'spaceAfter': 10,
        }
    )
    pdf_elements.append(maths_points_body_paragraph)

    # write students with above average english grade
    english_points_header_paragraph = get_pdf_paragraph(
        """<b>სტუდენტები ინგლისურის საშუალო ქულასთან შედარებით.</b>""",
        {
            'name': 'EnglishPointsHeaderStyle',
            'fontName': font_name,
            'fontSize': 13,
            'textColor': colors.black,
            'spaceAfter': 10,
        }
    )
    pdf_elements.append(english_points_header_paragraph)

    english_points_body_paragraph = get_pdf_paragraph(
        f"""
               • {get_abv_avg_eng_studs(students_table, grades)}<br/>
               • {get_bel_avg_eng_studs(students_table, grades)}<br/>
               """,
        {
            'name': 'EnglishPointsBodyStyle',
            'fontName': font_name,
            'fontSize': 11,
            'textColor': colors.black,
            'spaceAfter': 10,
        }
    )
    pdf_elements.append(english_points_body_paragraph)

    # create and add table header
    table_header_paragraph = get_pdf_paragraph(
        """<b>ყველა სტუდენტის ქულების ცხრილი</b>""",
        {
            'name': 'TableHeaderStyle',
            'fontName': font_name,
            'fontSize': 13,
            'textColor': colors.black,
            'spaceAfter': 15,
            'alignment': 1
        }
    )
    pdf_elements.append(table_header_paragraph)

    # style and add a table to the PDF elements
    table_data = [list(np_list) for np_list in students_table]
    table = Table(table_data, colWidths=[100] + [60] * (len(table_data[0]) - 1))  # Adjust width as needed

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.azure),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ])
    table.setStyle(style)
    pdf_elements.append(table)

    # build the PDF document
    pdf_document.build(pdf_elements)


def main():
    header = np.array(
        ['სახელები/საგნები', 'ქართული', 'მათემატიკა', 'ისტორია', 'ინგლისური', 'რუსული', 'ფიზიკა', 'ბიოლოგია', 'სპორტი']
    )

    # generate data table
    grades = np.random.randint(1, 101, size=(len(names) * 2, 8))
    names_last_names = np.array(
        [f"{name} {last_name}" for name, last_name in zip([*names, *names[::-1]], [*last_names, *last_names])]
    ).reshape(-1, 1)
    students_table = np.hstack((names_last_names, grades))
    students_table = np.vstack((header, students_table))

    # average grades
    print(get_highest_avg_grade(students_table, grades))
    print(get_lowest_avg_grade(students_table, grades))

    # math grades
    print(get_highest_math_grade(students_table, grades))
    print(get_lowest_math_grade(students_table, grades))

    # English students
    print(get_abv_avg_eng_studs(students_table, grades))
    print(get_bel_avg_eng_studs(students_table, grades))

    # full results
    print_full_results(students_table[1:], header, "grid")

    # generate report and write to pdf
    generate_report(students_table, grades, 'report.pdf')


if __name__ == '__main__':
    main()
