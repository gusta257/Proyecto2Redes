from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
import logging

class RegisterBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration

    def start(self, event):
        self.send_presence()
        self.get_roster()
        
        self.disconnect()

    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        
        try:
            resp.send(now=True)
            print("Account created for %s!" % self.boundjid)
            log = logging.getLogger("my-logger")
            log.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            print("Could not register account: %s" %
                    e.iq['error']['text'])
            log.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            log.error("No response from server.")
            self.disconnect()
class EchoBot(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        print("Creacion de eventos")
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.handleMessage)

    def start(self, event):
        print("demostrando presencia")
        self.send_presence(pstatus = "Send me a message")
        
    def run(self):
        print("connectandome")
        self.connect()
        self.get_roster()
        self.process(threaded=False)

    def handleMessage(self,message):    
        print("mandando mensaje")
        self.sendMessage(message["jid"],message["message"])
        
        

    
if __name__ == '__main__':

    domain = '@redes2020.xyz'
    username = 'asd1234'
    password = 'asd1234'
    opcion = 9
    
    while opcion != 0:

        opcion = int(input("Ingrese la opcion"))

        if opcion == 1:
            xmpp = RegisterBot(username + domain, password)
            if xmpp.connect():
                xmpp.process(block=True)
                print("Done")
            else:
                print("Unable to connect.")
        if opcion == 2:
            print("opcion 2 jeje")
            bot = EchoBot(username + domain, password)
            bot.run()
        if opcion == 0:
            print('fuera')
            xmpp.disconnect()
            
    
    
