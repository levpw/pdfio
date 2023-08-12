import os
import re
import tabula
import fitz
import pathlib

def find_files(work_directory="./", file_keywords=None, file_extensions=None, method="any"):
    """
    default work directory is current folder
    we can specify the work directory
    use file extension to specify the file type to find
    alternatively set file_extension to None to find any type of file
    """
    file_list = []
    if file_keywords is not None:
        if file_extensions is not None:
            file_list = [str(file) for file in pathlib.Path(os.path.normpath(work_directory)).rglob('*') if ((file.suffix.lower() in file_extensions) and (not file.name.startswith('~$')) and is_target_file(str(file), file_keywords, method=method))]
        else:
            file_list = [str(file) for file in pathlib.Path(os.path.normpath(work_directory)).rglob('*') if ((file.is_file() and not file.name.startswith('~$')) and (is_target_file(str(file), file_keywords, method=method)))]
    else:
        if file_extensions is not None:
            file_list = [str(file) for file in pathlib.Path(os.path.normpath(work_directory)).rglob('*') if ((file.suffix.lower() in file_extensions) and (not file.name.startswith('~$')))]
        else:
            file_list = [str(file) for file in pathlib.Path(os.path.normpath(work_directory)).rglob('*') if ((file.is_file()) and not (file.name.startswith('~$')))]
    return file_list

def is_target_file(filename, keywords, method="single"):
    """
    Check if the input filename contains the keyword
    Support three methods:
        single (default)
        any
        all
    """
    if method == "single":
        assert isinstance(keywords, str), f"To use this method {method}, you must provide a single keyword."
        return re.search(f"\\b{keywords}\\b", filename, re.IGNORECASE) is not None
    elif method == "any":
        # The \\b in the pattern is a word boundary, so it requires the keyword to appear as a whole word.
        assert isinstance(keywords, list), f"To use this method {method}, you must provide a list of keywords."
        filename = filename.replace("_"," ")
        for keyword in keywords:
            if re.search(f"\\b{re.escape(keyword)}\\b", filename, re.IGNORECASE) is not None:
                return True
        return False
    elif method == "all":
        assert isinstance(keywords, list), f"To use this method {method}, you must provide a list of keywords."
        # The \\b in the pattern is a word boundary, so it requires the keyword to appear as a whole word.
        filename = filename.replace("_"," ")
        for keyword in keywords:
            if re.search(f"\\b{re.escape(keyword)}\\b", filename, re.IGNORECASE) is None:
                return False
        return True
    else:
        raise NotImplementedError(f"The method {method} is undefined!")
    
def count_tables_in_pdf(pdf_file_path: str):
    tables = tabula.read_pdf(pdf_file_path, pages="all")
    tp = 0
    for table in tables:
        if not table.isna().all().all():
            tp += 1
            # print(table)
    return tp

def count_images_in_pdf(pdf_file_path: str, thres: float):
    assert (thres >= 0 and thres <= 1), "The ratio you provided is not in [0,1]!"
    pdf_file = fitz.open(pdf_file_path)
    images_count = 0
    for page_num in range(len(pdf_file)):
        page_content = pdf_file[page_num]
        _, _, pw, ph, = page_content.rect
        min_image_size = thres*pw*ph
        for _, _, w, h, *_ in page_content.get_images():
            if w*h >= min_image_size:
                images_count += 1
    return images_count
