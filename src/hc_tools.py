from langchain_core.tools import tool

class HCTools:
    @tool
    def schedule_appointment(self,patient_name:str, date:str, doctor: str)-> str:
        """Schedule an appointment """
        return f"Appointment booked for {patient_name} with Dr.{doctor} on {date}"

    @tool
    def search_symptoms(self,symptoms:str)-> str:
        """Search for infomation about medical symptoms"""
        return f"Symptoms: {symptoms}. Please consult the doctor for more information."

    @tool
    def get_medication_info(self,medication:str)->str:
        """Get Information about medicine"""
        return f"Here are your medicines: {medication}. Please follow doctor's prescription"