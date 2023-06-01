data = [
    ('M Hamza', '1', 'mhamza-1-4-9@iqra.edu', 'Final Exam', 'Math', 50, 100, "datetime.date(2023, 5, 19)"),
    ('M Hamza', '1', 'mhamza-1-4-9@iqra.edu', 'Final Exam', 'Urdu Book', 30, 100, "datetime.date(2023, 5, 19)"),
    ('M Hamza', '1', 'mhamza-1-4-9@iqra.edu', 'Mid Exam', 'English Book', 80, 100, "datetime.date(2023, 5, 19)")
]

grouped_data = {}  # Dictionary to group data by exam type and date

for item in data:
    exam_type = item[3]
    exam_date = item[7]

    key = (exam_type, exam_date)

    if key not in grouped_data:
        grouped_data[key] = []

    grouped_data[key].append(item)

# Access and print specific rows
row_index = 0
specific_rows = list(grouped_data.keys())  # Convert dict_keys object to a list
# for key in specific_rows:
#     print(key)
#     rows = grouped_data[key]
#     for row in rows:
#         print(row)

#     print()

# Access a specific row
print("hello")
specific_row = grouped_data[specific_rows[row_index]]
print(specific_row)

# Access a specific element from the row
element_index = 4
specific_element = specific_row[0][element_index]
print(specific_element)
