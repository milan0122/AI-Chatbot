from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import genric_helper

app = FastAPI()
inprogress_orders= {}
@app.post("/")
async def handle_request(request:Request):
    
    # reterive the json data
    payload = await request.json()

    #based on the structure 
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id = genric_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'track.order-context:ongoing-tracking': track_order,
        'order.add-context:ongoing-order' : add_to_order,
        'order.complete-context: ongoing-order': complete_order,
        # 'order.remove-contex:ongoing-order': remove_from_order()  
    }
    return intent_handler_dict[intent](parameters, session_id)
def save_to_db(order:dict):
    #taking next order_id 
    next_order_id = db_helper.get_next_order_id()
    # adding item to db
    for item,qty in order.items():
       rcode =  db_helper.insert_order_item(
            item,
            qty,
            next_order_id
        )
       
       if rcode == -1:
           return -1
       
       db_helper.insert_order_tracking(next_order_id,"in-progress")
    return next_order_id
def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                           f"Here is your order id # {order_id}. " \
                           f"Your order total is {order_total} which you can pay at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
    
def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = genric_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def track_order(parameters:dict):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



