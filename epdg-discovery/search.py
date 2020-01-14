import json
f = open("mcc_mnc_dump.json", "r")
content = json.loads(f.read())
count_total = len(content)
count_null = 0
count_valid = 0
for i in range(0, count_total):
    if (content[i]["epdg_ip"] == ""):
        count_null = count_null + 1
    else:
        print(content[i]["country"] + " - " + content[i]["network"] + " - " + content[i]["epdg"] + " - " + content[i]["epdg_ip"])
        count_valid = count_valid + 1

print str(count_valid) + " valid, ", str(count_null) + " invalid, ", str(count_total) + " total"