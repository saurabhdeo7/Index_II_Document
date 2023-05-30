import csv
import io
import os


def text_files_to_csv(files):
    """Files must be sorted lexicographically
    Filenames must be <row>-<colum>.txt.
    000-000.txt
    000-001.txt
    001-000.txt
    etc...
    """
    print("files"+str(files))
    rows = []
    for f in files:
        directory, filename = os.path.split(f)
        print("dir:"+directory+" , file: "+filename+" ")
        with open(f,encoding="utf-8") as of:
            txt = of.read().strip()
            print("txt"+txt)
        of.close()
        row, column = map(int, filename.split(".")[0].split("-"))
        print("row : " +str(row)+" col :"+str(column))

        if row == len(rows):
            rows.append([])
        rows[row].append(txt)

    csv_file = io.StringIO()
    writer = csv.writer(csv_file)
    writer.writerow("kv")
    writer.writerows(rows)
    return csv_file.getvalue()

# def text_files_to_csv(files):
#     rows=[]
#     for f in files:


def main(files):
    return text_files_to_csv(files)
