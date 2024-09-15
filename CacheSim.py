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

    def __init__(self, kc, ram):
        Memoria.__init__(self, ram.capacidade())
        self.ram = ram
        self.cache_sz = 2**kc
        self.dados = [0] * self.cache_sz
        self.bloco = -1
        self.modif = False

    def read(self, ender):
        if self.cache_hit(ender):
            print("cache hit:", ender)
        else:
            print("cache miss:", ender)
            bloco_ender = int(ender/self.cache_sz)
            if self.modif:
                # update ram
                for i in range(self.cache_sz):
                    self.ram.write(bloco_ender * self.cache_sz + i, self.dados[i])
            # update cache
            for i in range(self.cache_sz):
                self.dados[i] = self.ram.read(bloco_ender * self.cache_sz + i)
            self.bloco = bloco_ender
            self.modif = False
        return self.dados[ender % self.cache_sz]

    def write(self, ender, val):
        if self.cache_hit(ender):
            print("cache hit:", ender)
        else:
            print("cache miss:", ender)

            # complete!
            # ...

        self.dados[ender % self.cache_sz] = val
        self.modif = True

    def cache_hit(self, ender):
        bloco_ender = int(ender/self.cache_sz)
        return bloco_ender == self.bloco

try:

    io = IO()
    ram = RAM(12)
    cache = Cache(3, ram)
    cpu = CPU(cache, io)

    inicio = 0
    ram.write(inicio, 110)
    ram.write(inicio+1, 130)
    cpu.run(inicio)

except EnderecoInvalido as e:
    print("Endereco invalido:", e.ender)

