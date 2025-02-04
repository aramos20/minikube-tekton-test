# Despliegue de una Aplicación con arquitectura 3-Tier en Kubernetes

Este repositorio contiene los manifiestos de Kubernetes para desplegar una aplicación web compuesta por un frontend, un backend y una base de datos PostgreSQL.

## Componentes

1. **`k8s/postgres.yaml` - PostgreSQL (StatefulSet, Servicio y Secreto)**

   Este archivo define los recursos necesarios para ejecutar PostgreSQL en Kubernetes:

   * **StatefulSet:** Garantiza la persistencia de los datos mediante un volumen persistente y proporciona un nombre estable para el pod de PostgreSQL.
   * **Servicio:** Expone PostgreSQL internamente en el clúster bajo el nombre `postgres`, permitiendo que otros pods accedan a la base de datos.
   * **Secreto:** Almacena de forma segura las credenciales de acceso a la base de datos (usuario y contraseña).

2. **`k8s/backend.yaml` - Backend (Deployment y Servicio)**

   Contiene los manifiestos para el backend de la aplicación:

   * **Deployment:** Despliega el pod del backend utilizando una imagen Docker. La aplicación Flask se conecta a PostgreSQL mediante las variables de entorno definidas en el ConfigMap.
   * **Servicio:** Expone el backend externamente mediante un NodePort, permitiendo el acceso desde fuera del clúster.

3. **`k8s/frontend.yaml` - Frontend (ConfigMap, Deployment y Servicio)**

   Define los recursos para el frontend de la aplicación:

   * **ConfigMap:** Almacena los archivos estáticos (por ejemplo, `index.html`) que se sirven a través de un contenedor Nginx.
   * **Deployment:** Despliega el contenedor Nginx, que sirve los archivos estáticos desde el ConfigMap.
   * **Servicio:** Expone el frontend externamente mediante un NodePort, permitiendo el acceso desde fuera del clúster.

4. **`k8s/configmap.yaml` - ConfigMap de la Base de Datos**

   Contiene las variables de entorno necesarias para la conexión a la base de datos PostgreSQL:

   * `DB_HOST`: Nombre del servicio de PostgreSQL (`postgres`).
   * `DB_NAME`: Nombre de la base de datos.
   * `DB_USER`: Usuario para conectarse a la base de datos.

## Despliegue de la Aplicación

Para desplegar la aplicación en un clúster Kubernetes, sigue estos pasos:

1. **Crear los recursos de Kubernetes:**

   Aplica los manifiestos de Kubernetes para crear todos los recursos necesarios:

   ```bash
   kubectl apply -f k8s/postgres.yaml
   kubectl apply -f k8s/backend.yaml
   kubectl apply -f k8s/frontend.yaml
   ```
2. **Verificar los servicios y pods**

   Verifica que los servicios y pods se hayan creado correctamente:

   ```bash
   kubectl get pods
   kubectl get svc
   ```
3. **Acceder a la aplicación**

   El frontend será accesible en el puerto 30010 y el backend en el puerto 30007. Puedes verificar esto con el siguiente comando:

   ```bash
   kubectl get svc frontend-service
   kubectl get svc backend-service
   ```
   y luego
   ```bash
   kubectl port-forward svc/backend-service 30007:5000 &
   kubectl port-forward svc/frontend-service 30010:80 &
   ```
   La aplicación frontend será accesible a través de la IP del nodo y el puerto 30010, mientras que el backend será accesible a través del puerto 30007.

4. **Eliminar los recursos**

   Si deseas eliminar todos los recursos creados, puedes ejecutar:

   ```bash
   kubectl delete -f k8s/postgres.yaml
   kubectl delete -f k8s/backend.yaml
   kubectl delete -f k8s/frontend.yaml
   ```