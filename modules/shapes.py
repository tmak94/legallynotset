"""This Module creates the visual representation of a Card.

There are four identifiers a Card has:
the Number of shapes (1, 2, or 3)
the Shape type itself (Rectangle, Oval, or Diamond)
the shape's Color (Red, Green, or Purple)
the shape's Fill-type (Solid, Outline, or Striped)

Each identifier has a corresponding number from 1-3. When a Card is
initiated, it sends these numbers to this script. The script draws
the shapes on a new blank surface, and then returns the resulting
surface to the Card object.

This script requires that `pygame` is installed.

"""
from pygame import draw, Rect, Surface, SRCALPHA, font


def diaPoints(xy, dimensions):
    """Generates a list of positions used to draw the Diamond shape.

    Args:
        xy: The "top-right corner" of the Diamond.
        dimensions: The desired width and height of the Diamond.

    Returns:
        A list of positions for drawShapes. Since draw.polygon requires different
        parameters than draw.rect or draw.ellipse, this method helps standardizes
        things.
    """
    width_half = xy[0] + (dimensions[0]/2)
    height_half = xy[1] + (dimensions[1]/2)

    return [(xy[0], height_half), (width_half, xy[1]), (xy[0] + dimensions[0], height_half),
            (width_half, xy[1] + dimensions[1])]





def drawStripes(surface):
    # Draws white stripes over Card for fillType 3

    for i in range(10, 140, 3):
        draw.line(surface, (255, 255, 255), (i, 0), (i, 175))


# Assigns Coordinate locations for Shapes to be drawn based on Card's Number
numberCoord = {1: [(20, 70)], 2: [(20, 45), (20, 100)], 3: [(20, 20), (20, 70), (20, 120)]}

# Assigns 1 for Rectangles, 2 for Ovals, and 3 for Diamonds
shapes = {1: [draw.rect, Rect],
          2: [draw.ellipse, Rect],
          3: [draw.polygon, diaPoints]}

# Assigns 1 for Red, 2 for Green, and 3 for Purple
colors = {1: (255, 0, 0), 2: (0, 255, 0), 3: (255, 0, 255)}


def assignCardRender(number, shape, color, fill_type):
    """Creates the visual representation of a Card used in the game.

    The arguments are 1-3, designated by the numberCoord, shapes, and colors Dictionaries.
    Fill-Type does not have a Dictionary assigned to it as it is a special case.

    Args:
        number: The number of Shapes.
        shape: The type of Shapes.
        color: The color of the Shapes.
        fill_type: The fill-type of the Shapes.

    Returns:
        A Surface with the shapes drawn onto it. Shapes will move relative to Surface.
    """
    blank_card = Surface((150, 175))
    blank_card.fill((255, 255, 255))
    if fill_type < 3:
        for n in numberCoord[number]:
            shapes[shape][0](blank_card, colors[color], shapes[shape][1](n, (110, 40)), fill_type - 1)
    else:
        for n in numberCoord[number]:
            shapes[shape][0](blank_card, colors[color], shapes[shape][1](n, (110, 40)))
            drawStripes(blank_card)
    return blank_card


def cardOutline():
    outline = Surface((150, 175), SRCALPHA)
    outline.fill((255, 255, 0))
    outline.fill((255, 255, 255, 0.0), ((10, 10), (130, 155)))
    return outline


def text_object(text, font):
    return font.render(text, True, (0, 0, 0))



def sideMenu(score, remaining):
    sideBar = Surface((250, 575))
    sideBar.fill((220, 220, 220))
    largeText = font.Font('freesansbold.ttf', 25)
    numberText = font.Font('freesansbold.ttf', 50)


    draw.rect(sideBar, (255, 255, 255), ((25, 460), (200, 65)))


    sideBar.blit(text_object("Score", largeText), (5, 15))
    sideBar.blit(text_object(str(score), numberText), (5, 55))

    sideBar.blit(text_object("Cards Remaining", largeText), (5, 130))
    sideBar.blit(text_object(str(remaining), numberText), (5, 170))
    return sideBar

