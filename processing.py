import datetime
import hashlib
import json

from pymongo import MongoClient
from elasticsearch import Elasticsearch
import re


def process_criminal_record(document):
    record = str(document.get("criminal_record"))
    if record != "null":
        if "РСФСР" in record:
            print("\n" + record)
            record = re.findall(r'\b\d+\b', record)
            record = [x for x in record if not (int(x) > 1900 or int(x) < 105 or len(x) < 3)]
            for article in record:
                if article == 144:
                    record[article] = 158
                elif article == 213:
                    record[article] = 260
                elif article == 206:
                    record[article] = 213
                elif article == 211:
                    record[article] = 260
        else:
            print("\n" + record)
            record = re.findall(r'\b\d+\b', record)
            record = [x for x in record if not (int(x) > 1900 or int(x) < 105 or len(x) < 3)]
        print(str(record) + "\n\n")
        return record
    else:
        return []


def process_education_level(document):
    education = str(document.get("education")).lower()
    higher_edu_tags = ["университет", "высшего", "институт", "академия",
                       "научного", "консерватория", "филиал", "высшего",
                       "высшая школа", "инст", "впо", "во", "военное училище"]
    secondary_edu_tags = ["пту", "колледж", "училище", "техникум", "спо", "пу"]
    school_edu_tags = ["школа", "общее", "основное", "лицей", "гимназия"]

    for tag in higher_edu_tags:
        if tag in education:
            education = "higher"
            return education

    for tag in secondary_edu_tags:
        if tag in education:
            education = "secondary"
            return education

    for tag in school_edu_tags:
        if tag in education:
            education = "school"
            return education

    return "null"


def process_elected_status(document):
    elected = str(document.get("elected"))
    if elected == "избр.":
        return "избран"
    return elected


def process_inoagent_status(document):
    elected = str(document.get("inoagent"))
    if elected != "null":
        return "confirmed"
    return "null"


def process_subject_of_nomination(document):
    subject = str(document.get("subject_of_nominmation")).lower()
    er = ["Единая Россия", "мой район"]
    kprf = ["КПРФ", "КОММУНИСТИЧЕСКАЯ ПАРТИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
            "коммунистической партии российской федерации"]
    ldpr = ["ЛДПР", "Либерально-демократической партии России", "Либерально-демократическая партия России"]
    nl = ["Новые люди"]
    sr = ["СПРАВЕДЛИВАЯ РОССИЯ"]
    retiree_ss = ["Российская партия пенсионеров за социальную справедливость", "РППСС"]
    retiree = ["ПАРТИЯ ПЕНСИОНЕРОВ", "партии пенсионеров"]
    ne_kprf = ["Коммунисты России"]
    rodina = ["Родина"]
    self_nomination = ["Самовыдвижение", "Самовыдвиженец"]
    green = ["Зеленые", "Зелёные"]
    alt_green = ["Зеленая альтернатива", "Зелёная альтернатива"]
    yabloko = ["Яблоко"]
    rost = ["Партия Роста", "партии роста"]
    rpss = ["РПСС", "КПСС", "Российская партия социальной справедливости",
            "Коммунистическая партия социальной справедливости", "российская партия свободы и справедливости"]
    gp = ["Гражданская платформа"]

    for tag in er:
        if tag.lower() in subject:
            return "Единая Россия"
    for tag in kprf:
        if tag.lower() in subject:
            return "КПРФ"
    for tag in ldpr:
        if tag.lower() in subject:
            return "ЛДПР"
    for tag in nl:
        if tag.lower() in subject:
            return "Новые Люди"
    for tag in sr:
        if tag.lower() in subject:
            return "Справедливая Россия"
    for tag in retiree_ss:
        if tag.lower() in subject:
            return "РППСС"
    for tag in retiree:
        if tag.lower() in subject:
            return "Партия Пенсионеров"
    for tag in ne_kprf:
        if tag.lower() in subject:
            return "Коммунисты России"
    for tag in rodina:
        if tag.lower() in subject:
            return "Родина"
    for tag in self_nomination:
        if tag.lower() in subject:
            return "Самовыдвижение"
    for tag in green:
        if tag.lower() in subject:
            return "Зеленые"
    for tag in alt_green:
        if tag.lower() in subject:
            return "Зеленая альтернатива"
    for tag in yabloko:
        if tag.lower() in subject:
            return "Яблоко"
    for tag in rost:
        if tag.lower() in subject:
            return "Партия роста"
    for tag in rpss:
        if tag.lower() in subject:
            return "РПСС"
    for tag in gp:
        if tag.lower() in subject:
            return "Гражданская платформа"
    return "Минорная партия"


