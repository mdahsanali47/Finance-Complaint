variable "artifact_repository_iam_role_binding" {
  default = "roles/artifactregistry.writer"
  type    = string
}

variable "artifact_repository_iam_members" {
  default = "user:mdahsanali47@gmail.com"
  type    = string
}

variable "project_name" {
  default = "finance-complaint-project"
  type    = string
}

variable "artifact_repository_location" {
  default = "asia-south1"
  type    = string
}

variable "artifact_repository_repository_id" {
  default = "finance-repository"
  type    = string
}

variable "artifact_repository_format" {
  default = "DOCKER"
  type    = string
}