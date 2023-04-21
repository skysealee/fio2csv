from csv import DictWriter
from sys import argv
from os import getcwd, listdir
from os.path import exists
from time import strftime,strptime
# Talk is expensive, Give you my code
def newDict():
    return {'File Name': "",
            'Task Name': "",
            'Test Item': "",
            'Read Block Size': "",
            'Write Block Size': "",
            "Trim Block Size": "",
            'IO Engine': "",
            'IO Depth': "",
            "Number of Jobs": "",
            "Time of Reading": "",
            "Volume of Reading": "",
            "Time of Writing": "",
            "Volume of Writing": "",
            "Completed At": "",
            "FIO Version": "",
            "Minimal Read Bandwidth": "",
            "Maximum Read Bandwidth": "",
            "Average Read Bandwidth": "",
            "Read Bandwidth Standard Deviation": "",
            "Minimal Read IOPS": "",
            "Maximum Read IOPS": "",
            "Average Read IOPS": "",
            "Read IOPS Standard Deviation": "",
            "Minimal Read Latency": "",
            "Maximum Read Latency": "",
            "Average Read Latency": "",
            "Read Latency Standard Deviation": "",
            "Minimal Write Bandwidth": "",
            "Maximum Write Bandwidth": "",
            "Average Write Bandwidth": "",
            "Write Bandwidth Standard Deviation": "",
            "Minimal Write IOPS": "",
            "Maximum Write IOPS": "",
            "Average Write IOPS": "",
            "Write IOPS Standard Deviation": "",
            "Minimal Write Latency": "",
            "Maximum Write Latency": "",
            "Average Write Latency": "",
            "Write Latency Standard Deviation": "",
            "Latency Percentage of 50usec": "",
            "Latency Percentage of 100usec": "",
            "Latency Percentage of 250usec": "",
            "Latency Percentage of 500usec": "",
            "Latency Percentage of 750usec": "",
            "Latency Percentage of 1000usec": "",
            "Latency Percentage of 2msec": "",
            "Latency Percentage of 4msec": "",
            "Latency Percentage of 10msec": "",
            "Latency Percentage of 20msec": "",
            "Latency Percentage of 50msec": "",
            "Latency Percentage of 100msec": "",
            "Latency Percentage of 250msec": "",
            "Latency Percentage of 500msec": "",
            "Latency Percentage of 750msec": "",
            "Latency Percentage of 1000msec": "",
            "Latency Percentage of 2000msec": "",
            "Latency Percentage of over 2000msec": "",
            }


CWD = "" # Current Working Directory
isWrite = False  # IOPS, BW and Lat (Read or Write)
FIOResultList = [] # Final Result List
if len(argv) > 1 and exists(argv[1]):
    # If get path and this path existed, take this path as CWD
    CWD = argv[1]
else:
    # If no arg when running, take path of this py file as CWD
    CWD = getcwd()

