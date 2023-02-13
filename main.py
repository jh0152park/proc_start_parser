import os
import csv
import xlsxwriter

log_file = ""
for file in os.listdir(os.getcwd()):
    if file.endswith("eventlogcat.txt"):
        log_file = file

if not log_file:
    print(f"could not found Fulltime_eventlocat.txt file.")
    print("please try again with eventlog file.")
    exit(0)


event_sequence = []
proc_start_info = {}
proc_start_times = []
proc_start_reasons = []

reasons = []
processes = []

with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
    for log in f.readlines():
        if "am_proc_start" in log[:-1]:
            time = log[:-1].split()[1]
            process = log[:-1].split(",")[3]
            reason = log[:-1].split(",")[4]
            reasons.append(reason)

            proc_start_times.append(time)
            proc_start_reasons.append(reason)
            if process not in proc_start_info.keys():
                proc_start_info[process] = {
                    "times": [],
                    "reasons": [],
                    "occurred": 0
                }

            processes.append(process)
            proc_start_info[process]["occurred"] += 1
            proc_start_info[process]["times"].append(time)
            proc_start_info[process]["reasons"].append(reason)

            event_sequence.append({
                "event": "start",
                "time": time,
                "process": process
            })

        if "am_app_transition" in log[:-1]:
            time = log[:-1].split()[1]
            process = log[:-1].split(",")[0].split("[")[-1]
            processes.append(process)
            event_sequence.append({
                "event": "launch",
                "time": time,
                "process": process
            })

# compute how many events occurred ever each process
processes = list(set(processes))
times = [event["time"] for event in event_sequence]
events = [event["event"] for event in event_sequence]

workbook = xlsxwriter.Workbook("proc_start.xlsx")
sheet = workbook.add_worksheet("proc_start")

sheet.write_column("A3", processes)
sheet.write_row("B1", times)
sheet.write_row("B2", events)

for idx, sequence in enumerate(event_sequence):
    event = sequence["event"]
    process = sequence["process"]

    if event == "start":
        sheet.write_string(2 + processes.index(process), 1 + idx, "O")
    else:
        sheet.write_string(1, 1 + idx, process)
workbook.close()
