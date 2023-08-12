import argparse
import json
import time
import fitz
import tqdm

from main import find_files, count_tables_in_pdf, count_images_in_pdf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', default='./input/')
    parser.add_argument('--ratio', '-r', type=float, default=0.1)
    parser.add_argument('--out', '-o', default='./result.json')
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    args = parser.parse_args()

    pdf_files = find_files(args.path, file_extensions=[".pdf"])
    assert len(pdf_files) > 0, "No pdf files found in the path you provided!"

    out = {"num_images": 0, "num_tables": 0, "details": []}

    start_time = time.time()

    for pdf_file in tqdm.tqdm(pdf_files):
        n_tables = count_tables_in_pdf(pdf_file)
        n_images = count_images_in_pdf(pdf_file, thres=args.ratio)
        out["num_tables"] += n_tables
        out["num_images"] += n_images
        if args.verbose:
            out["details"].append((pdf_file, n_images, n_tables))
            
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    with open(args.out, "w") as outfile:
        json.dump(out, outfile)
