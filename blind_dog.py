from agents import *

class BlindDog(Agent):
    location = 1
    
    def movedown(self):
        self.location += 1
        
    def eat(self, thing):
        '''returns True upon success or False otherwise'''
        if isinstance(thing, Food):
            print("Dog: Ate food at {}.".format(self.location))
            return True
        return False
    
    def drink(self, thing):
        ''' returns True upon success or False otherwise'''
        if isinstance(thing, Water):
            print("Dog: Drank water at {}.".format(self.location))
            return True
        return False
        
def program(percepts):
    '''Returns an action based on it's percepts'''
    for p in percepts:
        if isinstance(p, Food):
            return 'eat'
        elif isinstance(p, Water):
            return 'drink'
    return 'move down'

class Food(Thing):
    pass

class Water(Thing):
    pass

class Park(Environment):
    def percept(self, agent):
        '''prints & return a list of things that are in our agent's location'''
        things = self.list_things_at(agent.location)
        print(things)
        return things
    
    def execute_action(self, agent, action):
        '''changes the state of the environment based on what the agent does.'''
        if action == "move down":
            agent.movedown()
        elif action == "eat":
            items = self.list_things_at(agent.location, tclass=Food)
            if len(items) != 0:
                if agent.eat(items[0]): #Have the dog pick eat the first item
                    self.delete_thing(items[0]) #Delete it from the Park after.
        elif action == "drink":
            items = self.list_things_at(agent.location, tclass=Water)
            if len(items) != 0:
                if agent.drink(items[0]): #Have the dog drink the first item
                    self.delete_thing(items[0]) #Delete it from the Park after.
                    
    def is_done(self):
        '''By default, we're done when we can't find a live agent, 
        but to prevent killing our cute dog, we will or it with when there is no more food or water'''
        no_edibles = not any(isinstance(thing, Food) or isinstance(thing, Water) for thing in self.things)
        dead_agents = not any(agent.is_alive() for agent in self.agents)
        return dead_agents or no_edibles
