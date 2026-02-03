import requests
import json
import os
from typing import Optional, Dict, Any

class OllamaClient:
    """
    A client for interacting with the Ollama API for local AI processing.
    """
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
    
    def generate(self, model: str, prompt: str, system_prompt: Optional[str] = None, 
                 temperature: float = 0.7, max_tokens: int = 2048) -> Optional[str]:
        """
        Generate a response from the specified model.
        
        Args:
            model: The name of the model to use (e.g., 'llama3', 'mistral')
            prompt: The input prompt for the model
            system_prompt: Optional system prompt to guide the model's behavior
            temperature: Controls randomness (lower = more deterministic)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response or None if an error occurred
        """
        url = f"{self.host}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.ConnectionError:
            print(f"Error: Could not connect to Ollama at {self.host}")
            print("Make sure Ollama is installed and running with 'ollama serve'")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return None
        except KeyError:
            print("Error: Unexpected response format from Ollama")
            return None

    def list_models(self) -> Optional[list]:
        """
        List all available models in Ollama.
        
        Returns:
            List of model information dictionaries
        """
        url = f"{self.host}/api/tags"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()["models"]
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama: {e}")
            return None

    def pull_model(self, model_name: str) -> bool:
        """
        Pull a model from the Ollama library.
        
        Args:
            model_name: Name of the model to pull (e.g., 'llama3')
            
        Returns:
            True if successful, False otherwise
        """
        url = f"{self.host}/api/pull"
        
        payload = {
            "name": model_name,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=600)  # 10 minute timeout for large models
            response.raise_for_status()
            print(f"Successfully pulled model: {model_name}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error pulling model {model_name}: {e}")
            return False

def demo_business_use_cases():
    """
    Demonstrate various business use cases for Ollama integration.
    """
    client = OllamaClient()
    
    print("🔍 Ollama Integration Demo for PAID LLC")
    print("=" * 50)
    
    # Check if Ollama is running
    models = client.list_models()
    if not models:
        print("❌ Ollama is not running or not properly configured.")
        print("Please ensure Ollama is installed and running with 'ollama serve'")
        return
    
    print(f"✅ Connected to Ollama. Available models: {len(models)}")
    
    # Use the first available model, or default to 'llama3'
    model_name = models[0]['name'].split(':')[0] if models else 'llama3'
    print(f"Using model: {model_name}\n")
    
    # Business Use Case 1: Document Analysis
    print("💼 Business Use Case 1: Document Analysis")
    doc_analysis_prompt = """
    Analyze the following business proposal and summarize the key points, 
    potential risks, and recommendations in a structured format:
    
    Proposal: Implementation of AI-driven customer service solution to reduce 
    operational costs by 30% while improving response time to under 2 minutes. 
    Initial investment required: $150,000. Expected ROI: 180% within 18 months.
    """
    
    result = client.generate(
        model=model_name,
        prompt=doc_analysis_prompt,
        system_prompt="You are an expert business analyst. Provide a clear, structured analysis with specific points.",
        temperature=0.3
    )
    
    if result:
        print(f"Analysis Result:\n{result[:500]}...\n")
    
    # Business Use Case 2: Content Creation
    print("✍️  Business Use Case 2: Content Creation")
    content_prompt = """
    Create a compelling LinkedIn post about the benefits of AI adoption for small businesses. 
    Keep it professional but engaging, around 200 words.
    """
    
    result = client.generate(
        model=model_name,
        prompt=content_prompt,
        system_prompt="You are a marketing expert crafting engaging LinkedIn content for business professionals.",
        temperature=0.7
    )
    
    if result:
        print(f"LinkedIn Post:\n{result[:300]}...\n")
    
    # Business Use Case 3: Data Insight Generation
    print("📊 Business Use Case 3: Data Insight Generation")
    data_insight_prompt = """
    Based on the following sales figures, identify trends and provide strategic recommendations:
    Q1: $250K, Q2: $320K, Q3: $280K, Q4: $350K
    Last year's Q4: $220K
    """
    
    result = client.generate(
        model=model_name,
        prompt=data_insight_prompt,
        system_prompt="You are a business intelligence analyst. Provide data-driven insights and actionable recommendations.",
        temperature=0.4
    )
    
    if result:
        print(f"Insights & Recommendations:\n{result[:400]}...\n")

def setup_ollama_for_business():
    """
    Guide the user through setting up Ollama for business use.
    """
    print("🔧 Setting up Ollama for Business Use")
    print("=" * 40)
    
    # Check if Ollama is running
    client = OllamaClient()
    models = client.list_models()
    
    if not models:
        print("Ollama is not running or models are not installed.")
        print("Suggested business-focused models to install:")
        business_models = [
            ("llama3", "General purpose business tasks"),
            ("nous-hermes2", "Business and analytical tasks"),
            ("mistral", "Creative and problem-solving tasks")
        ]
        
        for model, description in business_models:
            print(f"- {model}: {description}")
        
        install_choice = input("\nWould you like to install a model? (y/n): ")
        if install_choice.lower() == 'y':
            model_to_install = input("Enter model name to install (e.g., llama3): ").strip()
            if model_to_install:
                print(f"Installing {model_to_install}...")
                client.pull_model(model_to_install)
    else:
        print(f"✅ Ollama is running with {len(models)} models available.")
        print("Models available:")
        for model in models:
            print(f"- {model['name']} ({model['size']})")

if __name__ == "__main__":
    print("PAID LLC Ollama Integration Demo")
    print("=" * 40)
    
    # Perform setup check
    setup_ollama_for_business()
    
    print("\n" + "=" * 40)
    
    # Run business use case demonstrations
    demo_business_use_cases()
    
    print("\n🎉 Ollama integration demo completed!")
    print("Next steps:")
    print("1. Review the OLLAMA_INTEGRATION_SETUP.md for detailed configuration")
    print("2. Install additional models as needed for your business use cases")
    print("3. Integrate with your existing workflows")