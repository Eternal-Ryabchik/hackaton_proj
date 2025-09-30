import os
import requests
from typing import Any, Dict, List, Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Local models completely disabled - using external APIs only
TRANSFORMERS_AVAILABLE = False


class LLMClient:
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None
        
        # Initialize OpenAI if available
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
        
        # Initialize Gemini if available
        if GEMINI_AVAILABLE:
            api_key = os.getenv("GEMINI_API_KEY")
            print(f"Gemini API key found: {bool(api_key)}")
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    self.gemini_model = genai.GenerativeModel('gemini-pro')
                    print("Gemini model initialized successfully")
                except Exception as e:
                    print(f"Gemini initialization error: {e}")
            else:
                print("GEMINI_API_KEY not found in environment")
        else:
            print("GEMINI_AVAILABLE is False")
        
                # Using external APIs only - no local models
                # This ensures fast startup and reliable performance
    
    async def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response using available LLM"""
        
        # Try Groq first (fastest and free)
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key:
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [
                            {"role": "system", "content": "Ты - ассистент по data engineering. Помогаешь создавать ETL пайплайны и анализировать данные."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Groq error: {e}")
        
        # Try Gemini (fast and free)
        print(f"Gemini model available: {self.gemini_model is not None}")
        if self.gemini_model:
            try:
                full_prompt = f"""Ты - ассистент по data engineering. Помогаешь создавать ETL пайплайны и анализировать данные.

Пользователь: {prompt}

