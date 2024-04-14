import psycopg2
import csv
from datetime import datetime, date
import random
import os

# PostgreSQL connection details from environment variables
host = os.environ.get("PG_HOST")
database = os.environ.get("PG_DATABASE")
user = os.environ.get("PG_USER")
password = os.environ.get("PG_PASSWORD")

# Grade conversion dictionary
grade_conversion = {
    "A": 90,
    "B": 80,
    "C": 70,
    "D": 60,
    "F": 50,
    "E": 30,
}

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)
cur = conn.cursor()

# Fetch student data from the database
fetch_data_query = """
SELECT id, Prenom, Nom, Sexe, Niveux, Pays, Date_Naissance, Notes
FROM students
"""
cur.execute(fetch_data_query)
student_data = cur.fetchall()

# Convert the fetched data to a list of dictionaries
students = []
for row in student_data:
    student = {
        'id': row[0],
        'Prenom': row[1],
        'Nom': row[2],
        'Sexe': row[3],
        'Niveux': row[4],
        'Pays': row[5],
        'Date_Naissance': row[6],
        'Notes': [grade_conversion[note.strip()] for note in row[7].split(',')]
    }
    students.append(student)

def group_students(data):
    data = data.copy()
    random.shuffle(data)
    data.sort(key=lambda x: (x['Pays'], x['Niveux']))
    groups = []
    i = 0

    while i < len(data):
        group_size = min(3, len(data) - i)
        group = data[i:i+group_size]
        sex_set = set(student['Sexe'] for student in group)
        country_set = set(student['Pays'] for student in group)
        niveux_set = set(student['Niveux'] for student in group)

        if len(sex_set) == group_size and len(country_set) == group_size and len(niveux_set) == group_size:
            groups.append(group)
        else:
            swap_candidate_indices = []
            for j in range(i + group_size, len(data)):
                if data[j]['Sexe'] != group[0]['Sexe'] and data[j]['Pays'] != group[0]['Pays'] and data[j]['Niveux'] != group[0]['Niveux']:
                    swap_candidate_indices.append(j)

            if swap_candidate_indices:
                swap_index = random.choice(swap_candidate_indices)
                group.append(data[swap_index])
                groups.append(group)
            else:
                groups.append(group)

        i += group_size

        if len(data) - i < 3:
            break

    return groups

def calculate_group_stats(groups):
    for group in groups:
        group_notes = [student['Notes'] for student in group]
        group_ages = [calculate_age(student['Date_Naissance']) for student in group]

        group_avg_notes = sum(sum(notes) for notes in group_notes) / sum(len(notes) for notes in group_notes)
        group_total_age = sum(group_ages)
        group_avg_age = group_total_age / len(group)

        group.append({
            'Group Total Age': group_total_age,
            'Group Average Age': group_avg_age,
            'Group Average Notes': group_avg_notes
        })

    return groups

def sort_groups(groups):
    return sorted(groups, key=lambda g: (g[-1]['Group Average Notes'], g[-1]['Group Average Age']))

def save_to_csv(groups):
    with open("student_groups.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Group", "Student ID", "First Name", "Last Name", "Sexe", "Notes", "Pays", "Date of Birth", "Age", "Niveux", "Group Total Age", "Group Average Age", "Group Average Notes"])
        for i, group in enumerate(groups):
            for student in group[:-1]:
                writer.writerow([i+1, student['id'], student['Prenom'], student['Nom'], student['Sexe'], ",".join(map(str, student['Notes'])), student['Pays'], student['Date_Naissance'], calculate_age(student['Date_Naissance']), student['Niveux']])
            writer.writerow([i+1, "", "", "", "", "", "", "", "", "", group[-1]['Group Total Age'], group[-1]['Group Average Age'], group[-1]['Group Average Notes']])

def calculate_age(date_of_birth):
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

def main():
    groups = group_students(students)
    groups = calculate_group_stats(groups)
    groups = sort_groups(groups)
    save_to_csv(groups)

if __name__ == "__main__":
    main()