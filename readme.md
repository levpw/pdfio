# Count Images and Tables in pdf files

## Dependencies
- tabula-py
- pymupdf

You can install the conda environment by
```
conda env create -f environment.yml
```

## How to run
```
python run.py
```
- Use `-p DIR_TO_WORK_FOLDER_AS_STR` to set the work folder, default is `./input/`.
- Use `-r IMAGE_RATIO_AS_FLOAT` to set the minimum acceptable ratio for the image size relative to the page size, default is `0.1`.
- Use `-o OUTPUT_FILEPATH` to set your output filepath, default is `./result.json`.
- Use `-v` to record detailed number of images and tables in each file, default is off.

## Result
A json file in the format `{"images": num_images, "tables": num_tables, "details": []}`.