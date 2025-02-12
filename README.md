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
│ ├── configmap.yaml # Configuración de la base de datos y otros servicios 
│ └── service.yaml # Almacena credenciales seguras
└── tekton/ # Configuración de CI/CD con Tekton 
  ├── pipeline/ # Definición del pipeline
  ├── pipelineRun.yaml # Definición del PipelineRun 
  ├── tekton-configs.yaml # Configuración de la infraestructura y otros servicios de Tekton
  ├── tekton-service-account.yaml/ # Configuración de la cuenta de servicio
  └── tekton-tasks.yaml/ # Tareas de Tekton
```
La estructura del proyecto está organizada en tres directorios principales:

1. **`app/`**: Contiene el código de la aplicación y los archivos relacionados con la construcción de la imagen Docker.
2. **`k8s/`**: Contiene los manifiestos de Kubernetes para desplegar los servicios y recursos necesarios (incluyendo la base de datos y la aplicación).
3. **`tekton/`**: Contiene los archivos de configuración de **Tekton**, incluyendo el pipeline y las tareas necesarias para realizar el CI/CD.

## Directorios Principales

### 1. `app/`
Contiene el código fuente de la aplicación Flask y los archivos necesarios para construir la imagen Docker.
- **`app.py`**: Aplicación Flask principal.
- **`requirements.txt`**: Dependencias de Python.
- **`Dockerfile`**: Define la construcción de la imagen Docker.
- **`.dockerignore`**: Excluye archivos innecesarios en la imagen.

### 2. `k8s/`
Manifiestos de Kubernetes para desplegar la aplicación y sus servicios.
- **`backend.yaml`**: Despliegue del backend.
- **`frontend.yaml`**: Despliegue del frontend.
- **`postgres.yaml`**: Despliegue de PostgreSQL con StatefulSet.
- **`configmap.yaml`**: Configuración de variables de entorno (DB_HOST, DB_NAME, etc.).
- **`secret.yaml`**: Almacena credenciales seguras para PostgreSQL.

### 3. `tekton/`
Configuración de Tekton para automatizar el flujo CI/CD.

#### `pipeline.yaml`
Define el pipeline principal:
1. **`clone-repo`**: Clona el repositorio Git.
2. **`build-and-push`**: Construye y publica la imagen Docker con Kaniko.
3. **`deploy`**: Despliega la aplicación en Kubernetes.

#### `pipelineRun.yaml`
Ejecuta el pipeline con parámetros específicos, como el workspace compartido (`tekton-pvc`) y la cuenta de servicio `tekton-service-account`.

#### `tekton-infra.yaml`
Configura recursos necesarios:
- **PersistentVolumeClaim (`tekton-pvc`)**: Almacena datos compartidos entre tareas.
- **Secret (`regcred`)**: Credenciales de Docker Hub.
- **Role y RoleBinding**: Permisos para el `ServiceAccount`.

#### `tekton-tasks.yaml`
Define las tareas individuales:
1. **`git-clone-task`**: Clona el repositorio.
2. **`build-and-push-task`**: Construye y publica la imagen Docker.
3. **`deploy-task`**: Despliega la aplicación usando `kubectl apply`.
