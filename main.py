import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import reg
import stack


REGSIZE=[120,40]
WIDTH=300
HEIGHT=600

red=(244,67,54)
blue=(33,150,243)
green=(76,175,80)
yellow=(255,235,59)
BGCOLOR=(84,110,122)
STACKCOLOR=(238,238,238)
STACKDIVCOLOR=(189,189,189)


def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('Stack/Register')
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BGCOLOR)
    
    #create registers
    eax=reg.Register('eax',red)
    ebx=reg.Register('ebx',blue)
    ecx=reg.Register('ecx',green)
    edx=reg.Register('edx',yellow)
    registers=[eax,ebx,ecx,edx]
    
    #create stack
    stacky=stack.Stack()
    
    #modify register and push to stack
    eax.move('0x123C45A6')
    stacky.push(eax)
    ebx.move(eax)
    stacky.push(ebx)
    
    
    #draw registers
    i=0
    for register in registers:
        pygame.draw.rect(background, register.color , [0,i*80+40,REGSIZE[0],REGSIZE[1]])
        i+=1
    i=0    
    if pygame.font:
        #none 24
        #calibri 18
        font = pygame.font.Font(None, 24)
        for register in registers:
            regName = font.render(register.name, 1, (255, 255, 255))
            regNamepos = regName.get_rect()
            regNamepos.centerx=REGSIZE[0]/2
            regNamepos.centery=i*80+20
            background.blit(regName, regNamepos)
            regValue = font.render(register.value, 1, (0, 0, 0))
            regValuepos = regValue.get_rect()
            regValuepos.centerx=REGSIZE[0]/2
            regValuepos.centery=i*80+60
            background.blit(regValue, regValuepos)
            i+=1
    
    
    
    #draw stack
    def drawst():
        for i in range(stacky.number+1):
            pygame.draw.rect(background, STACKCOLOR,[WIDTH-REGSIZE[0],HEIGHT-(i+1)*REGSIZE[1],REGSIZE[0],REGSIZE[1]])
            stackValue= font.render(stacky.value[i],1,(0,0,0))
            stackValuepos= stackValue.get_rect()
            stackValuepos.centerx=WIDTH-REGSIZE[0]/2
            stackValuepos.centery=HEIGHT-(i+1)*REGSIZE[1]+REGSIZE[1]/2
            background.blit(stackValue,stackValuepos)
            if i!=0:
                pygame.draw.line(background, STACKDIVCOLOR,[WIDTH-REGSIZE[0],HEIGHT-i*REGSIZE[1]],[WIDTH,HEIGHT-i*REGSIZE[1]],1)
            
    
    clock = pygame.time.Clock()
    going = True
    
    ck=0
    
    while going:
        clock.tick(60)
        ck+=1

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    going = False
 
        
        #allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        #allsprites.draw(screen)
        drawst()
        pygame.display.flip()

    pygame.quit()
    
if __name__=="__main__":
    main()