#!/bin/bash

# Crea la base de datos
flask db init

# Ejecuta las migraciones
flask db migrate -m "Initial migration"
flask db upgrade

# Inicia el servidor Flask
flask run --host=0.0.0.0 --port=5000
