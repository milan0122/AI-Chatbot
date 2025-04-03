from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/")
async def handle_request(request:Request):
    
    # reterive the json data
    payload = await request.json()

    #based on the structure 
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['intent']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    if intent == 'track.order-context:ongoing-tracking':
        return JSONResponse(content={
            "fulfillmentText": f"Recieved {intent}"
        })
    
    def track_order():
        