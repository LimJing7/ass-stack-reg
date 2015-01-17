import pygame


class Stack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.number=0
        self.value=["\\0"]
    def push(self, source):
        self.number+=1
        self.value.append(source.value)
    def pop(self, destination):
        destination.value=self.value[self.number]
        self.number-=1
        