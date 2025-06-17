# Gunakan image Python 3.11 minimal
FROM python:3.11-slim

# Instal dependensi sistem untuk paket Python berat seperti scipy, sentence-transformers
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc g++ gfortran \
    libblas-dev liblapack-dev libatlas-base-dev \
    libffi-dev libssl-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Buat direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt saja dulu (biar cache build efisien)
COPY requirements.txt .

# Install dependensi Python dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file project ke dalam container
COPY . .

# Jalankan aplikasi Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
