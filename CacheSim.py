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
        print("ender" , ender)
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
        #quantidade de linhas = 128 palavras(0->127)
        #tamanho de cada linha = 16 palavras
        # Reservar duas colunas extras, a primeira para a tag e
        self.dados = []
        for i in range(int(2**self.totalcapac/2**self.tamcacheline)):
            linha = [0,0] # Cache por mapeamento direto tem uma tabela, o for cria uma tabela com o tamanho das cache lines          # + 2 colunas extras, uma pra TAG e outra para o bit que indica se foi modificada ou não.
            for a in range(2**tam_cache_line+2):  
                linha.append(0)
            self.dados.append(linha)
        print(self.dados)
        self.bloco = -1
        self.modif = False
        

    def read(self, ender):
        if self.cache_hit(ender):
            print("cache hit:", ender)
        else:
            print("cache miss:", ender)
            bloco_ender = int(ender/self.totalcapac)
            if self.modif:
                # update ram
                for i in range(self.totalcapac):
                    self.ram.write(bloco_ender * self.totalcapac + i, self.dados[i])
            # update cache
            for i in range(self.totalcapac):
                self.dados[i] = self.ram.read(bloco_ender * self.totalcapac + i)
            self.bloco = bloco_ender
            self.modif = False
        return self.dados[ender % self.totalcapac]

    def write(self, ender, val):
        if self.cache_hit(ender):
            print("cache hit:", ender)
        else:
            print("cache miss:", ender)

            # complete!
            # ...

        self.dados[ender % self.totalcapac] = val
        self.modif = True

    def cache_hit(self, ender):
        bloco_ender = int(ender/self.totalcapac)
        return bloco_ender == self.bloco

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

