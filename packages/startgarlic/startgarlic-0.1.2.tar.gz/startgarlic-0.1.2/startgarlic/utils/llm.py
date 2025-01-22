import subprocess
from typing import Optional

class LLMManager:
    def __init__(self, model_name: str = "llama2"):
        """Initialize LLM Manager"""
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """Generate response using Ollama"""
        try:
            # Use Ollama with proper encoding
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            
            # Send prompt and get response
            stdout, stderr = process.communicate(input=prompt)
            
            if process.returncode != 0:
                print(f"LLM error: {stderr}")
                return "I'm having trouble processing that. Could you rephrase?"

            response = stdout.strip()
            if not response:
                return "I understand your question. Could you provide more details?"

            return response

        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "I'm here to help! Could you rephrase your question?" 