Ответь кратко и по делу:"""
                print("Calling Gemini API...")
                response = self.gemini_model.generate_content(full_prompt)
                print(f"Gemini response received: {response.text[:100]}...")
                return response.text
            except Exception as e:
                print(f"Gemini error: {e}")
        else:
            print("Gemini model not initialized")
        
        # Try OpenAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Ты - ассистент по data engineering. Помогаешь создавать ETL пайплайны и анализировать данные."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"OpenAI error: {e}")
        
        # Try alternative APIs
        # 1. Try YandexGPT (if API key available)
        yandex_api_key = os.getenv("YANDEX_API_KEY")
        if yandex_api_key:
            try:
                response = requests.post(
                    "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                    headers={
                        "Authorization": f"Api-Key {yandex_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "modelUri": f"gpt://{os.getenv('YANDEX_FOLDER_ID', 'b1g...')}/yandexgpt",
                        "completionOptions": {
                            "stream": False,
                            "temperature": 0.7,
                            "maxTokens": max_tokens
                        },
                        "messages": [
                            {"role": "system", "content": "Ты - ассистент по data engineering. Помогаешь создавать ETL пайплайны и анализировать данные."},
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["result"]["alternatives"][0]["message"]["text"]
            except Exception as e:
                print(f"YandexGPT error: {e}")
        
        # 2. Try Groq (fast and free)
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key:
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [
                            {"role": "system", "content": "Ты - ассистент по data engineering. Помогаешь создавать ETL пайплайны и анализировать данные."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Groq error: {e}")
        
        # 3. Try Together AI (affordable)
        together_api_key = os.getenv("TOGETHER_API_KEY")
        if together_api_key:
            try:
                response = requests.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {together_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "meta-llama/Llama-2-7b-chat-hf",
                        "messages": [
                            {"role": "system", "content": "Ты - ассистент по data engineering. Помогаешь создавать ETL пайплайны и анализировать данные."},
                            {"role": "user", "content": prompt}
                        ],
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    },
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"Together AI error: {e}")
        
        # Ultimate fallback - provide helpful response instead of error
        # No local models - only external APIs for reliability
        if "etl" in prompt.lower() or "пайплайн" in prompt.lower():
            return "Для создания ETL пайплайна используйте вкладку 'Pipeline Preview'. Система автоматически сгенерирует план на основе вашего описания."
        elif "анализ" in prompt.lower() or "проанализируй" in prompt.lower():
            return "Для анализа данных загрузите файлы во вкладке 'Upload & Profile'. Система покажет структуру, типы данных и рекомендации по хранению."
        elif "рекомендации" in prompt.lower() or "хранение" in prompt.lower():
            return "Используйте вкладку 'Recommendations' для получения советов по выбору системы хранения (PostgreSQL/ClickHouse/HDFS) и генерации DDL."
        else:
            return "Я могу помочь с созданием ETL пайплайнов, анализом данных и рекомендациями по хранению. Используйте соответствующие вкладки в интерфейсе."
    
    async def parse_intent(self, text: str) -> Dict[str, Any]:
        """Parse user intent using LLM"""
        prompt = f"""
        Проанализируй следующий запрос пользователя и определи:
        1. Тип операции (etl, анализ, подключение к источнику)
        2. Источники данных (csv, json, xml, база данных)
        3. Целевое хранилище (postgres, clickhouse, hdfs)
        4. Операции трансформации (join, агрегация, фильтрация)
        
        Запрос: {text}
        
        Ответь в формате JSON:
        {{
            "intent": "etl|analysis|connection",
            "sources": ["csv", "json"],
            "target": "postgres|clickhouse|hdfs",
            "operations": ["join", "aggregate"],
            "schedule": "@daily|@hourly|manual"
        }}
        """
        
        response = await self.generate_response(prompt)
        
        # Try to extract JSON from response
        try:
            import json
            # Look for JSON in the response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception:
            pass
        
        # Fallback to simple parsing with better logic
        text_lower = text.lower()
        if any(word in text_lower for word in ["etl", "пайплайн", "конвейер", "объедини", "соедини"]):
            intent = "etl"
        elif any(word in text_lower for word in ["анализ", "проанализируй", "изучи"]):
            intent = "analysis"
        else:
            intent = "etl"  # Default to ETL for most requests
        
        # Detect sources
        sources = []
        if "csv" in text_lower:
            sources.append("csv")
        if "json" in text_lower:
            sources.append("json")
        if "xml" in text_lower:
            sources.append("xml")
        if not sources:
            sources = ["csv", "json"]  # Default sources
        
        # Detect target
        target = "postgres"
        if "clickhouse" in text_lower or "click" in text_lower:
            target = "clickhouse"
        elif "hdfs" in text_lower or "hadoop" in text_lower:
            target = "hdfs"
        
        return {
            "intent": intent,
            "sources": sources,
            "target": target,
            "operations": ["join", "aggregate"],
            "schedule": "@daily"
        }
    
    async def generate_pipeline_steps(self, intent_data: Dict[str, Any], profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate pipeline steps based on intent and data profiles"""
        
        prompt = f"""
        Создай план ETL пайплайна на основе:
        
        Намерение: {intent_data}
        Профили данных: {profiles}
        
        Верни массив шагов в формате:
        [
            {{"op": "read_csv", "name": "source1", "path": "./data/input.csv"}},
            {{"op": "read_json", "name": "source2", "path": "./data/input.json"}},
            {{"op": "join", "left": "source1", "right": "source2", "on": "user_id"}},
            {{"op": "aggregate", "by": "user_id", "metric": "avg", "column": "amount"}},
            {{"op": "write_postgres", "table": "public.result"}}
        ]
        
        Доступные операции: read_csv, read_json, read_xml, trim_strings, join, aggregate, filter, write_postgres, write_clickhouse
        """
        
        response = await self.generate_response(prompt, max_tokens=800)
        
        try:
            import json
            start = response.find('[')
            end = response.rfind(']') + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception:
            pass
        
        # Fallback to default steps
        return [
            {"op": "read_csv", "name": "csv", "path": "./data/input.csv"},
            {"op": "read_json", "name": "json", "path": "./data/input.json"},
            {"op": "join", "left": "csv", "right": "json", "on": "user_id"},
            {"op": "aggregate", "by": "user_id", "metric": "avg", "column": "amount", "alias": "avg_check"},
            {"op": "write_postgres", "table": "public.etl_result"}
        ]


# Global instance
llm_client = LLMClient()
