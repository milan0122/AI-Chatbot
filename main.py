from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import genric_helper

app = FastAPI()
inprogress_order = {}
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
        # 'order.complete-context: ongoing-order': complete_order(),
        # 'order.remove-contex:ongoing-order': remove_from_order()  
    }
    return intent_handler_dict[intent](parameters, session_id)

def add_to_order(parameters:dict,session_id:str):
    food_items = parameters['food-item']
    item_quantity = parameters['number']

    if len(food_items) != len(item_quantity):
        fulfillment_text = "Sorry I didn't understand. can you please specify food quantity agian?"
    else:
        new_food_item = dict(zip(food_items,item_quantity))
        if session_id  in inprogress_order:
            current_dict = inprogress_order[session_id]
            for item, qty in new_food_item.items():
                if item in current_dict:
                    current_dict[item] +=qty
                else:
                    current_dict[item] = qty
            inprogress_order[session_id]=current_dict
        else:
            inprogress_order[session_id] = new_food_item
        order_str = genric_helper.get_str_from_food_dict(inprogress_order[session_id])

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