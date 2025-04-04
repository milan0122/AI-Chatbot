import re

def extract_session_id(extract_session:str):

# Search for anything between "/sessions/" and "/contexts/"
    match = re.search(r"/sessions/(.*?)/contexts/", extract_session)

    # If it matches, extract the session ID
    if match:
        session_id = match.group(1)
        return session_id
    return " "


def get_str_from_food_dict(food_dict:dict):
    return ", ".join([f"{int(value)} {key}" for key,value in food_dict.items()])

# if __name__=='__main__':
    print(get_str_from_food_dict({'samosa':2,'chhole':5}))
    #result = extract_session_id("projects/khuma-chatbot-fqpb/agent/sessions/fb5abc19-fca7-eb70-191c-923c2760f731/contexts/ongoing-order")
    #print(result)
    # print(type(result))
   