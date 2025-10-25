# Restaurant Message Classifier

Sistem klasifikasi pesan restoran menggunakan GPT-5-nano dan Streamlit.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the application:
```bash
streamlit run main.py
```

## Features

- **Input Page**: Submit pesan dalam Bahasa Indonesia
- **Dashboard**: Admin view untuk melihat semua pesan
- **Auto Classification**: Menggunakan GPT-5-nano untuk klasifikasi otomatis
- **Database Storage**: Menyimpan ke Supabase

## Classification

- **Urgency**: Not Urgent, Urgent, Extremely Urgent  
- **Groups**: Facility, The Waiters, The Chef, Cleanse, Administration, Hospitality, The Foods
