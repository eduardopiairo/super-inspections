# Kubernetes Learning Plan

Learning Kubernetes through the Super Inspections project — from local cluster to production-grade deployment.

**Assumed baseline:** Comfortable with `kubectl`, written basic manifests, understand pods/deployments/services.

---

## Phase 1 — Containerize the App

**Goal:** Have a real multi-service app to deploy, not toy examples.

Tasks:
- Pick and scaffold the tech stack (e.g. Node.js API + PostgreSQL + React frontend)
- Write a `Dockerfile` for each service (API, frontend)
- Set up `docker-compose.yml` for local development
- Pin image versions and use multi-stage builds to keep images lean

Outcome: `docker-compose up` runs the full Super Inspections stack locally.

---

## Phase 2 — Local Kubernetes Cluster

**Goal:** Deploy Super Inspections to a real (local) cluster with proper K8s primitives.

Tasks:
- Stand up a local cluster with [kind](https://kind.sigs.k8s.io/) or [minikube](https://minikube.sigs.k8s.io/)
- Write `Deployment` and `Service` manifests for each component
- Use `Namespaces` to separate environments (e.g. `dev`, `staging`)
- Manage config with `ConfigMap` and sensitive values with `Secret`
- Expose the app externally with an `Ingress` (nginx ingress controller)

Outcome: Super Inspections accessible at `http://super-inspections.local` on your machine.

---

## Phase 3 — Stateful Workloads

**Goal:** Run PostgreSQL properly in Kubernetes (not as a plain Deployment).

Tasks:
- Replace Deployment with a `StatefulSet` for PostgreSQL
- Provision storage with `PersistentVolume` and `PersistentVolumeClaim`
- Use `Init Containers` to handle DB migrations before the API starts
- Understand headless services and stable pod DNS

Outcome: The database survives pod restarts without data loss.

---

## Phase 4 — Helm

**Goal:** Package the entire app as a reusable, configurable Helm chart.

Tasks:
- Scaffold a Helm chart with `helm create`
- Templatize all manifests (image tags, replica counts, resource limits, secrets)
- Create separate `values.dev.yaml` and `values.prod.yaml`
- Practice `helm upgrade --install` and `helm rollback`

Outcome: A single `helm upgrade` deploys or updates Super Inspections with environment-specific config.

---

## Phase 5 — Reliability & Scaling

**Goal:** Make the app resilient to failures and load spikes.

Tasks:
- Set `resources.requests` and `resources.limits` on every container
- Add `livenessProbe` and `readinessProbe` to the API
- Configure `Horizontal Pod Autoscaler` (HPA) based on CPU/memory
- Set `PodDisruptionBudget` to ensure availability during node drains
- Test rolling updates and practice `kubectl rollout undo`

Outcome: The app auto-scales and recovers from pod failures without downtime.

---

## Phase 6 — Observability

**Goal:** Know what's happening inside the cluster at all times.

Tasks:
- Deploy `kube-prometheus-stack` (Prometheus + Grafana) via Helm
- Add custom metrics to the Node.js API and scrape them
- Set up centralized logging with Grafana Loki (or EFK if you prefer)
- Create a Grafana dashboard for Super Inspections (request rate, error rate, latency)
- Configure alerts for API errors and pod crash loops

Outcome: A live dashboard showing the health of every Super Inspections component.

---

## Phase 7 — CI/CD & GitOps

**Goal:** Automate every deployment through git — no manual `kubectl apply`.

Tasks:
- Add a GitHub Actions workflow to build and push Docker images on merge to `main`
- Install [ArgoCD](https://argo-cd.readthedocs.io/) in the cluster
- Point ArgoCD at this repo so it syncs the Helm chart automatically
- Practice the GitOps loop: PR → merge → ArgoCD detects diff → deploys

Outcome: Pushing to `main` automatically deploys a new version of Super Inspections.

---

## Phase 8 — Cloud Deployment

**Goal:** Run Super Inspections on a managed Kubernetes service in the cloud.

Tasks:
- Provision a cluster on GKE, EKS, or AKS
- Use cloud-native storage classes and load balancers
- Set up RBAC — least-privilege `ServiceAccounts` for each workload
- Store secrets in a proper secrets manager (AWS Secrets Manager / GCP Secret Manager) and sync with the [External Secrets Operator](https://external-secrets.io/)
- Enable network policies to restrict pod-to-pod traffic

Outcome: Super Inspections running in the cloud with production-grade security and access control.

---

## Reference Resources

| Topic | Resource |
|---|---|
| Core concepts | [Kubernetes docs](https://kubernetes.io/docs/home/) |
| Hands-on labs | [KillerCoda](https://killercoda.com/), [Play with Kubernetes](https://labs.play-with-k8s.com/) |
| Helm | [Helm docs](https://helm.sh/docs/) |
| GitOps | [ArgoCD getting started](https://argo-cd.readthedocs.io/en/stable/getting_started/) |
| Observability | [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) |
| Certification (optional) | CKA (admin) or CKAD (developer) |
