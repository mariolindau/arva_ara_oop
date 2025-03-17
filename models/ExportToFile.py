import datetime

from models.Database import Database


class ExportToFile:
    def __init__(self, model):
        """Seadistame mudeli ja võtame andmebaasist vajalikud andmed."""
        self.model = model
        db = Database()  # Loo Database objekt
        self.data = db.for_export()  # Võta andmed andmebaasist
        self.columns = ['name', 'quess', 'steps', 'game_length']  # Veergude nimed

    @staticmethod
    def format_game_time(timestamp):
        """Vormindab mängu aja kujule PP.KK.AAAA HH:MM:SS."""
        return timestamp.strftime('%d.%m.%Y %H:%M:%S')

    @staticmethod
    def format_game_length(seconds):
        """Vormindab sekundid kujule 00:00:00."""
        return str(datetime.timedelta(seconds=seconds))

    def export(self):
        """Eksportib andmed .txt faili."""
        if not self.data:
            print("Andmebaasist ei saadud ühtegi kirjet.")
            return

        db = Database()
        file_name = f"{db.db_name}.txt"  # Faili nimi sama mis andmebaas

        with open(file_name, 'w') as file:
            # Kirjutab veergude nimed
            file.write(';'.join(self.columns) + '\n')

            # Kirjutab andmed faili
            for row in self.data:
                game_length = self.format_game_length(row[3])  # Vormindatud mängu pikkus
                game_time = self.format_game_time(
                    datetime.datetime.fromtimestamp(row[3], datetime.timezone.utc))  # Vormindatud mängu aeg

                # Kirjutame andmed faili
                file.write(f"{row[0]};{row[1]};{row[2]};{game_length};{game_time}\n")

            print(f"Edetabel eksporditi faili '{file_name}'.")