
all: preprocess

folders:
	mkdir data
	mkdir finished

preprocess: export.emoodsw folders
	@echo "Uncompressing data"
	@cp export.emoodsw export.zip
	@unzip export.zip -d data/
	@rm export.zip
	@echo "Cleaning columns"
	@python code/preprocess.py
	@mv data/data.csv .
	@rm data/*
	@mv data.csv data/

correlation_matrix: preprocess folders
	@echo "Running correlation matrix calculation"
	@python code/correlation_matrix.py

clean:
	@echo "Cleaning"
	@rm -v data/ -rf 
	@rm -v finished/ -rf
	@rm export.zip -rf
