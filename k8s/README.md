# Despliegue de una Aplicación 3-Tier en Kubernetes

Los siguientes directorios incluyen manifiestos de Kubernetes para desplegar una aplicación web con **frontend**, **backend** y base de datos **PostgreSQL**.

---

## Estructura del Directorio

```
k8s/
├── deployments/
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── postgres-stateful.yaml
├── services/
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   ├── frontend-service.yaml
│   ├── postgres-service.yaml
│   ├── secret.yaml
```

---

## Componentes

### PostgreSQL
 **`k8s/deployments/postgres-stateful.yaml`**
- **`StatefulSet`**: Proporciona persistencia de datos y nombre estable para PostgreSQL.

---

### Backend
 **`k8s/deployments/backend-deployment.yaml`**
- **`Deployment`**: Backend en Docker conectado a PostgreSQL mediante variables de entorno.

---

### Frontend
 **`k8s/deployments/frontend-deployment.yaml`**
- **`Deployment`**: Nginx sirviendo archivos estáticos desde un ConfigMap.

---

### Configuración y Seguridad
 **`k8s/services/configmap.yaml`**
- Contiene configuraciones necesarias para la aplicación.
- `DB_HOST`: Nombre del servicio de PostgreSQL.
- `DB_NAME`: Nombre de la base de datos.
- `DB_USER`: Usuario para conectarse a la base de datos.
- `index.html`: Archivo estático servido por Nginx.

 **`k8s/services/secret.yaml`**
- **`DB_PASS`**: Almacena credenciales seguras para PostgreSQL.

 **`k8s/services/backend-service.yaml`**
- **`Servicio`**: Expone el backend internamente como `backend-service`.

 **`k8s/services/frontend-service.yaml`**
- **`Servicio`**: Expone el frontend internamente como `frontend-service`.

 **`k8s/services/postgres-service.yaml`**
- **`Servicio`**: Expone la DB internamente como `postgres-service`.

---

## Despliegue de la Aplicación

### Aplicar los Recursos en Kubernetes
Ejecutar los siguientes comandos en orden:

```bash
kubectl apply -f k8s/services/secret.yaml
kubectl apply -f k8s/services/configmap.yaml
kubectl apply -f k8s/services/postgres-service.yaml
kubectl apply -f k8s/services/backend-service.yaml
kubectl apply -f k8s/services/frontend-service.yaml

kubectl apply -f k8s/deployments/postgres-statefulset.yaml
kubectl apply -f k8s/deployments/backend-deployment.yaml
kubectl apply -f k8s/deployments/frontend-deployment.yaml
```

---

### Acceder a la Aplicación

 **Exponer los Servicios en Minikube**
```bash
minikube service frontend-service
minikube service backend-service
```

 **Redirigir Puertos Manualmente**
> Minikube asigna puertos de manera aleatoria, por lo que es necesario redirigir los puertos manualmente para garantizar el acceso a los servicios en los puertos deseados.

```bash
kubectl port-forward svc/backend-service 30007:5000 &
kubectl port-forward svc/frontend-service 30010:80 &
```
