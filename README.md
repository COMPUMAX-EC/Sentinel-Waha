# 🛡️ Sentinel WhatsApp - Inteligencia de Datos y Optimización de Conversión

> **Sistema inteligente de análisis y automatización para WhatsApp Business usando infraestructura propia WAHA**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 🎯 El Problema

WhatsApp es actualmente una **"caja negra"** en nuestras operaciones de venta:

- ❌ **Tasa de Abandono Desconocida**: No sabemos en qué punto exacto el cliente deja de responder
- ❌ **Ventana de Oro Perdida**: Perdemos ventas por tardar más de 10 minutos en contestar
- ❌ **Fuga de Datos**: La información vive en teléfonos de vendedores, no en sistemas centralizados
- ❌ **Sin Métricas**: Imposible optimizar sin medir

## 💡 La Solución

**Sentinel WhatsApp** es un sistema de inteligencia que convierte WhatsApp en un canal de ventas medible y optimizable:

### ✨ Características Principales

1. **📊 Auditoría Histórica**
   - Extracción masiva de conversaciones pasadas
   - Análisis de patrones de éxito y abandono
   - Identificación de puntos críticos en el embudo

2. **🤖 Automatización Humanizada**
   - Respuestas que simulan comportamiento humano
   - Tiempos de escritura realistas
   - Uso inteligente de emojis, audios y reacciones

3. **📈 Analytics en Tiempo Real**
   - Dashboard de métricas de conversión
   - Alertas de clientes "calientes"
   - Seguimiento de KPIs críticos

4. **🎯 Clasificación por Intención**
   - **Alta**: Palabras clave como "precio", "pago", "envío" → Respuesta inmediata
   - **Media**: Preguntas técnicas o de garantía → Asignación a experto
   - **Baja**: Saludos o spam → Filtrado automático

## 🚧 Estado actual

Proyecto en desarrollo. Lo que ya está en el código:

| Módulo | Estado |
|---|---|
| `utils/waha_client.py`: cliente WAHA (sesión, chats, mensajes, enviar, escribiendo..., reacciones, webhook) | ✅ |
| `extractors/`: extracción de historial, tiempos de respuesta, preguntas frecuentes, tipos de mensaje | ✅ |
| `classifiers/`: clasificador de intención por palabras clave (alta / media / baja) y prioridad | ✅ |
| `response/`: motor de respuestas con plantillas, retraso y tiempo de escritura humanizados | ✅ |
| `webhooks/`: `POST /webhooks/waha`, `POST /webhooks/test`, `GET /webhooks/status` | ✅ |
| `analytics/` (rutas y dashboard), base de datos y migraciones, pruebas automatizadas | ⏳ pendiente |

> `main.py` ya importa `sentinel.analytics.routes`; mientras ese módulo no exista, comenta esa línea para levantar
> el servidor solo con los webhooks.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    WhatsApp Business API                     │
│                   (waha.compumax.tech)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  SENTINEL WHATSAPP                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Extractor   │  │  Classifier  │  │   Response   │      │
│  │   Module     │──│    Engine    │──│   Engine     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         ▼                  ▼                  ▼              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Analytics & Dashboard                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Fases del Proyecto

### Fase I: Diagnóstico (Backlog Analysis)
**Objetivo**: Entender qué está pasando

- Extracción masiva de mensajes vía API
- Procesamiento de historial completo
- Identificación de las 5 preguntas que matan o cierran ventas
- Análisis de tiempos de respuesta vs conversión

**Entregable**: Reporte de insights con patrones de éxito/fracaso

### Fase II: Automatización
**Objetivo**: Responder más rápido y mejor

- Configuración de Webhooks en tiempo real
- Motor de respuestas humanizadas
- Sistema de detección de intención
- Asignación inteligente a vendedores

**Entregable**: Sistema de respuestas automáticas activo 24/7

### Fase III: Monitoreo
**Objetivo**: Optimización continua

- Dashboard en tiempo real
- Métricas de conversión por vendedor
- Alertas de oportunidades
- A/B testing de respuestas

**Entregable**: Panel de control con visibilidad total del embudo

## 💰 Ventajas Competitivas

| Aspecto | Solución Tradicional | Sentinel WhatsApp |
|---------|---------------------|-------------------|
| **Costo** | $0.005-0.05 por mensaje | Infraestructura propia (costo fijo) |
| **Control** | Datos en servidores terceros | 100% en nuestros servidores |
| **Privacidad** | Compartida con proveedores | Total privacidad |
| **Escalabilidad** | Costo crece con volumen | Ilimitado sin costo adicional |
| **Personalización** | Limitada por API externa | Control total del código |

