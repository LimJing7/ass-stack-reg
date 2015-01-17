import pygame

class Register(pygame.sprite.Sprite):
    def __init__(self,name,color,value='\\0'):
        pygame.sprite.Sprite.__init__(self)
        
        self.name=name
        self.color=color
        self.value=value
    
    def move(self, source):
        if isinstance(source,str):
            self.value= source
        else:
            self.value=source.value
    