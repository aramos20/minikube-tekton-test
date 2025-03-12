# Tekton CI/CD Pipeline

Este directorio contiene los recursos de **Tekton Pipelines** para la automatización del CI/CD en Kubernetes.

---

## Estructura del Directorio

```
tekton/
├── pipelines/   # Definiciones de pipelines
│   ├── pipeline.yaml
│   └── pipelineRun.yaml
├── security/    # Seguridad y permisos
│   ├── docker-registry-secret.yaml
│   ├── role-binding.yaml
│   ├── role.yaml
│   └── service-account.yaml
├── storage/     # Almacenamiento Persistente
│   └── persistent-volume-claim.yaml
└── tasks/       # Definición de Tareas en el Pipeline
    ├── build-and-push-task.yaml
    ├── deploy-task.yaml
    └── git-clone-task.yaml
```

---

## Componentes Principales

### **Pipeline Principal** (`pipelines/pipeline.yaml`)
- **`clone-repo`**: Clona el código fuente desde GitHub usando `git-clone-task`.
- **`build-and-push`**: Construye y publica la imagen Docker en Docker Hub con Kaniko.
- **`deploy`**: Despliega la aplicación en Kubernetes con `kubectl apply`.

### **Ejecución del Pipeline** (`pipelines/pipelineRun.yaml`)
- Ejecuta el pipeline `ci-cd-pipeline` con un workspace compartido (`tekton-pvc`).

### **Tareas (`tasks/`)
- **`git-clone-task.yaml`**: Clona el código fuente desde un repositorio.
- **`build-and-push-task.yaml`**: Construye y publica la imagen Docker.
- **`deploy-task.yaml`**: Despliega la aplicación en Kubernetes.

### **Seguridad y Permisos (`security/`)
- **`docker-registry-secret.yaml`**: Credenciales para Docker Hub.
- **`service-account.yaml`**: Define permisos para la ejecución de Tekton.
- **`role.yaml` & `role-binding.yaml`**: Asignan permisos al `ServiceAccount`.

### **Almacenamiento (`storage/`)
- **`persistent-volume-claim.yaml`**: Proporciona almacenamiento compartido entre tareas.

---

## Uso

### **1️⃣ Instalar Tekton Pipelines**
```bash
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

### **2️⃣ Crear Secret para Docker Hub**
```bash
kubectl create secret docker-registry regcred \
  --docker-username=TU_USUARIO_DOCKERHUB \
  --docker-password=TU_CONTRASEÑA_DOCKERHUB \
  --docker-email=TU_EMAIL@EJEMPLO.COM
```

### **3️⃣ Aplicar los Recursos de Tekton**
```bash
kubectl apply -f tekton/storage/
kubectl apply -f tekton/security/
kubectl apply -f tekton/tasks/
```

### **4️⃣ Ejecutar el Pipeline**
```bash
kubectl apply -f tekton/pipelines/
```

### **5️⃣ Verificar el Estado de la Ejecución**
```bash
tkn pipeline list
tkn pipelinerun list
```

Para más detalles sobre la infraestructura Kubernetes, consulta [`k8s/README.md`](../k8s/README.md).
