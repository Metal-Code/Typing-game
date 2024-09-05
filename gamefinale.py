import copy
import pygame                                                                                                                # type: ignore
import random

pygame.init()

from nltk.corpus import words                                                                                                # type: ignore
#using the natural language toolkit to import words

wordlist = words.words()
len_indexes = []
length = 1
end = False

#sorting the words according to their length
wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))

#setting up the screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('T I N K T Y P E')
surface = pygame.Surface((WIDTH, HEIGHT))
timer = pygame.time.Clock()
fps = 60

#fonts to be used
header_font = pygame.font.Font('assets/fonts/square.ttf', 50)
pause_font = pygame.font.Font('assets/fonts/1up.ttf', 38)
banner_font = pygame.font.Font('assets/fonts/1up.ttf', 28)
ins_font = pygame.font.Font('assets/fonts/1up.ttf', 18)
font = pygame.font.Font('assets/fonts/AldotheApache.ttf', 48)

# music and sounds
pygame.mixer.init()
pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound('assets/sounds/click.mp3')
right = pygame.mixer.Sound('assets/sounds/right.mp3')
wrong = pygame.mixer.Sound('assets/sounds/wrong.mp3')
butt = pygame.mixer.Sound('assets/sounds/button.mp3')
butt.set_volume(1)
click.set_volume(0.5)
right.set_volume(0.3)
wrong.set_volume(0.3)
loselife = pygame.mixer.Sound('assets/sounds/loselife.mp3')
gameover = pygame.mixer.Sound('assets/sounds/gameover.mp3')
loselife.set_volume(1)
gameover.set_volume(1)

# game variables
global high_score
global score 
score = 0
level = 1
lives = 5
word_objects = []
file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()
pz = True 
new_level = True
submit = ''
active_string = ''
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
           'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# 2 letter, 3 letter, 4 letter, 5 letter, 6 letter, etc
choices = [False, False, False, False, False, False, False]



class Word:
    def __init__(self, text, speed, y_pos, x_pos):
        self.text = text
        self.speed = speed
        self.y_pos = y_pos
        self.x_pos = x_pos

    #generates a word
    def draw(self):
        color = 'white'
        screen.blit(font.render(self.text, True, 'white'), (self.x_pos, self.y_pos))
        act_len = len(active_string)
        if active_string == self.text[:act_len]:
            screen.blit(font.render(active_string, True, 'orange'), (self.x_pos, self.y_pos))
  
    #makes the word move from right to left by changing its x-position by a little
    def update(self):
        self.x_pos -= self.speed

class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    #draws a circular button 
    #it turns pink when we hover the mouse and red after clicking.
    def draw(self):
        cir = pygame.draw.circle(self.surf, (0,0,0), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
                click.play()
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))


def draw_screen():
    # screen outlines for main game window and 'header' section
    pygame.draw.rect(screen, (0,0,0), [0, HEIGHT - 100, WIDTH, 100], 0)
    pygame.draw.rect(screen, 'white', [0, 0, WIDTH, HEIGHT], 5)
    pygame.draw.line(screen, 'white', (0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.line(screen, 'white', (250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white', (700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.rect(screen, 'black', [0, 0, WIDTH, HEIGHT], 2)
    
    # text for showing current level, player's current string, high score and pause options
    screen.blit(header_font.render(f'Level: {level}', True, 'white'), (20, HEIGHT - 75))
    screen.blit(header_font.render(f'"{active_string}"', True, 'cyan'), (270, HEIGHT - 75))
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    
    # draw lives, score, and high score on top of screen
    screen.blit(banner_font.render(f'Score: {score}', True, 'white'), (265, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True, 'green'), (540, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True, 'red'), (30, 10))
    return pause_btn.clicked

#screen to be displayed when the game is paused
def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT))
    
    resume_btn = Button(160, 200, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(410, 200, 'X', False, surface)
    quit_btn.draw()
    surface.blit(header_font.render('- - - - - T I N K T Y P E - - - - -', True, 'orange'), (110, 110))
    surface.blit(header_font.render('PLAY!', True, 'green'), (210, 175))
    surface.blit(header_font.render('QUIT', True, 'red'), (450, 175))
    surface.blit(header_font.render(' Active Letter Lengths:', True, 'blue'), (110, 250))

    #buttons to choose the range of word lengths from
    for i in range(len(choices)):
        btn = Button(160 + (i * 80), 350, str(i + 2), False, surface)
        btn.draw() 
        
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
                
        #all the selected lengths will have a green circle around the button, indicating that it has been selected.
        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i * 80), 350), 35, 5)
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked

#generates a level with the number of words as the level number
def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
        
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i + 1]))
     
    #generating words       
    for i in range(level):
        speed = random.randint(2, 3)
        y_pos = random.randint(50 + (i * vertical_spacing), (i + 1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, y_pos, x_pos)
        word_objs.append(new_word)
        
    return word_objs


#checks if the submitted word is the same as that of the word on the screen
def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) / 3)
            scor += int(points)
            word_objects.remove(wrd)
            right.play()
    return scor


#updates high score if the current score is greater than existing high score
def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

