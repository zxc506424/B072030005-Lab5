import pygame
import os
import math
from menu import UpgradeMenu
from settings import WIN_WIDTH, WIN_HEIGHT

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.level = 0  # level of the tower
        self.range = [100, 110, 120, 130, 140, 150]  # tower attack range
        self.damage = [2.0, 2.1, 2.2, 2.3, 2.4, 2.5]   # tower damage
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.type = "tower"

    def attack(self, enemy_group):
        """
        Attack the enemy in range if it cool down
        :param enemy_group: EnemyGroup()
        :return: None
        """
        # cd
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return
        for en in enemy_group.get():
            # in range
            x1, y1 = en.rect.center
            x2, y2 = self.rect.center
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if distance <= self.range[self.level]:
                # attack
                en.health -= self.damage[self.level]
                self.cd_count = 0
                return

    def clicked(self, x, y):
        return True if self.rect.collidepoint(x, y) else False

    def draw_effect_range(self, win):
        """
        draw the tower effect range, which is a transparent circle.
        """
        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        transparency = 120
        pygame.draw.circle(surface, (128, 128, 128, transparency), self.rect.center, self.range[self.level])
        win.blit(surface, (0, 0))


class TowerGroup:
    def __init__(self):
        self.__towers = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]
        self.selected_tower = None
        self.upgrade_menu = None   # (UpgradeMenu)
        self.button_response = None  # (str)

    def update(self, enemy_group):
        """
        Update the tower action. (This function is call in main game loop)
        """
        for tw in self.__towers:
            tw.attack(enemy_group)
        # upgrade and sell
        if self.button_response == "upgrade":
            self.upgrade()
        elif self.button_response == "sell":
            self.sell()
        # update
        self.add_menu()
        self.button_response = None

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw tower
        for tw in self.__towers:
            win.blit(tw.image, tw.rect)
        # draw tower range
        if self.selected_tower is not None:
            self.selected_tower.draw_effect_range(win)
            self.upgrade_menu.draw(win)

    def get_click(self, x, y):
        """
        The tower group response to the player click action. (1) select the tower OR (2) get button response
        (This method is call in main game loop)
        :param x: mouse x
        :param y: mouse y
        :return: None
        """
        # if the tower is clicked, select the tower
        for tw in self.__towers:
            if tw.clicked(x, y):
                self.selected_tower = tw
                return
        # if the button is clicked, get the button response.
        # and keep selecting the tower.
        if self.upgrade_menu is not None:
            for btn in self.upgrade_menu.get_buttons():
                if btn.clicked(x, y):
                    self.button_response = btn.response()
            if self.button_response is None:
                self.selected_tower = None

    def add_menu(self):
        if self.selected_tower is None:
            self.upgrade_menu = None
        else:
            x, y = self.selected_tower.rect.center
            self.upgrade_menu = UpgradeMenu(x, y)

    def upgrade(self):
        """
        Bonus) Upgrade the selected tower (tower level + 1).
        (This method is called in self.update() method)
        :return: None
        """
        # This function is called in self.update() method.
        # Make sure that the level do not exceed level 5
        x, y = self.selected_tower.rect.center
        if self.selected_tower.level < 5 :
            self.selected_tower.level += 1

    def sell(self):
        """
        Bonus) Sell the tower (remove from self.__towers)
        (This method is called in self.update() method)
        :return: None
        """
        # (1) This function is called in self.update() method
        # (2) Make sure that the (a) upgrade menu object and the (b) selected tower object are also cleared
        # when the tower is removed
        self.__towers.remove(self.selected_tower)  # remove tower from tower list
        return None    
        #self.selected_tower = None


    def get(self):
        return self.__towers



