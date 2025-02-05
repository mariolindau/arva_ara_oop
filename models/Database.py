import sqlite3
import os
from datetime import datetime

class Database:
    db_name = 'game_leaderboard_v2.db' #Andmebaasi nimi
    table = 'ranking' #Vajalik tabeli nimi

    def __init__(self):
        """Konstruktor"""
        self.conn = None #Ühendus
        self.cursor = None
        self.connect() #loo ühendus

    def connect(self):
        """loo ühendus andmebaasiga"""
        try:
            if self.conn:
                self.conn.close()
                print("Varasem ühendus andmebaasiga suleti.")

            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Uus ühendus andmebaasiga {self.db_name} loodud.')
        except sqlite3.error as error:
            print(f'Tõrge andmebaasi ühenduse loomisel: {error}')
            self.conn = None
            self.cursor = None

    def close_connection(self):
        """Sulgeb andmebaasiga ühenduse"""
        try:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
        except Exception as error:
            print(f'Tõrge ühenduse loomisel: {error}')

    def read_records(self):
        """loeb andmebaasist kogu edetabeli"""
        if self.cursor:
            try:
                sql = f'SELECT * FROM {self.table};'
                self.cursor.execute(sql)
                data = self.cursor.fetchall() #kõik kirjed muutujasse data
                return data #Tagastab kõik kirjed
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return [] #Tagastab tühja listi
            finally:
                self.close_connection()
        else:
            print('Ühenduse andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

    def add_record(self, name, steps, pc_nr, cheater, seconds):
        """Lisab mängija andmed tabelisse"""
        if self.cursor:
            try:
                sql = f'INSERT INTO {self.table} (name, steps, quess, cheater, game_length) Values (?, ?, ?, ?, ?);'
                self.cursor.execute(sql, (name, steps, pc_nr, cheater, seconds))
                self.conn.commit()
                print('Mängija on lisatud tabelisse')
            except sqlite3.Error as error:
                print(f'Mängija lisamisel tekkis tõrge: {error}')
            finally:
                self.close_connection()
        else:
            print('Ühendus puudub! Palun loo ühendus andmebaasiga.')

    def no_cheater(self):
        """loeb andmebaasist kogu edetabeli"""
        if self.cursor:
            try:
                sql = f'SELECT name, quess, steps, game_length FROM {self.table} WHERE cheater=? ORDER BY steps ASC, name ASC LIMIT 10;'
                self.cursor.execute(sql, (0,))
                data = self.cursor.fetchall()  # kõik kirjed muutujasse data
                return data  # Tagastab kõik kirjed
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return []  # Tagastab tühja listi
            finally:
                self.close_connection()

        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

    def for_export(self):
        """Loeb kogu edetabeli ja tagastab kõik kirjed sorteerituna."""
        if self.cursor:
            try:
                sql = f'SELECT * FROM {self.table} ORDER BY steps ASC, game_length ASC, name ASC;'
                self.cursor.execute(sql)
                data = self.cursor.fetchall() # Kõik kirjed muutujasse data
                return data # Tagastab kõik kirjed
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return [] # Tagastab tühja listi
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

class ExportToFile:
    def __init__(self, model):
        """Algatab eksportimise, võttes mudelilt andmed"""
        self.model = model
        self.data = self.model.db.for_export() #Saadakse andmed andmebaasist meetodiga

    def format_time(self, seconds):
        """Formatib sekundi arvu inimlikuks ajaks (00:00:00)."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f'{hours:02}:{minutes:02}:{seconds:02}'

    def format_date(self, timestamp):
        """Formatib sekundite arvu kuupäeva ja kellaaja formaati (PP.KK.AAAA HH:MM:SS)."""
        return timestamp.strftime('%d/%m/%Y %H:%M:%S')

    def export(self):
        """Ekspordib andmed tekstifaili."""
        if self.data:
            # Andmebaasi veergude päis (muu struktuur ei ole dünaamiline)
            headers = ["id", "name", "steps", "quess", "cheater", "game_length", "date_time"]

            #Faili loomine
            filename = Database.db_name # Faili nimi on sama mis on andmebaasi nimi
            with open(filename, 'w') as file:
                # Kirjutame faili päise
                file.write(";".join(headers) + "\n")
                for record in self.data: # Kirjutame iga mängija andmed faili
                    name, quess, steps, game_length, cheater, date_time = record

                    # Mängu aeg formateerimine
                    game_length_formatted = self.format_time(game_length)
                    # Kuupäev formateerimine
                    date_time_formatted = self.format_date(date_time)

                    # Kirjutame ühe mängija andmed faili
                    file.write(f"{name};{quess};{steps};{cheater};{game_length_formatted};{date_time_formatted}\n")
                print(f"Edetabel on edukalt eksporditud faili {filename}")
        else:
                print("Tabel on tühi või pole andmeid eksportimiseks.")

class Model:
    def __init__(self):
        """Konstruktor"""
        self.reset_game()
        self.export_to_file = ExportToFile(self)  # Eksportimise objekt

    def show_leaderboard(self):
        """Näita edetabelit ja ekspordi andmed faili"""
        db = Database()
        data = db.read_records()
        if data:
            for record in data:
                print(record)
        self.export_to_file.export()  # Ekspordi andmed faili

