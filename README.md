# kissformylover

Telegram-бот із зображеннями й повідомленнями за розкладом.

| Розташування | Призначення |
| --- | --- |
| `Main.py` | запуск бота та фонових повідомлень |
| `Routes.py` | обробники та розклад |
| `images/` | зображення, які використовує бот |
| `.env` | особисті параметри та токен |
| `requirements.txt` | Python-залежності |
| `deploy/kissformylover.service` | шаблон служби Linux |
| `.git/`, `.agents/` | історія проєкту та службова папка |

Локальне середовище `.venv` у цій копії ще не створене. Для локального запуску
з цієї папки:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -B -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -B Main.py
```

Файл служби Cryptohelp перенесений до `../Cryptohelpvlaev/deploy/`.
