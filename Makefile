data:data/word.vectors

data/word.vectors:
	aws s3 cp s3://cscie29-data/14a291ef/pset_3/vectors.npy.gz data/ --request-payer=requester
	aws s3 cp s3://cscie29-data/14a291ef/pset_3/words.txt data/ --request-payer=requester