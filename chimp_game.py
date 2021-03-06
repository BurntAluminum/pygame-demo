import os, sys
import pygame as pg
from pygame.locals import *

if not pg.font: print('Warning, fonts disabled')
if not pg.mixer: print('Warning, sound disabled')

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pg.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pg.mixer.Sound(fullname)
    except pg.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

class Fist(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('fist.bmp', -1)
        self.punching = 0

    def update(self):
        """move the fist based on the mouse position"""
        pos = pg.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        """returns true if the fist collides with the target"""
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """called to pull the fist back"""
        self.punching = 0

class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self, background, background_color):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image('chimp.bmp', -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0
        self.background = background
        self.background_color = background_color

    def update(self):
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or \
                    self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, 1, 0)
            if self.rect.right % 13 == 0:
                self.image = pg.transform.flip(self.image, 1, 0)
                if self.background_color == (211, 4, 4):
                    self.background_color = (153, 229, 80)
                    self.background.fill(self.background_color)
                else:
                    self.background_color = (211, 4, 4)
                    self.background.fill(self.background_color)
            self.rect = newpos

    def _spin(self):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


def main():

    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((468, 60))
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(0)

    # Set Background
    
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background_color = (211, 4, 4)
    background.fill(background_color)

    if pg.font:
        font = pg.font.Font(None, 36)
        widtext = font.render("Punch the Chimp, Redeem FREE ipod", 1, (153, 229, 80))
        textpos = text.get_rect(centerx=background.get_th()/2)
        background.blit(text, textpos)

        
    screen.blit(background, (0, 0))
    pg.display.flip()

    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('punch.wav')
    chimp = Chimp(background, background_color)
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((fist, chimp))
    clock = pg.time.Clock()

    while 1:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

        
        pg.display.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()

    pg.quit()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()



    
