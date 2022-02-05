
from mycroft import MycroftSkill
from mycroft.messagebus import Message
import json

from .lib import MqttService



class MessageListener(MycroftSkill):
    
    # Initializing the skill
    def initialize(self):
        self.log.info("Initializing Skill MessageListener")
        self.add_event('speak', self.handler_speak)
        self.add_event('enclosure.mouth.viseme_list', self.handler_enclosure_mouth_viseme_list)
        self.mqttservice = MqttService("VisemeSkill", "mosquitto", self.log.info)
        self.prepare_for_webapp_message()
    
    def prepare_for_webapp_message(self):
        self.mqttservice.loopStart()
        self.mqttservice.subscribe("faceme/webapp", self.message_recieved)
           
    # acquiring speak data (the text mycroft will output):
    def handler_speak(self, message):
        self.text = message.data.get('utterance')

    # acquiring mouth_viseme_list data:
    def handler_enclosure_mouth_viseme_list(self, message):
        self.startTime = message.data.get('start')
        self.visemes = message.data.get('visemes')
        # Call method send_visemelist(build_json()) to send our now complete dataset via mqtt in a json string format
        self.send_visemelist(self.build_json()) 
   
   # Function to convert the strings acquired from the messagebus into a json string and return it:
    def build_json(self):
        data_set = {"text": self.text, "start": self.startTime, "visemes": self.visemes}
        json_dump = json.dumps(data_set)
        return json_dump
    
    def send_visemelist(self, payload):
        self.mqttservice.subscribe("faceme/mycroft/visemes", self.message_recieved) # Printet on_message von MQTT_service
        # Publish the payload we created in build_json() Wird richtig übertragen
        self.mqttservice.publish("faceme/mycroft/visemes", payload)
    
    def message_recieved(self, message):
        self.log.info("Es ist eine Nachricht angekommen: " + str(message.payload) + " topic: " + message.topic)
        if message.topic == "faceme/webapp":
            self.webapp_message(message) 

    def webapp_message(self, message):
        decoded_message = str(message.payload.decode("utf-8"))
        msg = json.loads(decoded_message)
        self.bus.emit(Message(msg["type"], msg["data"]))    
    
    def shutdown(self):
        self.mqttservice.loopStop()
        self.mqttservice.disconnect()

def create_skill():
    return MessageListener()

###### Unused Function #######
# Function adds the duration each viseme should be displayed to it's array so the data would be: "visemes": [[CODE, END_TIME, DURATION], ...]    
    #def addDuration(self):
        #self.visemes[0].append(self.visemes[0][1]) # Do we need this?
        #for x in range(len(self.visemes)):
          #if x < (len(self.visemes)-1):
            #duration = self.visemes[x+1][1] - self.visemes[x][1]
            #self.visemes[x+1].append(duration)