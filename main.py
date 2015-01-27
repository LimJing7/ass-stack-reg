import os, pygame
from pygame.locals import *
from pygame.compat import geterror
import reg
import stack


REGSIZE=[120,40]
WIDTH=700
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
    stacky=stack.Stack(4096)
    
    #create ebp and esp
    ebp=reg.special('ebp',stacky.start)
    esp=reg.special('esp',stacky.start)
    
    #set font
    if pygame.font:
        #none 24
        #calibri 18
        font = pygame.font.SysFont('calibri', 18)
    
    #draw registers
    def draw_reg():
        i=0
        for register in registers:
            pygame.draw.rect(background, register.color , [0,i*80+40,REGSIZE[0],REGSIZE[1]])
            i+=1
        i=0
        for register in registers:
            regName = font.render(register.name, 1, (255, 255, 255))
            regNamepos = regName.get_rect()
            regNamepos.centerx=REGSIZE[0]/2
            regNamepos.centery=i*80+20
            background.blit(regName, regNamepos)
            try:
                regValue = font.render(hex(register.value), 1, (0, 0, 0))
            except:
                regValue = font.render(register.value, 1, (0, 0, 0))
            regValuepos = regValue.get_rect()
            regValuepos.centerx=REGSIZE[0]/2
            regValuepos.centery=i*80+60
            background.blit(regValue, regValuepos)
            i+=1
    
    
    
    #draw stack
    def drawst():
        for i in range(len(stacky.value)):
            pygame.draw.rect(background, STACKCOLOR,[WIDTH-REGSIZE[0],HEIGHT-(i+1)*REGSIZE[1],REGSIZE[0],REGSIZE[1]])
            try:
                stackValue= font.render(hex(stacky.value[i]),1,(0,0,0))
            except:
                stackValue= font.render(str(stacky.value[i]),1,(0,0,0))
            stackValuepos= stackValue.get_rect()
            stackValuepos.centerx=WIDTH-REGSIZE[0]/2
            stackValuepos.centery=HEIGHT-(i+1)*REGSIZE[1]+REGSIZE[1]/2
            background.blit(stackValue,stackValuepos)
            if i!=0:
                pygame.draw.line(background, STACKDIVCOLOR,[WIDTH-REGSIZE[0],HEIGHT-i*REGSIZE[1]],[WIDTH,HEIGHT-i*REGSIZE[1]],1)
            
    def draw_word(wordy):
        pygame.draw.rect(background,(0,0,0),[WIDTH/2-(1.5)*REGSIZE[0],HEIGHT/2-REGSIZE[1]/2,3*REGSIZE[0],REGSIZE[1]])
        word=font.render(wordy, 1, (255,255,255))
        wordpos=word.get_rect()
        wordpos.centerx=WIDTH/2
        wordpos.centery=HEIGHT/2
        background.blit(word,wordpos)
    
    def draw_ebp_esp():
        ebpw=font.render('ebp',1,(255,255,255))
        ebppos=ebpw.get_rect()
        ebppos.centerx=WIDTH-REGSIZE[0]*1.5
        ebppos.centery=HEIGHT-((stacky.start-ebp.value)/4+1)*REGSIZE[1]+REGSIZE[1]/2
        background.blit(ebpw,ebppos)
        espw=font.render('esp',1,(255,255,255))
        esppos=espw.get_rect()
        esppos.centerx=WIDTH-REGSIZE[0]*2.5
        esppos.centery=HEIGHT-((stacky.start-esp.value)/4+1)*REGSIZE[1]+REGSIZE[1]/2
        background.blit(espw,esppos)
    
    
    #draw buttons
    pygame.draw.rect(background,(205,220,57),[0,HEIGHT-REGSIZE[1],REGSIZE[0],REGSIZE[1]]) #button for typing
    typew=font.render('type',1,(0,0,0))
    typepos=typew.get_rect()
    typepos.centerx=REGSIZE[0]/2
    typepos.centery=HEIGHT-(REGSIZE[1]/2)
    background.blit(typew,typepos)
    #pygame.draw.rect(background,(255,255,0),[500,100,REGSIZE[0],REGSIZE[1]])
    
    clock = pygame.time.Clock()
    going = True
    typing = False
    input=''
    
    ck=0
    
    while going:
        clock.tick(60)
        ck+=1
           
        #Handle Input Events
        if typing:
            draw_word(input)
            for event in pygame.event.get():
                if event.type==QUIT:
                    going = False
                elif event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        typing =False
                        pygame.draw.rect(background,BGCOLOR,[WIDTH/2-(1.5)*REGSIZE[0],HEIGHT/2-REGSIZE[1]/2,3*REGSIZE[0],REGSIZE[1]])
                    elif event.key==K_BACKSPACE:
                        input=input[:-1]
                    elif event.key==K_RETURN:
                        a=input.split()
                        try:
                            if a[0]=='push':
                                stacky.push(eval(a[1]))
                            elif a[0]=='pop':
                                stacky.pop(eval(a[1]))
                            elif a[0]=='mov':
                                if a[2][0]=='[' and a[2][-1]==']':
                                    if len(a[2])==3:
                                        eval(a[1]).move(stacky.value[(stacky.start-eval(a[2][1:4]).value)/4])
                                    else:
                                        eval(a[1]).move(stacky.value[(stacky.start-eval(str(eval(a[2][1:4]).value)+a[2][4:-1]))/4])
                                else:
                                    try:
                                        eval(a[1]).move(eval(a[2]))
                                    except TypeError:
                                        eval(a[1]).move(a[2])
                            elif a[0]=='add':
                                try: #if it is a register
                                    eval(a[1]).add(eval(a[2]))
                                except TypeError:
                                    eval(a[1]).add(a[2])
                            elif a[0]=='sub':
                                try:
                                    eval(a[1]).sub(eval(a[2]))
                                except TypeError:
                                    eval(a[1]).sub(a[2])
                            elif a[0]=='xor':
                                if a[1]==a[2]:
                                    eval(a[1]).xor()
                        except Exception as e:
                            print e
                        input=''
                    else:
                        input+=event.unicode
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        going = False
                    elif event.key==K_t:
                        typing=True
                elif event.type == MOUSEBUTTONDOWN and event.button==1:
                    a,b=pygame.mouse.get_pos()
                    if 0<a<0+REGSIZE[0] and HEIGHT-REGSIZE[1]<b<HEIGHT:
                        typing=True
                        input=''
        
        
        
        #allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        #allsprites.draw(screen)
        
        #draw stack location
        pygame.draw.rect(background,BGCOLOR,[WIDTH-3*REGSIZE[0],0,REGSIZE[0]*3,HEIGHT])
        drawst()
        
        #draw ebp and esp
        draw_ebp_esp()
        
        draw_reg()
        pygame.display.flip()

    pygame.quit()
    
if __name__=="__main__":
    main()