## 🛠️ Stack Tecnológico

- **Backend**: Python 3.9+ (FastAPI)
- **Base de Datos**: PostgreSQL + Redis
- **Analytics**: Pandas, NumPy, Scikit-learn
- **WhatsApp API**: WAHA (WhatsApp HTTP API)
- **Dashboard**: Streamlit / React
- **Infraestructura**: Compumax.tech VM

## 📦 Instalación

### Prerrequisitos

- Python 3.9 o superior
- Una instancia de [WAHA](https://waha.devlike.pro) (WhatsApp HTTP API) con su API key
- PostgreSQL y Redis quedan para las fases siguientes (analytics y caché)

### Setup Rápido

```bash
# Clonar repositorio
git clone https://github.com/COMPUMAX-EC/Sentinel-Waha.git
cd Sentinel-Waha

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Iniciar servidor (el paquete está en src/)
PYTHONPATH=src python main.py   # En Windows PowerShell: $env:PYTHONPATH="src"; python main.py
```

## ⚙️ Configuración

Edita el archivo `.env`:

```env
# WAHA API Configuration
WAHA_API_URL=https://waha.compumax.tech
WAHA_API_KEY=tu_api_key_aqui
WAHA_SESSION_NAME=default

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sentinel_waha
REDIS_URL=redis://localhost:6379/0

# Features
ENABLE_AUTO_RESPONSE=true
ENABLE_ANALYTICS=true
RESPONSE_DELAY_MIN=2
RESPONSE_DELAY_MAX=5

# Webhooks
WEBHOOK_SECRET=tu_secret_aqui
WEBHOOK_URL=https://tu-dominio.com/webhooks/waha
```

## 📊 Uso

### Extracción de Historial

```python
import asyncio
from sentinel.extractors import MessageExtractor

extractor = MessageExtractor()
messages = asyncio.run(extractor.extract_all_messages())
report = extractor.process_messages(messages)  # tiempos de respuesta, preguntas frecuentes, tipos de mensaje
```

### Análisis de Intención

```python
from sentinel.classifiers import IntentClassifier

classifier = IntentClassifier()
intent = classifier.classify("Cuál es el precio del producto?")

print(f"Intención: {intent.level}")  # Output: "high"
print(f"Confianza: {intent.confidence}")  # Output: 0.92
```

### Respuesta Automatizada

```python
from sentinel.classifiers import IntentClassifier
from sentinel.response import ResponseEngine, ResponseContext

message = "Me interesa el producto"
context = ResponseContext(
    customer_message=message,
    intent=IntentClassifier().classify(message),
    conversation_history=[],
)
response = ResponseEngine().generate_response(context, humanize=True)
print(response)  # texto, retraso y duración de "escribiendo..."
```

## 📈 Métricas Clave

El sistema monitorea automáticamente:

- **Tasa de Respuesta**: % de mensajes contestados
- **Tiempo de Primera Respuesta**: Promedio y percentil 90
- **Tasa de Abandono**: Por etapa del embudo
- **Tasa de Conversión**: Mensajes → Ventas cerradas
- **Palabras Calientes**: Keywords con mayor conversión
- **Horarios Óptimos**: Mejor momento para contactar

## 🧪 Testing

Las pruebas automatizadas todavía no están escritas; `pytest` y `pytest-asyncio` ya vienen en `requirements.txt`
para cuando se agreguen en `tests/`. Con `APP_DEBUG=true`, la API se puede probar a mano en `/docs` (Swagger).

## 🤝 Contribución

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Roadmap

- [x] **Q4 2025**: Fase I - Diagnóstico y análisis histórico
- [ ] **Q1 2026**: Fase II - Automatización de respuestas
- [ ] **Q2 2026**: Fase III - Dashboard y monitoreo en tiempo real
- [ ] **Q3 2026**: Machine Learning para optimización automática
- [ ] **Q4 2026**: Multi-canal (Instagram, Telegram)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

Desarrollado con ❤️ por el equipo de Compumax.tech

---

**¿Preguntas o sugerencias?** Abre un [issue](https://github.com/COMPUMAX-EC/Sentinel-Waha/issues).

---

*"No estamos instalando un bot de respuestas automáticas molesto. Estamos construyendo un sistema de inteligencia de ventas que nos permite estar presentes 24/7 con la misma calidad que si estuviéramos nosotros escribiendo, pero con la velocidad de un algoritmo."*
