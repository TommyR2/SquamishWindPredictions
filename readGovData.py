import mysql.connector
import pandas as pd

def query(year, month, day):
    connection = mysql.connector.connect(
        host="",
        user="",
        password="",
        database="")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    query = f"INSERT SQL QUERY"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Get column names from the cursor description
    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the rows and columns
    df = pd.DataFrame(rows, columns=columns)

    # Print the DataFrame
    print(df)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    return df

