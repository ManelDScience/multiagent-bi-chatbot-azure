# multiagent-bi-chatbot-azure
Chatbot BI con equipo de agentes, MCP Server propio, Azure SQL Database como BBDD, Azure container Apps y Microsoft Foundry como Cloud services.

## Objetivo

Construir un asistente BI capaz de actuar como un analista de datos senior, interpretando preguntas de negocio, generando consultas SQL seguras, analizando resultados y validando la calidad de las respuestas mediante un equipo multiagente.

## Arquitectura prevista

Usuario  

→ Chatbot / interfaz conversacional  

→ Equipo de agentes  

→ MCP Server  

→ Azure SQL Database  

→ Respuesta analítica de negocio

## Agentes previstos

- Planner Agent: interpreta la pregunta y define el plan de análisis.

- SQL Agent: genera y ejecuta consultas SQL de solo lectura.

- Data Quality Agent: revisa posibles problemas en los datos.

- Analyst Agent: interpreta los resultados.

- Critic Agent: valida la respuesta final.

## Stack tecnológico

- Azure SQL Database

- Azure Container Apps

- Microsoft Foundry

- Model Context Protocol

- Node.js

- Python

- AutoGen

- Docker

- LLMs locales para desarrollo

## Estado actual

- MCP Server básico desarrollado.

- Conexión con Azure SQL validada.

- Despliegue en Azure Container Apps probado.

- Integración inicial con Microsoft Foundry realizada.

- Próximo paso: construcción del equipo multiagente.

## Roadmap

- [ ] Estructurar el repositorio

- [ ] Documentar arquitectura

- [ ] Añadir capa semántica BI

- [ ] Implementar Planner Agent

- [ ] Implementar SQL Agent

- [ ] Implementar Analyst Agent

- [ ] Implementar Data Quality Agent

- [ ] Implementar Critic Agent

- [ ] Añadir demo

- [ ] Preparar despliegue final

## Seguridad

El sistema está diseñado para ejecutar únicamente consultas SQL de lectura. Las credenciales, claves API y variables de entorno no se incluyen en el repositorio.

## Autor

Manel  

Data & AI / BI Specialist
