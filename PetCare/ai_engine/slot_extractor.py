def extract_slots(text):
    text = text.lower()

    slots = {
        "product_name": None,
        "category": None,
        "pet_type": None,
        "service": None,
        "time_slot": None,
    }

    if "dog" in text:
        slots["pet_type"] = "Dog"
    if "cat" in text:
        slots["pet_type"] = "Cat"

    if "food" in text:
        slots["category"] = "Food"
    elif "toy" in text:
        slots["category"] = "Toys"
    elif "accessory" in text:
        slots["category"] = "Accessories"

    if "groom" in text:
        slots["service"] = "Grooming"
    elif "vet" in text:
        slots["service"] = "Veterinary"
    elif "walk" in text:
        slots["service"] = "Walking"

    if "morning" in text:
        slots["time_slot"] = "Morning"
    elif "evening" in text:
        slots["time_slot"] = "Evening"

    # simple product guess
    if "whiskas" in text:
        slots["product_name"] = "Whiskas Cat Food"
    elif "pedigree" in text:
        slots["product_name"] = "Pedigree Dog Food"

    return slots
