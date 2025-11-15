import random
import time
import string
import secrets
import ui

def map_print(map_count):
    x = map_count
    with open(f'{x}.map') as file:
        house = [list(i.rstrip()) for i in file]
    return house

def select_question(questions):
    question = random.choice(questions)
    questions.remove(question)
    return question

def ask_question(question):
    print(question["question"])
    for option in question["options"]:
        print(option)
    answer = input("Enter your answer (A-D): ").upper()
    return answer == question["answer"]

def question_for_hint(questions,seluc):
    global lives,xx,start
    attempts = 3
    encrypt = 0   
    start = ui.question_ui(code,start) 
    generate_hints(storage, encrypt, questions)
    if xx == True:
        xx = True 
    else:
        xx = False

def unlocking_door(lives,code,ans,house):
    global  map_count,xx,player_pos1,player_pos2,startx,starty,hints,start
    message=''
    for i in code:
        password = ord(i)
        thea = ord('a')
        message+=chr((password-thea+hints[0])%26+thea)
    count = 0
    check = 0
    while True:
        ui.door_ui()
        ui.player_ui(lives,code,hints,start,seluc)
        password = input('Input the password to unlock this door: ')
        count += 1
                    
        if count == 3:
            print('You have tried so many times ... something is pushing you back to the place you woke up!')
            house[startx][starty] = '♘'
            house[player_pos1][player_pos2] = ' '
            player_pos1,player_pos2 = startx,starty
            for map in house:
                print(''.join(map))
            ui.player_ui(lives,code,hints,start,seluc)
            break

        check = 0
        for row in house:
            if '♦' in row:
                check+=1

        if password == message:
            print('Yes!')
            time.sleep(0.5)
            print('【the door is unlocked ... 】')
            time.sleep(0.5)
            xx = True
            hints.remove(hints[0])
            map_count += 1
            if map_count == 4:
                ui.boss_anime(lives)
                break
            break

def generate_hints(storage,encrypt,questions):
    global lives,xx,code,ans
    chances = 3
    temp = 0
    while chances> 0:
        if questions == []:
            print("Congratulations! You have answered all the questions correctly.")
            break
        
        question = select_question(questions)
        is_correct = ask_question(question)
        
        if is_correct:
            print("Here's the hint ... ")
            x = random.randint(-3, 3)
            print(f'Hint: {x}')
            encrypt += x
            key = encrypt % 26

            storage.append(x)
            if len(storage) > 1:
                for i in range(len(storage)):
                    temp += storage[i]
                if len(hints) > 0:
                    hints.remove(hints[0])
                hints.append(temp)
            else:
                hints.append(storage[0])
            xx = True
            break

        if not is_correct:
            chances -= 1
            print("Try again. ")
        
        if chances == 0:
            print("I won, you lost one life")
            lives -= 1
            xx = False
            break        
        print("")
    
