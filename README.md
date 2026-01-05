Cloudopshub

This is the main application repository for Cloudopshub. It contains the source code for our microservices and the CI logic that keeps everything running.

We use a 3-repo GitOps architecture to keep things clean:

    App Repo (This one): Code, Dockerfiles, and Jenkins automation.

    Infra Repo: Terraform for the AWS VPC and EKS cluster.

    ArgoCD Repo: Kubernetes Helm charts and environment state.

Project Layout

The project is broken down into modular services. Each folder is self-contained with its own logic, dependencies, and tests:

    analysis-processing-service/: Python/Pandas logic for heavy data processing.

    data-api-service/: FastAPI-based entry point for metrics.

    data-ingest-service/: Handles incoming data streams and background tasks.

    Frontend Dashboard/: Nginx-based UI. It serves the static assets and acts as a reverse proxy to route /api calls to the backends.

    user-billing-service/: Manages user accounts and the Postgres database connection.

CI/CD Workflow (Jenkins + ArgoCD)

We don't do manual deployments. The entire lifecycle is automated via the Jenkinsfile in this root directory:

    Continuous Integration: Jenkins triggers a build on every push. It goes into each service folder, runs the unit tests (like test_das.py), and builds a new Docker image.

    Registry: Images are tagged with the build number and pushed to AWS ECR.

    The Handshake: Once the images are safe in ECR, Jenkins clones our ArgoCD/Manifest repo. It updates the image tags in the Helm values.yaml files and commits the change back to Git.

    GitOps Sync: ArgoCD detects the change in the manifest repo and automatically syncs the EKS cluster to match.

Local Development

To test a specific service locally, you can build it from the root using the specific path:
Bash

# Example: Building the Data API service
docker build -t cloudopshub-das ./data-api-service

Note on Networking: The UI is designed to look for backends at /api/<service-name>. This keeps our frontend code simple and avoids CORS headaches since Nginx handles the routing internally.
Security & Reliability

    Non-Root: Every Dockerfile is configured to run as an unprivileged user.

    Health Probes: We use /health and /ready endpoints across all services so Kubernetes can manage pod lifecycles effectively.

    Secrets: Never commit passwords or API keys here. Jenkins pulls credentials from the secure store during the build process.