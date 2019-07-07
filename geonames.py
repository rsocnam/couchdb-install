import csv
import json
import datetime
import requests
from hashlib import md5

filename = "allCountries.txt"

def getPois(filename):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            names = [row[1]]

            if row[2] not in names:
                names.append(row[2])

            for name in str(row[3]).split(","):
                if name not in names:
                    names.append(name)

            poi = {
                "id": int(row[0]),
                "names": list(filter(lambda o: len(o) > 0, names)),
                "latitude": float(row[4]),
                "longitude": float(row[5]),
                "feature_class": row[6].upper(),
                "feature_code": row[7].upper(),
                "country_code": row[8].upper(),
            }

            try:
                poi["elevation"] = int(row[15])
            except:
                poi["elevation"] = None

            yield poi


def display_progress(total):
    if total % 10000 == 0:
        print("{} {} inserted".format(datetime.datetime.now().time().isoformat(), total))

def import_couch(filename):
    def process_batch(b):
        if len(b) > 0:
            bulk_params = {"docs": []}
            for poi in b:
                bulk_params["docs"].append({
                    "id": str(poi["id"])
                })

            bulk_url = db_url+"/_bulk_get"
            res = requests.post(bulk_url, data=json.dumps(bulk_params), headers={"content-type": "application/json"})
            data = json.loads(res.content)

            bulk_docs_params = {"docs": []}

            if "results" in data:
                for i in range(0, len(data["results"])-1):
                    if "error" in data["results"][i]["docs"][0]:
                        obj = b[i]
                        bulk_docs_params["docs"].append(obj)
                    else:
                        if "ok" in data["results"][i]["docs"][0]:
                            old_hash = data["results"][i]["docs"][0]["ok"]["hash"]
                            new_hash = b[i]["hash"]
                            if (old_hash != new_hash):
                                last_revision = data["results"][i]["docs"][0]["ok"]["_rev"]
                                obj = b[i]
                                obj["_rev"] = last_revision
                                bulk_docs_params["docs"].append(obj)

            if (len(bulk_docs_params["docs"]) > 0):
                def replace_id_field(obj):
                    obj["_id"] = str(obj["id"])
                    del (obj["id"])
                    return obj

                bulk_docs_params["docs"] = list(map(replace_id_field, bulk_docs_params["docs"]))

                bulk_url = db_url+"/_bulk_docs"
                res = requests.post(bulk_url, data=json.dumps(bulk_docs_params), headers={"content-type": "application/json"})
                res = json.loads(res.content)
                for o in res:
                    if "ok" not in o:
                        print (o)


    shards = 4
    replicas = 3
    db_url = "http://nfe204:nfe204@192.168.122.201/geonames"
    response = json.loads(requests.get(db_url).content)

    if "error" in response:
        json.loads(requests.put("{}?n={}&q={}".format(db_url, str(replicas), str(shards))).content)

    total = 0
    batch = []
    batch_size = 1000

    for poi in getPois(filename):
        poi["hash"] = str(md5(bytearray(json.dumps(poi), "utf8")).hexdigest())[0:4]
        batch.append(poi)
        total += 1

        if batch_size == len(batch):
            process_batch(batch)
            batch.clear()

        display_progress(total)

    process_batch(batch)


import_couch(filename)
