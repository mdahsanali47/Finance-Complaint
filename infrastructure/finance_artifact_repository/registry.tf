provider "google" {
  credentials = file("/home/ali47/Desktop/project_2/keys for ali47 IAMS/finance-complaint-376721-065b12acb2f9.json")
  project     = var.project_name
  region      = "asia-south1"
  zone        = "asia-south1-c"
}

resource "google_artifact_registry_repository" "finance_repo" {
  location      = var.artifact_repository_location
  repository_id = var.artifact_repository_repository_id
  format        = var.artifact_repository_format
}