def all_movement():
    global lives,player_pos1,player_pos2,cules,seluc,startx,starty,xx,map_count,loser,house,ans,start,questions
    ghost, cules, seluc, room = [], [], [], []
    player_pos1, player_pos2, startx, starty, turn, lives_count, damage = 0, 0, 0, 0, 0, 0, 0
    house = map_print(map_count)
    ans = None
    traps(map_count)
    sp1, sp2 , lava = traps(map_count)
    for i, row in enumerate(house):
        for j, col in enumerate(row):
            if col == '♘':
                player_pos1,player_pos2 = i,j
                startx, starty = i,j
            elif col == '☿':
                ghost_pos1,ghost_pos2 = i,j
                ghost.append((ghost_pos1,ghost_pos2))
            elif col == '♦':
                cules.append((i,j))
                seluc.append((i,j))
            elif col == '▓':
                room.append((i,j))      
    encrypt=0
    adjacent_ghost = False
    for row in house:
        print(''.join(row))
        time.sleep(0.1)
    ui.player_ui(lives,code,hints,start,seluc)
    if map_count == 2:
        ui.map_2_opening()
    if map_count == 3:
        ui.map_3_opening()

    while True:  
        if turn == 0:
                for i,j in sp1:
                    house[i][j] = ' '
                for x1,y in sp2:
                    house[x1][y] = '◁'
                turn = 1
        elif turn == 1:
                for i,j in sp2:
                    house[i][j] = ' '
                for x1,y in sp1:
                    house[x1][y] = '▶'
                turn = 0        
        global direction
        direction = input('Which direction do you want to go?(w-a-s-d-q-p)').lower()
        if direction == 'q':
            return direction
        elif direction == 'p':
            if (player_pos1,player_pos2) in sp1 or (player_pos1,player_pos2) in sp2:
                house[player_pos1][player_pos2] = '♘'
                lives -= 1
                for row in house:
                    print(''.join(row))
                ui.player_ui(lives,code,hints,start,seluc)
            else:
                for row in house:
                    print(''.join(row))
                ui.player_ui(lives,code,hints,start,seluc)
            adjacent_ghost = False
            for q in range(len(ghost)):
                i, j = ghost[q]
                ghost_dt = random.choice(['w', 'a', 's', 'd'])
                mov_gh_x, mov_gh_y = i, j
                new_rows = {'w': mov_gh_x - 1, 'a': mov_gh_x, 's': mov_gh_x + 1, 'd': mov_gh_x}
                new_cols = {'w': mov_gh_y, 'a': mov_gh_y - 1, 's': mov_gh_y, 'd': mov_gh_y + 1}
                if ghost_dt == 'w':
                    mov_gh_x -= 1
                if ghost_dt == 'a':
                    mov_gh_y -= 1
                if ghost_dt == 's':
                    mov_gh_x += 1
                if ghost_dt == 'd':
                    mov_gh_y += 1
                if house[mov_gh_x][mov_gh_y] == ' ':
                    house[i][j] = ' '
                    house[mov_gh_x][mov_gh_y] = '☿'
                    ghost[q] = (mov_gh_x, mov_gh_y)
                    i, j = mov_gh_x, mov_gh_y
                elif house[mov_gh_x][mov_gh_y] == '♘':
                    adjacent_ghost = True
                    break
                elif house[mov_gh_x][mov_gh_y] == '☿':
                    house[i][j] = '☿'
                    house[mov_gh_x][mov_gh_y] = '☿'
                    ghost[q] = (mov_gh_x, mov_gh_y)
                    i, j = mov_gh_x, mov_gh_y               
                elif house[i][j] == '' :
                    pass
                elif house[i][j] == '◁' :
                    pass         
                elif house[i][j] == '▦' :
                    pass
                elif house[mov_gh_x][mov_gh_y] == '▕' or house[mov_gh_x][mov_gh_y] == '█' or house[mov_gh_x][mov_gh_y] == '▦':
                    pass
            if lives == 0 :
                ui.game_over_anime()
                loser = True
                break
        elif direction in ['w', 'a', 's', 'd']:
            movement_row, movement_col = player_pos1, player_pos2
            if direction == 'w': movement_row -= 1
            if direction == 'a': movement_col -= 1
            if direction == 's': movement_row += 1
            if direction == 'd': movement_col += 1
            rows = {'w': movement_row-1, 'a': movement_row, 's': movement_row+1, 'd': movement_row}
            cols = {'w': movement_col, 'a': movement_col-1, 's': movement_col, 'd': movement_col+1}
            if house[movement_row][movement_col] == ' ' or house[movement_row][movement_col] == '▒':
                    house[player_pos1][player_pos2] = ' '
                    house[movement_row][movement_col] = '♘'
                    if (player_pos1,player_pos2) in seluc: house[player_pos1][player_pos2] = '♦'
                    elif (player_pos1,player_pos2) in lava: house[player_pos1][player_pos2] = '▦'
                    player_pos1, player_pos2 = movement_row, movement_col
                    for map in house:
                        print(''.join(map)) 
                    ui.player_ui(lives,code,hints,start,seluc) 
            elif house[movement_row][movement_col] == '▶' or house[movement_row][movement_col] == '◁':
                lives -= 1
                house[player_pos1][player_pos2] = ' '
                house[movement_row][movement_col] = '♘'
                player_pos1,player_pos2 = movement_row,movement_col
                for map in house:
                        print(''.join(map)) 
                ui.player_ui(lives,code,hints,start,seluc)     
            elif house[movement_row][movement_col] == '✜':
                    i,j=random.choice(room)
                    house[i][j]=' '
                    room.remove((i,j))
                    house[movement_row][movement_col] = '♘'
                    house[player_pos1][player_pos2] = ' '
                    player_pos1,player_pos2 = movement_row,movement_col
                    for row in house:
                        print(''.join(row))
                    ui.player_ui(lives,code,hints,start,seluc)
            elif house[movement_row][movement_col] == '♦':
                    question_for_hint(questions,seluc)
                    house[player_pos1][player_pos2] = ' '
                    house[movement_row][movement_col] = '♘' 
                    if (player_pos1,player_pos2) in lava: house[player_pos1][player_pos2] = '▦' 
                    if xx == True: 
                        seluc.remove((movement_row,movement_col))
                        xx = False
                    player_pos1, player_pos2 = movement_row, movement_col    
                    for row in house:
                        print(''.join(row))
                    ui.player_ui(lives,code,hints,start,seluc)
            elif house[movement_row][movement_col] == '☿':
                lives -= 1
                for row in house:
                    print(''.join(row))
                ui.player_ui(lives, code, hints, start, seluc)
            elif house[movement_row][movement_col] == '▕':
                    unlocking_door(lives,code,ans,house)
                    if xx == True:
                        if lives < 5:
                            lives += 1
                        xx = False
                        break
            elif house[movement_row][movement_col] == '▦':
                lives -= 1
                house[player_pos1][player_pos2] = ' '
                house[movement_row][movement_col] = '♘'
                if (player_pos1,player_pos2) in lava: house[player_pos1][player_pos2] = '▦'
                player_pos1, player_pos2 = movement_row, movement_col
                for map in house:
                    print(''.join(map)) 
                ui.player_ui(lives,code,hints,start,seluc) 
            elif house[movement_row][movement_col] == '█' or house[movement_row][movement_col] == '▓':
                if house[player_pos1][player_pos2] == '▶' or house[player_pos1][player_pos2] == '◁':
                    lives -= 1
                    house[player_pos1][player_pos2] = '♘'
                    for row in house:
                        print(''.join(row))
                    ui.player_ui(lives, code, hints, start, seluc)       
                else:
                    house[player_pos1][player_pos2] = '♘'
                    for map in house:
                        print(''.join(map))
                    ui.player_ui(lives,code,hints,start,seluc)
            elif house[movement_row][movement_col] == '♜':
                ui.chating_npc_ui()
                house[movement_row][movement_col] = ' '
                for row in house:
                        print(''.join(row))
                ui.player_ui(lives,code,hints,start,seluc)
            adjacent_ghost = False
            for q in range(len(ghost)):
                i, j = ghost[q]
                ghost_dt = random.choice(['w', 'a', 's', 'd'])
                mov_gh_x, mov_gh_y = i, j
                new_rows = {'w': mov_gh_x - 1, 'a': mov_gh_x, 's': mov_gh_x + 1, 'd': mov_gh_x}
                new_cols = {'w': mov_gh_y, 'a': mov_gh_y - 1, 's': mov_gh_y, 'd': mov_gh_y + 1}
                if ghost_dt == 'w':
                    mov_gh_x -= 1
                if ghost_dt == 'a':
                    mov_gh_y -= 1
                if ghost_dt == 's':
                    mov_gh_x += 1
                if ghost_dt == 'd':
                    mov_gh_y += 1
                if house[mov_gh_x][mov_gh_y] == ' ':
                    house[i][j] = ' '
                    house[mov_gh_x][mov_gh_y] = '☿'
                    ghost[q] = (mov_gh_x, mov_gh_y)
                    i, j = mov_gh_x, mov_gh_y
                elif house[mov_gh_x][mov_gh_y] == '♘':
                    adjacent_ghost = True
                    break
                elif house[mov_gh_x][mov_gh_y] == '☿':
                    house[i][j] = ' '
                    house[mov_gh_x][mov_gh_y] = '☿'
                    ghost[q] = (mov_gh_x, mov_gh_y)
                    i, j = mov_gh_x, mov_gh_y                
                elif house[i][j] == '' :
                    pass       
                elif house[i][j] == '◁' :
                    pass         
                elif house[i][j] == '▦' :
                    pass
                elif house[mov_gh_x][mov_gh_y] == '▕' or house[mov_gh_x][mov_gh_y] == '█' or house[mov_gh_x][mov_gh_y] == '▦':
                    pass  
            lives_count = 0
            if adjacent_ghost:
                lives -= 1
                lives_count += 1
                print("you're attacked by the ghost!")
                for row in house:
                    print(''.join(row))
                ui.player_ui(lives,code,hints,start,seluc)

            if lives_count > 1:
                if lives_count == 2 :
                    lives += 1
                elif lives_count == 3 :
                    lives += 2
                elif lives_count == 4 :
                    lives += 3
                elif lives_count == 5 :
                    lives += 4

            if lives == 0 :
                ui.game_over_anime()
                loser = True
                break
        else:
            print(" Guess it is not the direction i want to go. ")           

