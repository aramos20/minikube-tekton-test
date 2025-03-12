# Despliegue de una Aplicación 3-Tier en Kubernetes

Este directorio contiene los manifiestos de Kubernetes necesarios para desplegar una aplicación con **frontend, backend y base de datos PostgreSQL**.

---

## Estructura del Directorio

```
k8s/
├── deployments/   # Despliegues (Deployments & StatefulSets)
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── postgres-statefulset.yaml
├── networking/    # Ingress y Configuración de Red
│   └── ingress.yaml
└── services/      # Servicios y Configuraciones
    ├── backend-service.yaml
    ├── configmap.yaml
    ├── frontend-service.yaml
    ├── postgres-service.yaml
    └── secret.yaml
```

---

## Componentes

### **PostgreSQL**  
📌 `k8s/deployments/postgres-statefulset.yaml`
- **`StatefulSet`**: Asegura persistencia de datos y estabilidad en los nombres del servicio de base de datos.

### **Backend**  
📌 `k8s/deployments/backend-deployment.yaml`
- **`Deployment`**: Ejecuta la lógica de negocio y se conecta a PostgreSQL mediante variables de entorno.
- **`Service`**: `k8s/services/backend-service.yaml` expone el backend internamente.

### **Frontend**  
📌 `k8s/deployments/frontend-deployment.yaml`
- **`Deployment`**: Nginx sirviendo archivos estáticos almacenados en un ConfigMap.
- **`Service`**: `k8s/services/frontend-service.yaml` expone el frontend internamente.

### **Configuración y Seguridad**
📌 `k8s/services/configmap.yaml`  
- Contiene configuraciones necesarias para la aplicación, incluyendo:
  - `DB_HOST`: Nombre del servicio de PostgreSQL.
  - `DB_NAME`: Nombre de la base de datos.
  - `DB_USER`: Usuario de conexión.
  - `index.html`: Página servida por Nginx.

📌 `k8s/services/secret.yaml`  
- **`DB_PASS`**: Almacena credenciales seguras para PostgreSQL.

📌 `k8s/networking/ingress.yaml`  
- **`Ingress`**: Define reglas de acceso para exponer frontend y backend a través de Traefik.

---

## Despliegue de la Aplicación

### **1️⃣ Aplicar los Recursos de Kubernetes**
```bash
kubectl apply -f k8s/
```

### **2️⃣ Exponer Servicios con Minikube Tunnel**
```bash
minikube tunnel
```

### **3️⃣ Verificar que todo está corriendo**
```bash
kubectl get ingressclass
kubectl get pods -n default
kubectl get svc -n default
```

Para más detalles sobre el pipeline de CI/CD, consulta [`tekton/README.md`](../tekton/README.md).
