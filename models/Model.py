from random import randint

from models.Stopwatch import Stopwatch


class Model:
    #Defineeri klassi muutujad
    pc_nr = randint(1,100) #Juhuslik number
    steps = 0 #Sammude arv
    game_over = False # Mäng ei ole läbi
    cheater = False # Mängija ei ole petja
    stopwatch = Stopwatch() #loome stopper objekti

    def __init__(self):
        """Konstruktor"""
        self.reset_game()

    def reset_game(self):
        """Teeb uue mängu"""
        self.pc_nr = randint(1,100) #juhuslik number
        self.steps = 0 #Sammude arv
        self.game_over = False #Mäng ei ole läbi
        self.cheater = False #Mängija ei ole petja
        self.stopwatch.reset() #nullib stopperi
        self.stopwatch.start() #Käivitab stopperi

    def ask(self):
        """Küsib numbrit ja kontrollib"""
        user_nr = int(input(f"Siseta number:")) # Küsi kasutajalt numbrit
        self.steps += 1 #Sammude arv kasvab ühe võrra

        if user_nr == 1000: #tagauks
            self.cheater = True #Sa oled petja
            self.game_over = True #Mäng sai läbi
            self.stopwatch.stop() #Peata aeg
            print(f'Leidsid mu nõrga koha. Õige number oli {self.pc_nr}.')
        elif user_nr > self.pc_nr:
            print("Väiksem")
        elif user_nr < self.pc_nr:
            print('Suurem')
        elif user_nr == self.pc_nr:
            self.game_over = True
            self.stopwatch.stop()
            print(f'Leidsid õige numbri {self.steps} sammuga.')

    def lets_play(self):
        """Mängime mängu - avalik meetod"""
        while not self.game_over:
            self.ask()

        # Näita mängu aega
        print(f'Mäng kestis {self.stopwatch.format_time()}')