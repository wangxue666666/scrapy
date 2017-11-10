from pydispatch import dispatcher


def get_singal():
    print('get the singal')


dispatcher.connect(get_singal,signal='123')
dispatcher.send(signal='123')
