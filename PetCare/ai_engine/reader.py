# ai_engine/reader.py

def read_list(items, item_type):
    response = f"Available {item_type} are. "

    for i, item in enumerate(items, start=1):
        response += f"Option {i}: {item}. "

    response += "Please say the option number or name."
    return response
