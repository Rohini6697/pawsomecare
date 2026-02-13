def get_rule_based_response(message):
    message = message.lower().strip()

    greetings = ["hi", "hello", "hey"]
    product_keywords = ["food", "toy", "product", "accessory", "dog food", "cat food", "pet food", "grooming", "health care"]
    care_keywords = ["feed", "care", "groom", "puppy", "kitten", "health", "vet", "training"]
    navigation_keywords = ["where", "page", "section", "contact", "about"]

    if any(word in message for word in greetings):
        return "Hi! Welcome to PetCare 🐾<br>How can I help you today?"

    elif any(word in message for word in ["food", "dog food", "cat food", "pet food"]):
        return "🍖 Pet Food includes:<br>✔ Dog Food<br>✔ Cat Food<br>✔ Treats<br>✔ Special Diets<br>Please visit the Products section for details."

    elif "grooming" in message:
        return "✂️ Grooming products and services include:<br>✔ Shampoos & Conditioners<br>✔ Brushes & Combs<br>✔ Nail Care<br>✔ Grooming Appointments<br>Check the Products section for more info."

    elif any(word in message for word in ["accessory", "toy", "product"]):
        return "🧸 Pet Accessories include:<br>✔ Toys<br>✔ Leashes & Collars<br>✔ Beds & Crates<br>✔ Feeding Bowls<br>Visit the Products section to explore more."

    elif any(word in message for word in ["health", "care", "vet", "training"]):
        return "🩺 Pet Health Care includes:<br>✔ Vitamins & Supplements<br>✔ Medicines<br>✔ Vet Consultation<br>✔ Training Aids<br>Make sure to visit the Health Care section."

    elif any(word in message for word in navigation_keywords):
        return "You can use the navigation menu at the top of the website to explore different sections like Products, Services, Contact, and About."

    else:
        return "Sorry, I can assist only with PetCare related questions. 🐾<br>You can ask about:<br>• Pet Food<br>• Grooming<br>• Accessories<br>• Health Care<br>• Services<br>• Contact Details"
