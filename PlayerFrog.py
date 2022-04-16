class PlayerFrog(Player):

    def __init__(self, pos):
        super().__init__(pos)
        self.animations = self.animation_dict()

    @staticmethod
    def animation_dict():
        """
        With the path to the sheet sprite images, loads all the sheets and
         gets the individual images for each action in a dictionary
        :return: dictionary of the different states of the player with a list of images for each one
        :rtype: dict
        """
        animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        scale_index = 2     # For scaling the images
        # Animation paths
        idle_path = "Pixel Adventure 1/Main Characters/Ninja Frog/Idle (32x32).png"
        run_path = "Pixel Adventure 1/Main Characters/Ninja Frog/Run (32x32).png"
        jump_path = "Pixel Adventure 1/Main Characters/Ninja Frog/Jump (32x32).png"
        fall_path = "Pixel Adventure 1/Main Characters/Ninja Frog/Fall (32x32).png"
        # Animation sheets
        idle_sheet = SpriteSheet(idle_path, True)
        run_sheet = SpriteSheet(run_path, True)
        jump_sheet = SpriteSheet(jump_path, True)
        fall_sheet = SpriteSheet(fall_path, True)
        # jump and fall are both single images
        # Completing dictionary
        animations['idle'] = idle_sheet.load_grid_images(
            1, 11, 4, x_padding=9, y_margin_top=6, y_margin_bottom=0, scale_index=scale_index, colorkey=-1)
        # Because lack of symmetry we need to do many rectangles for run
        rects_run = [
            (4, 4, 23, 28), (36, 4, 23, 28), (68, 4, 23, 28), (100, 4, 23, 28), (131, 4, 25, 28), (163, 4, 25, 28),
            (196, 4, 24, 28), (228, 4, 24, 28), (260, 4, 24, 28), (292, 4, 24, 28), (323, 4, 25, 28), (355, 4, 25, 28)
        ]
        animations['run'] = run_sheet.images_at(rects_run, -1, scale_index)
        jump_image = jump_sheet.image_at((4, 4, 23, 28), -1, scale_index)
        fall_image = fall_sheet.image_at((4, 6, 24, 26), -1, scale_index)
        animations['jump'].append(jump_image)
        animations['fall'].append(fall_image)
        return animations
