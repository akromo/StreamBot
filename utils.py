import config
import time
from requests import post, get, exceptions


def send_message(channel, message):
    """
    Отправка сообщение в Discord канал
    :param channel: ID Discord канала
    :param message: Сообщение которое будет отправлено (TTS = False)
    :return: Ничего не возвращает
    """
    r = post(config.URL_DISCORD_API + '/channels/%s/messages' % channel, headers={'Authorization': config.TOKEN_DIS},
             json={"content": message, "tts": "false"})
    r.raise_for_status()


def mess(sock, channel, message):
    """
    Отправляет сообщение message в чат канала config.CHAN_TW
    :param channel: канал в который будет отправленно сообщение
    :param sock: Сокет через который будет отправляться сообщение
    :param message: Сообщение которое будет отправлено
    :return: Ничего не возвращает
    """
    sock.send("PRIVMSG #{} :{}\r\n".format(channel, message).encode('utf-8'))


def ban(sock, channel, user, reason):
    mess(sock, channel, '.ban {} {}'.format(user, reason))


def timeout(sock, user, seconds=500):
    mess(sock, '.timeout {}'.format(user, seconds))


def fillOpList(chan):
    """
    Заполнить словарь oplist информацие о пользователях в чате
    :return: Ничего не возвращает, но меняет словарь oplist из модуля config
    """
    while True:
        url = 'http://tmi.twitch.tv/group/user/%s/chatters' % chan
        req = get(url, headers={'accept': '*/*'})
        res = req.json()
        if res != 0:
            config.oplist.clear()
            data = res
            for p in data['chatters']['broadcaster']:
                config.oplist[p] = 'mod'
            for p in data['chatters']['moderators']:
                config.oplist[p] = 'mod'
            for p in data['chatters']['global_mods']:
                config.oplist[p] = 'mod'
            for p in data['chatters']['admins']:
                config.oplist[p] = 'mod'
            for p in data['chatters']['staff']:
                config.oplist[p] = 'staff'
        time.sleep(20)


def isOp(user):
    """
    Проверяет является ли пользователь user модератором в чате канала
    :param user: Проверяемый пользователь
    :return: True/False
    """
    return config.oplist[user] == 'mod'


def check_user(channel):
    """
    Проверка ведется ли в данный момент трансляция на канале CHAN_TW
    :return: (0: online / 1: offline / 2: not found / 3: error) и dict
    """

    streamInfoURL = 'https://api.twitch.tv/helix/streams?user_login=' + channel
    info = None
    status = 3
    sep = '='*50
    try:
        r = get(streamInfoURL, headers={"Client-ID": config.CLIENT_ID_TW,
                                        'Authorization': 'Bearer '+config.AUTHORIZATION_TW})
        r.raise_for_status()
        info = r.json()

        if not info['data']:
            print(time.asctime() + ': Stream offline')
            status = 1
        else:
            #print(sep + '\n' + time.asctime() + '\n' + 'user_name: ' + info['data'][0]['user_name'] + '\n' +
            #      'viewer_count: ' + str(info['data'][0]['viewer_count']) + '\n' + 'game_id: ' +
            #      str(info['data'][0]['game_id']) + '\n' + 'title: ' + info['data'][0]['title'] + '\n' + sep)
            status = 0
    except exceptions.RequestException as e:
        print('error')
        print(e)
        print(e.response)
        if e.response:
            if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                status = 2

    return status, info

