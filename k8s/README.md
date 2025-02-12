# Despliegue de una Aplicación 3-Tier en Kubernetes

Este repositorio incluye manifiestos de Kubernetes para desplegar una aplicación web con **frontend** , **backend** y base de datos **PostgreSQL** .

---

## Componentes

### 1. `k8s/postgres.yaml`
- **`StatefulSet`**: Persistencia de datos y nombre estable para PostgreSQL.
- **`Servicio`**: Expone PostgreSQL internamente como `postgres`.

---

### 2. `k8s/backend.yaml`
- **`Deployment`**: Backend en Docker conectado a PostgreSQL mediante variables de entorno.
- **`Servicio`**: Exposición externa vía `NodePort`.

---

### 3. `k8s/frontend.yaml`
- **`Deployment`**: Nginx sirviendo archivos estáticos desde un ConfigMap.
- **`Servicio`**: Exposición externa vía `NodePort`.

---

### 4. `k8s/configmap.yaml`
- `DB_HOST`: Nombre del servicio de PostgreSQL.
- `DB_NAME`: Nombre de la base de datos.
- `DB_USER`: Usuario para conectarse a la base de datos.
- `index.html`: Almacena un archivo que se sirve después a través de Nginx

---

### 5. `k8s/secret.yaml`
- **`DB_PASS`**: Almacena credenciales seguras para PostgreSQL.

---

## Despliegue de la Aplicación

### 1. Crear los recursos de Kubernetes
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml
```
### 2. Acceder a la aplicación
Exponer servicios:
```bash
minikube service frontend-service
minikube service backend-service
```
Redirigir puertos:
```bash
kubectl port-forward svc/backend-service 30007:5000 &
kubectl port-forward svc/frontend-service 30010:80 &
```
