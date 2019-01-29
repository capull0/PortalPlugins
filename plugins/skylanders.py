import yaml
import os
import sys
#from hexdump import hexdump

config_path = sys.path[0] + '/skylanders.yaml'

images = {}
config = {}


def read_config():
    global config
    with open(config_path, 'r') as ymlfile:
        config = yaml.load(ymlfile)


def send_data(ddata):
    global images, config
    data = list(ddata)
    if len(data) > 3:
        cmd = data[0]
        sid = ord(data[1])
        block = ord(data[2])

        if cmd == 'Q' and sid >= 0x10:
            if block == 0:
                print "SID: %02X" % (sid)
                skylander_id = "%02X-%02X-%02X-%02X" % (ord(data[3]), ord(data[4]), ord(data[5]), ord(data[6]))
                read_config()
                if skylander_id in config['mapping']:
                    print "Skylander-ID: {} -> {}".format(skylander_id, config['mapping'][skylander_id])
                    images[sid] = {'name': config['mapping'][skylander_id], 'new': False, 'id': skylander_id, 'data': read_image(config['mapping'][skylander_id])}
                else:
                    print "Skylander-ID: {} -> new".format(skylander_id)
                    images[sid] = {'name': skylander_id, 'new': True, 'id': skylander_id, 'data': read_image('initial')}

            if sid in images:
                if images[sid]['new']:
                    block_data = []
                    for d in ddata[3:19]:
                        block_data.append(ord(d))
                    write_block(sid, block, block_data)
                else:
                    a = 2
                    for i in range(block * 0x10, block * 0x10 + 0x10):
                        a += 1
                        try:
                            data[a] = images[sid]['data'][i]
                        except KeyError:
                            print "Keyerror - SID: %02X COUNT: %d" % (sid, i)

    return ''.join(data)


def receive_data(ddata):
    data = list(ddata)
    if len(data) > 8:
        cmd = data[8]
        if cmd == 'W' and len(data) > 10:
            sid = ord(data[9])
            block = ord(data[10])
            if sid and block and sid in images and not images[sid]['new']:
                block_data = []
                for i in ddata[11:27]:
                    block_data.append(ord(i))
                write_block(sid, block, block_data)
                new_data = data[0:9]
                new_data[8] = 'S'
                return ''.join(new_data)

    return ''.join(data)


def read_image(image):
    if image == 'initial':
        return list("\x00" * 1024)

    path = "{}/{}.bin".format(config['path'], image)
    with open(path, 'rb') as file:
        data = file.read()

    return list(data)

def write_block(s_id, block, block_data):
    global images

    if s_id in images:
        path = "{}/{}.bin".format(config['path'], images[s_id]['name'])
        if images[s_id]['new']:
            if not os.path.exists("{}/new".format(config['path'])):
                os.makedirs("{}/new".format(config['path']))
            path = "{}/new/{}.bin".format(config['path'], images[s_id]['name'])
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    for i in range(1024):
                        f.write(chr(0))

        with open(path, 'r+b') as f:
            f.seek(block * 0x10)
            offset = block * 0x10
            for i in block_data:
                images[s_id]['data'][offset] = chr(i)
                offset += 1
                f.write(chr(i))
