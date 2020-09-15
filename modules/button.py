"""""This Module contains the Class used to Create Buttons used in all game states"""""
from pygame import Surface, font, mouse


class Button:
    """""
    The Button is used for the User to navigate the Program

        Attributes:
            function: The Function that is run when the User clicks the Button
            render: A Surface Object for the Button's image
            rect: A Rect Object derived from the render 
    """""

    def __init__(self, text, function):
        """
        Initiates Button with Attributes

        Args:
            text: A String Object that describes the Button's use for the User
            function: The Function that is run when the User clicks the Button
        """
        self.function = function
        button = Surface((200, 65))
        button.fill((255, 255, 255))
        words = font.Font('freesansbold.ttf', 25).render(text, True, (0, 0, 0))
        button.blit(words, (100 - words.get_width() // 2, 33 - words.get_height() // 2))
        self.render = button
        self.rect = button.get_rect()

    def drawButton(self, surface, pos):
        """
        Draws the Button

        Args:
            surface: Where the button is drawn (almost always display)
            pos: The position where the button is drawn
        """
        surface.blit(self.render, pos)
        self.rect.topleft = pos

    def clicked(self):
        """
        Determines if the user clicks the button (used with event handler methods)

        Returns: The method attached to the Button

        """
        if self.rect.collidepoint(mouse.get_pos()):
            return self.function()
