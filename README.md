# Minikube + Tekton CI/CD + Traefik

Este proyecto implementa un flujo de CI/CD en Kubernetes utilizando **Minikube, Tekton y Traefik** para gestionar el despliegue de una aplicación 3-Tier con **backend, frontend y base de datos PostgreSQL**.

## Estructura del Proyecto

```
./
├── README.md
├── Dockerfile
├── app.py
├── requirements.txt
├── .dockerignore
├── k8s/
│   ├── README.md
│   ├── deployments/
│   │   ├── backend-deployment.yaml
│   │   ├── frontend-deployment.yaml
│   │   └── postgres-statefulset.yaml
│   ├── networking/
│   │   └── ingress.yaml
│   └── services/
│       ├── backend-service.yaml
│       ├── configmap.yaml
│       ├── frontend-service.yaml
│       ├── postgres-service.yaml
│       └── secret.yaml
└── tekton/
    ├── README.md
    ├── pipelines/
    │   ├── pipeline.yaml
    │   └── pipelineRun.yaml
    ├── security/
    │   ├── docker-registry-secret.yaml
    │   ├── role-binding.yaml
    │   ├── role.yaml
    │   └── service-account.yaml
    ├── storage/
    │   └── persistent-volume-claim.yaml
    └── tasks/
        ├── build-and-push-task.yaml
        ├── deploy-task.yaml
        └── git-clone-task.yaml
```

---

## Debes tener previamente instalado:

- **Kubernetes (Minikube):** Clúster local para desplegar los servicios.
- **Helm (Minikube):** Clúster local para desplegar los servicios.

---

## Instalación y Configuración

### **1️⃣ Iniciar Minikube**
```bash
minikube start
```

### **2️⃣ Instalar Tekton**
```bash
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

### **3️⃣ Instalar Traefik con Helm**
```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik \
  -n default
```

### **4️⃣ Aplicar y Ejecutar el Pipeline en Tekton**
```bash
kubectl apply -f tekton/storage/
kubectl apply -f tekton/security/
kubectl apply -f tekton/tasks/
kubectl apply -f tekton/pipelines/pipeline.yaml
kubectl apply -f tekton/pipelines/pipelineRun.yaml
```

### **5️⃣ Exponer Servicios con Minikube Tunnel**
```bash
minikube tunnel
```

### **Acceder a la Aplicación con Traefik**
Si configuraste el `Ingress.yaml` con `nip.io`, accede desde el navegador a:
```
http://backend.127.0.0.1.nip.io
http://frontend.127.0.0.1.nip.io
```
Si prefieres usar nombres personalizados, agrega la IP de Minikube a `/etc/hosts`:
```bash
minikube ip
```
Ejemplo si la IP es `192.168.49.2`:
```
192.168.49.2 backend.local
192.168.49.2 frontend.local
```
Luego accede a:
```
http://backend.local
http://frontend.local
```

---

## 🔄 Flujo CI/CD con Tekton
1️⃣ **Clona el código fuente desde GitHub.**  
2️⃣ **Construye y publica la imagen Docker usando Kaniko en Docker Hub.**  
3️⃣ **Despliega la aplicación en Kubernetes aplicando los manifiestos YAML.**  

Para más detalles, consulta los README específicos dentro de [`k8s/`](k8s/README.md) y [`tekton/`](tekton/README.md).