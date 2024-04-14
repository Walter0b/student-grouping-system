
# Student Data Management and Analysis

This Python project consists of two scripts for managing and analyzing student data:

1. **Importing Student Data**: This script imports student data from a CSV file into a PostgreSQL database.
2. **Student Grouping and Statistics Generator**: This script fetches student data from the PostgreSQL database, groups students based on certain criteria, calculates statistics for each group, and saves the grouped data into a CSV file.

## Prerequisites

Before running the scripts, ensure you have the following:

- Python 3.x installed on your system.
- Required Python packages installed (`psycopg2`, `csv`, `datetime`, `os`, `random`).
- Access to a PostgreSQL database for storing student data.
- PostgreSQL connection details set as environment variables:
  - `PG_HOST`: Hostname of the PostgreSQL server.
  - `PG_DATABASE`: Name of the PostgreSQL database.
  - `PG_USER`: Username to access the database.
  - `PG_PASSWORD`: Password for the database user.

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Walter0b/student-grouping-system.git
   ```

2. Navigate to the directory containing the scripts:

   ```bash
   cd student_data_management
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Importing Student Data**:
   - Ensure your student data is in CSV format and named `student_data.csv`.
   - Run the script:

     ```bash
     python import_student_data.py
     ```

5. **Student Grouping and Statistics Generator**:
   - Ensure the PostgreSQL database contains the imported student data.
   - Run the script:

     ```bash
     python student_grouping.py
     ```

6. Once the scripts finish executing, you'll find the grouped student data and statistics in a file named `student_groups.csv`.

## Customization

You can customize the scripts to fit your specific requirements:

- Modify the database schema in the PostgreSQL database to match your student data structure.
- Adjust the grouping criteria and statistics calculations in the `student_grouping.py` script.
- Customize the CSV output format to include additional fields or change the structure.

## License

This project is licensed under the [MIT License](LICENSE).
