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


def get_next_order_id():

    cursor = cnx.cursor()
    query = "Select Max(order_id) from orders"
    cursor.execute(query)

    result = cursor.fetchone()[0]

    cursor.close()
    
    if result is None:
        return 1
    else: 
        return result + 1 
    
def insert_order_item(food_item, quantity,order_id):
    try:

        cursor = cnx.cursor()
        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        cnx.commit()

        cursor.close()
        print("Order item inserted successfully !")

    except mysql.connector.Error as err:
       print(f"Error due to :{err}")

       #roolback
       cnx.rollback()
       return -1
    except Exception as e:
        print(f"error due to {e}")
        cnx.rollback()
        return -1
    
def get_total_order_price(order_id):

    cursor = cnx.cursor()

    query = f"Select get_total_order_price({order_id})"
    cursor.execute(query)

    # fetching the result 
    result = cursor.fetchone()[0]

    #closing 
    cursor.close()
    return result
        
def insert_order_tracking(order_id,status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()