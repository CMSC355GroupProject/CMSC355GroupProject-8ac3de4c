def format_patient(patient_doc):
    return {
        "id": str(patient_doc["_id"]),
        "username": patient_doc.get("username"),
        "email": patient_doc.get("email"),
        "dob": patient_doc.get("dob"),
        "height": patient_doc.get("height"),
        "weight": patient_doc.get("weight"),
        "biological_gender": patient_doc.get("biological_gender"),
        "phone_number": patient_doc.get("phone_number")
    }