import openai
import requests
from rag import RAGRetriever
from groq import Groq


class Chatbot:
    def __init__(self, api_key):
        self.api_key = api_key
        self.state = {
            "mode": None, 
            "complaint_data": {}
        }
        self.rag = RAGRetriever()

    def handle_input(self, user_input):
        if self.state["mode"] == "register_complaint":
            return self._handle_complaint_registration(user_input)

        kb_hits = self.rag.query(user_input)
        kb_context = "\n".join(kb_hits)

        prompt = (
            f"You are a helpful customer service chatbot.\n"
            f"Your job is to detect if the user wants to:\n"
            f"1. Register a complaint\n"
            f"2. Check status of a registered complaint\n"
            f"3. Ask some general question (then just answer it)\n\n"
            f"Customer input: {user_input}\n"
            f"Relevant info: {kb_context}\n"
            f"Respond by indicating the detected intent in this JSON format:\n"
            f'{{"intent": "register_complaint" | "check_complaint" | "general_query", "complaint_id": "<id_if_applicable>", "reply": "<your reply>"}}'
        )

        llm_reply = self.query_llm(prompt)

        import json
        try:
            result = json.loads(llm_reply)
        except json.JSONDecodeError:
            return "Sorry, I couldn't understand. Could you rephrase?"

        intent = result.get("intent")
        reply = result.get("reply", "")

        if intent == "register_complaint":
            self.state["mode"] = "register_complaint"
            self.state["complaint_data"] = {}
            return reply + "\nCould you please tell me your name?"

        elif intent == "check_complaint":
            complaint_id = result.get("complaint_id")
            if complaint_id:
                return f"Thanks for waiting. Here are the details:\n{self.get_complaint(complaint_id)}"
            else:
                return reply + "\nCould you please provide your complaint ID?"

        else:
            return reply

    def _handle_complaint_registration(self, user_input):
        data = self.state["complaint_data"]

        if "name" not in data:
            data["name"] = user_input
            return "Thanks! May I have your phone number?"
        
        if "phone_number" not in data:
            data["phone_number"] = user_input
            return "Great. Could you provide your email address?"

        if "email" not in data:
            data["email"] = user_input
            return "Almost done. Please describe your complaint."

        if "complaint_details" not in data:
            data["complaint_details"] = user_input
            complaint_id = self.register_complaint(data)
            self.state = {"mode": None, "complaint_data": {}}
            return f"Thank you! Your complaint has been registered. Your complaint ID is: {complaint_id}"

        return "I'm not sure what to do next. Let's start over."

    def register_complaint(self, data):
        response = requests.post("http://127.0.0.1:8002/complaints/", json=data)
        print(response.status_code, "=======status=========")
        if response.status_code == 200:
            return response.json().get("complaint_id", "UNKNOWN")
        else:
            return "Error while Registering!!!"

    def get_complaint(self, complaint_id):
        response = requests.get(f"http://127.0.0.1:8002/complaints/{complaint_id}")
        if response.status_code == 200:
            data = response.json()
            return (
                f"Complaint ID: {data['complaint_id']}\n"
                f"Name: {data['name']}\n"
                f"Phone: {data['phone_number']}\n"
                f"Email: {data['email']}\n"
                f"Details: {data['complaint_details']}\n"
                f"Created At: {data['created_at']}"
            )
        else:
            return "Complaint not found!!!"    
    

    def query_llm(self, prompt):
        client = Groq(
            api_key=self.api_key
        )

        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a polite and helpful customer service assistant that interact with user."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=300
        )

        return chat_completion.choices[0].message.content
