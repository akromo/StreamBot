import sys
import os

import utils
import argparse
import config
import time
import socket
import _thread as thread
from DBconfig import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def startChatBot(chan):
    print('Chat bot starting')
    s = socket.socket()
    s.connect((config.HOST_TW, config.PORT_TW))
    s.send('PASS {}\r\n'.format(config.PASS_TW).encode('utf-8'))
    s.send('NICK {}\r\n'.format(config.NICK_TW).encode('utf-8'))
    s.send('JOIN #{}\r\n'.format(chan).encode('utf-8'))
    time.strftime("%I:%M %B %d %Y")

    print("Bot started")
    timecount = time.time()
    thread.start_new_thread(utils.fillOpList, (chan,))

    while True:
        if time.time() - timecount >= 15*60:
            utils.mess(s, chan, '=> https://discord.gg/UnUhDNz <=')
            timecount = time.time()

        response = s.recv(1024).decode('utf-8')
        print('\n', response, sep='', end='=====================================')

        if str(response)[0:19] in 'PING :tmi.twitch.tv':
            s.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))

        else:
            try:
                username = str(response).split('!')[0][1:]
            except Exception as x:
                print('==achtung==achtung==achtung==achtung==achtung==achtung==achtung=='.upper())
                print('===== Exeption =====')
                print(x, x.args)
                print('===== Exeption =====')
                print('===== Response =====')
                print(response, end='')
                print('===== Response =====')
                print('===== Username =====')
                print(username)
                print('===== Username =====')
                print('==achtung==achtung==achtung==achtung==achtung==achtung==achtung=='.upper())
            message = str(response).split('#%s :' % chan)[-1].strip()
            print('\n "%s"' % message, sep='')
            print('\n "%s"' % username, sep='')
            if message == '!discord':
                utils.mess(s, chan, "=>https://discord.gg/UnUhDNz<=")
            if message.strip() == "!test" and utils.isOp(username):
                utils.mess(s, chan, "=>https://discord.gg/UnUhDNz<=(test)")

        time.sleep(1)


if __name__ == '__main__':
    name = os.path.join('logs', 'log_%s.txt' % time.strftime("%H:%M_%m.%d.%Y"))
    #file = open(name, 'w')
    #file.close()
    #sys.stdout = file
    #sys.stderr = file
    parser = argparse.ArgumentParser(description='Test')
    parser.add_argument("--test", default=False, help="Test mod")
    test = parser.parse_args().test
    engine = create_engine('sqlite:///Data.db', echo=False)
    Session = sessionmaker(bind=engine)
    isThreadRun = False
    if test:
        server = config.TEST_SERVER_ID_DIS
        channel = config.CHAN_TW_Test
    else:
        server = config.MAIN_SERVER_ID_DIS
        channel = config.CHAN_TW
    session = Session()
    user = session.query(User).filter(User.user_login.in_([channel])).first()
    if user == None:
        session.add(User(channel, 'none'))
        session.commit()
        user = session.query(User).filter(User.user_login.in_([channel]).first())
        print('Add %s user to DB' % user)


    while True:
        status, info = utils.check_user(channel)
        if status == 0:
            if info['data'][0]['started_at'] != user.date:
                print('Отправляю уведомление')
                utils.send_message(server, '@everyone %s https://www.twitch.tv/rocksun_wow' %
                             info['data'][0]['title'])
                user.date = info['data'][0]['started_at']
                print('Уведомление отправленно \nNew time: %s' % user.date)
                session.commit()
                print(user)
            if not isThreadRun:
                thread.start_new_thread(startChatBot, (channel,))  # Нужно прочитать по поводу закрытия потока
                isThreadRun = True
                print('isThreadRun', isThreadRun)
            time.sleep(60)
        else:
            time.sleep(10)
