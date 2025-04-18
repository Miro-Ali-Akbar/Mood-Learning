
all: preprocess

data:
	mkdir data

preprocess: export.emoodsw data
	@echo "Uncompressing data"
	@cp export.emoodsw export.zip
	@unzip export.zip -d data/
	@rm export.zip
	@python code/preprocess.py
	@mv data/data.csv .
	@rm data/*
	@mv data.csv data/

clean:
	@rm -v data/ -rf 
	@rm export.zip -rf
