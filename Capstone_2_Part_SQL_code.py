{
  "cells": [
    {
      "cell_type": "markdown",
      "id": "b097e738",
      "metadata": {
        "id": "b097e738"
      },
      "source": [
        "## Capstone 1 - Part 2\n",
        "\n",
        "In the first part of the capstone, we focused on Data Retrieval, Data Preprocessing, Feature Engineering and Exploratory Data Analysis using Python & its libraries. Now we are going to shift gears and gain insights into our HR Analytics dataset using SQL.\n",
        "\n",
        "## TODO: Make use of SQL to do the following:\n",
        "\n",
        "### Create a SQLITE3 DB using the CSV file (2 pts). Please refer this [link](https://www.linkedin.com/pulse/accessing-sqlite3-database-from-jupyter-notebook-using-varun-lobo/) and this [link](https://www.geeksforgeeks.org/how-to-import-csv-file-in-sqlite-database-using-python/) to know more.\n",
        "\n",
        "### Calculate the Attrition Rate and summarize attrition (3 pts) by:\n",
        "- Gender\n",
        "- Department\n",
        "- Age\n",
        "- Average monthly income by job level\n",
        "- Years at company\n",
        "\n",
        "### Continue using SQL to explore main reasons for attrition (3 pts), For example:\n",
        "- Why do more people over 50 years old leave the company than people who aged 40-50?\n",
        "- Why do people with higher pay still leave the company?\n",
        "- Which factors drive employees who work at company less than 5 years to leave?\n",
        "\n",
        "### Effective Communication (2 pts)\n",
        "- Please make use of markdown cells to communicate your thought process, why did you think of performing a step? what was the observation from the query? etc.\n",
        "- The code should be commented so that it is readable for the reviewer.\n",
        "\n",
        "### Grading and Important Instructions\n",
        "- Each of the above steps are mandatory and should be completed in good faith\n",
        "- Make sure before submitting that the code is in fully working condition\n",
        "- It is fine to make use of ChatGPT, stackoverflow type resources, just provide the reference links from where you got it\n",
        "- Debugging is an art, if you find yourself stuck with errors, take help of stackoverflow and ChatGPT to resolve the issue and if it's still unresolved, reach out to me for help.\n",
        "- You need to score atleast 7/10 to pass the project, anything less than that will be marked required, needing resubmission.\n",
        "- Feedback will be provided on 3 levels (Awesome, Suggestion, & Required). Required changes are mandatory to be made.\n",
        "- For submission, please upload the project on github and share the link to the file with us through LMS."
      ]
    },
    {
      "cell_type": "markdown",
      "id": "179020d0",
      "metadata": {
        "id": "179020d0"
      },
      "source": [
        "#### Calculate Attrition Rate\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 13,
      "id": "9e6465d9",
      "metadata": {
        "id": "9e6465d9",
        "outputId": "464422cf-8ef8-4e79-ea93-09dcf6fcabef",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Database loaded successfully!\n",
            "  Attrition AttritionRate\n",
            "0        No         83.9%\n",
            "1       Yes         16.1%\n"
          ]
        }
      ],
      "source": [
        "import sqlite3\n",
        "import pandas as pd\n",
        "\n",
        "# Load CSV file into a DataFrame\n",
        "df = pd.read_csv('/content/HR-Analytics.csv')\n",
        "\n",
        "# Create a SQLite database in memory\n",
        "conn = sqlite3.connect(':memory:')\n",
        "\n",
        "# Load the DataFrame into the SQLite database\n",
        "df.to_sql('hr_data', conn, index=False, if_exists='replace')\n",
        "\n",
        "print(\"Database loaded successfully!\")\n",
        "\n",
        "query = \"\"\"\n",
        "SELECT\n",
        "    Attrition,\n",
        "    ROUND((CAST(COUNT(*) AS FLOAT) * 100 / (SELECT COUNT(*) FROM hr_data)), 1) || '%' AS AttritionRate\n",
        "FROM hr_data\n",
        "GROUP BY Attrition;\n",
        "\"\"\"\n",
        "\n",
        "# Execute query\n",
        "result = pd.read_sql_query(query, conn)\n",
        "\n",
        "# Display the result\n",
        "print(result)\n",
        "\n"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Before working with SQL, we need to prepare the data and environment. SQLite is built into Python, so no separate installation is required, but we need to ensure the dataset is loaded into the workspace.\n",
        "Colab requires an in-memory SQLite database to process SQL queries, which ensures the operations are lightweight and don’t require external server setup.\n",
        "The dataset, in CSV format, needs to be uploaded and loaded into a Pandas DataFrame. This step is essential to transfer the data to SQLite for querying.\n",
        "\n",
        "Grouping by Attrition:\n",
        "The dataset likely has a column Attrition with values True (employees who left) and False (employees who stayed). Grouping by this column lets us calculate counts for each group.\n",
        "\n",
        "Calculating Total Count:\n",
        "Use a subquery (SELECT COUNT(*) FROM hr_data) to get the total number of employees in the dataset.\n",
        "\n",
        "Calculating Percentage:\n",
        "For each Attrition group, calculate the percentage:\n",
        "\n",
        "AttritionRate\n",
        "=\n",
        "(\n",
        "Group Count\n",
        "Total Count\n",
        ")\n",
        "×\n",
        "100\n",
        "AttritionRate=(\n",
        "Total Count\n",
        "Group Count\n",
        "​\n",
        " )×100\n",
        "Use ROUND to format the rate to one decimal place.\n",
        "\n",
        "Formatting the Output:\n",
        "Use || '%' to append a percentage sign to the calculated rate."
      ],
      "metadata": {
        "id": "mirajNHGaCYS"
      },
      "id": "mirajNHGaCYS"
    },
    {
      "cell_type": "markdown",
      "id": "41bab6fc",
      "metadata": {
        "id": "41bab6fc"
      },
      "source": [
        "#### Sample Output\n",
        "\n",
        "![image](https://api-v4.skyprepapp.com/public_api/da/857886?view_key=eyJvYmplY3RfdHlwZSI6ImFydGljbGUiLCJvYmplY3RfaWQiOjg1Nzg4NiwiaG1hYyI6ImUyNGU0YWRhNWQwMDkxNWE2NWNiY2EwNGFlNDNiMTBlYmYyNWY0YzAiLCJleHBpcmVzX2F0Ijo0ODkxMzgxMTk5LCJvdHRfdG9rZW4iOm51bGx9)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "723146e8",
      "metadata": {
        "id": "723146e8"
      },
      "source": [
        "#### Find Attrition by Gender"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 18,
      "id": "91cf1ab8",
      "metadata": {
        "id": "91cf1ab8",
        "outputId": "903ceeae-aa96-4f99-a2ba-caf3fa434d05",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "  Attrition  Gender  Count_Gender  Attrition_by_Gender\n",
            "0        No  Female           501                 85.2\n",
            "1       Yes  Female            87                 14.8\n",
            "2        No    Male           732                 83.0\n",
            "3       Yes    Male           150                 17.0\n"
          ]
        }
      ],
      "source": [
        "query = \"\"\"\n",
        "WITH GenderTotals AS (\n",
        "    SELECT\n",
        "        Gender,\n",
        "        COUNT(*) AS Total_Gender\n",
        "    FROM hr_data\n",
        "    GROUP BY Gender\n",
        ")\n",
        "SELECT\n",
        "    hr_data.Attrition,\n",
        "    hr_data.Gender,\n",
        "    COUNT(*) AS Count_Gender,\n",
        "    ROUND((CAST(COUNT(*) AS FLOAT) * 100 / Total_Gender), 1) AS Attrition_by_Gender\n",
        "FROM hr_data\n",
        "JOIN GenderTotals ON hr_data.Gender = GenderTotals.Gender\n",
        "GROUP BY hr_data.Gender, hr_data.Attrition, GenderTotals.Total_Gender;\n",
        "\"\"\"\n",
        "\n",
        "# Execute query\n",
        "result = pd.read_sql_query(query, conn)\n",
        "\n",
        "# Display the result\n",
        "print(result)"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Use a Common Table Expression (WITH) to Calculate Total Employees by Gender:\n",
        "\n",
        "GenderTotals calculates the total number of employees for each gender. This acts as a reference for calculating percentages.\n",
        "Join the GenderTotals with the Main Table:\n",
        "\n",
        "The total employee count (Total_Gender) is brought into the main query by joining on Gender.\n",
        "Calculate Percentages:\n",
        "\n",
        "For each Gender and Attrition group, calculate the percentage as:\n",
        "Attrition_by_Gender\n",
        "=\n",
        "(\n",
        "Count of Group\n",
        "Total Employees by Gender\n",
        ")\n",
        "×\n",
        "100\n",
        "Attrition_by_Gender=(\n",
        "Total Employees by Gender\n",
        "Count of Group\n",
        "​\n",
        " )×100"
      ],
      "metadata": {
        "id": "24Pzgv86hcTC"
      },
      "id": "24Pzgv86hcTC"
    },
    {
      "cell_type": "markdown",
      "id": "8da31e8b",
      "metadata": {
        "id": "8da31e8b"
      },
      "source": [
        "#### Sample output\n",
        "\n",
        "![image](https://api-v4.skyprepapp.com/public_api/da/857882?view_key=eyJvYmplY3RfdHlwZSI6ImFydGljbGUiLCJvYmplY3RfaWQiOjg1Nzg4MiwiaG1hYyI6IjM1NDU5N2E4MjZmMTMxNWFhMTA4NzFiYTFkZjQ5YjBhNTYyOWYwMzgiLCJleHBpcmVzX2F0Ijo0ODkxMzgxMTk5LCJvdHRfdG9rZW4iOm51bGx9)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "40708d2a",
      "metadata": {
        "id": "40708d2a"
      },
      "source": [
        "#### Find Attrition by Dept"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 19,
      "id": "58b8581b",
      "metadata": {
        "id": "58b8581b",
        "outputId": "d555c48e-0903-4d64-e18c-23353ada3d57",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "               Department Attrition  Department_Attrition\n",
            "0         Human Resources        No                    51\n",
            "1         Human Resources       Yes                    12\n",
            "2  Research & Development        No                   828\n",
            "3  Research & Development       Yes                   133\n",
            "4                   Sales        No                   354\n",
            "5                   Sales       Yes                    92\n"
          ]
        }
      ],
      "source": [
        "query = \"\"\"\n",
        "SELECT\n",
        "    Department,\n",
        "    Attrition,\n",
        "    COUNT(*) AS Department_Attrition\n",
        "FROM hr_data\n",
        "GROUP BY Department, Attrition;\n",
        "\"\"\"\n",
        "\n",
        "# Execute the query\n",
        "result = pd.read_sql_query(query, conn)\n",
        "\n",
        "# Display the result\n",
        "print(result)\n",
        "\n"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Group by Department and Attrition:\n",
        "\n",
        "This groups the dataset by each department and whether employees stayed (No) or left (Yes).\n",
        "Count Employees in Each Group:\n",
        "\n",
        "COUNT(*) calculates the number of employees in each department and attrition status combination.\n",
        "Column Names:\n",
        "\n",
        "Department and Attrition represent the department and whether employees stayed or left.\n",
        "Department_Attrition is the count of employees in each group."
      ],
      "metadata": {
        "id": "m0eOFqocbR7m"
      },
      "id": "m0eOFqocbR7m"
    },
    {
      "cell_type": "markdown",
      "id": "e23bee46",
      "metadata": {
        "id": "e23bee46"
      },
      "source": [
        "#### Sample Output\n",
        "\n",
        "<img src=\"https://api-v4.skyprepapp.com/public_api/da/857884?view_key=eyJvYmplY3RfdHlwZSI6ImFydGljbGUiLCJvYmplY3RfaWQiOjg1Nzg4NCwiaG1hYyI6IjdmOTA4NzJjODZmYTgxOGUyMzkyYTBlZjhjYjljNjA4ZGM3NjkzMWYiLCJleHBpcmVzX2F0Ijo0ODkxMzgxMTk5LCJvdHRfdG9rZW4iOm51bGx9\" width=\"450\" height=\"450\">"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "a2cef9d3",
      "metadata": {
        "id": "a2cef9d3"
      },
      "source": [
        "#### Find Attrition by Age Groups"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 21,
      "id": "088d0ac6",
      "metadata": {
        "id": "088d0ac6",
        "outputId": "3fda0386-a209-45db-eebe-c00f8417ea69",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "  Attrition Age_Group  num  percent_by_age\n",
            "0        No     30-40  585           86.16\n",
            "1       Yes     30-40   94           13.84\n",
            "2        No     41-50  288           89.44\n",
            "3       Yes     41-50   34           10.56\n",
            "4        No   Over 50  125           87.41\n",
            "5       Yes   Over 50   18           12.59\n",
            "6        No  Under 30  235           72.09\n",
            "7       Yes  Under 30   91           27.91\n"
          ]
        }
      ],
      "source": [
        "query = \"\"\"\n",
        "WITH AgeGroups AS (\n",
        "    SELECT\n",
        "        CASE\n",
        "            WHEN Age < 30 THEN 'Under 30'\n",
        "            WHEN Age BETWEEN 30 AND 40 THEN '30-40'\n",
        "            WHEN Age BETWEEN 41 AND 50 THEN '41-50'\n",
        "            ELSE 'Over 50'\n",
        "        END AS Age_Group,\n",
        "        Attrition,\n",
        "        COUNT(*) AS num\n",
        "    FROM hr_data\n",
        "    GROUP BY Age_Group, Attrition\n",
        ")\n",
        "SELECT\n",
        "    Attrition,\n",
        "    Age_Group,\n",
        "    num,\n",
        "    ROUND((CAST(num AS FLOAT) * 100 / SUM(num) OVER (PARTITION BY Age_Group)), 2) AS percent_by_age\n",
        "FROM AgeGroups;\n",
        "\"\"\"\n",
        "\n",
        "# Execute query\n",
        "result = pd.read_sql_query(query, conn)\n",
        "\n",
        "# Display the result\n",
        "print(result)"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Create Age Groups:\n",
        "\n",
        "Use a CASE statement to bucket employees into age groups:\n",
        "Under 30\n",
        "30-50\n",
        "Over 50\n",
        "Count Employees by Age Group and Attrition:\n",
        "\n",
        "Count the number of employees (COUNT(*)) for each combination of Age_Group and Attrition.\n",
        "Calculate Percentage (percent_by_age):\n",
        "\n",
        "Use SUM(num) OVER (PARTITION BY Age_Group) to calculate the total employees within each age group.\n",
        "Divide the count (num) by the total and multiply by 100 to compute the percentage.\n",
        "Final Output:\n",
        "\n",
        "Display the age group, attrition status, count (num), and percentage (percent_by_age).\n"
      ],
      "metadata": {
        "id": "O1mtV2b2bqQy"
      },
      "id": "O1mtV2b2bqQy"
    },
    {
      "cell_type": "markdown",
      "id": "7eb8bfc8",
      "metadata": {
        "id": "7eb8bfc8"
      },
      "source": [
        "#### Sample Output\n",
        "\n",
        "![image](https://api-v4.skyprepapp.com/public_api/da/857885?view_key=eyJvYmplY3RfdHlwZSI6ImFydGljbGUiLCJvYmplY3RfaWQiOjg1Nzg4NSwiaG1hYyI6IjcwNGVlOWIwYzg1MmMwNmNhODg0NmYyZDFlNWE3OTU1MTFhMGVmYWYiLCJleHBpcmVzX2F0Ijo0ODkxMzgxMTk5LCJvdHRfdG9rZW4iOm51bGx9)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "67dbffff",
      "metadata": {
        "id": "67dbffff"
      },
      "source": [
        "#### Find Attrition by Monthly Income"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 27,
      "id": "9f954d18",
      "metadata": {
        "id": "9f954d18",
        "outputId": "3cb4cf91-44a6-4f18-94fd-4a369a3dbc1d",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "               Department  JobLevel  avg_income  attrition_avg_income  \\\n",
            "0         Human Resources         1      2733.2                2415.7   \n",
            "1         Human Resources         2      5563.5                   NaN   \n",
            "2  Research & Development         1      2840.1                2687.4   \n",
            "3  Research & Development         2      5291.2                5372.0   \n",
            "4  Research & Development         3     10170.5                9503.8   \n",
            "5  Research & Development         4     15634.7               12169.0   \n",
            "6  Research & Development         5     19218.5               19550.0   \n",
            "7                   Sales         1      2506.7                2373.4   \n",
            "\n",
            "   difference  \n",
            "0       317.5  \n",
            "1         NaN  \n",
            "2       152.7  \n",
            "3       -80.8  \n",
            "4       666.6  \n",
            "5      3465.7  \n",
            "6      -331.5  \n",
            "7       133.3  \n"
          ]
        }
      ],
      "source": [
        "query = \"\"\"\n",
        "WITH DepartmentIncome AS (\n",
        "    SELECT\n",
        "        Department,\n",
        "        JobLevel,\n",
        "        AVG(MonthlyIncome) AS avg_income\n",
        "    FROM hr_data\n",
        "    GROUP BY Department, JobLevel\n",
        "),\n",
        "AttritionIncome AS (\n",
        "    SELECT\n",
        "        Department,\n",
        "        JobLevel,\n",
        "        AVG(MonthlyIncome) AS attrition_avg_income\n",
        "    FROM hr_data\n",
        "    WHERE Attrition = 'Yes'\n",
        "    GROUP BY Department, JobLevel\n",
        ")\n",
        "SELECT\n",
        "    d.Department,\n",
        "    d.JobLevel,\n",
        "    ROUND(d.avg_income, 1) AS avg_income,\n",
        "    ROUND(a.attrition_avg_income, 1) AS attrition_avg_income,\n",
        "    ROUND(d.avg_income - a.attrition_avg_income, 1) AS difference\n",
        "FROM DepartmentIncome d\n",
        "LEFT JOIN AttritionIncome a\n",
        "    ON d.Department = a.Department AND d.JobLevel = a.JobLevel\n",
        "WHERE\n",
        "    (d.Department = 'Sales' AND d.JobLevel = 1) OR\n",
        "    (d.Department = 'Human Resources' AND d.JobLevel IN (1, 2)) OR\n",
        "    (d.Department = 'Research & Development' AND d.JobLevel IN (1, 2, 3, 4, 5))\n",
        "ORDER BY d.Department, d.JobLevel;\n",
        "\"\"\"\n",
        "\n",
        "# Execute query\n",
        "result = pd.read_sql_query(query, conn)\n",
        "\n",
        "# Display the result\n",
        "print(result)"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Step 1: Compute Average Income by Department and JobLevel:\n",
        "\n",
        "DepartmentIncome calculates the average income for each department and job level combination.\n",
        "AttritionIncome calculates the average income for employees who left (Attrition = 'Yes).\n",
        "Step 2: Join the Results:\n",
        "\n",
        "Match department and job level averages with attrition-specific averages.\n",
        "Step 3: Filter Rows for Specific Departments:\n",
        "\n",
        "Sales: Include only 1 row (JobLevel = 1).\n",
        "Human Resources: Include 2 rows (JobLevels 1 and 2).\n",
        "Research & Development: Include 5 rows (JobLevels 1 through 5).\n",
        "Step 4: Format and Sort:\n",
        "\n",
        "Use ROUND to format averages and differences.\n",
        "Order by Department and JobLevel to organize the output."
      ],
      "metadata": {
        "id": "Q1GQwLkfwcRh"
      },
      "id": "Q1GQwLkfwcRh"
    },
    {
      "cell_type": "markdown",
      "id": "124f8cee",
      "metadata": {
        "id": "124f8cee"
      },
      "source": [
        "#### Sample Output\n",
        "\n",
        "![image](https://api-v4.skyprepapp.com/public_api/da/857883?view_key=eyJvYmplY3RfdHlwZSI6ImFydGljbGUiLCJvYmplY3RfaWQiOjg1Nzg4MywiaG1hYyI6Ijg3NTU4ZDU1ZjRjN2U1YWI3ODQzYjM1NzFkNjBjMjEwNGY5NWI5ODUiLCJleHBpcmVzX2F0Ijo0ODkxMzgxMTk5LCJvdHRfdG9rZW4iOm51bGx9)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "018c4ff6",
      "metadata": {
        "id": "018c4ff6"
      },
      "source": [
        "#### Find Attrition by Years At Company"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 33,
      "id": "ee8af448",
      "metadata": {
        "id": "ee8af448",
        "outputId": "139bece2-6c7a-4d0e-de3f-7d6c45fca38e",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "   Row   tenure_years  num  percent\n",
            "0    1      2-5 years  561     38.2\n",
            "1    2      New Hires  215     14.6\n",
            "2    3     6-10 years  448     30.5\n",
            "3    4    11-20 years  180     12.2\n",
            "4    5  Over 20 years   66      4.5\n"
          ]
        }
      ],
      "source": [
        "query = \"\"\"\n",
        "WITH TenureGroups AS (\n",
        "    SELECT\n",
        "        CASE\n",
        "            WHEN YearsAtCompany BETWEEN 0 AND 1 THEN 'New Hires'\n",
        "            WHEN YearsAtCompany BETWEEN 2 AND 5 THEN '2-5 years'\n",
        "            WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'\n",
        "            WHEN YearsAtCompany BETWEEN 11 AND 20 THEN '11-20 years'\n",
        "            ELSE 'Over 20 years'\n",
        "        END AS tenure_years,\n",
        "        COUNT(*) AS num\n",
        "    FROM hr_data\n",
        "    GROUP BY tenure_years\n",
        ")\n",
        "SELECT\n",
        "    ROW_NUMBER() OVER (ORDER BY\n",
        "        CASE\n",
        "            WHEN tenure_years = '2-5 years' THEN 1\n",
        "            WHEN tenure_years = 'New Hires' THEN 2\n",
        "            WHEN tenure_years = '6-10 years' THEN 3\n",
        "            WHEN tenure_years = '11-20 years' THEN 4\n",
        "            WHEN tenure_years = 'Over 20 years' THEN 5\n",
        "        END) AS Row,\n",
        "    tenure_years,\n",
        "    num,\n",
        "    ROUND((CAST(num AS FLOAT) * 100 / SUM(num) OVER ()), 1) AS percent\n",
        "FROM TenureGroups\n",
        "ORDER BY Row;\n",
        "\"\"\"\n",
        "\n",
        "result = pd.read_sql_query(query, conn)\n",
        "print(result)\n"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "ae528e04",
      "metadata": {
        "id": "ae528e04"
      },
      "source": [
        "#### Sample Output\n",
        "\n",
        "![image](https://api-v4.skyprepapp.com/public_api/da/857881?view_key=eyJvYmplY3RfdHlwZSI6ImFydGljbGUiLCJvYmplY3RfaWQiOjg1Nzg4MSwiaG1hYyI6IjFhYmY3NGI4MzQ1NzViMWZkNDJlMjcwYTUyOTQ0OWQwZjJjMjhmNWUiLCJleHBpcmVzX2F0Ijo0ODkxMzgxMTk5LCJvdHRfdG9rZW4iOm51bGx9)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "b35f060a",
      "metadata": {
        "id": "b35f060a"
      },
      "source": [
        "#### Continue using SQL to explore main reasons for attrition (3 pts), For example:\n",
        "- Why do more people over 50 years old leave the company than people who aged 40-50?\n",
        "- Why do people with higher pay still leave the company?\n",
        "- Which factors drive employees who work at company less than 5 years to leave?"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 34,
      "id": "263d4f81",
      "metadata": {
        "id": "263d4f81",
        "outputId": "8aafd8a2-6d3b-4480-f59d-411941b501e4",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Query 1: Attrition Analysis for Age Over 40\n",
            "    Age  avg_job_satisfaction  avg_work_life_balance  \\\n",
            "0    41              2.666667               2.000000   \n",
            "1    42              2.000000               2.500000   \n",
            "2    43              3.000000               2.500000   \n",
            "3    44              2.333333               2.666667   \n",
            "4    45              1.500000               3.000000   \n",
            "5    46              3.000000               3.500000   \n",
            "6    47              2.666667               2.000000   \n",
            "7    48              3.000000               3.000000   \n",
            "8    49              2.500000               3.500000   \n",
            "9    50              2.600000               3.000000   \n",
            "10   51              3.500000               3.500000   \n",
            "11   52              2.666667               2.333333   \n",
            "12   53              2.500000               2.500000   \n",
            "13   55              2.666667               2.333333   \n",
            "14   56              3.000000               2.333333   \n",
            "15   58              2.800000               2.400000   \n",
            "\n",
            "    avg_environment_satisfaction  avg_monthly_income  employees_left  \n",
            "0                       1.666667         7153.000000               6  \n",
            "1                       3.000000         8258.500000               2  \n",
            "2                       2.000000         3891.500000               2  \n",
            "3                       2.333333         4876.833333               6  \n",
            "4                       1.000000        11555.000000               2  \n",
            "5                       2.750000         8988.750000               4  \n",
            "6                       2.000000        10394.000000               3  \n",
            "7                       2.500000         4018.000000               2  \n",
            "8                       2.000000         5969.000000               2  \n",
            "9                       2.600000         6357.800000               5  \n",
            "10                      1.000000         6555.500000               2  \n",
            "11                      2.000000        11077.333333               3  \n",
            "12                      2.000000        10308.500000               2  \n",
            "13                      2.666667        12904.666667               3  \n",
            "14                      2.333333         3296.333333               3  \n",
            "15                      3.800000         8885.000000               5  \n"
          ]
        }
      ],
      "source": [
        "query_1 = \"\"\"\n",
        "SELECT\n",
        "    Age,\n",
        "    AVG(JobSatisfaction) AS avg_job_satisfaction,\n",
        "    AVG(WorkLifeBalance) AS avg_work_life_balance,\n",
        "    AVG(EnvironmentSatisfaction) AS avg_environment_satisfaction,\n",
        "    AVG(MonthlyIncome) AS avg_monthly_income,\n",
        "    COUNT(*) AS employees_left\n",
        "FROM hr_data\n",
        "WHERE Attrition = 'Yes' AND Age > 40\n",
        "GROUP BY Age\n",
        "ORDER BY Age;\n",
        "\"\"\"\n",
        "result_1 = pd.read_sql_query(query_1, conn)\n",
        "print(\"Query 1: Attrition Analysis for Age Over 40\")\n",
        "print(result_1)\n"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Analyze the average job satisfaction, work-life balance, environment satisfaction, and monthly income.\n",
        "# - This data can help identify if older employees have lower satisfaction, poorer work-life balance, or lower income, which may explain the higher attrition."
      ],
      "metadata": {
        "id": "PfUw5aQV0Wkt"
      },
      "id": "PfUw5aQV0Wkt"
    },
    {
      "cell_type": "code",
      "source": [
        "query_2 = \"\"\"\n",
        "SELECT\n",
        "    JobLevel,\n",
        "    AVG(JobSatisfaction) AS avg_job_satisfaction,\n",
        "    AVG(WorkLifeBalance) AS avg_work_life_balance,\n",
        "    AVG(EnvironmentSatisfaction) AS avg_environment_satisfaction,\n",
        "    AVG(DistanceFromHome) AS avg_distance_from_home,\n",
        "    COUNT(*) AS employees_left\n",
        "FROM hr_data\n",
        "WHERE Attrition = 'Yes' AND MonthlyIncome > (SELECT AVG(MonthlyIncome) FROM hr_data)\n",
        "GROUP BY JobLevel\n",
        "ORDER BY JobLevel;\n",
        "\"\"\"\n",
        "result_2 = pd.read_sql_query(query_2, conn)\n",
        "print(\"\\nQuery 2: Attrition Analysis for Higher Pay Employees\")\n",
        "print(result_2)"
      ],
      "metadata": {
        "id": "JYUw42q3ZjK1",
        "outputId": "36dba537-85df-4c46-8664-7636e9a125a1",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "id": "JYUw42q3ZjK1",
      "execution_count": 35,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Query 2: Attrition Analysis for Higher Pay Employees\n",
            "   JobLevel  avg_job_satisfaction  avg_work_life_balance  \\\n",
            "0         2              1.909091               2.909091   \n",
            "1         3              2.548387               2.677419   \n",
            "2         4              2.600000               2.000000   \n",
            "3         5              2.400000               3.000000   \n",
            "\n",
            "   avg_environment_satisfaction  avg_distance_from_home  employees_left  \n",
            "0                      2.272727               10.454545              11  \n",
            "1                      2.387097               13.451613              31  \n",
            "2                      2.000000               12.000000               5  \n",
            "3                      2.400000                4.000000               5  \n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Despite higher pay, employees may leave due to low job satisfaction, poor work-life balance, or long commutes.\n",
        "# - Job stagnation or lack of growth opportunities might also be a reason for leaving, regardless of pay."
      ],
      "metadata": {
        "id": "NbsZrT0P0eqB"
      },
      "id": "NbsZrT0P0eqB"
    },
    {
      "cell_type": "code",
      "source": [
        "query_3 = \"\"\"\n",
        "SELECT\n",
        "    YearsAtCompany,\n",
        "    AVG(JobSatisfaction) AS avg_job_satisfaction,\n",
        "    AVG(EnvironmentSatisfaction) AS avg_environment_satisfaction,\n",
        "    AVG(WorkLifeBalance) AS avg_work_life_balance,\n",
        "    AVG(TrainingTimesLastYear) AS avg_training_times,\n",
        "    AVG(RelationshipSatisfaction) AS avg_relationship_satisfaction,\n",
        "    COUNT(*) AS employees_left\n",
        "FROM hr_data\n",
        "WHERE Attrition = 'Yes' AND YearsAtCompany < 5\n",
        "GROUP BY YearsAtCompany\n",
        "ORDER BY YearsAtCompany;\n",
        "\"\"\"\n",
        "result_3 = pd.read_sql_query(query_3, conn)\n",
        "print(\"\\nQuery 3: Attrition Analysis for Employees with Less than 5 Years Tenure\")\n",
        "print(result_3)\n"
      ],
      "metadata": {
        "id": "2ZOyMYiAZllc",
        "outputId": "e8829c58-abbd-45d9-e949-790faac1cb1a",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "id": "2ZOyMYiAZllc",
      "execution_count": 36,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "Query 3: Attrition Analysis for Employees with Less than 5 Years Tenure\n",
            "   YearsAtCompany  avg_job_satisfaction  avg_environment_satisfaction  \\\n",
            "0               0              2.250000                      2.687500   \n",
            "1               1              2.525424                      2.525424   \n",
            "2               2              2.592593                      2.259259   \n",
            "3               3              2.000000                      2.000000   \n",
            "4               4              2.684211                      2.263158   \n",
            "\n",
            "   avg_work_life_balance  avg_training_times  avg_relationship_satisfaction  \\\n",
            "0               2.750000            2.875000                       2.937500   \n",
            "1               2.694915            2.728814                       2.423729   \n",
            "2               2.518519            2.592593                       3.000000   \n",
            "3               2.950000            2.500000                       2.600000   \n",
            "4               2.421053            2.368421                       2.526316   \n",
            "\n",
            "   employees_left  \n",
            "0              16  \n",
            "1              59  \n",
            "2              27  \n",
            "3              20  \n",
            "4              19  \n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "Employees with less than 5 years of tenure might leave due to insufficient training, poor career development, or unsatisfactory relationships with managers or colleagues.\n",
        "# - Low job satisfaction or dissatisfaction with the work environment can also be significant contributors."
      ],
      "metadata": {
        "id": "7AvFP2c40kOX"
      },
      "id": "7AvFP2c40kOX"
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "TyxdW57RZpLO"
      },
      "id": "TyxdW57RZpLO",
      "execution_count": null,
      "outputs": []
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.9.7"
    },
    "colab": {
      "provenance": []
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}