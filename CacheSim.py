import math

class IO: # Implementado pelo professor
    def output(self, s):
        print(s, end='')

    def input(self, prompt):
        return input(prompt)

class EnderecoInvalido(Exception): # Implementado pelo professor
    def __init__(self, ender):
        self.ender = ender

class Memoria:
    def __init__(self, tam):
        self.tamanho = tam

    def capacidade(self):
        return self.tamanho

    def verifica_endereco(self, ender):
        if (ender < 0) or (ender >= self.tamanho):
            raise EnderecoInvalido(ender)


class RAM(Memoria):
    # Capacidade da RAM = 4096 = 2**12

    def __init__(self, k):
        Memoria.__init__(self, 2**k)
        self.memoria = [0] * self.tamanho

    def read(self, ender):
        self.verifica_endereco(ender)
        return self.memoria[ender]

    def write(self, ender, val):
        self.verifica_endereco(ender)
        self.memoria[ender] = val


class CPU: # Implementado pelo professor
    def __init__(self, mem, io):
        self.mem = mem
        self.io = io
        self.PC = 0                    # program counter
        self.A = self.B = self.C = 0   # registradores auxiliares

    def run(self, ender):
        self.PC = ender
        # lê "instrução" no endereço PC
        self.A = self.mem.read(self.PC)
        self.PC += 1
        self.B = self.mem.read(self.PC)
        self.PC += 1

        self.C = 1
        while self.A <= self.B:
            self.mem.write(self.A, self.C)
            self.io.output(f"{self.A} -> {self.C}\n")
            self.C += 1
            self.A += 1


class Cache(Memoria):

    def __init__(self, total_cache, tam_cache_line, ram):
        Memoria.__init__(self, ram.capacidade())
        self.ram = ram
        self.totalcapac = total_cache
        self.tamcacheline = tam_cache_line
        #palavra = número inteiro
        #quantidade de linhas = 8 palavras(0->7)
        #tamanho de cada linha = 16 palavras
        self.dados = []
        for i in range(int(2**self.totalcapac/2**self.tamcacheline)):
            linha = [-1,0]     
            for a in range(2**tam_cache_line):  
                linha.append(0)
            self.dados.append(linha)
        self.bloco = -1
        self.modif = False
        

    def read(self, ender):
        w,r,t = self.pegarinfo(ender)
        if self.cache_hit(ender):                                                                                                                                              
            print("cache hit em um read no endereço:", ender)
        else:
            print("cache miss em um read no endereço:", ender)
            inforam=[0,0]
            inforam[0]=(int(ender/2**self.totalcapac))
            inforam[1]=0
            for i in range(0,2**self.tamcacheline,1):
                inforam.append(self.ram.memoria[r*2**self.tamcacheline+i])
            if self.dados[r][1] == 1:
                self.ram.memoria[t**self.totalcapac+r*2**self.tamcacheline+w] = self.dados[r][w]
            self.dados[r] = inforam
        return self.dados[r][w+2]

    def write(self, ender, val):
        w,r,t = self.pegarinfo(ender)
        if self.cache_hit(ender):
            print("cache hit em um write no endereço:", ender)
        else:
            print("cache miss em um write no endereço:", ender)
            inforam=[0,0]
            inforam[0]=(ender//2**self.totalcapac)
            inforam[1]=0
            for i in range(0,2**self.tamcacheline,1):
                inforam.append(self.ram.memoria[r*2**self.tamcacheline+i])
            if self.dados[r][1] == 1:
                for i in range(0,16,1):
                    print([r][0])
                    self.ram.memoria[self.dados[r][0]*2**self.totalcapac+r*2**self.tamcacheline+i] = self.dados[r][i+2]                  
            
            self.dados[r] = inforam
        self.dados[r][w+2] = val
        self.dados[r][1] = 1

        

    def cache_hit(self, ender):
    
        w,r,t =self.pegarinfo(ender)
        if self.dados[r][0] == t:
            return True
        else:
            return False

    def pegarinfo(self,ender):
        def repeat_ones(x):
            if x < 1: raise ValueError("The input must be a positive integer.")
            binary_str = '1' * int(x)
            return int(binary_str, 2)
        x = ender
        w = x & repeat_ones(self.tamcacheline)
        r = (x >> self.tamcacheline) & repeat_ones(self.totalcapac-self.tamcacheline)
        t = x >> (self.tamcacheline + int(self.totalcapac-self.tamcacheline))
        return w,r,t
    
try:
    io = IO()
    ram = RAM(12)   # 4K de RAM (2**12)
    cache = Cache(7, 4, ram) # total cache = 128 (2**7), cacheline = 16 (2**4)
    cpu = CPU(cache, io)

    inicio = 0
    ram.write(inicio, 110)
    ram.write(inicio+1, 130)
    cpu.run(inicio)
except EnderecoInvalido as e:
    print("Endereco inválido:", e.ender, file=sys.stderr)

