from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
from .models import Request
from .WaBot import WaBot
from .WaStat import WaStat
import json
from django.core.files.uploadedfile import SimpleUploadedFile

#https://fast-mountain-84176.herokuapp.com/webhook/

user_access_token = 'EAAUxZBG03YFABAKVMF0kZCI3NCVOggzYWb4KMK4wZAS5ZBY4QCoWCo8UUz3wZBuOMxj6ivSFunqqGqh2lHTavhX5vSzgtZAFjxORsEEbd00VxZCZAW6gzZAaMZCdqvQ021xFIM68LFuPvbiS040yuSZCCte2C7fHtfVC0U427cVwGWwPCEpy9SKssrqS42fgXfMHitQIk0rY1H5NAZDZD'
phone_number_ID = '110760258382662'
#recipient_phone_number = '542494566070'

bot = WaBot(token=user_access_token, numberId=phone_number_ID)
stats = WaStat()

@csrf_exempt
def webhook(request):
    data = request.body
    json_data = json.loads(data)
    print(json_data)
    if request.method == 'POST':
        income = bot.filterRequest(request)
        try:
            msg_sent = Request.objects.filter(msg_id=income['msg_id']).exists()
        except:
            msg_sent = True
        if not msg_sent:   
            if income['type'] == 'text': 
                if not Request.objects.filter(user_id=income['user_id']).exists():
                    recipient_phone_number = income['phone_number']
                    new_message = Request(msg_id=income['msg_id'], user_id=income['user_id'], user_name=income['user_name'])
                    new_message.save()   
                    user_name = income['user_name']
                    msg1 = f'Hola {user_name}! soy Wasaby \U0001F916, el bot que te va a generar estadisticas sobre tu grupo de Whatsapp \U0001F9BE\n\n'
                    msg1 += '\U0001F449 Queres saber quien es la persona que mas mensajes manda en tu grupo?\n\U0001F449 Cual es la hora del dia con mas actividad?'
                    print(bot.sendText(toNumber=recipient_phone_number, text=msg1))
                    msg2 = 'Enviame tu historial de chat en formato .txt \U0001F4C4 y despues de unos segundos te voy a mandar todas las estadisticas'
                    bot.sendText(toNumber=recipient_phone_number, text=msg2)
                    msg3 = 'Si no sabes como hacerlo aca te dejo instrucciones según tu sistema operativo'
                    bot.sendText(toNumber=recipient_phone_number, text=msg3)
                    buttons = {
                        '1': 'Android',
                        '2': 'IOs',
                        }
                    bot.sendButton(toNumber=recipient_phone_number, body='Que sistema operativo tenés?', buttons=buttons)
                else:
                    recipient_phone_number= income['phone_number']
                    print(recipient_phone_number)
                    new_message = Request(msg_id=income['msg_id'], user_id=income['user_id'], user_name=income['user_name'])
                    new_message.save() 
                    msg = 'No te entendí...\n\nLo unico que se hacer por ahora es leer chats de WhatsApp'
                    print(bot.sendText(toNumber=recipient_phone_number, text=msg))

            if income['type'] == 'document':
                recipient_phone_number= income['phone_number']
                new_message = Request(msg_id=income['msg_id'], user_id=income['user_id'], user_name=income['user_name'])
                new_message.save() 
                bot.sendText(toNumber=recipient_phone_number, text='Analizando... \U0001F9D0')
                data = bot.getUrl(income)
                json_data = json.loads(data)
                url = json_data['url']
                document = bot.downloadMedia(url)
                doc = SimpleUploadedFile("chat.txt", document, content_type="text/plain")
                file_doc = Chat(file=doc)
                file_doc.save()
                path = Chat.objects.last().file.path
                with open(path, 'r',encoding='utf-8') as f:
                    file = f.name
                    txt = f
                    try:
                        os_chat = stats.checkOs(txt)
                    except:
                        bot.sendText(toNumber=recipient_phone_number, text='Solo se leer archivos .txt \U0001F614')
                        msg = 'Acá te dejo las instrucciones para enviarme el historial de tu chat'
                        bot.sendText(toNumber=recipient_phone_number, text=msg)
                        buttons = {
                            '1': 'Android',
                            '2': 'IOs',
                            }
                        bot.sendButton(toNumber=recipient_phone_number, body='Que sistema operativo tenés?', buttons=buttons)
                        return
                df = stats.cleanTxt(file, os_chat)
                graphs = stats.graphs(df)

                ranking = graphs[0]
                msg = 'RANKING DE MENSAJES POR PERSONA\n'
                for rank in ranking:
                    msg += f'\n{rank[0]} ---> {rank[1]} mgs'

                bot.sendText(toNumber=recipient_phone_number, text=msg)

                id = json.loads(bot.getMediaId('media/graphs/rank-per-year.png', 'rank-per-year'))['id']
                bot.sendImage(toNumber=recipient_phone_number, id=id, caption="Quien envió mas mensajes por año")
                id = json.loads(bot.getMediaId('media/graphs/chronology.png', 'chronology'))['id']
                bot.sendImage(toNumber=recipient_phone_number, id=id, caption="Cronologia de mensajes")
                id = json.loads(bot.getMediaId('media/graphs/histogram.png', 'histogram'))['id']
                bot.sendImage(toNumber=recipient_phone_number, id=id, caption="Histograma de mensajes diario")
                id = json.loads(bot.getMediaId('media/graphs/week.png', 'week'))['id']
                bot.sendImage(toNumber=recipient_phone_number, id=id, caption="Que dia de la semana se envia más mensajes")
                id = json.loads(bot.getMediaId('media/graphs/year.png', 'year'))['id']
                bot.sendImage(toNumber=recipient_phone_number, id=id, caption="Que mes del año se envia más mensajes")

            if income['type'] =='interactive':
                recipient_phone_number= income['phone_number']
                new_message = Request(msg_id=income['msg_id'], user_id=income['user_id'], user_name=income['user_name'])
                new_message.save() 
                if income['message'][0]['interactive']['button_reply']['title'] == 'Android':
                    msg = 'INSTRUCCIONES PARA ANDROID\n\n'
                    msg += '1 - Agendame como cualquier otro contacto\n'
                    msg += '2 - Andá al chat que queres que analice\n'
                    msg += '3 - Apretá los 3 puntitos arriba a la derecha\n'
                    msg += '4 - ---> Más\n'
                    msg += '5 - ---> Exportar chat\n'
                    msg += '6 - ---> Sin archivos\n'
                    msg += '7 - Enviamelo a mi y esperá los resultados \U0001F91F'
                    bot.sendText(toNumber=recipient_phone_number, text=msg)
                elif income['message'][0]['interactive']['button_reply']['title']  == 'IOs':
                    msg = 'No tengo iphone'
                    bot.sendText(toNumber=recipient_phone_number, text=msg) 
            return HttpResponse(status=204)

    if request.method == 'GET':
        data = request.GET
        data_dict = data.dict()
        print(data_dict)
        token = data_dict['hub.verify_token']
        mode = data_dict['hub.mode']
        challenge = data_dict['hub.challenge']
        if token and mode:
            if mode == 'subscribe' and token == 'betun':
                return HttpResponse(challenge)

    return HttpResponse('No hay data')

