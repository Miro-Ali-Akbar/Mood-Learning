
all: preprocess

data:
	mkdir data

preprocess: export.emoodsw data
	@echo "Uncompressing data"
	@cp export.emoodsw export.zip
	@unzip export.zip -d data/
	@rm export.zip

clear:
	@rm -v data/ -rf 
	@rm export.zip
