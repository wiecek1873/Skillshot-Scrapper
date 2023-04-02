import csv
import os

def serialize_to_csv(file_name, job_offers):
    extension = ".csv"
    directory = "data/"

    header = [
        "Title",
        "Company",
        "Location",
        "Category",
        "Job_Type",
        "Seniority",
        "Salary_Min",
        "Salary_Max",
        "Date",
        "Views",
        "Url",
    ]

    if os.path.exists(directory) == False:
        os.mkdir(directory)

    with open(directory + file_name + extension, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for job_offer in job_offers:
            if job_offer != None:
                writer.writerow(job_offer.__dict__)
        f.close()
