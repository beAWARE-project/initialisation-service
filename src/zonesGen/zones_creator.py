from bus.bus_producer import BusProducer
import json
from datetime import datetime, timedelta
import os

def generateTopic():
    owd = os.getcwd()
    producer = BusProducer()

    os.chdir('zonesGen/sample_json/')
    with open('TOP106_Sample.json') as f:
        msg = json.load(f)
    f.close()
    dataStreamID = msg['body']['dataStreamID']

    polygons = ['polygon1.json','polygon2.json', 'polygon3.json', 'polygon4.json']
    iter = 0
    for jsonFile in polygons:
        with open(jsonFile) as f:
            plgn = json.load(f)
        f.close()

        iter += 1
        msg['body']['dataStreamID'] = dataStreamID + '_'+ str(10000*abs(plgn['center']['latitude']))[:4] + str(10000*abs(plgn['center']['longitude']))[:4]
        polygonStruct = []
        polygonStruct.append(plgn['polygon'])
        msg['body']['polygons'] = polygonStruct
        msg['body']['position'] = plgn['center']
        msg['body']['dataStreamName'] = 'ZONE ' + str(iter).zfill(2)
        plgn['polygon']['properties']['label'] = 'ZONE ' + str(iter).zfill(2)
        plgn['polygon']['properties']['color'] = {"r": 0,"g": 0, "b": 0}
        msg['body']['dataStreamDescription'] = plgn['Name']

        msg['header']["sentUTC"] = str("{}Z".format((datetime.utcnow() - timedelta(hours=0)).replace(microsecond=0).isoformat()))
        msg['header']['msgIdentifier'] = msg['header']["sentUTC"]

        print(json.dumps(msg))
        #with open('ZONE' + str(iter) + '.json', 'w') as outfile:
        #    outfile.write(msg)
        #outfile.close()
        producer.send(msg["header"]["topicName"], json.dumps(msg))

    os.chdir(owd)
    #print('round ended')
#generateTopic()