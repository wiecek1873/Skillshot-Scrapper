from typing import final
import requests
from bs4 import BeautifulSoup
from skillshot_parser import ParserGPT
from skillshot_parser import Parser
from job_offer import JobOffer
from serializer import serialize_to_csv
import random
import time


def get_soup(url):
    response = requests.get(url)

    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        pass


def get_job_offer(url):
    soup = get_soup(url)
    if soup != None:
        parser = ParserGPT(soup)

        if parser.is_valid():
            return JobOffer(
                parser.get_title(),
                parser.get_company(),
                parser.get_location(),
                parser.get_category(),
                parser.get_job_type(),
                parser.get_seniority(),
                parser.get_salary_min(),
                parser.get_salary_max(),
                parser.get_date(),
                parser.get_views(),
                url,
            )
        else:
            return None
    else:
        return None


base_url = "https://www.skillshot.pl/jobs/"


# print(get_job_offer(base_url + "31000").__dict__)

while True:
    from_string = input("Please enter starting offer index: ")
    if from_string.isdigit():
        break
    else:
        print("Invalid input. Please enter a positive number.")

while True:
    count_string = input("Please enter count: ")
    if count_string.isdigit():
        break
    else:
        print("Invalid input. Please enter a positive number.")

while True:
    data_batch_max_size_string = input("Please enter data batch size: ")
    if count_string.isdigit():
        break
    else:
        print("Invalid input. Please enter a positive number.")

index_start = int(from_string)
index_count = int(count_string)
data_batch_max_size = int(data_batch_max_size_string)
data_batch_size = 0
batch_index = 0

offers = []
csv_files = []

try:
    for index in range(index_start, index_start + index_count):
        time.sleep(random.randint(2,5))

        url = base_url + str(index)
        print(f"Parsing offer with url {url}")

        jobOffer = get_job_offer(url)

        if jobOffer != None:
            offers.append(get_job_offer(url))

            data_batch_size += 1

            if data_batch_size > data_batch_max_size - 1:
                print(f"Saving batch {batch_index} with {data_batch_size} rows...")
                file_name = "job_offers" + "_" + str(batch_index)
                serialize_to_csv(file_name, offers)
                csv_files.append(file_name)
                batch_index += 1
                offers.clear()
                data_batch_size = 0
finally:
    print("Saving...")
    file_name = "job_offers" + "_" + str(batch_index)
    serialize_to_csv(file_name, offers)
    csv_files.append(file_name)

    #import pandas as pd
    #dfs = []

    #for csv_file in csv_files:
    #    df = pd.read_csv(csv_file)
    #    dfs.append(df)
    #    concatenated_df = pd.concat(dfs, ignore_index=True)
    #    concatenated_df.to_csv('concatenated_file.csv', index=False)

