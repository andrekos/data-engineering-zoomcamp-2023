## Week 1 Homework

In this homework we'll prepare the environment by creating resources in GCP with Terraform. In your VM on GCP install Terraform. Copy the files from the course repo [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/week_1_basics_n_setup/1_terraform_gcp/terraform) to your VM. Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 1. Creating Resources 🏁

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form. For completeness, we post it here as well. 

The full output includes these lines, some of which refer to a specific project_id:
```
google_bigquery_dataset.dataset: Creating...
google_storage_bucket.data-lake-bucket: Creating...
google_storage_bucket.data-lake-bucket: Creation complete after 2s [id=dtc_data_lake_civil_civil-entry-376015]
google_bigquery_dataset.dataset: Creation complete after 2s [id=projects/civil-entry-376015/datasets/trips_data_all]
```

The final output in colour (green) is as follows and I guess submitting just this line may not suffice. 
```
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```


## Submitting the solutions

* Form for submitting: [form](https://forms.gle/S57Xs3HL9nB3YTzj9)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 30 January (Monday), 22:00 CET

