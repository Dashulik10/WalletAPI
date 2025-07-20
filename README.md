# WalletAPI

✅ User registration with password hashing

✅ Basic Authentication for protected endpoints

✅ Fund account (deposit money)

✅ Pay another user

✅ Check your balance

✅ See your transaction history

✅ Add products to a global catalog

✅ Buy products using wallet balance

---

## **Требования**

Для запуска необходимо:

- Python 3.9 или выше
- Установленный Git
- Зависимости, указанные в `requirements.txt`

---

## **Запуск проекта**

### **1. Клонирование репозитория**
Склонируйте проект

Перейдите в папку проекта

---

### **2. Установка зависимостей**

Рекомендуется использовать виртуальное окружение:

```
python -m venv venv  # Создаём виртуальное окружение
```
```
source venv/bin/activate  # Linux/macOS
```
```
venv\Scripts\activate  # Windows
```

Установите зависимости:

```
pip install -r requirements.txt
```

---

### **3. Настройка `.env`**

Создайте файл `.env` в корне проекта и заполните его следующими данными:

```
SECRET_KEY=your_secret_key 
```
```
ALGORITHM=HS256 
```
```
ACCESS_TOKEN_EXPIRE_MINUTES=30 
```
```
DATABASE_URL=postgresql://postgres:123456@postgres_db:5432/wallet
```

Замените значения на свои данные, если нужно.

---

### **4. Запуск проекта**

Для локального запуска используйте следующую команду:

```
uvicorn main:app --reload
```

После запуска приложение будет доступно по адресу:
