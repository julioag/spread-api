# Nombre de la Aplicación

Spread Api desarrollada con el framework FastAPI

## Requisitos previos

- Tener instalado docker
- Tener instalado docker-compose

## Instalación

1. Clona el repositorio: `git clone https://github.com/julioag/spread-api.git`
2. Navega al directorio del proyecto: `cd spread-api`
3. Instala las dependencias: `docker-compose build`

## Uso

1. Ejecuta la aplicación: `docker-compose up`
2. Abre tu navegador y visita `http://localhost`
3. Para abrir la documentación de Swagger visita `http://localhost/docs`

## Tests

1. Ejecuta los tests: `docker-compose run --rm web pytest`
2. Verifica que todos los tests pasen correctamente