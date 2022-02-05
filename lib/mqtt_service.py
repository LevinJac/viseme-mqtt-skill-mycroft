

import paho.mqtt.client as mqtt

class MqttService:
  def __init__(self, name, host, logger):
      self.mycroftlogger = logger
      self.name = name
      self.host = host
      self.callback = None
      self.mqttc = mqtt.Client(name)
      self.mqttc.on_connect = self.on_connect
      self.mqttc.on_publish = self.on_publish
      self.mqttc.on_message = self.on_message
      self.mqttc.on_disconnect = self.on_disconnect
      self.mqttc.connect(host)

  def log(self, message):
      self.mycroftlogger(message)
  
  # The callback for when the client receives a CONNACK response from the server.
  def on_connect(self, mqttc, userdata, flags, rc, properties=None):
      self.log("Connected with result code "  +str(rc))
    
  # with this callback you can see if your publish was successful
  def on_publish(self, mqttc, userdata, mid, properties=None):
      self.log("mid: " + str(mid))
    
  # print message, useful for checking if recieving was successful
  def on_message(self, mqttc, userdata, msg):
      self.callback(msg)
  
  def subscribe(self, topic, callback):
      self.mqttc.subscribe(topic)
      self.callback = callback 
  
  def publish(self, topic, payload):
      self.mqttc.publish(topic, payload)  
  
  def disconnect(self):
      self.mqttc.disconnect()
  
  def on_disconnect(self, client, userdata, rc):
      if rc != 0:
        self.log("Unexpected disconnection")
      else:
        self.log("Disconnected succesfully")

  def loopStart(self):
      self.mqttc.loop_start()
  
  def loopStop(self):
      self.mqttc.loop_stop()

