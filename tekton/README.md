# Tekton CI/CD Pipeline

Este repositorio define un pipeline de CI/CD utilizando **Tekton** para automatizar el flujo de trabajo de una aplicación. El pipeline clona un repositorio Git, construye y publica una imagen Docker, y despliega la aplicación en Kubernetes.

## Componentes Principales

### `pipeline.yaml`

Define el pipeline principal `ci-cd-pipeline` con las siguientes tareas:

1. **`clone-repo`**: Clona el repositorio Git (por defecto: `https://github.com/aramos20/test.git`, rama `main`) usando `git-clone-task`.
2. **`build-and-push`**: Construye y publica la imagen Docker (por defecto: `docker.io/aramos20/myapi:latest`) usando **Kaniko**.
3. **`deploy`**: Despliega la aplicación en Kubernetes aplicando manifiestos YAML.

### `pipelineRun.yaml`

Ejecuta el pipeline con parámetros específicos, como el workspace compartido (`tekton-pvc`). Usa la cuenta de servicio `tekton-service-account`.

---

### `tekton-infra.yaml`

Configura los recursos necesarios:

- **PersistentVolumeClaim (`tekton-pvc`)**: Almacena datos compartidos entre tareas.
- **Secret (`regcred`)**: Almacena credenciales de Docker Hub para autenticación.
- **Role y RoleBinding**: Otorgan permisos al `ServiceAccount` para ejecutar tareas.

---

### `tekton-tasks.yaml`

Define las tareas individuales:

1. **`git-clone-task`**: Clona el repositorio.
2. **`build-and-push-task`**: Construye y publica la imagen Docker.
3. **`deploy-task`**: Despliega la aplicación usando `kubectl apply`.

---

## Uso

### 1. Instalar Tekton Pipelines

```bash
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```
### 2. Crear Secret para Docker Hub
```
kubectl create secret docker-registry regcred \
  --docker-username=TU_USUARIO_DOCKERHUB \
  --docker-password=TU_CONTRASEÑA_DOCKERHUB \
  --docker-email=TU_EMAIL@EJEMPLO.COM
```
### 3. Aplicar los recursos

```bash
kubectl apply -f tekton/storage/
kubectl apply -f tekton/security/
kubectl apply -f tekton/tasks/
kubectl apply -f tekton/pipelines/pipeline.yaml
kubectl apply -f tekton/pipelines/pipelineRun.yaml
```
### 4. Ejecutar el Pipeline
```bash
kubectl apply -f tekton/pipelineRun.yaml
```