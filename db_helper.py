import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
api_token = os.getenv('password')
if not api_token:
    raise ValueError("Check your env files")
global cnx
cnx = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = api_token,
        database = "pandeyji_eatery"
    )


def get_order_status(order_id):
    cursor = cnx.cursor()

    # Executing the SQL query to fetch the order status
    query = f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()

    # Returning the order status
    if result:
        return result[0]
    else:
        return None



