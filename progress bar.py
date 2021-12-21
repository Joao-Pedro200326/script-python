class Barra:
    def __init__(self, tam_max, n=40):
        self.tam_max = tam_max
        self.tam_b = 0
        self.tam = 0
        self.n = n
        self.car = '#'
        self.acar = '-'

        #print(f'|{self.acar*n}|', end='', flush=True)

    def update(self, plus):
        self.tam += plus
        x = int((self.tam/self.tam_max)*self.n)
        if self.tam_b != x:
            self.tam_b = x
        data = f'|{self.car*self.tam_b}{self.acar*(self.n-self.tam_b)}|{self.tam}/{self.tam_max} {int((self.tam/self.tam_max)*100)}%'
        print('\b'*len(data) + data, end='', flush=True)

        if self.tam == self.tam_max:
            print()

    def update_thr(self, plus):
        r = ''
        self.tam += plus
        x = int((self.tam/self.tam_max)*self.n)
        if self.tam_b != x:
            self.tam_b = x
        data = f'|{self.car*self.tam_b}{self.acar*(self.n-self.tam_b)}|{self.tam}/{self.tam_max} {int((self.tam/self.tam_max)*100)}%'
        r += data

        if self.tam == self.tam_max:
            r += '\n'
        return r


if __name__ == '__main__':
    from time import sleep
    from threading import Thread, Lock
    lock = Lock()
    buffer = {}
    
    def titulo(text, n=50, n_enter=2):
        n -= len(text)//2
        if len(text) % 2 == 1:
            return f'{"-"*n}{text}{"-"*(n-1)}' + '\n'
        return f'{"-"*n}{text}{"-"*n}' + '\n'

    def abc(name):
        global buffer, lock
        m = 1000
        b = Barra(m)
        for i in range(m):
            with lock:
                buffer[f'{name}'] = b.update_thr(1)
                # print(b.update(1))
            sleep(0.01)
        del buffer[f'{name}']

    def pbuffer():
        global buffer, lock
        import os
        cl = 'clear'
        if 0 != os.system(cl):
            cl = 'cls'
        while 1:
            os.system(cl)
            with lock:
                for key in buffer.keys():
                    print(
                        titulo(key, int(len(buffer[key])/2)) + buffer[key] + '\n', end='')

    z = Thread(target=abc, args=['t 1'])
    y = Thread(target=abc, args=['t2'])
    Thread(target=pbuffer, daemon=True).start()
    z.start()
    sleep(3)
    y.start()