for fio_result_txt in listdir(CWD):
    if fio_result_txt.endswith("txt"):
        # List dir and read txt
        with open(CWD+"\\"+fio_result_txt, "r") as fp_result:
            csv_fields = newDict()
            # See above
            result_lines = fp_result.readlines()
            for i in range(0, len(result_lines)):
                if i == 0:
                    # First Line to read
                    line1 = result_lines[i].strip().split(",")
                    csv_fields["Task Name"] = line1[0].split(":")[0].strip()
                    csv_fields["Test Item"] = line1[0].split(":")[
                        2].split("=")[1].strip()
                    csv_fields["Read Block Size"] = line1[1].split(" ")[
                        2].strip()
                    csv_fields["Write Block Size"] = line1[2].split(" ")[
                        2].strip()
                    csv_fields["Trim Block Size"] = line1[3].split(" ")[
                        2].strip()
                    csv_fields["IO Engine"] = line1[4].split("=")[1].strip()
                    csv_fields["IO Depth"] = line1[5].split("=")[1].strip()
                elif i == 1:
                    # Second Line to read FIO version
                    csv_fields["FIO Version"] = result_lines[i].strip().split(
                        "-")[1].strip()
                else:
                    # Other Lines
                    line = result_lines[i].strip()
                    if line.startswith(csv_fields["Task Name"]):
                        # If Line start with task name readed in Line one, it's a correct line to read
                        csv_fields["Number of Jobs"] = line.split(
                            ":")[1].split(",")[1].split("=")[1][:-1].strip()
                        csv_fields["Completed At"] = strftime("%Y/%m/%d %H:%M:%S",strptime(":".join(
                            line.split(":")[4:]).strip()[4:],"%b %d %H:%M:%S %Y"))
                    if line.startswith("read"):
                        # If Line start with "read", current and following line are about read lat/iops/bw
                        isWrite = False
                        csv_fields["Time of Reading"] = str(int(int(line.split(
                            ",")[1].split("/")[-1][:-5].strip())/1000))
                        csv_fields["Volume of Reading"] = line.split(
                            "/")[2].split("(")[1].strip()
                    if line.startswith("write"):
                        # If Line start with "write", current and following line are about write lat/iops/bw
                        isWrite = True
                        csv_fields["Time of Writing"] = str(int(int(line.split(
                            ",")[1].split("/")[-1][:-5].strip())/1000))
                        csv_fields["Volume of Writing"] = line.split(
                            "/")[2].split("(")[1].strip()
                    if line.startswith("lat"):
                        if line.find("%") == -1:
                            # If line start with lat and do not contain "%", it's about lat summary
                            unit_str=line.split(
                                ":")[0].strip().split("(")[1][:-1].strip()
                            min_lat=line.split(
                                ",")[0].split(":")[1].split("=")[1].strip() 
                            max_lat=line.split(",")[1].split("=")[1].strip()
                            avg_lat=line.split(",")[2].split("=")[1].strip()
                            stdev_lat=line.split(",")[3].split("=")[1].strip()
                            if unit_str=="usec":
                                # if Unit is USEC not easy to read, translate to MSEC
                                min_lat = min_lat[:-1] if min_lat.endswith("k") else str(float(min_lat)/1000)
                                max_lat = max_lat[:-1] if max_lat.endswith("k") else str(float(max_lat)/1000)
                                avg_lat = avg_lat[:-1] if avg_lat.endswith("k") else str(float(avg_lat)/1000)
                                stdev_lat = stdev_lat[:-1] if stdev_lat.endswith("k") else str(float(stdev_lat)/1000)
                            # Judge read or write and give value to Read/Write Latency result
                            csv_fields["Minimal " + ("Write" if isWrite else "Read") + " Latency"] = min_lat
                            csv_fields["Maximum " + ("Write" if isWrite else "Read") +
                                       " Latency"] = max_lat
                            csv_fields["Average " + ("Write" if isWrite else "Read") +
                                       " Latency"] = avg_lat
                            csv_fields[("Write" if isWrite else "Read") +
                                       " Latency Standard Deviation"] = stdev_lat
                        elif line.find("percentile") == -1:
                            # If line start with "percentile", it's about Latency detail result
                            unit_str = line.split(
                                ":")[0].strip().split("(")[1][:-1].strip()
                            # Get unit type USEC or MSEC 
                            for splited_value in line.split(","):
                                if splited_value.find(unit_str) != -1:
                                    # First value to splited as XX=YY
                                    splited_value = splited_value.split(":")[
                                        1].strip()
                                else:
                                    splited_value = splited_value.strip()
                                    # Second and following value splited as XX=YY
                                splited_value = splited_value.replace(
                                    ">=2000", "over 2000")
                                # replace latency ">=2000" as "over 2000" for easy reading
                                size_str, percentage = splited_value.split("=")
                                # Split XX=YY to size & percentage
                                csv_fields["Latency Percentage of " +
                                           size_str+unit_str] = percentage.strip()
                                # Add to dict
                    if line.startswith("bw"):
                        # Bandwidth result, splitted method like before
                        csv_fields["Minimal " + ("Write" if isWrite else "Read") + " Bandwidth"] = line.split(
                            ",")[0].split(":")[1].split("=")[1].strip()
                        csv_fields["Maximum " + ("Write" if isWrite else "Read") +
                                   " Bandwidth"] = line.split(",")[1].split("=")[1].strip()
                        csv_fields["Average " + ("Write" if isWrite else "Read") +
                                   " Bandwidth"] = line.split(",")[3].split("=")[1].strip()
                        csv_fields[("Write" if isWrite else "Read") +
                                   " Bandwidth Standard Deviation"] = line.split(",")[4].split("=")[1].strip()
                    if line.startswith("iops"):
                        # IOPS result, splitted method like before
                        csv_fields["Minimal " + ("Write" if isWrite else "Read") + " IOPS"] = line.split(
                            ",")[0].split(":")[1].split("=")[1].strip()
                        csv_fields["Maximum " + ("Write" if isWrite else "Read") +
                                   " IOPS"] = line.split(",")[1].split("=")[1].strip()
                        csv_fields["Average " + ("Write" if isWrite else "Read") +
                                   " IOPS"] = line.split(",")[2].split("=")[1].strip()
                        csv_fields[("Write" if isWrite else "Read") +
                                   " IOPS Standard Deviation"] = line.split(",")[3].split("=")[1].strip()
            csv_fields["File Name"] = fio_result_txt
            FIOResultList.append(csv_fields)
            # Add to Result List
        with open(CWD+"\\"+"fio_results.csv", "w", newline="") as fp_csv:
            fieldnames = newDict().keys()
            # Generate CSV table title
            writer = DictWriter(fp_csv, fieldnames=fieldnames)
            # Generate CSV Writer
            writer.writeheader()
            # Write CSV table title
            writer.writerows(FIOResultList)
            # Write Result to be a row