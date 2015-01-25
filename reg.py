import pygame

class Register(pygame.sprite.Sprite):
    def __init__(self,name,color,value='\\0'):
        pygame.sprite.Sprite.__init__(self)
        
        self.name=name
        self.color=color
        self.value=value
    
    def move(self, source):
        try:
            self.value=source.value
        except AttributeError:
            self.value= source
            
    def add(self, source):
        try:
            self.value +=source.value
        except AttributeError:
            self.value += int(source)
    
    def sub(self, source):
        try:
            self.value -=source.value
        except AttributeError:
            self.value -= int(source)
    
    def __add__(self, source):
        return self.value+source
    
    def __sub__(self,source):
        return self.value-source
    
    def __str__(self):
        return "value: "+str(self.value)

class special(pygame.sprite.Sprite):
    def __init__(self,name,value=0,pos=1):
        pygame.sprite.Sprite.__init__(self)
        self.name=name
        self.pos=pos
        self.value=value
    def sub(self, source):
        try:
            self.value -=source.value
            self.pos+=(source.value)/4
        except AttributeError:
            self.value -= int(source)
            self.pos+=int(source)/4
    def add(self,source):
        try:
            self.value +=source.value
            self.pos-=(source.value)/4
        except:
            self.value += int(source)
            self.pos-=int(source)/4
    
    def __add__(self, source):
        return self.value+source
    
    def __sub__(self,source):
        return self.value-source
    
    def move(self, source):
        try:
            self.value=source.value
            self.pos=source.pos
        except AttributeError:
            self.value= source