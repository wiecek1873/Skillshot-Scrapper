import csv

def serialize(file_name, job_offers):
    header = [
        "Title",
        "Company",
        "Location",
        "Remote",
        "Category",
        "Job_Type",
        "Seniority",
        "Salary",
        "Date",
        "Views",
        "Url"
    ]

    with open(file_name, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for job_offer in job_offers:
            if(job_offer != None):
                writer.writerow(job_offer.__dict__)
        f.close()