def process_position(document):
    position = str(document.get("position"))
    director = ["директор", "генеральный директор", "директриса"]
    unemployed = ["домохозяин", "домохозяйка", "временно не работает", "временно не работающая", "безработный", "безработная",
                  "временно неработающий", "временно неработающая"]
    vice = ["заместитель директора", "заместитель"]
    retiree = ["пенсионер", "пенсионерка"]

    for tag in director:
        if tag in position.lower():
            return "Директор"

    for tag in unemployed:
        if tag in position.lower():
            return "Безработный"

    for tag in vice:
        if tag in position.lower():
            return "Заместитель"

    for tag in retiree:
        if tag in position.lower():
            return "Пенсионер"

    return position

def push_candidates(database):
    print("Candidates pushing started")
    candidates = database['candidates']
    cursor = candidates.find({})
    obj_count = 0
    for document in cursor:
        id = document["_id"]
        document.pop("_id")
        record = process_criminal_record(document)
        document["criminal_record"] = record
        education = process_education_level(document)
        document["education"] = education
        inoagent = process_inoagent_status(document)
        document["inoagent"] = inoagent
        subject = process_subject_of_nomination(document)
        document["subject_of_nominmation"] = subject
        elected = process_elected_status(document)
        document["elected"] = elected
        position = process_position(document)
        document["position"] = position

        es.create(index="candidates", id=id, body=document)
        obj_count += 1

    print(str(obj_count) + " Candidates pushing ended")


def push_elections(database):
    print("Elections pushing started")
    candidates = database['elections']
    cursor = candidates.find({})
    obj_count = 0
    for document in cursor:
        id = document["_id"]
        document.pop("_id")

        es.create(index="elections", id=id, body=document)
        obj_count += 1
    print(str(obj_count) + " Elections pushing ended")


def push_districts(database):
    print("Districts pushing started")
    candidates = database['districts']
    cursor = candidates.find({})
    obj_count = 0
    for document in cursor:
        id = document["_id"]
        document.pop("_id")
        document.pop("uik_id")

        es.create(index="districts", id=id, body=document)
        obj_count += 1
    print(str(obj_count) + " Districts pushing ended")


def push_results(database):
    print("Result pushing started")
    candidates = database['results']
    cursor = candidates.find({})
    obj_count = 0
    for document in cursor:
        id = document["_id"]
        document.pop("_id")
        try:
            es.create(index="results", id=id, body=document)
            obj_count += 1
        except:
            pass
    print(str(obj_count) + " Result pushing ended\n")


def setup_index(database, es):
    candidate_sample = database['candidates'].find_one()
    del candidate_sample['_id']
    district_sample = database['districts'].find_one()
    del district_sample['_id']
    del district_sample['uik_id']
    elections_sample = database['elections'].find_one()
    del elections_sample["_id"]
    results_sample = database['results'].find_one()
    del results_sample["_id"]

    es.index(index="candidates", id=1, body=candidate_sample)
    es.index(index="districts", id=2, body=district_sample)
    es.index(index="elections", id=3, body=elections_sample)
    es.index(index="results", id=4, body=results_sample)


client = MongoClient('0.0.0.0', 27017, username="admin", password="admin")
es = Elasticsearch("http://localhost:9200")
db = client["gas_vybory"]

push_candidates(db)
push_districts(db)
push_elections(db)
push_results(db)

