# Tekton CI/CD Pipeline

Aquí se define un pipeline de CI/CD utilizando **Tekton** para automatizar el flujo de trabajo de una aplicación. El pipeline clona un repositorio Git, construye y publica una imagen Docker, y despliega la aplicación en Kubernetes.

## Estructura del Directorio
```
tekton/
├── pipelines/
│   ├── pipeline.yaml
│   ├── pipelineRun.yaml
├── security/
│   ├── docker-registry-secret.yaml
│   ├── role-binding.yaml
│   ├── role.yaml
│   ├── service-account.yaml
├── storage/
│   ├── persistent-volume-claim.yaml
├── tasks/
│   ├── build-and-push-task.yaml
│   ├── deploy-task.yaml
│   ├── git-clone-task.yaml
```

## Componentes Principales

### `pipelines/`
 **`pipeline.yaml`**: Define el pipeline principal `ci-cd-pipeline` con las siguientes tareas:

1. **`clone-repo`**: Clona el repositorio Git (por defecto: `https://github.com/aramos20/test.git`, rama `main`) usando `git-clone-task`.
2. **`build-and-push`**: Construye y publica la imagen Docker (por defecto: `docker.io/aramos20/myapi:latest`) usando **Kaniko**.
3. **`deploy`**: Despliega la aplicación en Kubernetes aplicando manifiestos YAML.

 **`pipelineRun.yaml`**: Ejecuta el pipeline con parámetros específicos, como el workspace compartido (`tekton-pvc`). Usa la cuenta de servicio `tekton-service-account`.

---

### `tasks/`
Define las tareas individuales que se ejecutan dentro del pipeline:

- **`git-clone-task.yaml`** → Clona el repositorio.
- **`build-and-push-task.yaml`** → Construye y publica la imagen Docker usando Kaniko.
- **`deploy-task.yaml`** → Despliega la aplicación en Kubernetes ejecutando `kubectl apply`.

---

### `storage/`
 **`persistent-volume-claim.yaml`**: Proporciona un volumen persistente (`tekton-pvc`) para compartir datos entre tareas.

---

### `security/`
 **`docker-registry-secret.yaml`**: Almacena credenciales de Docker Hub para autenticación.

 **`service-account.yaml`**: Define la `ServiceAccount` utilizada por Tekton.

 **`role.yaml` & `role-binding.yaml`**: Otorgan permisos al `ServiceAccount` para ejecutar tareas en Kubernetes.

---

## Uso

### Instalar Tekton Pipelines
```bash
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

### Crear Secret para Docker Hub
```bash
kubectl create secret docker-registry regcred \
  --docker-username=TU_USUARIO_DOCKERHUB \
  --docker-password=TU_CONTRASEÑA_DOCKERHUB \
  --docker-email=TU_EMAIL@EJEMPLO.COM
```

### Aplicar los recursos de Tekton
```bash
kubectl apply -f tekton/storage/
kubectl apply -f tekton/security/
kubectl apply -f tekton/tasks/
kubectl apply -f tekton/pipelines/pipeline.yaml
kubectl apply -f tekton/pipelines/pipelineRun.yaml
```

### Ejecutar el Pipeline
```bash
kubectl apply -f tekton/pipelines/pipelineRun.yaml
```
