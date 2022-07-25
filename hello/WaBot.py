import requests
import json

class WaBot:
    def __init__(self, token: str, numberId: str):
        self.token = token
        self.numberId = numberId
        self.version = 'v13.0'

    def filterRequest(self, request):
        data = request.body
        json_data = json.loads(data)
        try: 
            message = json_data['entry'][0]['changes'][0]['value']['messages']
            user_name = json_data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name'].split(' ')[0]
            recipient_phone_number = json_data['entry'][0]['changes'][0]['value']['messages'][0]['from']
            phone_number = recipient_phone_number[:2] + recipient_phone_number[3:]
            return {
                'msg_id': message[0]['id'],
                'user_id': phone_number,
                'user_name': user_name,
                'type': message[0]['type'],
                'message': message,
                'phone_number': phone_number
            }
        except:
            return {
                'type': 'status'
            }
    
    def getMediaId(self, path, name):
        url = f"https://graph.facebook.com/{self.version}/{self.numberId}/media"

        payload={'messaging_product': 'whatsapp'}
        files=[
            ('file',(f'{name}.jpg',open(path,'rb'),'image/jpeg'))
        ]
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return response.text

    def getUrl(self, income):
        media_id = income['message'][0]['document']['id'] 

        url = f"https://graph.facebook.com/{self.version}/{media_id}"

        payload={}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text
    
    def downloadMedia(self, URL):
        url = URL

        payload={}
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.content
        
    def sendTemplate(self, toNumber: str, templateName: str, language: str):
        url = f"https://graph.facebook.com/{self.version}/{self.numberId}/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toNumber,
            "type": "template",
            "template": {
                "name": templateName,
                "language": {
                    "code": language
                }
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def sendText(self, toNumber: str, text: str):
        url = f"https://graph.facebook.com/{self.version}/{self.numberId}/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toNumber,
            "type": "text",
            "text": { 
                "preview_url": False,
                "body": text
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
            }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text

    def sendImage(self, toNumber:str, id, caption):
        url = f"https://graph.facebook.com/{self.version}/{self.numberId}/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toNumber,
            "type": "image",
            "image": {
                "id": id,
                "caption": caption
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    
    def sendButton(self, toNumber: str, body: str, buttons: dict):
        url = f"https://graph.facebook.com/{self.version}/{self.numberId}/messages"
        
        buttons_str = []
        for id, title in buttons.items():
            button = {
                    "type": "reply",
                    "reply": {
                        "id": id,
                        "title": title
                    }
                }
            buttons_str.append(button)

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toNumber,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "action": {
                    "buttons": buttons_str
                }
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
            }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response
    
    class CreateList:
        def __init__(self, header: str, body: str, footer: str, secciones: list):
            self.header = header
            self.body = body
            self.footer = footer
            self.secciones = secciones
            self.lista = None
            self.sections = {}
            for seccion in self.secciones:
                self.sections[seccion] = []
            
        def agregarElemento(self, seccion: str, id: str, title: str, description: str):
            elemento = {
                        "id": id,
                        "title": title,
                        "description": description
                        }
            self.sections[seccion].append(elemento)

            secciones = []

            for title, rows in self.sections.items():
                seccion = {
                            "title": title,
                            "rows": rows
                        }
                secciones.append(seccion)

            self.lista = {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": self.header
                },
                "body": {
                    "text": self.body
                },
                "footer": {
                    "text": self.footer
                },
                "action": {
                    "button": f"Ver {self.header.lower()}",
                    "sections": secciones
                }
            }     

    def sendList(self, lista, toNumber):
        url = f"https://graph.facebook.com/{self.version}/{self.numberId}/messages"

        payload = json.dumps({
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": toNumber,
            "type": "interactive",
            "interactive": lista
        })
        
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.token}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response


#-----SEND LISTA-----

#secciones = ['Deportes', 'Limpieza']
#listaProductos = bot.CreateList('Catalogo', 'Estos son los productos que tenemos disponibles', 'Hace click en el producto para obtener mas informacion', secciones)

#listaProductos.agregarElemento('Deportes', 'raqueta', 'Raqueta', '$12000')
#listaProductos.agregarElemento('Deportes', 'pelota', 'Pelota', '$7000')
#listaProductos.agregarElemento('Deportes', 'camiseta', 'Camiseta adidas', '$20000')

#listaProductos.agregarElemento('Limpieza', 'cepillo', 'Cepillo', '$300')
#listaProductos.agregarElemento('Limpieza', 'lavandina', 'Lavandina', '$250')

#bot.sendList(listaProductos.lista, toNumber=recipient_phone_number)

#------SEND BUTTON------

#buttons = {
#'1': 'Malo',
#'2': 'Regular',
#'3': 'Bueno'
#}
#bot.sendButton(toNumber=recipient_phone_number, body='Que te pareció el servicio?', buttons=buttons)

                

    