#!/bin/bash

# Función que espera a que PostgreSQL haya sido inicializado.
function pg_wait {
  while : ; do
    pg_isready --host db --user postgres
    if [ $? == 0 ]; then
      break
    else
      sleep 1
    fi
  done
}

# Función que espera a que RabbitMQ haya sido inicializado.
# Actualmente, sólo espera 3 segundos, sin efectuar verificaciones.
function rabbitmq_wait {
  sleep 3
}

pg_wait
rabbitmq_wait

celery worker -A reservas -B -l info
