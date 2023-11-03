import random
from itertools import permutations
import numpy as np
import gym

# world height
WORLD_HEIGHT = 5

# world width
WORLD_WIDTH = 5

# possible actions
ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3


class Maze_game():
    def __init__(self):
        self.player_n = 2

        self.done = False
        self.turn = 0
        self.a_start_index = 0
        self.d_start_index = 4
        self.goal_index = 24
        self.start_index = [self.a_start_index,self.d_start_index]
        self.current_index= self.start_index
        self.pre_index = self.start_index
        self.mazeIndexList = []
        for i in range(0, WORLD_HEIGHT):
            for j in range(0, WORLD_WIDTH):
                self.mazeIndexList.append(WORLD_WIDTH * i + j)

        self.locationValidActions = {}
        for i in self.mazeIndexList:
            self.locationValidActions[i] = []

        for i in range(0, WORLD_HEIGHT):
            for j in range(0, WORLD_WIDTH):
                gridIndexNumber = WORLD_WIDTH * i + j
                if i != WORLD_HEIGHT - 1:
                    self.locationValidActions[gridIndexNumber].append(ACTION_DOWN)
                if i != 0:
                    self.locationValidActions[gridIndexNumber].append(ACTION_UP)
                if j != 0:
                    self.locationValidActions[gridIndexNumber].append(ACTION_LEFT)
                if j != WORLD_WIDTH - 1:
                    self.locationValidActions[gridIndexNumber].append(ACTION_RIGHT)
                #set blocked grid
                #(0,3)
                if i==0 and j==2:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_RIGHT)
                if i==1 and j==3:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_UP)
                if i==0 and j==4:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_LEFT)
                #(1,1)
                if i==1 and j==0:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_RIGHT)
                if i==0 and j==1:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_DOWN)
                if i==1 and j==2:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_LEFT)
                if i==2 and j==1:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_UP)
                #(2,4)
                if i==2 and j==3:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_RIGHT)
                if i==1 and j==4:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_DOWN)
                if i==3 and j==4:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_UP)
                #(3,2）
                if i==3 and j==1:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_RIGHT)
                if i==3 and j==3:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_LEFT)
                if i==2 and j==2:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_DOWN)
                if i==4 and j==2:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_UP)
                #(4,0)
                if i==3 and j==0:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_DOWN)
                if i==4 and j==1:
                    self.locationValidActions[gridIndexNumber].remove(ACTION_LEFT)

        self.actions = [ACTION_UP, ACTION_DOWN, ACTION_LEFT, ACTION_RIGHT]

    def init_index(self):
        return self.start_index

    def init_validactions(self):
        return self.locationValidActions

    def step(self, joint_action):

        self.turn +=1
        joint_reward = {}
        is_done = False
        action = [0,0]

        print('index: ',self.current_index)

        if joint_action[0]==ACTION_UP:#attacker up
            if ACTION_UP in self.locationValidActions[self.current_index[0]]:#if can move
                self.current_index[0] = self.current_index[0] - 5
            else:
                action[0] = -1

        if joint_action[0]==ACTION_DOWN:#attacker down
            if ACTION_DOWN in self.locationValidActions[self.current_index[0]]:
                self.current_index[0] = self.current_index[0] + 5
            else:
                action[0] = -1

        if joint_action[0]==ACTION_LEFT:#attacker left
            if ACTION_LEFT in self.locationValidActions[self.current_index[0]]:
                self.current_index[0] = self.current_index[0] - 1
            else:
                action[0] = -1

        if joint_action[0]==ACTION_RIGHT:#attacker right
            if ACTION_RIGHT in self.locationValidActions[self.current_index[0]]:
                self.current_index[0] = self.current_index[0] + 1
            else:
                action[0] = -1


        #defender
        if joint_action[1]==ACTION_UP:#defender up
            if ACTION_UP in self.locationValidActions[self.current_index[1]]:
                self.current_index[1] = self.current_index[1] - 5
            else:
                action[1] = -1

        if joint_action[1]==ACTION_DOWN:#defender down
            if ACTION_DOWN in self.locationValidActions[self.current_index[1]]:
                self.current_index[1] = self.current_index[1] + 5
            else:
                action[1] = -1

        if joint_action[1]==ACTION_LEFT:#defender left
            if ACTION_LEFT in self.locationValidActions[self.current_index[1]]:
                self.current_index[1] = self.current_index[1] - 1
            else:
                action[1] = -1

        if joint_action[1]==ACTION_RIGHT:#defender right
            if ACTION_RIGHT in self.locationValidActions[self.current_index[1]]:
                self.current_index[1] = self.current_index[1] + 1
            else:
                action[1] = -1


        if self.current_index[0] == 24:
            joint_reward[0] = 50
            joint_reward[1] = -100
            is_done = True
            #self.reset()

        elif self.current_index[0] == self.current_index[1]:
            joint_reward[0] = -100
            joint_reward[1] = 50
            is_done = True
            #self.reset()

        elif (self.pre_index[0] == self.pre_index[1] + 5 and (joint_action[0] == 0 and joint_action[1] == 1)) or \
                (self.pre_index[0] == self.pre_index[1] - 5 and (joint_action[0] == 1 and joint_action[1] == 0)) or \
                (self.pre_index[0] == self.pre_index[1] + 1 and (joint_action[0] == 2 and joint_action[1] == 3) and self.pre_index[1]//5 == self.pre_index[0]//5) or \
                (self.pre_index[0] == self.pre_index[1] - 1 and (joint_action[0] == 3 and joint_action[1] == 2) and self.pre_index[1]//5 == self.pre_index[0]//5):
            joint_reward[0] = -100
            joint_reward[1] = 50
            is_done = True

        else:
            if action[0] == -1 or action[1] == -1:
                print('joint_action: ',joint_action)
                if action[0] == -1 and action[1] == -1:
                    joint_reward[0] = -5
                    joint_reward[1] = -2
                if action[0] == -1 and action[1] != -1:
                    joint_reward[0] = -5
                    joint_reward[1] = -1
                if action[0] != -1 and action[1] == -1:
                    joint_reward[0] = -1
                    joint_reward[1] = -2
            else:
                joint_reward[0] = -1
                joint_reward[1] = -1


        obs = self.current_index
        self.pre_index = self.current_index

        print("obs:",obs)

        return obs, joint_reward, is_done

    def reset(self):

        self.turn=0
        self.current_index = [0,4]
        self.pre_index = [0,4]
        self.done = False

        return self.current_index



