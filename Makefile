build:
	rm -r ./lib && pip install -t lib -r requirements.txt

deploy:
	 gcloud app deploy