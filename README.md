# Proyecto de Aplicación con CI/CD en Kubernetes

Este proyecto incluye una aplicación **Flask** que se despliega en un clúster **Kubernetes**, con un pipeline de **CI/CD** utilizando **Tekton** para automatizar la construcción y despliegue de la aplicación.

## Estructura del Proyecto

```bash
./ 
├── app/ # Código de la aplicación 
│ ├── app.py # Archivo principal de la aplicación Flask 
│ ├── requirements.txt # Dependencias de la aplicación 
│ ├── Dockerfile # Dockerfile para construir la imagen de la app 
│ └── .dockerignore # Archivos a excluir durante la construcción 
├── k8s/ # Manifiestos de Kubernetes 
│ ├── backend.yaml # Despliegue del backend de la aplicación 
│ ├── frontend.yaml # Despliegue del frontend de la aplicación 
│ ├── postgres.yaml # Despliegue del servicio de PostgreSQL 
│ └── configmap.yaml # Configuración de la base de datos y otros servicios 
└── tekton/ # Configuración de CI/CD con Tekton 
  ├── pipeline/ # Definición del pipeline
  ├── pipelineRun.yaml # Definición del PipelineRun 
  ├── tekton-infra.yaml # Configuración de la infraestructura de Tekton
  ├── tekton-service-account.yaml/ # Configuración de la cuenta de servicio
  └── tekton-tasks.yaml/ # Tareas de Tekton
```

La estructura del proyecto está organizada en tres directorios principales:

1. **`app/`**: Contiene el código de la aplicación y los archivos relacionados con la construcción de la imagen Docker.
2. **`k8s/`**: Contiene los manifiestos de Kubernetes para desplegar los servicios y recursos necesarios (incluyendo la base de datos y la aplicación).
3. **`tekton/`**: Contiene los archivos de configuración de **Tekton**, incluyendo el pipeline y las tareas necesarias para realizar el CI/CD.

## Descripción de los Directorios

### 1. `app/`

Este directorio contiene el código fuente de la aplicación Flask que se ejecutará dentro del contenedor Docker.

- **`app.py`**: Archivo principal de la aplicación Flask. Aquí se manejan las rutas y la conexión con la base de datos.
- **`requirements.txt`**: Contiene las dependencias necesarias para la aplicación, como `Flask` y `psycopg2` para la conexión con la base de datos PostgreSQL.
- **`Dockerfile`**: Define cómo construir la imagen Docker para la aplicación. Se asegura de copiar el código, instalar las dependencias y ejecutar la aplicación.
- **`.dockerignore`**: Lista los archivos que no deben ser incluidos en la construcción de la imagen Docker, como archivos temporales o de configuración local.

### 2. `k8s/`

Contiene los manifiestos de Kubernetes necesarios para desplegar la aplicación y sus servicios asociados.

- **`backend.yaml`**: Manifiesto de Kubernetes para desplegar el contenedor de la aplicación backend en un pod.
- **`frontend.yaml`**: Manifiesto de Kubernetes para desplegar el frontend (si se tiene uno).
- **`postgres.yaml`**: Manifiesto de Kubernetes para desplegar PostgreSQL en un StatefulSet.
- **`configmap.yaml`**: Configuración de Kubernetes que contiene valores como el nombre de la base de datos, usuario y contraseña para el backend y PostgreSQL.

### 3. `tekton/`

Contiene todos los archivos de configuración de **Tekton** necesarios para automatizar el flujo de trabajo CI/CD.

#### **`pipeline/`**

- **`pipeline.yaml`**: Define el pipeline de Tekton, que consta de varias tareas (clonar el repositorio, construir la imagen Docker, y desplegar la aplicación).
- **`pipelinerun.yaml`**: Configura la ejecución de un pipeline con los parámetros necesarios, como el nombre de la imagen.

#### **`tasks/`**

- **`git-clone-task.yaml`**: Tarea de Tekton para clonar el repositorio de Git.
- **`build-and-push-task.yaml`**: Tarea de Tekton para construir y subir la imagen Docker a un registro (Docker Hub, por ejemplo).
- **`deploy-task.yaml`**: Tarea de Tekton para desplegar los recursos de Kubernetes (utilizando `kubectl apply`).

#### **`service-account/`**

- **`tekton-service-account.yaml`**: Define la cuenta de servicio que Tekton usará para ejecutar el pipeline. Esta cuenta tiene acceso a los secretos y los permisos necesarios para interactuar con el clúster Kubernetes.

#### **`infrastructure/`**

- **`tekton-infra.yaml`**: Define recursos como Persistent Volume Claims (PVCs) necesarios para almacenar los artefactos de construcción y otros archivos generados durante la ejecución del pipeline.

#### **`secrets/`**

- **`regcred.yaml`**: Contiene las credenciales necesarias para acceder a los registros de Docker privados (como Docker Hub) durante el proceso de construcción y despliegue.
