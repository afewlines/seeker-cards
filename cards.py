
import csv
from random import shuffle


class Card():
    def __init__(self, id, text):
        self.id = int(id)
        self.text = text

    def show(self):
        print("ID:   {:04d}".format(self.id))
        print("TEXT: {}".format(self.text))

    def to_string(self):
        return "{:04d}{}".format(self.id, self.text)


class CardPrompt(Card):
    def __init__(self, id, text, special):
        super().__init__(id, text)
        if special[-1:] != '':
            self.difference = int(special[-1:])
        else:
            self.difference = 1

    def show(self):
        print("  PROMPT")
        super().show()
        print("PICK: {}".format(self.difference))


class CardResponse(Card):
    def __init__(self, id, text):
        super(CardResponse, self).__init__(id, text)

    def show(self):
        print("  RESPONSE")
        super().show()


class DeckManager():
    def __init__(self):
        self.total_all = 0
        self.total_prompt = 0
        self.total_respose = 0
        self.cards_all = {}
        self.cards_prompt = []
        self.cards_response = []
        self.deck_prompt = []
        self.deck_response = []

    def load_cards(self, target_file):
        with open(target_file, 'r') as csvfile:
            parsed_csv = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in parsed_csv:
                if row[0].lower() == "prompt":
                    self.cards_all[self.total_all] = CardPrompt(
                        self.total_all, row[1], row[2])
                    self.cards_prompt.append(self.total_all)
                    self.total_prompt += 1
                else:
                    self.cards_all[self.total_all] = CardResponse(
                        self.total_all, row[1])
                    self.cards_response.append(self.total_all)
                    self.total_respose += 1
                self.total_all += 1

    def form_decks(self):
        self.deck_prompt = [card for card in self.cards_prompt]
        self.deck_response = [card for card in self.cards_response]
        self.shuffle_deck('prompt')
        self.shuffle_deck('response')

    def shuffle_deck(self, deck):
        if deck.lower() == 'prompt':
            shuffle(self.deck_prompt)
        elif deck.lower() == 'response':
            shuffle(self.deck_response)
        else:
            print("INVALID DECK")

    def get_card(self, deck):
        if deck.lower() == 'prompt':
            if len(self.deck_prompt) <= 0:
                return "0000OUTOFCARDS"
            return self.cards_all[self.deck_prompt.pop(0)]
        elif deck.lower() == 'response':
            if len(self.deck_response) <= 0:
                return "0000OUTOFCARDS"
            return self.cards_all[self.deck_response.pop(0)]
        else:
            return None

    def find_id(self, id):
        return self.cards_all[int(id)].text
