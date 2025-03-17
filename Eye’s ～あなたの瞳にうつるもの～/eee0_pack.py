import os
import struct

game = 'Eye’s ～あなたの瞳にうつるもの～'
file = 'eee0.dat'
xor = 0x00


def 解包(p1, file):
    f = open(file, 'rb')
    fl = f.read()
    info = fl[0:4]
    cont = 0
    for i in range(len(info) - 1, -1, -1):
        t = info[i]
        t = t
        if i != 0:
            cont = cont + t * 16 ** (2 * i)
        else:
            cont = cont + t
    print('文件数：', cont)
    for i in range(cont):
        x = 8 + i * 8
        y = 8 + i * 8 + 8
        info = fl[x + 4:x + 8]
        cont1 = 0
        filename = (8 - len(str(i))) * '0' + str(i) + '.png'
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filesize = cont1
        # print(filesize)
        # exit()
        info = fl[x + 0:x + 4]
        cont1 = 0
        for j in range(len(info) - 1, -1, -1):
            t = info[j]
            t = t
            if j != 0:
                cont1 = cont1 + t * 16 ** (2 * j)
            else:
                cont1 = cont1 + t
        filepos = cont1
        print(hex(filepos))
        # exit(1)
        print(filename)
        # print(hex(filesize))
        # print(hex(filepos))
        # print()
        f1 = open(p1 + filename, 'wb')
        dec = fl[filepos:filesize + filepos]
        for i in dec:
            t = i ^ xor
            bt = struct.pack('B', t)
            f1.write(bt)
            # t = 0xfe - i
            # if t < 0:
            #     bt = struct.pack('B', i)
            #     f1.write(bt)
            # else:
            #     bt = struct.pack('B', t)
            #     f1.write(bt)
        # f1.write(fl[filesize:filesize + filepos])
        f1.close()
    f.close()


p1 = './img_temp\\'
p2 = './img_new\\'
if not os.path.exists(p1):
    os.mkdir(p1)
if not os.path.exists(p2):
    os.mkdir(p2)
解包(p1, file)
# exit(1)
files = os.listdir(p2)
fw = open('' + file.replace('dat', 'cn_'), 'wb')
l1 = len(files) * [0]
i = 0
z = len(os.listdir(p2))  # 计算文件数
z = hex(z).replace('0x', '')
if len(z) % 2 != 0:
    z = '0' + z
z = bytes.fromhex(z)
zc = 4 - len(z)
z = b'\x00' * zc + z
for i in range(3, -1, -1):  # 写入计算文件数
    t = struct.pack('B', z[i])
    fw.write(t)
fw.write(b'\xff' * 4)
st = len(files) * 8 + 8 + 4
stats = 0
l1[0] = st
for file in files:
    if i == 0:
        l1[i] = st + stats
    else:
        l1[i] = l1[i - 1] + stats
    i = i + 1
    stats = os.stat(p2 + file).st_size
i = 0
for file in files:
    bt = 8 * [b'\x00']
    b0 = file
    j = 0
    z = hex(l1[i]).replace('0x', '')
    if len(z) % 2 != 0:
        z = '0' + z
    z = bytes.fromhex(z)
    zc = 4 - len(z)
    z = b'\x00' * zc + z
    j = len(z) - 1
    for i1 in range(0, 4):  # 位置
        t = struct.pack('B', z[j] ^ 0)
        bt[i1] = t
        j = j - 1
    stats = os.stat(p2 + file).st_size
    z = hex(stats).replace('0x', '')
    if len(z) % 2 != 0:
        z = '0' + z
    z = bytes.fromhex(z)
    zc = 4 - len(z)
    z = b'\x00' * zc + z
    j = len(z) - 1
    for i1 in range(4, 8):  # 大小
        t = struct.pack('B', z[j] ^ 0)
        bt[i1] = t
        j = j - 1
    for k in bt:
        fw.write(k)
    i = i + 1
    # exit()
fw.write(b'\x00' * 4)
for file in files:
    print(file)
    f = open(p2 + file, 'rb')
    stats = os.stat(p2 + file).st_size
    b = f.read()
    if xor != 0:
        for i in b:
            j = i ^ xor
            bt = struct.pack('B', j)
            fw.write(bt)
    else:
        fw.write(b)
    f.close()
fw.close()
files = os.listdir(p1)
# for i in files:
#     os.remove(p1 + i)
