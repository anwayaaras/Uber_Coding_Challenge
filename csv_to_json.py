#!/usr/bin/python

import sys, getopt
import csv
import json

#Get Command Line Arguments
def main(argv):
    input_file = ''
    output_file = ''
    format = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'csv_json.py -i <path to inputfile> -o <path to outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'csv_json.py -i <path to inputfile> -o <path to outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    read_csv(input_file, output_file)

#Read CSV File
def read_csv(file, json_file):
    f = open(json_file, "w")
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            current_row = {}
            for i in range(len(title)):
                if title[i] != "Latitude" and title[i] != "Longitude":
                    current_row[title[i]] = row[title[i]]
            # Only including rows with a valid Latitude and Longitude
            if row["Longitude"] != "" and row["Latitude"] != "":
                current_row["loc"] = {
                    "type": "Point",
                    "coordinates" : [ float(row["Longitude"]), float(row["Latitude"]) ]
                    }

                json.dump(current_row, f)
                f.write("\n")

if __name__ == "__main__":
   main(sys.argv[1:])

