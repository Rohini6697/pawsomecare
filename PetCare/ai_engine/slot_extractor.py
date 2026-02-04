# ai_engine/slot_extractor.py

def extract_slots(text):
    text = text.lower()

    slots = {
        "intent_type": None,
        "product_name": None,
        "category": None,
        "pet_type": None,
        "price_range": None,
        "pet_id": None,
        "service": None,
        "provider_id": None,
        "time_slot": None
    }

    # Intent type
    if "buy" in text or "order" in text:
        slots["intent_type"] = "product_booking"
    elif "book" in text or "appointment" in text:
        slots["intent_type"] = "service_booking"

    # Pet type
    if "dog" in text:
        slots["pet_type"] = "Dog"
    elif "cat" in text:
        slots["pet_type"] = "Cat"

    # Services
    if "groom" in text:
        slots["service"] = "Grooming"
    elif "vet" in text:
        slots["service"] = "Veterinary"
    elif "training" in text:
        slots["service"] = "Training"

    # Time
    if "morning" in text:
        slots["time_slot"] = "Morning"
    elif "evening" in text:
        slots["time_slot"] = "Evening"

    return slots
