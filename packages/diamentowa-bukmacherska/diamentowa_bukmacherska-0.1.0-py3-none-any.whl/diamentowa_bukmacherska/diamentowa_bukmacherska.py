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
