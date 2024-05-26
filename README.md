# Telegram Bot

Этот Telegram бот может тегать всех участников группы по команде "взываю к небесам" и позволяет пользователям устанавливать свои ники для использования в тегах.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Создайте и активируйте виртуальное окружение:

    - Для Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - Для macOS и Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4. Создайте файл `settings.py` и добавьте в него ваш токен:

    ```python
    # settings.py
    TOKEN = 'YOUR_BOT_API_TOKEN'
    ```

## Запуск

Запустите бота:

```bash
python main.py
