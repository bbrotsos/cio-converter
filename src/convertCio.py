'''
This script converts between csv and json.

Convert csv to json:
python3 convertCio.py cio-example.csv output.json

Convert json to csv:
python3 convertCio.py cio-example.json output.csv

'''

import sys
import json
import csv
import jsonschema

from jsonschema import validate

class ConvertCioData:
    
    DATA_DIRECTORY = ""
    SCHEMA_DIRECTORY = "schema/"
    
    cioFieldNames = ["bureauCode", "positionTitleDescription", "employmentTypeCode", "employmentTypeOther", "appointmentTypeCode", "otherResponsibilities", "evaluationRatingOfficialTitle", "evaluationReviewingOfficialTitle", "keyBureauIndicator"]
    contactPointFieldNames = ["fn", "hasEmail"]
    
    def __init__(self, cioJsonFileName, cioCsvFileName, cioOutputFileName):
        self._cioJsonFileName = cioJsonFileName
        self._cioCsvFileName = cioCsvFileName
        self._outputFileName = cioOutputFileName
        self._csv = []
        self._json = {}
        
    def _validateJson(self, cioJson):
        with open(self.SCHEMA_DIRECTORY + "cio_list.json") as data_file:
            cioJsonSchema = json.load(data_file)
            try:
                #TODO: lazy validation
                validate(cioJson, cioJsonSchema)
            except jsonschema.ValidationError as e:
                print (e.message)
        
    def convertToCioJson(self):
        '''
        converts csv to json
        '''
        with open(self.DATA_DIRECTORY + self._cioCsvFileName) as csvfile:
            cio_reader = csv.DictReader(csvfile)
            cio_list = []
            for row in cio_reader:
                cio = {}
                for cioField in self.cioFieldNames:
                
                    if cioField in row:
                        #TODO: Optimize booleans from csv?
                        if (cioField == "keyBureauIndicator"):
                            if (row[cioField] == "true"):
                                cio[cioField] = True
                            else:
                                cio[cioField] = False
                        else:
                            cio[cioField] = row[cioField]
                
                contactPoint = {}
                for contactPointField in self.contactPointFieldNames:
                    contactPoint[contactPointField] = row[contactPointField]
                cio["contactPoint"] = contactPoint
                cio_list.append(cio)
                
        self._json["cio"] = cio_list
        self.createJsonFile()
                
    def createJsonFile(self):
        with open(self.DATA_DIRECTORY + self._outputFileName, "w") as cioJson:
            self._validateJson(self._json)
            json.dump(self._json, cioJson, indent=4, sort_keys=True)
            print ("Successfully created json:" + self._outputFileName + " from csv file:" + self._cioCsvFileName)

        
    def convertToCioCsv(self):
        with open(self.DATA_DIRECTORY + self._cioJsonFileName) as data_file:
            data = json.load(data_file)
            self._validateJson(data)

        for cio_list in data["cio"]:
            self.__createCsvRow(cio_list)
        
        self.createCsvFile()
    
    def __createCsvRow(self, cio):        
        cioRow = dict()
        for cioField in self.cioFieldNames:
            if cioField in cio:
            	cioRow[cioField] = cio[cioField]
            else:
                cioRow[cioField] = ""
        
        for contactField in self.contactPointFieldNames:
            if contactField in cio["contactPoint"]:
                cioRow[contactField] = cio["contactPoint"][contactField]
            else:
                cioRow[contactField] = ""
        
        self._csv.append(cioRow)
        
    def createCsvFile(self):
        cio_keys = self._csv[0].keys()
        with open(self.DATA_DIRECTORY + self._outputFileName, 'wt') as csvfile:
            cio_writer = csv.DictWriter(csvfile, cio_keys)
            cio_writer.writeheader()
            cio_writer.writerows(self._csv)
            print ("Successfully created csv:" + self._outputFileName + " from json file:" + self._cioJsonFileName)
                     
def main():
    
    try:
    	convertFileName = sys.argv[1]
    	outputFileName = sys.argv[2]
    except:
        print("The first arg is input file name and second arg is output file name.")
        sys.exit(2)
    
    if convertFileName.endswith(".json"):
        convert = ConvertCioData(sys.argv[1], "", outputFileName)
        convert.convertToCioCsv()
    elif convertFileName.endswith(".csv"):
        convert = ConvertCioData("", sys.argv[1], outputFileName)
        convert.convertToCioJson()
    else:
        print ("Please use a json or csv file extension for first argument")
    
if __name__ == "__main__":
    main()    