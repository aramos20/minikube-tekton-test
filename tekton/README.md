# Tekton Pipelines para CI/CD

Este repositorio contiene definiciones de Tekton Pipelines para implementar un flujo de Integración Continua y Entrega Continua (CI/CD) para una aplicación.  El pipeline clona un repositorio Git, construye y publica una imagen Docker a Docker Hyb, y despliega la aplicación en Kubernetes.

## Descripción de los Archivos

### `pipeline.yaml`

Define el pipeline principal `ci-cd-pipeline`. Este pipeline consta de tres tareas:

1.  **`clone-repo`**: Clona el repositorio Git especificado en el parámetro `url` (por defecto: `https://github.com/aramos20/test.git`) y la revisión especificada en el parámetro `revision` (por defecto: `main`). Utiliza la tarea `git-clone-task`.
2.  **`build-and-push`**: Construye y publica la imagen Docker. Utiliza la tarea `build-and-push-task` y recibe como parámetro `IMAGE` el nombre de la imagen (por defecto: `docker.io/aramos20/myapi:latest`). Se ejecuta después de `clone-repo`.
3.  **`deploy`**: Despliega la aplicación en Kubernetes. Utiliza la tarea `deploy-task` y se ejecuta después de `build-and-push`.

### `pipelineRun.yaml`

Define la ejecución del pipeline `ci-cd-pipeline`.  Especifica los valores para los parámetros del pipeline, como `IMAGE` (que sobreescribe el valor por defecto en este caso) y el `persistentVolumeClaim` llamado `tekton-pvc` para el workspace compartido.  También define la cuenta de servicio `tekton-service-account` que se utilizará.

### `tekton-infra.yaml`

Define los recursos de infraestructura necesarios para Tekton:

*   **`PersistentVolumeClaim (tekton-pvc)`**:  Solicita 1 Gi de almacenamiento para el workspace compartido entre las tareas del pipeline.  El modo de acceso es `ReadWriteMany`, lo que permite que múltiples pods accedan al volumen simultáneamente.
*   **`Secret (regcred)`**: Almacena las credenciales de Docker Hub en formato `.dockerconfigjson`.  Este secreto se monta en la tarea `build-and-push-task` para permitir la autenticación al publicar la imagen.
*   **`RoleBinding (pipeline-run-access)`**: Otorga permisos al `ServiceAccount` `tekton-service-account` en el namespace `default`. En este caso, se le otorga el rol `admin`, lo cual no es recomendable para un entorno de producción; se debe ajustar a los permisos mínimos necesarios.
*   **`ClusterRoleBinding (tekton-service-account-admin-binding)`**: Otorga permisos de ClusterRole al `ServiceAccount` `tekton-service-account`. De igual manera que el RoleBinding, se otorga el rol `cluster-admin`, lo cual no es recomendable y debe ajustarse a los permisos mínimos necesarios.

### `tekton-service-account.yaml`

Define la cuenta de servicio `tekton-service-account` que se utiliza para ejecutar el pipeline.  Asocia el secreto `regcred` a esta cuenta de servicio.

### `tekton-tasks.yaml`

Define las tareas que componen el pipeline:

*   **`git-clone-task`**: Clona un repositorio Git.  Recibe como parámetros la URL del repositorio (`url`) y la revisión (`revision`).  Verifica la existencia del archivo `Dockerfile` dentro de la carpeta `app` del repositorio clonado.
*   **`build-and-push-task`**: Construye y publica una imagen Docker utilizando Kaniko. Recibe como parámetro el nombre de la imagen (`IMAGE`) y el directorio del Dockerfile (`CONTEXT_DIR`). Utiliza el secreto `regcred` para la autenticación con Docker Hub.
*   **`deploy-task`**: Despliega la aplicación en Kubernetes.  Copia los archivos de manifiesto desde el directorio especificado por el parámetro `MANIFEST_DIR` y los aplica con `kubectl apply`.  Los manifiestos de Kubernetes (configmap.yaml, postgres.yaml, backend.yaml, frontend.yaml) deben estar presentes en el workspace.

## Uso

1.  **Instalación de Tekton:** Asegúrate de tener Tekton Pipelines instalado en tu clúster de Kubernetes. Puedes instalarlo con:

    ```bash
    kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
    ```

2.  **Activación de addons de Minikube (si usas Minikube):** Si estás utilizando Minikube, asegúrate de activar los addons necesarios:

    ```bash
    minikube addons enable ingress
    ```

    El addon `ingress` permite exponer servicios a través de un Ingress.

3.  **Creación de Secret para Kaniko:** Kaniko necesita credenciales para acceder al registro de Docker Hub. Crea un secret llamado `regcred` con tus credenciales:

    ```bash
    kubectl create secret docker-registry regcred \
      --docker-username=TU_USUARIO_DOCKERHUB \
      --docker-password=TU_CONTRASEÑA_DOCKERHUB \
      --docker-email=TU_EMAIL@EJEMPLO.COM \
      --namespace=default
    ```

    Este comando crea un secret en el namespace `default`. Si deseas usar un namespace diferente, asegúrate de ajustarlo.

4.  **Guardar el Secret en un archivo YAML (Opcional):** Si deseas mantener una copia del secret en un archivo YAML, puedes exportarlo con:

    ```bash
    kubectl get secret docker-credential -o yaml > key-alt.yaml
    ```

5.  **Aplicación de los recursos:**

    ```bash
    kubectl apply -f tekton/pipeline.yaml
    kubectl apply -f tekton/tekton-infra.yaml
    kubectl apply -f tekton/tekton-service-account.yaml
    kubectl apply -f tekton/tekton-tasks.yaml
    ```

6.  **Ejecución del Pipeline:**

    ```bash
    kubectl apply -f tekton/pipelineRun.yaml
    ```

## Notas Importantes

*   **Seguridad**:  El uso del rol `admin` en RoleBinding y ClusterRoleBinding no son recomendables para entornos de producción.  Deben ajustarse para mayor seguridad.
*   **Credenciales**: Asegúrate de que el secreto `regcred` contenga las credenciales correctas de Docker Hub.
*   **Manifiestos de Kubernetes**: Los manifiestos de Kubernetes para la aplicación (configmap.yaml, postgres.yaml, backend.yaml, frontend.yaml) deben estar presentes en el directorio especificado por el parámetro `MANIFEST_DIR` en `deploy-task`.
*   **Workspace**: El `persistentVolumeClaim` `tekton-pvc` debe existir y tener suficiente espacio disponible.

Este README proporciona una descripción general de los pipelines de Tekton.  Para obtener información más detallada sobre cada componente, consulta la documentación oficial de Tekton.