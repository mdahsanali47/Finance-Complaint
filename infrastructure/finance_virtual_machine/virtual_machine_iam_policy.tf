provider "google" {
  credentials = file("/home/ali47/Desktop/project_2/keys for ali47 IAMS/finance-complaint-376721-065b12acb2f9.json")
  project     = var.finance_project_name
  region      = "asia-south1"
  zone        = "asia-south1-c"
}

data "google_iam_policy" "admin" {
  binding {
    role = var.finance_iam_user_role
    members = [
      var.finance_iam_user_email,
    ]
  }
}

resource "google_compute_instance_iam_policy" "finance_compute_instance_iam_policy" {
  project       = google_compute_instance.finance_compute_instance.project
  zone          = google_compute_instance.finance_compute_instance.zone
  instance_name = google_compute_instance.finance_compute_instance.name
  policy_data   = data.google_iam_policy.admin.policy_data
}