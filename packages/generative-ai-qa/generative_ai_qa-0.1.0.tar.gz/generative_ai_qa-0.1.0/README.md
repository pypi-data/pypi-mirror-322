# Generative AI QA

A Python package for question answering using Google Generative AI.

## Installation

Install the package using pip:

```bash
pip install generative_ai_qa

from generative_ai_qa import GenerativeAIQuestionAnswering

api_key = "YOUR_API_KEY"
model_name = "gemini-1.5-flash"
file_path = "data1.txt"

ai_qa = GenerativeAIQuestionAnswering(api_key, model_name, file_path)
ai_qa.load_data_from_file()
session_id = ai_qa.create_session()
ai_qa.ask_questions(session_id)
