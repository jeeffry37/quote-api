#📖 Quote API (Frases Motivacionales)
📌 Descripción del proyecto

Quote API es una aplicación cloud-native construida con Python (Flask) que devuelve frases motivacionales.
El objetivo es demostrar el uso de contenedorización (Docker), orquestación (Kubernetes), monitorización (Prometheus + Grafana) e Infraestructura como Código (IaC con Terraform).

Endpoints principales:

GET / → mensaje de bienvenida.
GET /quote → devuelve una frase aleatoria.
GET /quotes → devuelve todas las frases.
POST /quote → añade una frase nueva (en memoria).
GET /healthz → health check para Kubernetes.
GET /metrics → métricas en formato Prometheus.

🚀 Cómo ejecutar el proyecto
🔹 1. Local (Flask)
# Clonar el repo
git clone https://github.com/<tu-usuario>/quote-api.git
cd quote-api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar app
python app/app.py

🔹 2. Docker
# Construir imagen
docker build -t quote-api:1.0 .

# Ejecutar contenedor
docker run -d -p 5000:5000 quote-api:1.0

# Si quieres subirla a DockerHub
docker tag quote-api:1.0 "usuario de docker"/quote-api:1.0
docker push "usuario de docker"/quote-api:1.0

🔹 3. Kubernetes (Minikube / local)
# Crear namespace
kubectl apply -f k8s/namespace.yaml

# Crear despliegue y servicio
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml


# Exponer servicio con NodePort en Minikube
minikube service -n quote-api quote-api-service --url
📊 Monitorización

Prometheus scrapea métricas desde /metrics.

Grafana muestra dashboards con:

Requests totales (http_requests_total).

Latencia (http_request_duration_seconds).

Errores (status != 200).
