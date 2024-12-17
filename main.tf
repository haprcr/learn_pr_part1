# Create a BigQuery View
resource "google_bigquery_table" "business_function_projects_view" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "business_function_project_mapping"

  view {
    query          = file("business_function_projects.sql")
    use_legacy_sql = false
  }
}