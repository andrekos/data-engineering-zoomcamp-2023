## Week 3 Homework
<b><u>Important Note:</b></u> <p>You can load the data however you would like, but keep the files in .GZ Format. 
If you are using orchestration such as Airflow or Prefect do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>
<u>NOTE:</u> You can use the CSV option for the GZ files when creating an External Table</br>

<b>SETUP:</b></br>
Create an external table using the fhv 2019 data. </br>
Create a table in BQ using the fhv 2019 data (do not partition or cluster this table). </br>
Data can be found here: https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/fhv </p>

create an external table 
```sql
CREATE OR REPLACE EXTERNAL TABLE `civil-entry-376015.homework3.fhv_tripdata_external`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_civil_civil-entry-376015/fhv/fhv_tripdata_2019-*.csv.gz']
);
```

```sql
CREATE OR REPLACE TABLE `civil-entry-376015.homework3.fhv_tripdata_not_partitioned`

AS SELECT * FROM `civil-entry-376015.homework3.fhv_tripdata_fhv_tripdata_external`;
```


## Question 1: What is the count for fhv vehicle records for year 2019? 🏁

- 43,244,696

```sql
SELECT count(*) FROM `civil-entry-376015.homework3.fhv_tripdata_not_partitioned`;
```

## Question 2:  Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table? 🏁

- 0 MB for the External Table and 317.94MB for the BQ Table 

```sql
SELECT count(DISTINCT(affiliated_base_number)) FROM `civil-entry-376015.homework3.fhv_tripdata_external`
```

```sql
SELECT count(DISTINCT(affiliated_base_number)) FROM `civil-entry-376015.homework3.fhv_tripdata_not_partitioned`
```


## Question 3: How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset? 🏁

- 717,748

```sql
SELECT count(*) FROM `civil-entry-376015.homework3.fhv_tripdata_external`
WHERE DOlocationID is null AND PUlocationID is null
```


## Question 4: What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number? 🏁

- Partition by pickup_datetime Cluster on affiliated_base_number


## Question 5: Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive). Use the BQ table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? Choose the answer which most closely matches. 🏁

- 647.87 MB for non-partitioned table and 23.06 MB for the partitioned table

```sql
CREATE OR REPLACE TABLE `civil-entry-376015.homework3.fhv_tripdata_partitioned` 
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS (
  SELECT * FROM civil-entry-376015.homework3.fhv_tripdata_not_partitioned
)
```

```sql
SELECT DISTINCT(affiliated_base_number) FROM civil-entry-376015.homework3.fhv_tripdata_not_partitioned
WHERE pickup_datetime BETWEEN TIMESTAMP("2019-03-01") AND TIMESTAMP("2019-03-31");
```

```sql
SELECT DISTINCT(affiliated_base_number) FROM civil-entry-376015.homework3.fhv_tripdata_partitioned WHERE pickup_datetime BETWEEN TIMESTAMP("2019-03-01") AND TIMESTAMP("2019-03-31");
```

## Question 6:  Where is the data stored in the External Table you created? 🏁

- GCP Bucket

## Question 7: It is the best practice in Big Query to always cluster your data. 🏁

- False


## (Not required) Question 8:
A better format to store these files may be parquet. Create a data pipeline to download the gzip files and convert them into parquet. Upload the files to your GCP Bucket and create an External and BQ Table.  Note: Column types for all files used in an External Table must have the same datatype. While an External Table may be created and shown in the side panel in Big Query, this will need to be validated by running a count query on the External Table to check if any errors occur. 
 
## Submitting the solutions

* Form for submitting: https://forms.gle/rLdvQW2igsAT73HTA
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 13 February (Monday), 22:00 CET


## Solution

We will publish the solution here
