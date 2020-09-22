from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
import threading
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

        self.presences_received = threading.Event()

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer
        
    def session_start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
        roster = self.get_roster()
        #print(roster)
        
    def mandarPresence(self, show, status):
        print("demostrando presencia")
        self.send_presence(pshow=show, pstatus = status)
    
    def SendMessageTo(self, jid, message):
        self.send_message(mto=jid, mbody=message, mtype='chat')

    def SendMessageRoom(self, room, message):
        self.send_message(mto=room, mbody=message, mtype='groupchat')
    
    def message(self, msg):
        print("Tipo de mensaje",msg['type'])
        print("De",msg['from'])
        print(msg['body'])


    def Login(self):
        success = False
        if self.connect():
            self.process()
            success = True
            print('Login exitoso')
        else:
            print('Ha ocurrido un error')

        return success

    def Unregister(self):
        print(self.boundjid.user)
        iq = self.make_iq_set(ito='redes2020.xyz', ifrom=self.boundjid.user)
        item = ET.fromstring("<query xmlns='jabber:iq:register'> \
                                <remove/> \
                              </query>")
        iq.append(item) 
        res = iq.send()
        print(res)


    def misUsers(self):
        try:
            self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()


        print('Waiting for presence updates...\n')
        self.presences_received.wait(5)

        print('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s) [%s]' % (name, jid, sub))
                else:
                    print(' %s [%s]' % (jid, sub))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])


    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    def AddUser(self, jid):
        self.send_presence_subscription(pto=jid)
    
    def Roster(self):
        roster = self.get_roster()
        
        print(roster)

    def Rooms(self, room, nickname):
        self.plugin['xep_0045'].joinMUC(room+"@conference.redes2020.xyz", nickname, wait=True)

    def GetUsers(self):
        
        iq = self.Iq()
        iq['type'] = 'set'
        iq['id'] = 'search_result'
        iq['to'] = 'search.redes2020.xyz'

        item = ET.fromstring("<query xmlns='jabber:iq:search'> \
                                <x xmlns='jabber:x:data' type='submit'> \
                                    <field type='hidden' var='FORM_TYPE'> \
                                        <value>jabber:iq:search</value> \
                                    </field> \
                                    <field var='Username'> \
                                        <value>1</value> \
                                    </field> \
                                    <field var='search'> \
                                        <value>*</value> \
                                    </field> \
                                </x> \
                              </query>")
        iq.append(item)
        res = iq.send()
        
        data = []
        temp = []
        cont = 0
        for i in res.findall('.//{jabber:x:data}value'):
            cont += 1
            txt = ''
            if i.text != None:
                temp.append(i.text)

            if cont == 4:
                cont = 0
                data.append(temp)
                temp = []

        return data

    def GetUser(self, username):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['id'] = 'search_result'
        iq['to'] = 'search.redes2020.xyz'

        item = ET.fromstring("<query xmlns='jabber:iq:search'> \
                                <x xmlns='jabber:x:data' type='submit'> \
                                    <field type='hidden' var='FORM_TYPE'> \
                                        <value>jabber:iq:search</value> \
                                    </field> \
                                    <field var='Username'> \
                                        <value>1</value> \
                                    </field> \
                                    <field var='search'> \
                                        <value>" + username + "</value> \
                                    </field> \
                                </x> \
                              </query>")
        iq.append(item)
        res = iq.send()
        
        data = []
        temp = []
        cont = 0
        for i in res.findall('.//{jabber:x:data}value'):
            cont += 1
            txt = ''
            if i.text != None:
                temp.append(i.text)

            if cont == 4:
                cont = 0
                data.append(temp)
                temp = []

        return data
        
        

    
if __name__ == '__main__':

    domain = '@redes2020.xyz'
    username = ''
    password = ''
    opcion = 9
    
    while opcion != 0:
        print("1. Crear Cuenta.  2. Iniciar sesion. 0. Salir")
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
                print("0. Deconectarse\n1. Obtener roster\n2. Agregar un usuario a los contactos.\n3. Eliminar mi cuenta.\n4. Mandar mensaje.\n5. Mostrar todos los usuarios registrados\n6. Buscar un usuario en especifico\n7. Ingresar o crear room")

                option = int(input("Ingrese la opcion: "))
                if option == 1:
                    print("opcion 1")
                    bot.Roster()
                if option == 2:
                    print("opcion 2")
                    user = input("Ingrese el Ingrese el jid:")
                    bot.AddUser(user)
                if option == 3:
                    bot.Unregister()
                    option = 0 
                if option == 4:
                    user  = input("Ingrese el Ingrese el jid: ")
                    msj = input("Ingrese el Ingrese el mensaje: ")
                    bot.SendMessageTo(user,msj)
                if option == 5:
                    server_users = bot.GetUsers()
                    print("USUARIOS REGISTRADOS EN EL SERVER: ")
                    for i in server_users:
                        print ("*",i)

                if option == 6:
                    specific_user = input("Ingrese el usuario a buscar: ")
                    user = bot.GetUser(specific_user)
                    for i in user:
                        print ("*",i[0])
                if option == 7:
                    cuarto = input("Ingrese el room a ingresar: ")
                    nick = input("Ingrese su nickname para este room: ")
                    bot.Rooms(cuarto, nick)
                if option ==8:
                    cuarto = input("Ingrese el room a escribir: ")
                    mensaje = input("igrese mensaje ")
                    print("*"*20)
                    print("El mensaje",mensaje,"se mandara al cuarto",cuarto)
                    print("*"*20)
                    bot.SendMessageRoom(cuarto, mensaje)
                if option ==9:
                    bot.misUsers()
                if option==10:
                    status = input("Agrega tu nuevo status: ")
                    show = input('Ingresa tu show:\nchat\naway\nxa\ndnd\n')
                    bot.mandarPresence(show,status)
                if option == 0:
                    print('Desconectandome')
                    bot.disconnect()


        if opcion == 0:
            print('Saliendo del programa')

            
    
    
