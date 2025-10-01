# DataEngineer AI 🚀

**Intelligent Data Engineering Platform with LLM Integration**

## 🎯 **Уникальная фишка: Semantic Data Engineer**

Наша платформа использует **семантическое понимание данных** для автоматического создания ETL пайплайнов. AI понимает контекст ваших данных и предлагает оптимальные решения без ручного программирования.

## ✨ **Ключевые возможности:**

### 🤖 **AI-Powered Data Engineering**
- **Семантический анализ данных** - AI понимает структуру и назначение данных
- **Автоматическое создание ETL** - Генерация пайплайнов по описанию на естественном языке
- **Умные рекомендации** - AI предлагает оптимальные решения для хранения и обработки
- **Проактивная оптимизация** - Система сама находит узкие места и предлагает улучшения

### 🔧 **Технические возможности**
- **Мультиформатная поддержка** - CSV, JSON, XML
- **Интеллектуальное профилирование** - Автоматический анализ качества данных
- **Векторный поиск** - Семантический поиск по документации и метаданным
- **Real-time мониторинг** - Отслеживание выполнения пайплайнов
- **Генерация DDL** - Автоматическое создание схем БД

## 🏗️ **Архитектура**

```
Frontend (React + TypeScript)
    ↓
API Gateway (FastAPI)
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Data Profiling │   LLM Services  │   Pipeline Exec │
│   - CSV/JSON/XML │   - Groq API    │   - DAG Engine  │
│   - Quality Check│   - Gemini API  │   - Airflow Gen │
│   - Schema Detect│   - OpenAI API  │   - Monitoring  │
└─────────────────┴─────────────────┴─────────────────┘
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   PostgreSQL    │   ClickHouse     │   ChromaDB      │
│   - Metadata    │   - Analytics    │   - Vector DB   │
│   - Pipeline Log│   - Data Storage │   - Semantic    │
└─────────────────┴─────────────────┴─────────────────┘
```

## 🚀 **Быстрый старт**

### **1. Клонирование репозитория**
```bash
git clone https://github.com/yourusername/dataengineer-ai.git
cd dataengineer-ai
```

### **2. Настройка LLM API (обязательно!)**
Создайте файл `.env` в корне проекта:
```bash
# Groq API (рекомендуется - бесплатно и быстро)
GROQ_API_KEY=your_groq_api_key_here

# Альтернативные API
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
YANDEXGPT_API_KEY=your_yandex_api_key_here
```

### **3. Запуск через Docker**
```bash
# Запуск всех сервисов
docker compose up -d --build

# Проверка статуса
docker compose ps
```

### **4. Доступ к приложению**
- **Frontend:** http://localhost:5132
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## 🎮 **Как пользоваться**

### **1. Загрузка и профилирование данных**
- Перетащите файлы CSV/JSON/XML в интерфейс
- Система автоматически проанализирует структуру и качество данных
- Получите детальный отчет с рекомендациями

### **2. Создание ETL пайплайнов**
- Опишите задачу на естественном языке: *"Объедини данные по user_id и посчитай сумму"*
- AI автоматически создаст оптимальный пайплайн
- Визуализируйте граф выполнения в реальном времени

### **3. Мониторинг и оптимизация**
- Отслеживайте выполнение пайплайнов
- Получайте рекомендации по оптимизации
- Анализируйте производительность через дашборд

## 🔧 **Локальная разработка**

### **Backend (Python)**
```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Frontend (React)**
```bash
cd frontend
npm install
npm run dev
```

### **База данных**
```bash
docker compose up -d postgres redis clickhouse chroma
```

## 📊 **Технологический стек**

### **Backend**
- **FastAPI** - Высокопроизводительный API
- **Pandas** - Обработка данных
- **PostgreSQL** - Метаданные и логи
- **ClickHouse** - Аналитическое хранилище
- **ChromaDB** - Векторная база данных

### **Frontend**
- **React 18** - Современный UI
- **TypeScript** - Типизированный JavaScript
- **Ant Design** - Компоненты интерфейса
- **ECharts** - Визуализация данных

### **AI/ML**
- **Groq API** - Быстрые LLM запросы
- **Google Gemini** - Резервный LLM
- **OpenAI GPT** - Дополнительные возможности
- **Векторный поиск** - Семантический анализ

### **DevOps**
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация
- **GitHub Actions** - CI/CD (планируется)

## 🎯 **Уникальные особенности**

### **1. Semantic Data Engineer**
- AI понимает контекст данных, а не просто обрабатывает их
- Автоматическое предложение связей между таблицами
- Генерация data contracts на основе семантики

### **2. Intent-Driven Pipeline Creation**
- Создание пайплайнов по описанию на естественном языке
- Автоматическая оптимизация на основе понимания задачи
- Проактивные рекомендации по улучшению

### **3. Intelligent Data Contracts**
- Автоматическая генерация контрактов данных
- Валидация схем на основе семантического понимания
- Предотвращение breaking changes

## 📈 **Roadmap**

- [ ] **Интеграция с Apache Airflow** - Полноценная оркестрация
- [ ] **ML Pipeline Support** - Поддержка ML пайплайнов
- [ ] **Real-time Streaming** - Обработка потоковых данных
- [ ] **Multi-cloud Support** - Поддержка различных облаков
- [ ] **Advanced Monitoring** - Расширенная аналитика

## 🤝 **Участие в разработке**

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull request

## 👥 **Команда**

- **Backend:** FastAPI, Python, LLM Integration
- **Frontend:** React, TypeScript, Data Visualization
- **AI/ML:** Semantic Understanding, Pipeline Generation
- **DevOps:** Docker, Containerization, CI/CD
