#!/usr/bin/env python
# -*- coding: utf-8 -*-

import file
from neighbor import Neighbor
from heuristic import Heuristic
import random
from math import exp

# Algoritmo Simulated Annealing adaptado de : https://pt.wikipedia.org/wiki/Simulated_annealing

class SimulatedAnnealing(object):

    # maxDisc -> Numero maximo de perturbacoes na temperatura
    # maxSuc -> Numero maximo de sucessos por iteracao
    # alpha -> fator de reducao da temperatura
    def __init__(self, iterate, maxDis, maxSuc, alpha, startTemp):
        self.iterate = iterate
        self.maxDis = maxDis
        self.maxSuc = maxSuc
        self.alpha = alpha
        self.startState = file.read()
        self.neighbor = Neighbor(self.startState)
        self.startTemp = startTemp

    def simulate(self):
        i = 0
        success = None
        currentState = self.startState
        t = self.startTemp

        solutions = []

        while not(success == 0) and i < self.iterate:
            j = 0
            success = 0
            while success <= self.maxSuc and j < self.maxDis:
                f1 = Heuristic(currentState).attacks()
                newState = self.neighbor.generateState()

                if Heuristic(newState).attacks() == 0:
                    solutions.append(Heuristic(newState).queensPosition())

                #print Heuristic(currentState).queensPosition() ," -> ", Heuristic(newState).queensPosition()

                f2 = Heuristic(newState).attacks()
                deltaF = f2 - f1
                if not t == 0.0:
                    if (deltaF <= 0) or (exp(-deltaF/t) > random.random()):
                        currentState = newState
                        success += 1

                j += 1
                self.neighbor = Neighbor(currentState)

            t = self.alpha * t
            i += 1

        file.write(Heuristic(currentState).queensPosition(), self.neighbor.createBoard(), url='./resource/newBoard.txt')
        print "Contagem final de sucessos : ", success
        print "Temperatura final : ", t
        print "Numero de iteracoes : " , i
        print "Posicao Inicial das ", len(self.startState), " rainhas : ", Heuristic(self.startState).queensPosition()
        print "Posicao Final das ", len(self.startState), " rainhas : ", Heuristic(currentState).queensPosition()
        print "\tNumero de rainhas atacando : ", Heuristic(currentState).colision.count(1)

        print "Solucoes encontradas: "

        aux = []
        for s in solutions:
            if s not in aux:
                aux.append(s)
                print s

        return Heuristic(currentState).colision.count(1)