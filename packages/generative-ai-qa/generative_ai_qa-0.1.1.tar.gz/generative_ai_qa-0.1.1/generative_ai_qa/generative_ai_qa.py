import google.generativeai as genai
from uuid import uuid4

class GenerativeAIQuestionAnswering:
    def __init__(self, api_key, model_name, file_path):
        """
        Initializes the GenerativeAIQuestionAnswering instance.

        :param api_key: API key for Google Generative AI.
        :param model_name: Name of the generative model.
        :param file_path: Path to the text file containing the data.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.file_path = file_path
        self.model = None
        self.data = None
        self.sessions = {}  # Dictionary to store session data
        self.configure_model()

    def configure_model(self):
        """Configures the Generative AI model."""
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def load_data_from_file(self):
        """Loads data from the specified file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.data = file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
            self.data = None

    def create_session(self):
        """
        Creates a new session for a user.

        :return: A unique session ID.
        """
        session_id = str(uuid4())
        self.sessions[session_id] = {"questions": [], "answers": []}
        return session_id

    def generate_response(self, question, session_id):
        """
        Generates a response to the given question using the loaded data for a specific session.

        :param question: User's question.
        :param session_id: Unique session ID.
        :return: Response text from the model.
        """
        if not self.data:
            return "Error: No data loaded to generate a response."
        
        if session_id not in self.sessions:
            return "Error: Invalid session ID."

        prompt = f"Using the provided information below, answer the question:\n{self.data}\nQuestion: {question}"
        response = self.model.generate_content(prompt)

        # Save the question and response to the session
        self.sessions[session_id]["questions"].append(question)
        self.sessions[session_id]["answers"].append(response.text)

        return response.text

    def ask_questions(self, session_id):
        """
        Allows the user to interactively ask questions based on the text data for a specific session.

        :param session_id: Unique session ID.
        """
        if not self.data:
            print("Error: No data loaded. Please check the file path and contents.")
            return
        
        while True:
            # Get user question
            question = input("Ask a question based on the provided text (or type 'exit' to quit): ")
            
            # Exit if the user types 'exit'
            if question.lower() == 'exit':
                print("Exiting session...")
                break
            
            # Generate and display the response
            response = self.generate_response(question, session_id)
            print("Response:", response)

# Main execution
if __name__ == "__main__":
    # Specify the API key, model name, and file path
    API_KEY = "AIzaSyD7c5Y3QIN0mfymznS8RpoSzkkogyYVFN0"
    MODEL_NAME = "gemini-1.5-flash"
    FILE_PATH = "data1.txt"  # Replace with the path to your text file

    # Create an instance of the class
    ai_qa = GenerativeAIQuestionAnswering(API_KEY, MODEL_NAME, FILE_PATH)
    
    # Load the data from the file
    ai_qa.load_data_from_file()
    
    # Start a new session
    session_id = ai_qa.create_session()
    print(f"Session started. Your session ID is: {session_id}")
    
    # Allow the user to ask questions
    ai_qa.ask_questions(session_id)
