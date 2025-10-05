# 🌦️ API Fusion - Sistema de Predicción Meteorológica Inteligente

## 🏆 Proyecto Hackathon - Los Migajeros de Norte

**API Fusion** fue desarrollado durante un hackathon por el equipo **Los Migajeros de Norte**, demostrando innovación y excelencia técnica en el campo de la inteligencia artificial aplicada a la meteorología.

## 🚀 Descripción

**API Fusion** es un sistema avanzado de predicción meteorológica que combina **4 modelos de inteligencia artificial** entrenados con datos históricos de la NASA para generar predicciones meteorológicas de alta precisión. Este sistema representa una **fusión inteligente** de múltiples algoritmos de machine learning que trabajan en conjunto para superar las limitaciones de los pronósticos meteorológicos tradicionales.

### 🎯 Objetivo del Proyecto
Desarrollar una solución innovadora que revolucione la predicción meteorológica mediante la aplicación de técnicas avanzadas de machine learning, combinando datos de múltiples fuentes para lograr predicciones de mayor precisión y utilidad práctica.

## 🧠 Modelos de Inteligencia Artificial

### Modelos Entrenados
El sistema utiliza **4 modelos especializados** entrenados con datos históricos de la NASA:

- **🌡️ Modelo T2M** - Predicción de temperatura a 2 metros
- **💧 Modelo RH2M** - Predicción de humedad relativa a 2 metros  
- **💨 Modelo WS2M** - Predicción de velocidad del viento a 2 metros
- **📊 Modelo PS** - Predicción de presión superficial

### Características de los Modelos
- **Entrenamiento con datos de la NASA**: Utilizan datos históricos de alta calidad del sistema POWER de la NASA
- **Algoritmos de Machine Learning**: Implementan técnicas avanzadas de aprendizaje automático
- **Predicción a largo plazo**: Capaces de predecir condiciones meteorológicas para el próximo mes
- **Precisión mejorada**: Combinan datos históricos con patrones temporales para mayor exactitud

## 🔬 Arquitectura del Sistema

### Fusión de Datos
El sistema implementa una **arquitectura de fusión** que combina:

1. **Datos Históricos de la NASA** (7 meses de datos históricos)
2. **Patrones Temporales** (6 lags temporales por variable)
3. **Contexto Estacional** (información del mes actual)
4. **Referencia de OpenWeatherMap** (solo para pronósticos a corto plazo)

### Procesamiento de Características
- **25 características por predicción**: 24 variables de lag temporal + mes actual
- **6 lags temporales**: Análisis de patrones históricos de 6 meses
- **4 variables meteorológicas**: Temperatura, humedad, viento y presión
- **Preprocesamiento inteligente**: Manejo de valores faltantes y normalización

## 🛠️ Tecnologías Utilizadas

### Machine Learning
- **Scikit-learn**: Framework principal para los modelos de ML
- **Joblib**: Serialización y carga de modelos entrenados
- **Pandas**: Manipulación y procesamiento de datos
- **NumPy**: Operaciones numéricas optimizadas

### API y Servicios
- **Flask**: Framework web para la API REST
- **NASA POWER API**: Obtención de datos históricos meteorológicos
- **OpenWeatherMap API**: Referencia para pronósticos a corto plazo (5 días)

## 📊 Capacidades de Predicción

### Predicciones a Corto Plazo (5 días)
- Pronósticos diarios con condiciones generales
- Temperaturas mínimas y máximas
- Condiciones climáticas
- Humedad y velocidad del viento

### Predicciones a Largo Plazo (Próximo mes)
- **Temperatura promedio** (T2M) en Celsius
- **Humedad relativa** (RH2M) en porcentaje
- **Velocidad del viento** (WS2M) en m/s
- **Presión superficial** (PS) en kPa

## 🚀 Instalación y Uso

### Requisitos del Sistema
```bash
pip install -r requirements.txt
```

### Variables de Entorno
```bash
export OPENWEATHERMAP_API_KEY="tu_api_key_aqui"
```

### Ejecución
```bash
python app.py
```

## 📡 Endpoints de la API

### Predicción Completa
```
GET /predict/full?lat={latitude}&lng={longitude}
```

**Parámetros:**
- `lat`: Latitud de la ubicación
- `lng`: Longitud de la ubicación

