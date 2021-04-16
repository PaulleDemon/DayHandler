from datetime import datetime


def convertDateToName(date, input_format="%Y-%m-%d", output_format="%A, %b, %Y"):
    return datetime.strptime(date, input_format).strftime(output_format)


def convertDayNameToDate(date, input_format="%A, %b, %Y", output_format="%Y/%m/%d"):
    print("DAY NAE", datetime.strptime(date, input_format).strftime(output_format))
    return datetime.strptime(date, input_format).strftime(output_format)


def convert12hrsTo24hrs(time):
    print("TIME: ", repr(time))
    # print("DAY TIME", datetime.strptime(time, "%I:%M %p"))
    return datetime.strptime(time.strip(), "%I:%M %p").strftime("%H:%M:%S")


def convert24hrsTo12hrs(time):

    return datetime.strptime(time, "%H:%M:%S").strftime("%I:%M %p")