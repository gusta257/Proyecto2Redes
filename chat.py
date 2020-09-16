from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File

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
        except IqError as e:
            print("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            self.disconnect()

            
class EchoBot(ClientXMPP):
    
    
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer
        
    def session_start(self, event):
        self.send_presence(pshow='chat', pstatus='sito')
        roster = self.get_roster()
        print(roster)
        
    def start(self, event):
        print("demostrando presencia")
        self.send_presence(pstatus = "Send me a message")
    
    def SendMessageTo(self, jid, message):
        self.send_message(mto=jid, mbody=message, mtype='chat')
    
    def message(self, msg):
        print(msg)


    def Login(self):
        success = False
        if self.connect():
            self.process()
            success = True
            print('Login exitoso')
        else:
            print('Ha ocurrido un error')

        return success



    def AddUser(self, jid):
        self.send_presence_subscription(pto=jid)
    
    def Roster(self):
        roster = self.get_roster()
        print(roster)
        
        

    
if __name__ == '__main__':

    domain = '@redes2020.xyz'
    username = ''
    password = ''
    opcion = 9
    
    while opcion != 0:
        print("1. Crear Cuenta.  2. Iniciar sesion.   3.Eliminar la cuenta del servidor  0. Salir")
        opcion = int(input("Ingrese la opcion: "))

        if opcion == 1:
            username = input("Ingrese el usuario: ")
            password = input("Ingrese la contraseña: ")
            xmpp = RegisterBot(username + domain, password)
            if xmpp.connect():
                xmpp.process(block=True)
                print("Done")
            else:
                print("Unable to connect.")
        if opcion == 2:
            option = 100
            username = input("Ingrese el usuario: ")
            password = input("Ingrese la contraseña: ")

            bot = EchoBot(username + domain, password)
     
            if bot.Login():
                print("Hice login")
            
            while option != 0:
                print("1.obtener roster  \n2. Agregar un usuario a los contactos. \n3. Mostrar detalles de contacto de un usuario. \n4.Comunicación 1 a 1 con cualquier usuario / contacto.")

                option = int(input("Ingrese la opcion: "))
                if option == 1:
                    print("opcion 1")
                    bot.Roster()
                if option == 2:
                    print("opcion 2")
                    user = input("Ingrese el Ingrese el jid:")
                    bot.AddUser(user)

                if option == 4:
                    user  = input("Ingrese el Ingrese el jid:")
                    msj = input("Ingrese el Ingrese el mensaje:")
                    bot.SendMessageTo(user,msj)
                if option == 0:
                    print('fuera')
                    xmpp.disconnect()


        if opcion == 0:
            print('fuera')
            xmpp.disconnect()
            
    
    
