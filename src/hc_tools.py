from langchain_core.tools import tool


@tool
def schedule_appointment(patient_name: str, date: str, doctor: str) -> str:
    """Schedule an appointment"""
    return f"Appointment booked for {patient_name} with Dr.{doctor} on {date}"


@tool
def search_symptoms(symptoms: str) -> str:
    """Search for infomation about medical symptoms"""
    return f"Symptoms: {symptoms}. Please consult the doctor for more information."


@tool
def get_medication_info(medication: str) -> str:
    """Get Information about medicine"""
    return f"Here are your medicines: {medication}. Please follow doctor's prescription"
