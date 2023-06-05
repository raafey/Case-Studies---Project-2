import csv


def save_dat_as_csv(csv_file_path, dat_file_path):
    file_content = [i.strip().split() for i in open(dat_file_path, encoding="utf-8").readlines()]

    with open(csv_file_path, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(file_content)