class ImpossibleCardsDealException(ValueError):
    """Exception raised for errors in the dealing operation.

        Attributes:
            message -- explanation of the error
    """
    def __init__(self, remaining_cards_count: int, cards_to_deal_count: int):
        self.message = f'Requested {cards_to_deal_count} cards to deal while just {remaining_cards_count} cards remaining.'
