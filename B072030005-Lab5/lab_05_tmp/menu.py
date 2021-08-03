import pygame
import os

UPGRADE_MENU_IMAGE = pygame.image.load(os.path.join("images", "upgrade_menu.png"))
SELL_IMAGE = pygame.image.load(os.path.join("images", "sell.png"))
UPGRADE_IMAGE = pygame.image.load(os.path.join("images", "upgrade.png"))

class UpgradeMenu:
    def __init__(self, x, y):
        self.__buttons = []  # (Q2) Add buttons here
        self.image = pygame.transform.scale(UPGRADE_MENU_IMAGE, (200, 200) ) # image of the upgrade_menu
        self.upgrade_image = pygame.transform.scale(UPGRADE_IMAGE, (50, 50)) # image of the upgrade_botton
        self.sell_image = pygame.transform.scale(SELL_IMAGE, (50, 50)) # image of the sell_bottons
        self.rect = self.image.get_rect() #center of upgrade_menu 
        self.rect.center = (x, y)
          
        pass

    def draw(self, win):
        """
        (Q1) draw menu itself and the buttons
        (This method is call in draw() method in class TowerGroup)
        :return: None
        """
        # draw menu
        win.blit(self.image, self.rect)

        # draw button
        # (Q2) Draw buttons here
        win.blit(self.upgrade_image,(self.rect.x+ 70 , self.rect.y))
        win.blit(self.sell_image,(self.rect.x+ 70 , self.rect.y +150))

        #There is something wrong,but I can't solve.
        self.__buttons.append(Button(self.upgrade_image, "upgrade",self.rect.x + 70 , self.rect.y))
        self.__buttons.append(Button(self.sell_image, "sell", self.rect.x+ 70 , self.rect.y +150))
        

    def get_buttons(self):
        """
        (Q1) Return the button list.
        (This method is call in get_click() method in class TowerGroup)
        :return: list
        """
        
        return self.__buttons

class Button:
    def __init__(self, image, name, x, y):
        self.name = name

    def clicked(self, x, y):
        """
        (Q2) Return Whether the button is clicked
        (This method is call in get_click() method in class TowerGroup)
        :param x: mouse x
        :param y: mouse y
        :return: bool
        """
        return True if self.rect.collidepoint(x, y) else False


    def response(self):
        """
        (Q2) Return the button name.
        (This method is call in get_click() method in class TowerGroup)
        :return: str
        """ 
        return self.name



