# -*- coding: utf-8 -*-
from .mdpsoccer import SoccerAction
from .utils import Vector2D,dump_jsonz
import logging
##############################################################################
# SoccerStrategy
##############################################################################

class Strategy(object):
    """ Strategie : la fonction compute_strategie est interroge a chaque tour de jeu, elle doit retourner un objet
    SoccerAction
    """
    def __init__(self, name="Vide"):
        """
        :param name: nom de la strategie
        :return:
        """
        self.name = name
    def compute_strategy(self, state, id_team, id_player):
        """ Fonction a implementer pour toute strategie
        :param state: un objet SoccerState
        :param id_team: 1 ou 2
        :param id_player: numero du joueur interroge
        :return:
        """
        return SoccerAction()

    def begin_match(self, team1, team2, state):
        """  est appelee en debut de chaque match
        :param team1: nom team1
        :param team2: nom team2
        :param state: etat initial
        :return:
        """
        pass

    def begin_round(self, team1, team2, state):
        """ est appelee au debut de chaque coup d'envoi
        :param team1: nom team 1
        :param team2: nom team 2
        :param state: etat initial
        :return:
        """
        pass

    def end_round(self, team1, team2, state):
        """ est appelee a chaque but ou fin de match
        :param team1: nom team1
        :param team2: nom team2
        :param state: etat initial
        :return:
        """
        pass

    def update_round(self, team1, team2, state):
        """ est appelee a chaque tour de jeu
        :param team1: nom team 1
        :param team2: nom team 2
        :param state: etat courant
        :return:
        """
        pass

    def end_match(self, team1, team2, state):
        """ est appelee a la fin du match
        :param team1: nom team 1
        :param team2: nom team 2
        :param state: etat courant
        :return:
        """
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.__class__).split(".")[-1]+": "+ self.__str__()

class PermanentKeyboardStrategy(Strategy):
    def __init__(self,name="KBCommande",reset=False):
        super(KeyboardStrategy,self).__init__(name)
        self.dic_keys=dict()
        self.cur = None
        self.states=[]
        self.state=None
        self.idt = 1
        self.idp = 0
        self.reset = reset

    def add(self,key,strategy):
        self.dic_keys[key]=strategy
        if not self.cur:
            self.cur = key
            self.name = strategy.name

    def compute_strategy(self,state,id_team,id_player):
        self.state = state
        self.idt = id_team
        self.idp = id_player
        return self.dic_keys[self.cur].compute_strategy(state,id_team,id_player)

    def send_strategy(self,key):
        if not self.state:
            return
        if key in self.dic_keys.keys():
            self.cur=key
            self.name = self.dic_keys[self.cur].name
            self.states.append((self.state, (self.idt,self.idp,self.name)))
    def begin_match(self,team1,team2,state):
        if self.reset:
            self.states=[]

class KeyboardStrategy(Strategy):
    def __init__(self,name="KBCommande",reset=False):
        super(KeyboardStrategy,self).__init__(name)
        self.dic_keys=dict()
        self.cur = None
        self.cur_step = 0
        self.states=[]
        self.state=None
        self.idt = 1
        self.idp = 0
        self.reset = reset

    def add(self,key,strategy):
        self.dic_keys[key]=strategy
        if not self.cur:
            self.cur = key
            self.name = strategy.name

    def compute_strategy(self,state,id_team,id_player):
        self.state = state
        self.idt = id_team
        self.idp = id_player
        if self.cur is None:
            return SoccerAction()
        else:
            action = self.dic_keys[self.cur].compute_strategy(state,id_team,id_player)
            self.cur_step += 1
            if self.cur_step > 3:
                self.cur_step = 0
                self.cur = None
            return action

    def send_strategy(self,key):
        if not self.state:
            return
        if key in self.dic_keys.keys():
            self.cur=key
            self.name = self.dic_keys[self.cur].name
            self.states.append((self.state, (self.idt,self.idp,self.name)))
    def begin_match(self,team1,team2,state):
        if self.reset:
            self.states=[]


class DTreeStrategy(Strategy):
    def __init__(self,tree,dic,get_features):
        super(DTreeStrategy,self).__init__("Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.get_features = get_features
        self.logger = logging.getLogger("arbrestrategie")

    def compute_strategy(self, state, id_team, id_player):
        label = self.tree.predict([self.get_features(state,id_team,id_player)])[0]
        if label not in self.dic:
            self.logger.error("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)
