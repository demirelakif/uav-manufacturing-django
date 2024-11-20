# Temel imajı seçiyoruz
FROM python:3.10.5

# Çalışma dizini ayarlıyoruz
WORKDIR /app

# Gereksinim dosyasını kopyalıyoruz ve bağımlılıkları yüklüyoruz
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Proje dosyalarını kopyalıyoruz
COPY . /app/

# Çalışma dizinine geçiyoruz
WORKDIR /app/uav_manufacturing_django 

# Gerekli komutları çalıştırıyoruz
# RUN python manage.py migrate 
# RUN python manage.py loaddata fixtures/initial_teams.json
# RUN python manage.py collectstatic --noinput

# Django sunucusunu başlatıyoruz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
