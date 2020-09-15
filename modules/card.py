"""This Module defines the Card class and its functions."""

from pygame import mouse

from .shapes import assignCardRender, cardOutline


class Card:
    """
    There are four identifiers a Card has:
    the Number of shapes (1, 2, or 3)
    the Shape type itself (Rectangle, Oval, or Diamond)
    the shape's Color (Red, Green, or Purple)
    the shape's Fill-type (Solid, Outline, or Striped)

    The Card Class takes these 4 identifiers, assigns each of them a number between 1-3
    and then uses that to assign a unique 4-digit ID.


    Attributes:
        number: An integer count of the number of shapes
        shape: An integer designation of the type of shapes
        color: An integer designation of the color of shapes
        fill: An integer designation of the fill of shape
        id: A four-digit integer used to identify Card
        render: A Surface object for the card's image
        rect: A Rect object derived from render
        isSelected: A boolean indicating if the User has clicked on a Card
        outline: A Surface object for designating isSelected
    """

    def __init__(self, number, shape, color, fill):
        """
        Initiates Card with Attributes
        """
        self.number = number
        self.shape = shape
        self.color = color
        self.fill = fill
        self.id = number*1000 + shape*100 + color*10 + fill
        self.render = assignCardRender(self.number, self.shape, self.color, self.fill)
        self.rect = self.render.get_rect()
        self.outline = cardOutline()

    def __eq__(self, otherCardId):
        return self.id == otherCardId

    def __repr__(self):
        return repr(self.id)

    def getID(self):
        return self.id

    def renderCard(self, display, pos, cards):
        """

        Args:
            cards: the list of cards that Player has clicked
            display: The window of the game, where the cards are drawn.
            pos: The position where the Card is rendered

        """


        display.blit(self.render, pos)
        self.rect.topleft = pos


        if self.id in cards:
            display.blit(self.outline, pos)


    def highlight(self, cards):
        """
        Lights up Cards to show User whether they have Selected a Card

        Args:
            cards: The list of Cards that have already been Selected

        """
        if self.rect.collidepoint(mouse.get_pos()):
            if self.id not in cards:
                #self.isSelected = True
                cards.append(self.id)

            else:
                cards.remove(self.id)
            # self.isSelected = False
            print(cards)


