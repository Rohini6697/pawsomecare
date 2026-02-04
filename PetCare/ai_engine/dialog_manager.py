# ai_engine/dialog_manager.py

def next_question(slots):
    if slots["intent_type"] == "product_booking":
        if not slots["pet_type"]:
            return "Is this for a dog or a cat?"

        if not slots["category"]:
            return "Which category do you want? Food, toys, or accessories?"

        if not slots["product_name"]:
            return "Which product would you like?"

        return None

    if slots["intent_type"] == "service_booking":
        if not slots["pet_id"]:
            return "Which of your registered pets is this for?"

        if not slots["service"]:
            return "Which service do you want?"

        if not slots["provider_id"]:
            return "Which service provider would you like?"

        if not slots["time_slot"]:
            return "Which time slot do you prefer?"

        return None
