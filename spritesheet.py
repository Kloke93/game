"""
Date: 4/15/2022
Author: Eric Matthes and Tomas Dal Farra
class SpriteSheet from (Eric Matthes):
https://ehmatthes.github.io/pcc_2e/beyond_pcc/pygame_sprite_sheets/#loading-the-first-piece
with changes in description and increased functionalities of some functions
"""
import pygame


class SpriteSheet:
    """ """
    def __init__(self, filename, needs_alpha):
        """
        Loads the sprite sheet
        :param filename: path to the sprite sheet in computer
        :type filename: str
        :param needs_alpha: if for importing the sheet needs convert_alpha
        :type needs_alpha: bool
        """
        try:
            if needs_alpha:
                self.sheet = pygame.image.load(filename).convert_alpha()
            else:
                self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load sprite sheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None, scale_index=1):
        """
        Load a specific image from a specific rectangle.
        :param rectangle: Rectangle to take from sheet
        :param colorkey: Chroma key composition
        :param scale_index: for scaling the images if not one
        :return: image we selected of the sheet
        """
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = (0, 0, 0)
            elif colorkey == -2:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        if scale_index == 1:
            return image
        else:
            return pygame.transform.scale(image, (rect[2] * scale_index, rect[3] * scale_index))

    def images_at(self, rectangles, colorkey=None, scale_index=1):
        """
        Load a bunch of images and return them as a list
        :param rectangles: multiple rectangles to take from sheet
        :param colorkey: Chroma key composition
        :param scale_index: for scaling the images if not one
        :return: multiple images that we selected with rectangles
        """
        return [self.image_at(rect, colorkey, scale_index) for rect in rectangles]

    # I won't be using this function
    def load_strip(self, rect, image_count, colorkey=None):
        """
        Load a whole strip of images, and return them as a list
        only work for absolutely symmetrical sheets
        :param rect: Rectangle to take from sheet in different positions
        :param image_count: How many images we want to take
        :param colorkey: Chroma key composition
        :return: images in same line
        """
        rect_stripe = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(rect_stripe, colorkey)

    def load_grid_images(self, num_rows, num_cols, x_margin_left=0, x_margin_right=None, x_padding=0,
                         y_margin_top=0, y_margin_bottom=None, y_padding=0, colorkey=None, scale_index=1):
        """
        Load a grid of images
        :param num_rows: number of rows
        :param num_cols: number of columns
        :param x_margin_left: space between top of sheet and top of first row
        :param x_margin_right: if not symmetrical same but in the right
        :param x_padding: space between rows
        :param y_margin_top: space between the top of the sheet and the top of the first row character
        :param y_margin_bottom: if not symmetrical same but in the bottom
        :param y_padding: space between columns
        :param colorkey: to replace in every image of the grid
        :param scale_index: for scaling the images if not one
        Calls self.images_at() to get list of images.
        """
        # In case there are symmetrical margins
        if x_margin_right is None:
            x_margin_right = x_margin_left
        if y_margin_bottom is None:
            y_margin_bottom = y_margin_top

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size
        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        x_sprite_size = (sheet_width - (x_margin_left + x_margin_right) - (num_cols - 1) * x_padding) / num_cols
        y_sprite_size = (sheet_height - (y_margin_top + y_margin_bottom) - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin_left + col_num * (x_sprite_size + x_padding)
                y = y_margin_top + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        grid_images = self.images_at(sprite_rects, colorkey, scale_index)

        return grid_images
