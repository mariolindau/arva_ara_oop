from random import randint
from turtledemo.nim import NimModel

from models.Database import Database
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
        # self.stopwatch.start() #Käivitab stopperi

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
        self.stopwatch.start() # käivitab kellaaeja
        while not self.game_over:
            self.ask()

        # Näita mängu aega
        print(f'Mäng kestis {self.stopwatch.format_time()}')
        self.what_next() # Mis on järgmiseks :) Nime küsimine ja kirje lisamine
        self.show_menu() # Näita mängu menüüd

    def what_next(self):
        """Küsime mängija nime ja lisame info andmebaasi"""
        name = self.ask_name()
        db = Database() # Loo andmebaasi objekt
        db.add_record(name, self.steps, self.pc_nr, self.cheater, self.stopwatch.seconds)

    @staticmethod #Praegu tohib staatiliseks teha, aga teatud juhtudel ei tohi seda teha
    def ask_name():
        """Küsib nime ja tagastab korrekte mängija nime"""
        name = input("Kuidas on mängija nimi? ")
        if not name.strip():
            name = 'Teadmata'
        return name.strip()

    def show_menu(self):
        """Näita mängu menüüd"""
        print('1 - Mängima')
        print('2 - Edetabel')
        print('3 - Välju programmist')
        user_input = int(input('Sisesta number [1, 2 või 3]: '))
        if 1 <= user_input <= 3:
            if user_input == 1:
                self.reset_game() # Algseadista mäng
                self.lets_play()  #lähme mängima
            elif user_input == 2:
                self.show_leaderboard()
                self.show_menu()
            elif user_input == 3:
                print('Bye, bye :)')
                exit() #Igasuguse skripti töö lõppeb
        else:
            self.show_menu()

    @staticmethod
    def show_leaderboard():
        db = Database()
        data = db.read_records()
        if data:
            for record in data:
                print(record) # name -> record[1]

    def show_leaderboard(self):
        """Näita edetabelit"""
        db = Database()
        data = db.read_records()
        if data:
         for record in data:
            print(record) #name -> record[1]
def show_no_cheater(self):
    """Edetabel ausatele mängijatele"""
    db = Database()
    data = db.no_cheater()
    if data:
        #Vormindus funktsioon veerule
        formatters = {
            'Mängu aeg': self.format_time,}

        print() #Tühirida enne edetabelit
        #self.print_table(data, formatters)
        self.manual_table(data)
        print() #Tühirida peale tabelit


    @staticmethod
    def format_time(self):
        hours = self.seconds // 3600
        minutes = (self.seconds % 3600) // 60
        seconds = self.seconds % 60
        # return "%02d:%02d:%02d" % (hours, minutes, seconds)
        return f'{hours:02}:{minutes:02}:{seconds:02}'

    @staticmethod
    def print_table(data, formatters=None):
        def format_cell(value, width, column_name=None, target_column=None):
            # Rakenda vormindus kui veerule on määratud formatter
            if formatters and column_name in formatters:
                value = formatters[column_name](value)
            value = str(value)

            # Lühenda ainult sihtveeru väärtusi (Nimi maksimaalselt 15 märki)
            if column_name == target_column and len(value) > width:
                value = value[:width]

            # Numbrid paremale tekstid vasakule
            return value.rjust(width) if value.isdigit() else value.ljust(width)

        headers =['Nimi', 'Number', 'Sammud', 'Mängu aeg'] # veergude nimed
        column_widths = [15, 7, 7, 9] # Veergude laiused

        # Loob tabeli päise
        header_row = ' | '.join(f'{header:<{width}}'
                                for header, width in zip(headers, column_widths))
        print(header_row)  # Väljastab tabeli päise
        print('-' * len(header_row))  # Printib eraldusjoone päise alla

        for row in data:  # Väljastab iga mängija kohta info
            print(' | '.join(
                format_cell(item, width, column_name=headers, target_column='Nimi')
                for item, width, column in zip(row, column_widths, headers)))

    def manual_table(self, data):
        print('Nimi             Number Sammud Mängu aeg')
        for row in data:
            print(f'{row[0] [:15]:<16} {row[1]:>6} {row[2]:>6} {self.format_time(row[3]):>9}')
