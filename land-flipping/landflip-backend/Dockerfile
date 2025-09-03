FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# System deps for Postgres, GeoPandas/GDAL stack, build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev \
    gdal-bin libgdal-dev \
    libgeos-dev libproj-dev \
    && rm -rf /var/lib/apt/lists/*
ENV GDAL_DATA=/usr/share/gdal
ENV PROJ_LIB=/usr/share/proj
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
