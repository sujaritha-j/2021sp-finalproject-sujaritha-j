data:data/learn.parquet

data/learn.parquet:
	aws s3 cp s3://cscie29-data/14a291ef/pset_3/learn.parquet data/ --request-payer=requester
	aws s3 cp s3://cscie29-data/14a291ef/pset_3/vectors.npy.gz data/ --request-payer=requester
	aws s3 cp s3://cscie29-data/14a291ef/pset_3/words.txt data/ --request-payer=requester