#screen to be displayed when the game ends.
def draw_end():
    global score
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT))
    
    if(score<high_score):
        #resume and quit button
        resume_btn = Button(140, 200, '>', False, surface)
        resume_btn.draw()
        quit_btn = Button(500, 200, 'X', False, surface)
        quit_btn.draw()
    else:
        resume_btn = Button(140, 265, '>', False, surface)
        resume_btn.draw()
        quit_btn = Button(500, 265, 'X', False, surface)
        quit_btn.draw()
    
    
    #if new high score is made, let the user know
    if(score<high_score):          
        surface.blit(header_font.render(f'GAME OVER!!      Score: {score}', True, 'yellow'), (110, 110))
        surface.blit(header_font.render('PLAY AGAIN!', True, 'green'), (180, 175))
        surface.blit(header_font.render('QUIT!', True, 'red'), (550, 175))
        surface.blit(header_font.render('- - - - - T I N K T Y P E - - - - -', True, 'orange'), (110, 250))
    else:
        surface.blit(header_font.render(f'  - !!!!CONGRATULATIONS!!!! -', True, 'cyan'), (110, 110))
        surface.blit(header_font.render(f'  -> New High Score : {score} <-', True, 'cyan'), (110, 175))
        surface.blit(header_font.render('PLAY AGAIN!', True, 'green'), (180, 240))
        surface.blit(header_font.render('QUIT!', True, 'red'), (550, 240))
        surface.blit(header_font.render('- - - - - T I N K T Y P E - - - - -', True, 'orange'), (110, 315))
    screen.blit(surface, (0, 0))
    
    
    return resume_btn.clicked, quit_btn.clicked

#to show an instructions button which shows instructions on clicking
class InstructionsButton:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        pygame.draw.rect(self.surf, (0, 0, 0), [self.x_pos, self.y_pos, 200, 50], 0)
        if self.x_pos <= pygame.mouse.get_pos()[0] <= self.x_pos + 200 and self.y_pos <= pygame.mouse.get_pos()[1] <= self.y_pos + 50:
            pygame.draw.rect(self.surf, (190,89,135), [self.x_pos, self.y_pos, 200, 50], 0)
            self.clicked = True
        else:
            pygame.draw.rect(self.surf, (0,0,0), [self.x_pos, self.y_pos, 200, 50], 0)
        pygame.draw.rect(self.surf, 'white', [self.x_pos, self.y_pos, 200, 50], 3)
        self.surf.blit(ins_font.render(self.text, True, 'white'), (self.x_pos + 15, self.y_pos + 10))


#the screen will show instructions if the button is clicked
def draw_instructions_screen():
    surface = pygame.Surface((WIDTH, HEIGHT))
    go_back_btn = Button(300, 500, '<', False, surface)
    go_back_btn.draw()
    
    surface.blit(banner_font.render('GO BACK', True, 'orange'), (350, 480))
    surface.blit(header_font.render('INSTRUCTIONS', True, 'orange'), (250, 100))
    
    instructions_text = [
        "> You get 5 chances in life before it ends.",
        "> Type the words as they appear on the screen.",
        "> Press SPACE or ENTER to submit your typed word.",
        "> Submit your word before it escapes the screen!",
        "> Press ESC to pause the game and adjust settings.",
        "> Choose the word lengths to type in the game.",
        "> Spell and Score!"
    ]
    
    y_offset = 200
    for line in instructions_text:
        surface.blit(ins_font.render(line, True, 'white'), (30, y_offset))
        y_offset += 30
    screen.blit(surface, (0, 0))
    return go_back_btn.clicked

#main code to be run
run = True
show_instructions = False
while run:
    screen.fill('black')
    timer.tick(fps)
    pause_butt = draw_screen()

    
    #if game is paused
    if pz: 
        #if game is over
        if end: 
            resume_butt, quit_butt = draw_end()  
            if resume_butt:           
                  
                  pygame.mixer.music.load('assets/sounds/music.mp3')
                  pygame.mixer.music.set_volume(0.2)
                  pygame.mixer.music.play(-1) 
                  pz = True                  
                  score = 0
                  end = False
        else:
            resume_butt, changes, quit_butt = draw_pause()
        
            
            #if instructions button is pressed
            if show_instructions: 
                if draw_instructions_screen():
                 show_instructions = False
                 
            else:
                 instructions_btn = InstructionsButton(500, 20, 'instructions', False, screen)
                 instructions_btn.draw()
                 #if instructions button is pressed
                 if instructions_btn.clicked: 
                   show_instructions = True
         
        #if resume button is pressed           
        if resume_butt: 
                  pz = False
                  
         
        #if user quits game         
        if quit_butt: 
            check_high_score()
            run = False
        
    #if a level is finished and game is not paused        
    if new_level and not pz: 
        word_objects = generate_level()
        new_level = False
        
    else:
        for w in word_objects:
            w.draw()
            if not pz:
                w.update()
                
            # if word is out of the screen, decrease a life. 
            # < -200 is put such that longer words can fully disappear from the screen
            if w.x_pos < -200: 
                word_objects.remove(w)
                lives -= 1
                loselife.play()
             
    #if all the words for that level are typed, increase the level.           
    if len(word_objects) <= 0 and not pz: 
        level += 1
        new_level = True

    #if the submitted string is not blank, check answer
    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()

    #if game is quit, check high score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False
        
        #if keyboard is used (keydown)
        if event.type == pygame.KEYDOWN:
            #if not paused
            if not pz: 
                #if the letter is typed, then add it to the active string 
                if event.unicode.lower() in letters:
                    active_string += event.unicode
                    #play click sound on each letter typed
                    click.play()
                    
                #if backspace is pressed, a letter is deleted from active string
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                    
                #word is submitted on pressing enter or space
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            
            #user can pause and unpause the game using escape key        
            if event.key == pygame.K_ESCAPE:
                if pz:
                    pz = False
                else:
                    pz = True
                    
        if event.type == pygame.MOUSEBUTTONUP and pz:
            if event.button == 1:
                choices = changes

    if pause_butt:
        pz = True
    
    #game ends when lives are less than zero
    if lives < 0:
        pygame.mixer.music.stop()
        gameover.play()
        pz = True
        end = True
        level = 1
        lives = 5
        word_objects = []
        new_level = True
        check_high_score()
        

    pygame.display.flip()
pygame.quit()

