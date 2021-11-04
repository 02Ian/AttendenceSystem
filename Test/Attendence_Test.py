import datetime
from csv import writer

def markAttendance(strName):
    # Import writer class from csv module
    # List
    datetimeEntryValue =  datetime.datetime.now()
    convertedFormat = datetimeEntryValue.strftime("%b-%d-%Y %H:%M:%S")
    strNameCsvData = strName.split("@")
    locationCsvData = strNameCsvData[1].split(".")

    List = [strNameCsvData[0], locationCsvData[0], convertedFormat, datetimeEntryValue.strftime("%A")]

    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open("/Attendence.csv", 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()

strName = "Mohit_Athani@Pune.jpg"
markAttendance(strName)
