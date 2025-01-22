import math

class DiamentowaBukmacherska:
    """
    Główna klasa biblioteki Diamentowa Bukmacherska.
    """

    @staticmethod
    def calculate_goals(avg_scored, avg_conceded):
        """
        Oblicza przewidywaną liczbę bramek na podstawie średnich.

        :param avg_scored: Średnia liczba bramek strzelonych.
        :param avg_conceded: Średnia liczba bramek straconych.
        :return: Przewidywana liczba bramek.
        """
        return avg_scored * avg_conceded

    @staticmethod
    def poisson_probability(goals, expected_goals):
        """
        Oblicza prawdopodobieństwo liczby bramek przy użyciu rozkładu Poissona.

        :param goals: Liczba bramek.
        :param expected_goals: Oczekiwana liczba bramek.
        :return: Prawdopodobieństwo zdarzenia.
        """
        return (math.exp(-expected_goals) * expected_goals**goals) / math.factorial(goals)

    # MODELE DO SPECJALISTYCZNYCH ZDARZEŃ

    @staticmethod
    def predict_cards(avg_cards_per_game, team_intensity):
        """
        Prognozuje liczbę kartek na podstawie średniej i intensywności gry drużyny.

        :param avg_cards_per_game: Średnia liczba kartek na mecz.
        :param team_intensity: Wskaźnik intensywności gry (np. agresywności).
        :return: Przewidywana liczba kartek.
        """
        return avg_cards_per_game * team_intensity

    @staticmethod
    def predict_offsides(avg_offsides_per_game, attack_frequency):
        """
        Prognozuje liczbę spalonych na podstawie średniej i częstotliwości ataków.

        :param avg_offsides_per_game: Średnia liczba spalonych na mecz.
        :param attack_frequency: Częstotliwość ataków drużyny.
        :return: Przewidywana liczba spalonych.
        """
        return avg_offsides_per_game * attack_frequency

    @staticmethod
    def predict_corners(avg_corners_per_game, team_pressure):
        """
        Prognozuje liczbę rzutów rożnych na podstawie średniej i presji drużyny.

        :param avg_corners_per_game: Średnia liczba rzutów rożnych na mecz.
        :param team_pressure: Wskaźnik presji drużyny (np. nacisk na obronę przeciwnika).
        :return: Przewidywana liczba rzutów rożnych.
        """
        return avg_corners_per_game * team_pressure

    @staticmethod
    def predict_penalty_kicks(foul_probability, penalty_area_presence):
        """
        Prognozuje szansę na rzut karny.

        :param foul_probability: Prawdopodobieństwo faulu.
        :param penalty_area_presence: Obecność drużyny w polu karnym przeciwnika.
        :return: Prawdopodobieństwo rzutu karnego.
        """
        return foul_probability * penalty_area_presence

    @staticmethod
    def predict_weather_impact(weather_condition, avg_goals):
        """
        Prognozuje wpływ pogody na liczbę bramek.

        :param weather_condition: Wskaźnik warunków pogodowych (np. -1 dla złych, 0 dla neutralnych, +1 dla dobrych).
        :param avg_goals: Średnia liczba bramek na mecz.
        :return: Skorygowana średnia liczba bramek.
        """
        return avg_goals * (1 + 0.1 * weather_condition)

    @staticmethod
    def predict_injuries(avg_injuries_per_game, intensity_factor):
        """
        Prognozuje liczbę kontuzji na podstawie średniej i intensywności gry.

        :param avg_injuries_per_game: Średnia liczba kontuzji na mecz.
        :param intensity_factor: Wskaźnik intensywności meczu.
        :return: Przewidywana liczba kontuzji.
        """
        return avg_injuries_per_game * intensity_factor

    @staticmethod
    def predict_delays(avg_delays_per_game, external_factors):
        """
        Prognozuje przerwy w meczu na podstawie średniej i czynników zewnętrznych.

        :param avg_delays_per_game: Średnia liczba przerw na mecz.
        :param external_factors: Wskaźnik czynników zewnętrznych (np. protesty kibiców, warunki pogodowe).
        :return: Przewidywana liczba przerw.
        """
        return avg_delays_per_game * external_factors