def generate_code():
    code = ''.join(secrets.choice(string.ascii_lowercase) for i in range(5))
    return code
    
def traps(map_count):
    sp1,sp2,lava = [],[],[]
    house = map_print(map_count)
    for i, row in enumerate(house):
        for j, col in enumerate(row):
            if col == '▶':
                sp1.append((i,j))
            elif col == '◁':
                sp2.append((i,j))
            elif col == '▦':
                lava.append((i,j))
    return sp1,sp2,lava

def main():
    global code,lives,hints,storage,map_count,loser,xx,start,questions
    questions = [   
        {   "question": "The Pythagorean theorem was found by a famous philosopher called Pythagoras. Do you know where was he from?",
            "options": ["A. Greek", "B. Rome", "C. Egypt", "D. China"],
            "answer": "A"   },

        {   "question": "What is value of the gravitational constant G?",
            "options": ["A. 6.6743 x 10^-10", "B. 6.6743 x 10^-9", "C. 6.6743 x 10^-19", "D. 6.6743 x 10^-11"],
            "answer": "D"   },

        {   "question": "A and B are both holding a clock in their hands, if A travels around the globe with light speed c=3x10^8, according to special relativity, what will happen? ",
            "options":["A. Nothing happened", "B. B's clock is slower with respect to A", "C. A's clock is slower with respect to B", "D. A's clock is slower"],
            "answer": "C"   },

        {   "question": "What was the name of the first atomic bomb used in World War 2?",
            "options": ["A. Little boy", "B. Big boy", "C. Tiny boy", "D. Fat man"],
            "answer": "A"   },

        {   "question": "Where was the second atomic bomb detonated at in World War 2?",
            "options":["A. Nagasaki", "B. Hiroshima", "C. Okinawa", "D. Fukoda"],
            "answer": "A"   },

        {   "question": "When is exact date of the end of the World War 2?",
            "options":["A. 1/9/1945", "B. 2/9/1945", "C. 3/9/1945", "D. 4/9/1945"],
            "answer": "B"   },

        {   "question": "The well-known AI ChatGPT. Do you know what does 'GPT' stand for?",
            "options":["A. Generator Performance Transmitter", "B. Generation Performance Transformer", "C. Generative Pre-trained Transformer", "D. Generative Performance Transformer"],
            "answer": "C"   },

        {   "question": "Do you know the exact value of Avogadro's Constant?",
            "options":["A. 6.02 x 10^20", "B. 6.02 x 10^21", "C. 6.02 x 10^22", "D. 6.02 x 10^23"],
            "answer": "D"   },

        {   "question": "How long is human's body small intestine on average?",
            "options":["A. About 2 metres", "B. About 7 metres", "C. About 10 metres", "D. About 15 metres"],
            "answer": "B"   },

        {   "question": "When was the University of Hong Kong first established?",
            "options":["A. 1910", "B. 1911", "C. 1912", "D. 1913"],
            "answer": "B"   },

        {   "question": "How fast is the fastest human in the world?",
            "options":["A. About 30km/h", "B. About 35km/h", "C. About 40km/h", "D. About 45km/h"],
            "answer": "D"   },

        {   "question": "Do you know where was the famous scientist Galileo born?",
            "options":["A. Italy", "B. England", "C. Germany", "D. Sweden"],
            "answer": "A"   },

        {   "question": "Which of the following is not one of the 8 planets of our solar system?",
            "options":["A. Pluto", "B. Venus", "C. Uranus", "D. Neptune"],
            "answer": "A"   },

        {   "question": "Which of the following is NOT a programming language?",
            "options":["A. Python", "B. Java", "C. HTML", "D. MySQL"],
            "answer": "C"   },

        {   "question": "What is the chemical symbol for gold?",
            "options":["A. Au", "B. Ag", "C. Fe", "D. Hg"],
            "answer": "A"   },

        {   "question": "What is the largest ocean on Earth?",
            "options":["A. Atlantic Ocean", "B. Indian Ocean", "C. Arctic Ocean", "D. Pacific Ocean"],
            "answer": "D"   },

        {   "question": "Which planet is known as the 'Morning Star' or 'Evening Star'?",
            "options":["A. Mars", "B. Venus", "C. Mercury", "D. Uranus"],
            "answer": "B"   },

        {   "question": "How long did the revolution of the France last?",
            "options":["A. 1 year", "B. 2 years", "C. 5 years", "D. 10 years"],
            "answer": "D"   },

        {   "question": "How old was the famous French military commander Napoleon when he died?",
            "options":["A. 21", "B. 31", "C. 41", "D. 51"],
            "answer": "D"   },

        {   "question": "Do you know where was the famous musician Mozart born in?",
            "options":["A. Italy", "B. Autria", "C. France", "D. Germany"],
            "answer": "B"   },
        
        {   "question": "Log3 x Log6=?",
            "options":["A. 18", "B. 9", "C. 0.5", "D. 0.37"],
            "answer": "D"   },

        {   "question":"There are 2 identical coins,A and B.They are of different weight, A is heavier than B.If they are dropped from the same height, which of them will reach the ground faster?",
            "options":["A. B is faster", "B. A is faster", "C. No difference", "D. Depends on the type of the coins"],
            "answer": "C"   },
        
        {   "question":" Is the gravity on Earth or on the Moon greater?",
            "options":["A. Gravity on Earth is greater", "B. Gravity on Moon is greater", "C. the Moon has no gravity", "D. Depends on different positions"],
            "answer": "A"   },
        
        {   "question":" How long does it take for the Moon to revolve around Earth?",
            "options":["A. About 1 day", "B. About half a month", "C. About 1 month", "D. About a week"],
            "answer": "C"   },
        
        {   "question":" Which of the following is NOT one of the classical music period?",
            "options":["A. Baroque", "B. Early Romantic", "C. Renaissance", "D. Modern"],
            "answer": "D"   },
        
        {   "question":" Which of the following is NOT a stringed instrument?",
            "options":["A. Guitar", "B. Bass", "C. Violin", "D. Trumpet"],
            "answer": "D"   },
        
        {   "question":" Which of the following is not one of the 4 ancient civilizations?",
            "options":["A. Egypt", "B. China", "C. Atlantis", "D. Mesopotamia"],
            "answer": "C"   },

        {   "question":" Which of the following is not a Europe country",
            "options":["A. Sweden", "B. Italy", "C. Greek", "D. Argentina"],
            "answer": "D"   },
        
        {   "question":" How long does it take for the Earth to complete a full rotation among its axis?",
            "options":["A. 25hours", "B. 25 hours and 26 minutes", "C. 25 hours and 39 minutes", "D. 23 hours and 56 minutes"],
            "answer": "D"   },
        
        {   "question":" Which of the following is not a Vector?",
            "options":["A. Velocity", "B. Force", "C. Acceleration", "D. Angular speed"],
            "answer": "D"   },
        
        {   "question":" What will increase with an object is falling?",
            "options":["A. Gravity", "B. Momentum", "C. Energy", "D. Inertia"],
            "answer": "B"   },
        
        {   "question":" Which of the following computer component is mainly responsible for accelerating graphics rendering?",
            "options":["A. CPU", "B. GPU", "C. Hard disk", "D. Ram disk"],
            "answer": "B"   },
        
        {   "question":" Which of the following mainly contributes for the rigidity of a wood?",
            "options":["A. Phloem", "B. Xylem", "C. Water", "D. Minerals"],
            "answer": "B"   },
        
        {   "question":" sin45=?",
            "options":["A. 1", "B. 0.5", "C. √2/2", "D. √2"],
            "answer": "C"   },
        
        {   "question":" Which of the following is not a computer brand?",
            "options":["A. Unity", "B. Apple", "C. Window", "D. ASUS"],
            "answer": "A"   },
        
        {   "question":" Which of the following is not one of the past US presidents?",
            "options":["A. Obama", "B. Donald Trump", "C. George W. Bush", "D. Jill Tracy"],
            "answer": "D"   },
        
        {   "question":" Which of the following is the molecular formular of nitrogen oxide?",
            "options":["A. N2", "B. NO", "C. NO2", "D. N2O2"],
            "answer": "B"   },

        {   "question":" How many percent of human body are composed of water?",
            "options":["A. 50%", "B. 60%", "C. 70%", "D. 80%"],
            "answer": "C"   },
        
        {   "question":" Which of the following is NOT one of the 4 oceans?",
            "options":["A. Pacific Ocean", "B. Atlantic Ocean", "C. Indian Ocean", "D. Mediterranean"],
            "answer": "D"   }
    ]
    lives = 5
    hints = []
    storage = []
    start = 0
    xx = False
    password = 0
    map_count = 1

    loser = False
    ui.game_start_ui()
    while True:
        start_game = input()
        if start_game == '':
            break
        else:
            print('Invalid input, please try again!') 
    ui.game_start_anime()
    ui.start_story_anime()
    ui.game_start_anime()
    ui.story_ui()
    while map_count != 4:
        code = generate_code()
        map_print(map_count)
        all_movement()     
        if direction == 'q':
            ui.game_over_anime()
            break
        if loser == True:
            break
    

main()
