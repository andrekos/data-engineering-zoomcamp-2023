# Week 1 Homework

In this homework we'll prepare the environment  and practice with Docker and SQL


## Question 1. Knowing docker tags 🏁

Run the command to get information on Docker `docker --help`. Now run the command to get help on the "docker build" command. Which tag has the following text? - *Write the image ID to the file* 

- `--iidfile string`

```docker
> docker --help build
```


```
Usage:  docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile

Options:
      --add-host list           Add a custom host-to-IP mapping (host:ip)
      --build-arg list          Set build-time variables
      --cache-from strings      Images to consider as cache sources
      --disable-content-trust   Skip image verification (default true)
  -f, --file string             Name of the Dockerfile (Default is
                                'PATH/Dockerfile')
      --iidfile string          Write the image ID to the file
```

## Question 2. Understanding docker first run 🏁

Run docker with the python:3.9 image in an interactive mode and the entry point of bash. Now check the python modules that are installed ( use pip list).  How many python packages/modules are installed?

- 3

First, run this line in cmd to get a shell prompt 
```
docker run -it --rm --entrypoint /bin/bash python:3.9
```

then  type ``pip list` at the shell prompt to list the globally installed packages
```bash
root@4e4e38f47005:/# pip list
Package    Version
---------- -------
pip        22.3.1
setuptools 58.1.0
wheel      0.38.4
root@4e4e38f47005:/#
```


# Prepare Postgres

Run Postgres and load data as shown in the videos. We'll use the green taxi trips from January 2019: `wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz`

You will also need the dataset with zones: `wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv` Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

## Question 3. Count records 🏁

How many taxi trips were totally made on January 15? Tip: started and finished on 2019-01-15. 

- 20530

```sql
select count(*) from green_taxi_trips where date(lpep_pickup_datetime) = '2019-01-15' and  date(lpep_dropoff_datetime) = '2019-01-15'
```

```
+-------+
| count |
|-------|
| 20530 |
+-------+
SELECT 1
Time: 0.080s
```


## Question 4. Largest trip for each day 🏁

Which was the day with the largest trip distance. Use the pick up time for your calculations.

- 2019-01-15

```sql
SELECT max(trip_distance) as max_distance, date(lpep_pickup_datetime) as date FROM green_taxi_trips GROUP BY date order by max_distance desc limit 4
```

```
+--------------+------------+
| max_distance | date       |
|--------------+------------|
| 117.99       | 2019-01-15 |
| 80.96        | 2019-01-18 |
| 64.27        | 2019-01-28 |
| 64.2         | 2019-01-10 |
+--------------+------------+
SELECT 4
Time: 0.186s
```


## Question 5. The number of passengers 🏁

In 2019-01-01 how many trips had 2 and 3 passengers?
 
 - 2: 1282 ; 3: 254

```sql
SELECT passenger_count, COUNT(1) as count, date(lpep_pickup_datetime) as date FROM green_taxi_trips WHERE date(lpep_pickup_datetime)='2019-01-01' and (passenger_count = 2 or passenger_count=3) GROUP BY date, passenger_count
```

```
+-----------------+-------+------------+
| passenger_count | count | date       |
|-----------------+-------+------------|
| 2               | 1282  | 2019-01-01 |
| 3               | 254   | 2019-01-01 |
+-----------------+-------+------------+
SELECT 2
Time: 0.075s
```

## Question 6. Largest tip 🏁

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

- Long Island City/Queens Plaza

```sql
SELECT puz."Zone" as "pickup_location", doz."Zone" as "dropoff_location", max(tip_amount) as max_tip_amount FROM green_taxi_trips t JOIN taxi_lookup_zones puz on t."PULocationID" = puz."LocationID" JOIN taxi_lookup_zones doz on t."DOLocationID" = doz."LocationID" where puz."Zone" = 'Astoria' group by 1, 2 order by max_tip_amount desc limit 3
```

```
+-----------------+-------------------------------+----------------+
| pickup_location | dropoff_location              | max_tip_amount |
|-----------------+-------------------------------+----------------|
| Astoria         | Long Island City/Queens Plaza | 88.0           |
| Astoria         | Central Park                  | 30.0           |
| Astoria         | Jamaica                       | 25.0           |
+-----------------+-------------------------------+----------------+
SELECT 3
Time: 0.092s
```

## Submitting the solutions

* Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 30 January (Monday), 22:00 CET


## Solution

The course instructor solutions are published at TBC
