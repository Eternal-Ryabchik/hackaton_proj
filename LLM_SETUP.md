# 🤖 Настройка LLM API

**Проект использует только внешние LLM API - никаких локальных моделей!**

## Быстрый старт (рекомендуется)

### 1. **Google Gemini API** (БЕСПЛАТНО, БЫСТРО, КАЧЕСТВЕННО) ⭐
1. Зарегистрируйтесь на https://makersuite.google.com/app/apikey
2. Получите API ключ (бесплатно!)
3. Добавьте в docker-compose.yml:
   ```yaml
   environment:
     - GEMINI_API_KEY=your_gemini_key_here
   ```
4. Перезапустите: `docker compose up -d --build api`

### 2. **Groq API** (БЕСПЛАТНО, БЫСТРО) ⭐ РЕКОМЕНДУЕТСЯ
1. Зарегистрируйтесь на https://console.groq.com/
2. Получите API ключ (начинается с `gsk_`)
3. Добавьте в docker-compose.yml:
   ```yaml
   environment:
     - GROQ_API_KEY=ваш_реальный_ключ_здесь
   ```
4. Перезапустите: `docker compose up -d --build api`

### 2. **YandexGPT** (РУССКИЙ, ДЕШЕВО)
1. Зарегистрируйтесь на https://cloud.yandex.ru/
2. Создайте сервисный аккаунт
3. Получите API ключ и Folder ID
4. Добавьте в docker-compose.yml:
   ```yaml
   environment:
     - YANDEX_API_KEY=your_yandex_key_here
     - YANDEX_FOLDER_ID=your_folder_id_here
   ```

### 3. **OpenAI API** (КАЧЕСТВЕННО, ДОРОГО)
1. Получите ключ на https://platform.openai.com/
2. Добавьте в docker-compose.yml:
   ```yaml
   environment:
     - OPENAI_API_KEY=your_openai_key_here
   ```

### 4. **Together AI** (ДЕШЕВО, ОТКРЫТЫЕ МОДЕЛИ)
1. Зарегистрируйтесь на https://api.together.xyz/
2. Получите API ключ
3. Добавьте в docker-compose.yml:
   ```yaml
   environment:
     - TOGETHER_API_KEY=your_together_key_here
   ```

## Приоритет API (по порядку):
1. **Groq** (БЕСПЛАТНО, СУПЕР БЫСТРО) ⭐
2. **Gemini** (БЕСПЛАТНО, быстро, качественно)
3. **OpenAI** (если есть ключ)
4. **YandexGPT** (русский язык)
5. **Together AI** (дешево)
6. **Fallback** (умные правила)

## Стоимость (примерно):
- **Groq**: БЕСПЛАТНО (до лимитов) ⭐
- **Gemini**: БЕСПЛАТНО (до 15 запросов в минуту)
- **YandexGPT**: ~$0.01 за 1K токенов
- **Together AI**: ~$0.002 за 1K токенов
- **OpenAI**: ~$0.002 за 1K токенов

## Рекомендация для демо:
Используйте **Groq** - бесплатно, СУПЕР быстро, надежно! 🚀

## Преимущества внешних API:
- ✅ Быстрый запуск (нет загрузки моделей)
- ✅ Надежность (Google/OpenAI инфраструктура)
- ✅ Качество (лучшие модели)
- ✅ Масштабируемость
- ✅ Нет проблем с памятью/GPU