**Respuesta:**
```json
{
  "location": "Lima, Peru (lat: -12.0464, lon: -77.0428)",
  "short_term_forecast_5_days": [...],
  "long_term_ml_prediction_next_month_avg": {
    "temperature_celsius": 22.5,
    "humidity_percent": 78.3,
    "wind_speed_ms": 3.2,
    "pressure_kpa": 101.2
  }
}
```

## 🎯 Ventajas del Sistema

### Precisión Mejorada
- **Modelos especializados**: Cada variable meteorológica tiene su propio modelo optimizado
- **Datos históricos robustos**: 7 meses de datos de la NASA para entrenamiento
- **Patrones temporales**: Análisis de 6 lags temporales para capturar tendencias

### Escalabilidad
- **Arquitectura modular**: Fácil adición de nuevos modelos
- **API REST**: Integración sencilla con otros sistemas
- **Carga eficiente**: Modelos pre-entrenados cargados en memoria

### Confiabilidad
- **Múltiples fuentes de datos**: NASA + OpenWeatherMap
- **Validación cruzada**: Comparación entre predicciones a corto y largo plazo
- **Manejo de errores**: Sistema robusto de recuperación ante fallos

## 🔬 Metodología Científica

### Entrenamiento de Modelos
1. **Recolección de datos**: 7 meses de datos históricos de la NASA
2. **Preprocesamiento**: Limpieza y normalización de datos
3. **Feature Engineering**: Creación de variables de lag temporal
4. **Entrenamiento**: Optimización de hiperparámetros
5. **Validación**: Evaluación de rendimiento con datos de prueba

### Validación de Predicciones
- **Comparación con datos reales**: Validación contra observaciones meteorológicas
- **Métricas de precisión**: RMSE, MAE, y R² para cada modelo
- **Análisis de tendencias**: Evaluación de patrones temporales

## 🌟 Características Destacadas

- **🤖 4 Modelos de IA Especializados**: Cada uno optimizado para una variable meteorológica específica
- **🛰️ Datos de la NASA**: Utilización de la base de datos meteorológica más confiable del mundo
- **📈 Predicciones a Largo Plazo**: Capacidad única de predecir condiciones del próximo mes
- **🔬 Arquitectura de Fusión**: Combinación inteligente de múltiples fuentes de datos
- **⚡ Alta Precisión**: Modelos entrenados con datos históricos robustos
- **🌍 Cobertura Global**: Funciona en cualquier ubicación del planeta

## 📈 Casos de Uso

- **Agricultura**: Planificación de cultivos y riego
- **Energía Renovable**: Optimización de parques eólicos y solares
- **Logística**: Planificación de rutas y transporte
- **Turismo**: Predicción de condiciones para actividades al aire libre
- **Investigación**: Estudios climáticos y meteorológicos

## 🔧 Mantenimiento

### Actualización de Modelos
Los modelos pueden ser re-entrenados periódicamente con nuevos datos de la NASA para mantener y mejorar la precisión de las predicciones.

### Monitoreo de Rendimiento
- Seguimiento continuo de la precisión de las predicciones
- Alertas automáticas en caso de degradación del rendimiento
- Logs detallados para análisis y debugging

## 👥 Equipo Desarrollador

### Los Migajeros de Norte
Este proyecto fue desarrollado con pasión y dedicación por el equipo **Los Migajeros de Norte** durante un hackathon, demostrando:

- **🚀 Innovación Técnica**: Implementación de soluciones avanzadas de machine learning
- **🔬 Rigor Científico**: Uso de datos de la NASA y metodologías de validación
- **⚡ Eficiencia**: Desarrollo completo en tiempo limitado de hackathon
- **🌍 Impacto Social**: Solución con aplicaciones prácticas en múltiples sectores

### Logros del Equipo
- **Desarrollo completo** de un sistema de predicción meteorológica de vanguardia
- **Integración exitosa** de múltiples fuentes de datos (NASA + OpenWeatherMap)
- **Implementación de 4 modelos de IA** especializados y optimizados
- **API REST funcional** con documentación completa
- **Arquitectura escalable** preparada para producción

---

**API Fusion** representa el futuro de la predicción meteorológica, combinando la potencia de la inteligencia artificial con datos científicos de la más alta calidad para ofrecer predicciones meteorológicas de precisión excepcional.

*Desarrollado con ❤️ por Los Migajeros de Norte durante el hackathon*
