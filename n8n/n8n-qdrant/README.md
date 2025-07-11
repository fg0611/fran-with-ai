Poryecto n8n con Qdrant y modelos Ollama phi3 con 

Aca estamos generando un sistema RAG (Retrieval Aug Generation) en local
con n8n, Qdrant para almacenar chats y vectores y Ollama para el agente de IA

Hay un docker-compose.yaml que conecta todos los servicios y los volumenes para persistencia


🔧 Pasos para levantar correr la imagen, instanciarla y usar el RAg local:

Abrí terminal en la carpeta n8n-qdrant.

Correr:

docker compose up -d

Entra a n8n:
http://localhost:5678
Usuario: admin
Contraseña: admin

Ollama responderá por http://localhost:11434 (en n8n seria http://ollama:11434)

Qdrant estará disponible en:
http://localhost:6333 (en n8n seria http://qdrant:6333)

Si no aun no estan decargados los modelos, descargarlos y dejarlos en la ruta deseada, 
recordar modificar el .yaml

 Verificar modelos cargados en Ollama
Una vez levantado, en otra terminal podés hacer:
Ejecta un GET 
curl http://localhost:11434/api/tags
Y deberías ver phi3:latest y all-minilm:latest listados.
