# air_quality_prediction


//openaq data 
aws s3 cp \
--no-sign-request \
--recursive \
s3://openaq-data-archive/records/csv.gz/locationid=2178/year=2020/ \
data