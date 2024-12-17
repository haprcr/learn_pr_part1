import json
from google.cloud import bigquery


# Function to fetch the list of projects from BigQuery and update terraform.tfvars.json
def get_tables_of_business_function(
        bigquery_billing_project_id,
        bigquery_billing_dataset_id,
        bigquery_billing_view_id,
        tfvars_data
):

    # BigQuery query to retrieve data from the view
    query = f"""
                SELECT * 
                FROM `{bigquery_billing_project_id}.{bigquery_billing_dataset_id}.{bigquery_billing_view_id}`
        """

    # Initialize BigQuery client
    bq_client = bigquery.Client()

    # Execute the query
    query_job = bq_client.query(query)
    rows = query_job.result()

    # Process the query results
    for row in rows:
        try:
            # Update terraform.tfvars.json with project lists for each business function
            tfvars_data["budgets_config"][row["label_value"]
                                          ]["projects"] = row["p_list"]
        except KeyError as e:
            print("Missing Business Function configuration for ",
                  row["label_value"], " in terraform.tfvars.json file. Please add the configuration in terraform.tfvars.json file.")
        except Exception as e:
            print("An error occurred:", str(e))

    # Write updated data back to terraform.tfvars.json
    with open("terraform.tfvars.json", "w") as tfvars:
        tfvars = json.dump(tfvars_data, tfvars, indent=4)


if __name__ == "__main__":
    # Load configuration files
    with open("config.json") as config_data:
        config_data = json.load(config_data)

    with open("terraform.tfvars.json") as tfvars_data:
        tfvars_data = json.load(tfvars_data)

    # Extract BigQuery parameters from the config file
    bq_billing_project_id = config_data["bigquery_billing_project_id"]
    bq_billing_dataset_id = config_data["bigquery_billing_dataset_id"]
    bq_billing_view_id = config_data["bigquery_billing_view_id"]

    # Execute the main function
    get_tables_of_business_function(
        bq_billing_project_id, 
        bq_billing_dataset_id, 
        bq_billing_view_id, 
        tfvars_data
    )