from shekar.utils import load_words
from typing import List


class AutoCorrect:
    def __init__(self):
        self.words = load_words()

    def __generate_n_edits(self, word: str, n: int) -> List[str]:
        """
        Generates all possible edits of a word by applying n edits.

        Args:
            word (str): The input word to generate edits for.
            n (int): The number of edits to apply.

        Returns:
            List[str]: A list of all possible edits of the input word.
        """

    def __known(self, words: List[str]) -> List[str]:
        """
        Filters the list of words to return only the known words.

        Args:
            words (List[str]): A list of words to filter.

        Returns:
            List[str]: A list of known words.
        """

    def correct(self, word: str, top_n: int = 5, n_edits: int = 3) -> List[str]:
        """
        Corrects the input word by returning the top n most similar words from the dictionary.

        Args:
            word (str): The input word to be corrected.
            top_n (int): The number of most similar words to return.

        Returns:
            List[str]: A list of the top n most similar words from the dictionary.

        Example:
            >>> corrector = AutoCorrect()
            >>> word = "خونه"
            >>> corrector.correct(word)
            ['خون', 'خانه', 'جون', 'دونه', 'خو']
        """
