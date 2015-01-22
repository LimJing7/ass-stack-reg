import pygame


class Stack(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.value=["\\0"]
    def push(self, source):
        self.value.append(source.value)
    def pop(self, destination):
        destination.value=self.value.pop()