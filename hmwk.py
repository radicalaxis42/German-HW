import pygame
import string
import random
pygame.init()
colour = (104, 136, 190)
white = (255, 255, 255)
black = (0, 0, 0)
alphabet_list = list(string.ascii_lowercase)
with open('verbs.txt',encoding='utf-8') as f:
    contents = f.readlines()
    f.close()
contents += contents
while "\n" in contents:
    del contents[contents.index("\n")]
window = pygame.display.set_mode([800,800])
window.fill(colour)
myfont = pygame.font.SysFont('Comic Sans MS', 30)
tenses = ['Infinitive', 'Present', 'Imperfect', 'Past Participle', 'English']
letters = ['*', 'ä', 'β']
for i in range(5):
    pygame.draw.rect(window, white, (40, 40 + 120*i, 500, 70))
    pygame.draw.rect(window, black, (30, 30 + 120*i, 520, 90), 20, 20)
    textsurface = myfont.render(tenses[i], False, (0, 0, 0, 128))
    window.blit(textsurface,(50, 50 + 120*i))
    for j in range(3):
        pygame.draw.rect(window, white, (575 + 75*j, 40 + 120*i, 40, 70))
        pygame.draw.rect(window, black, (565 + 75*j, 40 + 120*i, 60, 80), 10, 10)
        textsurface = myfont.render(letters[j], False, (0, 0, 0))
        window.blit(textsurface, (585 + 75*j, 50 + 120*i))
pygame.draw.rect(window, white, (40, 650, 500, 70))
pygame.draw.rect(window, black, (30, 640, 520, 90), 20, 20)
textsurface = myfont.render('Check', False, (0, 0, 0, 128))
window.blit(textsurface, (50, 660))
typing = [False, False, False, False, False]
string_list = ['', '', '', '', '']
running = True
playing = False
word = contents[random.randint(0, len(contents) - 1)]
correct = True
reading = False
won = False

def segment(word):
    t = False
    words_list = ['', '', '', '', '']
    string_bool = [True, False, False, False, False]
    for letter in range(len(word)):
        if t:
            if word[letter] != "\t":
                ind = string_bool.index(True)
                string_bool[ind] = False
                if ind < 4:
                    string_bool[ind + 1] = True
                t = False
            else:
                continue
        if word[letter] != "\t" and word[letter] != "\n":
            words_list[string_bool.index(True)] += word[letter]
        else:
            t = True
    for i in range(5):
        n = 0
        while words_list[i][n] == ' ':
            n += 1
        words_list[i].replace(' ', '', n)
    return words_list


def write(i, letter):
    pygame.draw.rect(window, white, (40, 40 + 120*i, 500, 70))
    pygame.draw.rect(window, black, (30, 30 + 120*i, 520, 90), 20, 20)
    textsurface = myfont.render(string_list[i] + letter, False, (0, 0, 0, 128))
    window.blit(textsurface,(50, 50 + 120*i))
    string_list[i] += letter


segmented = segment(word)
given = random.randint(0, len(segmented) - 1)
write(given, segmented[given])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            mx, my = pygame.mouse.get_pos()
            if len(contents) == 0:
                running = False
                won = True
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(5):
                        if i != given and not reading:
                            if my > 40 + 120*i and my < 110 + 120*i:
                                if mx > 40 and mx < 500:
                                    for j in range(5):
                                        typing[j] = False
                                        if string_list[j] == '' and j != i:
                                            textsurface = myfont.render(tenses[j], False, (0, 0, 0, 128))
                                            window.blit(textsurface, (50, 50 + 120 * j))
                                    pygame.draw.rect(window, white, (40, 40 + 120 * i, 500, 70))
                                    pygame.draw.rect(window, black, (30, 30 + 120 * i, 520, 90), 20, 20)
                                    string_list[i] = ''
                                    typing[i] = True
                                elif mx > 575 and mx < 615:
                                    write(i, '*')
                                elif mx > 650 and mx < 690:
                                    write(i, 'ä')
                                elif mx > 725 and mx < 765:
                                    write(i, 'β')
                    if my > 650 and my < 720:
                        if mx > 40 and mx < 500:
                                if not reading:
                                    for i in range(5):
                                        if string_list[i] != segmented[i]:
                                            correct = False
                                    if correct:
                                        del contents[contents.index(word)]
                                        if len(contents) != 0:
                                            word = contents[random.randint(0, len(contents) - 1)]
                                            segmented = segment(word)
                                            for i in range(5):
                                                string_list[i] = ''
                                                pygame.draw.rect(window, white, (40, 40 + 120 * i, 500, 70))
                                                pygame.draw.rect(window, black, (30, 30 + 120 * i, 520, 90), 20, 20)
                                                textsurface = myfont.render(tenses[i], False, (0, 0, 0, 128))
                                                window.blit(textsurface, (50, 50 + 120 * i))
                                            given = random.randint(0, len(segmented) - 1)
                                            string_list[given] = ''
                                            write(given, segmented[given])
                                    else:
                                        contents.append(word)
                                        word = contents[random.randint(0, len(contents) - 1)]
                                        for j in range(len(segmented)):
                                            string_list[j] = ''
                                            write(j, segmented[j])
                                        pygame.draw.rect(window, white, (40, 650, 500, 70))
                                        pygame.draw.rect(window, black, (30, 640, 520, 90), 20, 20)
                                        textsurface = myfont.render('Continue', False, (0, 0, 0, 128))
                                        window.blit(textsurface, (50, 660))
                                        reading = True
                                else:
                                    word = contents[random.randint(0, len(contents) - 1)]
                                    segmented = segment(word)
                                    given = random.randint(0, len(segmented) - 1)
                                    for i in range(len(string_list)):
                                        string_list[i] = ''
                                        write(i, tenses[i])
                                    string_list[given] = ''
                                    write(given, segmented[given])
                                    pygame.draw.rect(window, white, (40, 650, 500, 70))
                                    pygame.draw.rect(window, black, (30, 640, 520, 90), 20, 20)
                                    textsurface = myfont.render('Check', False, (0, 0, 0, 128))
                                    window.blit(textsurface, (50, 660))
                                    reading = False
                elif event.type == pygame.KEYDOWN:
                    for i in range(5):
                        if i != given:
                            if typing[i]:
                                try:
                                    if event.key == pygame.K_SPACE:
                                        write(i, ' ')
                                    else:
                                        write(i, alphabet_list[event.key - 97])
                                except IndexError:
                                    pass
    pygame.display.flip()

if won:
    pygame.init()
    window = pygame.display.set_mode([800,800])
    window.fill(colour)
    pygame.draw.rect(window, white, (200, 400, 400, 70))
    pygame.draw.rect(window, black, (190, 390, 420, 90), 20, 20)
    textsurface = myfont.render('You win!', False, (0, 0, 0, 128))
    window.blit(textsurface, (340, 410))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()