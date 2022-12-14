from kafka import KafkaConsumer
from pymongo import MongoClient
import json

topics = ["vrn", "vrn_oik", "vrn_oik_uik", "vrn_candidate"]
envir = os.environ

try:
    client = MongoClient(envir["mongo_ip"], int(envir["mongo_port"]), username=envir["mongo_usr"], password=envir["mongo_pwd"])
    db = client.gas_vybory
    print("Connected successfully!")
except:
    print("Could not connect to MongoDB")

server = list(envir["mongo_ip"] + str(":") + envir["kafka_port"])
consumer = KafkaConsumer(*topics, bootstrap_servers=server)
for msg in consumer:
    if msg.topic == "vrn":
        record = json.loads(msg.value)
        vrn = record['vrn']
        title = record['title']
        level = record['level']
        date = record['date']
        try:
            vrn_rec = {'vrn': vrn, 'title': title, 'level': level, 'date': date}
            rec_id = db.elections.insert_one(vrn_rec)
            print("Data inserted with record ids", rec_id)
        except:
            print("Could not insert into MongoDB")
    elif msg.topic == "vrn_oik":
        record = json.loads(msg.value)
        vrn = record['vrn']
        oik_id = record['oik_id']
        try:
            vrn_oik_rec = {'vrn': vrn, 'oik_id': oik_id}
            rec_id = db.districts.insert_one(vrn_oik_rec)
            print("Data inserted with record ids", rec_id)
        except:
            print("Could not insert into MongoDB")
    elif msg.topic == "vrn_oik_uik":
        record = json.loads(msg.value)
        vrn = record['vrn']
        oik_id = record['oik_id']
        uik_id = record['uik_id']
        total_voters = record['total_voters']
        recieved_ballots = record['recieved_ballots']
        issued_ballots_inside = record['issued_ballots_inside']
        issued_ballots_outside = record['issued_ballots_outside']
        not_used_ballots = record['not_used_ballots']
        ballots_from_outside_boxes = record['ballots_from_outside_boxes']
        ballots_from_inside_boxes = record['ballots_from_inside_boxes']
        invalid_ballots = record['invalid_ballots']
        lost_ballots = record['lost_ballots']
        not_counted_recieved_ballots = record['not_counted_recieved_ballots']
        candidates_results = record['candidates_results']
        try:
            vrn_oik_rec = {'vrn': vrn, 'oik_id': oik_id, 'uik_id': uik_id, 'total_voters': total_voters,
                           'recieved_ballots': recieved_ballots, 'issued_ballots_inside': issued_ballots_inside,
                           'issued_ballots_outside': issued_ballots_outside, 'not_used_ballots': not_used_ballots,
                           'ballots_from_outside_boxes': ballots_from_outside_boxes,
                           'ballots_from_inside_boxes': ballots_from_inside_boxes, 'invalid_ballots': invalid_ballots,
                           'lost_ballots': lost_ballots, 'not_counted_recieved_ballots': not_counted_recieved_ballots,
                           'candidates_results': candidates_results}
            rec_id = db.results.insert_one(vrn_oik_rec)
            print("Data inserted with record ids", rec_id)
        except:
            print("Could not insert into MongoDB")
    elif msg.topic == "vrn_candidate":
        record = json.loads(msg.value)
        vrn = record['vrn']
        oik_id = record['oik_id']
        candidate_id = record['candidate_id']
        name = record['name']
        dob = record['dob']
        place_of_birth = record['place_of_birth']
        place_of_living = record['place_of_living']
        education = record['education']
        employer = record['employer']
        position = record['position']
        deputy_info = record['deputy_info']
        criminal_record = record['criminal_record']
        inoagent = record['inoagent']
        status = record['status']
        subject_of_nominmation = record['subject_of_nominmation']
        nomination = record['nomination']
        registration = record['registration']
        elected = record['elected']
        try:
            vrn_oik_rec = {'vrn': vrn, 'oik_id': oik_id, 'candidate_id': candidate_id, 'name': name, 'dob': dob,
                           'place_of_birth': place_of_birth, 'place_of_living': place_of_living, 'education': education,
                           'employer': employer, 'position': position, 'deputy_info': deputy_info,
                           'criminal_record': criminal_record, 'inoagent': inoagent, 'status': status,
                           'subject_of_nominmation': subject_of_nominmation, 'nomination': nomination,
                           'registration': registration, 'elected': elected}
            rec_id = db.candidates.insert_one(vrn_oik_rec)
            print("Data inserted with record ids", rec_id)
        except:
            print("Could not insert into MongoDB")
