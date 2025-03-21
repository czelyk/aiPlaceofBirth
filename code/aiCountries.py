import ollama

class AICountries:
    def __init__(self):
        self.model = ollama

    def get_random_countries(self):
        try:
            response = self.model.chat(model="llama2", messages=[{"role": "user", "content": "Generate the name of 10 countries randomly and one celebrity from them and which city they were born in."}])
            content = response['message']['content'] if 'message' in response and 'content' in response['message'] else ''

            countries = content.split("\n") if content else ["No countries generated"]
            return [country.strip() for country in countries if country.strip()]
        except Exception as e:
            print(f"Error: {e}")
            return ["Error retrieving countries"]
