import os
import pickle
import pprint
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import csv


def csv_write(filename, mylist, mode="w", directory="./"):
    with open(os.path.join(directory, filename), mode, newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(mylist)


def csv_reader(filename, directory="./"):
    with open(os.path.join(directory, filename), newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        mylist = []
        for row in reader:
            mylist.append(row[0].split(","))
        return mylist
