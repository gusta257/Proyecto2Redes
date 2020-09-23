from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
import threading
from sleekxmpp.plugins.xep_0096 import stanza, File

class Registro(ClientXMPP):

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

            
class Cliente(ClientXMPP):
    
    
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.yo = jid
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)
        self.add_event_handler("groupchat_message", self.notificacionMencion)
        
        self.presences_received = threading.Event()

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer
        
    def session_start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
        self.show = 'chat'
        roster = self.get_roster()
        #print(roster)

          

    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            who = presence['from'].bare
            index2 = who.find('@conference')
            print("\n")
            print("*************************NOTIFICACION**************************")
            print(presence['muc']['nick'],"ha entrado al grupo",who[:index2])
            print("***************************************************************")
        

    def notificacionMencion(self, msg):
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            who = str(msg['from'])
            index2 = who.find('@conference')
            
            print("*************************NOTIFICACION**************************")
            print(msg['mucnick'],"te ha mencionado en el grupo",who[:index2])
            print("***************************************************************")
            

    def mandarPresence(self, show, status):
        print('\n')
        print("Status cambiado")
        print('\n')
        self.send_presence(pshow=show, pstatus = status)
    
    def SendMessageTo(self, jid, message):
        self.send_message(mto=jid+"@redes2020.xyz", mbody=message, mtype='chat')

    def SendMessageRoom(self, room, message):
        self.send_message(mto=room+"@conference.redes2020.xyz", mbody=message, mtype='groupchat')
    
    def logOut(self):
            self.show = 'dnd'
            self.send_presence(pshow=self.show, pstatus = "Desconectado")

    def message(self, msg):
        
        if(msg['type']=='chat'):
            print("\n")
            print("*"*40)
            who = str(msg['from'])
            index = who.find('/') 
            
            print("Mensaje privado")
            print("De:",who[:index])
            print("Mensaje:",msg['body'])
            print("*"*40)

        elif(msg['type']=='groupchat'):
            who = str(msg['from'])
            index = who.find('/') 
            index2 = who.find('@conference')

            if who[index+1:] != self.nick:

                print("\n")
                print("*"*40)
                

                print("Grupo:",who[:index2])
                print("De:",who[index+1:])
                print("Mensaje:",msg['body'])
                print("*"*40)

        
        

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

        print('  Amigos de %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            print('-' * 72)
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if (jid != self.yo):
                    print(' * User: %s' % (jid))

                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = self.show
                    if pres['show'] and jid != self.yo:
                        show = pres['show']
                    if jid != self.yo:
                        print(' - Estado: (%s)' % (show))
                    if pres['status'] and jid != self.yo and len(str(pres['status'])) > 0:
                        print(' - Status: %s' % pres['status'])
                print('-' * 72)
                print
                    


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
        self.send_presence_subscription(pto=jid+"@redes2020.xyz")
    
    def Roster(self):
        roster = self.get_roster()
        
        print(roster)

    def CreateRooms(self, room, nickname):
        self.nick = nickname
        status = "Bienvenido"
        self.room = room+"@conference.redes2020.xyz"
        self.plugin['xep_0045'].joinMUC(room+"@conference.redes2020.xyz", nickname, pstatus=status, pfrom=self.boundjid.full)
        self.plugin['xep_0045'].setAffiliation(room+"@conference.redes2020.xyz", self.boundjid.full, affiliation='owner')
        self.plugin['xep_0045'].configureRoom(room+"@conference.redes2020.xyz", ifrom = self.boundjid.full)
        self.add_event_handler("muc::"+room+"@conference.redes2020.xyz::got_online" , self.muc_online)
    
    def Rooms(self, room, nickname):
        self.nick = nickname
        self.plugin['xep_0045'].joinMUC(room+"@conference.redes2020.xyz", nickname)
        self.add_event_handler("muc::"+room+"@conference.redes2020.xyz::got_online" , self.muc_online)

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
            xmpp = Registro(username + domain, password)
            if xmpp.connect():
                xmpp.process(block=True)
                print("Done")
            else:
                print("Unable to connect.")
        if opcion == 2:
            option = 100
            username = input("Ingrese el usuario: ")
            password = input("Ingrese la contraseña: ")

            bot = Cliente(username + domain, password)
     
            if bot.Login():
                print("Hice login")
            
            while option != 0:
                print("0. Desconectarse\n1. Agregar nuevo Status\n2. Agregar un usuario a los contactos.\n3. Eliminar mi cuenta.\n4. Mandar mensaje.\n5. Mostrar todos los usuarios registrados\n6. Buscar un usuario en especifico\n7. Ingresar a room\n8. Mandar mensaje grupal\n9. Mostrar usuarios agregados\n10. Crear un room")

                option = int(input("Ingrese la opcion: "))
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
                    mensaje = input("Ingrese mensaje: ")
                    bot.SendMessageRoom(cuarto, mensaje)
                if option ==9:
                    bot.misUsers()
                if option==1:
                    status = input("Agrega tu nuevo status: ")
                    show = input('Ingresa tu show:\nchat\naway\nxa\ndnd\n')
                    bot.mandarPresence(show,status)
                if option==10:
                    cuarto = input("Ingrese el nombre del nuevo room: ")
                    nick = input("Ingrese su nickname para este room: ")
                    bot.CreateRooms(cuarto, nick)
                if option == 0:
                    print('Desconectandome')
                    bot.logOut()
                    bot.disconnect()


        if opcion == 0:
            print('Saliendo del programa')

            
    
    
'''
chat Announces that you are available for, and actively seeking, conversation (perhapsyou’re feeling especially sociable).
away Indicates that you are gone from your IM client, computer, or device for a shortperiod of time; this state is often triggered without human intervention through afeature known as auto-away, commonly found in many IM clients.
xa Indicates that you are gone for a longer period of time (xa is shorthand for “eX-tended Away”); your IM client can also automatically generate this state.
dnd Announces that you are busy and don’t want to be interrupted right now (dnd isshorthand for “do not disturb”).

'''