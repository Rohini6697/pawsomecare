def next_question(slots):

    if slots["intent_type"] == "ecommerce":

        if not slots["pet_type"]:
            return "Is this for a dog or a cat?"

        if not slots["category"]:
            return "What category do you want? Food, toys, or accessories?"

        if not slots["product_name"]:
            return "Which product would you like?"

        return None

    if slots["intent_type"] == "service_booking":

        if not slots["pet_type"]:
            return "Is this for a dog or a cat?"

        if not slots["service"]:
            return "Which service do you need? Grooming, walking, or vet?"

        if not slots["time_slot"]:
            return "Which time slot do you prefer?"

        return None

    return "How can I help you?"
