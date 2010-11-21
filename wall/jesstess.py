import random
import time
import colorsys
from effects import Effect
import ascii8x8
import itertools

class Mondrian(Effect):
    def _init(self, kw):
        red = (0, 1, 1)
        blue = (.6, 1, .7)
        yellow = (.2, 1, 1)
        black = (0, 0, 0)
        self.colors = [red, blue, yellow, black]

    def drawLine(self, color):
        vert = random.choice((0, 1))

        if vert:
            x = random.randint(0, 7)
            y = random.choice((0, 7))
        else:
            x = random.choice((0, 7))
            y = random.randint(0, 7)

        if vert and y:
            self.vert_line(color, x, y, -1) # line up
        elif vert:
            self.vert_line(color, x, y, 1) # line up
        elif x:
            self.horiz_line(color, x, y, -1) # line up
        else:
            self.horiz_line(color, x, y, 1) # line down            

    def vert_line(self, color, x, y, direction):
        for i in range(8):
            pixel = self.wall.pixel(x, y + i*direction)
            pixel.hsv = color
            self.wall.draw()

    def horiz_line(self, color, x, y, direction):
        for i in range(8):
            pixel = self.wall.pixel(x + i*direction, y)
            pixel.hsv = color
            self.wall.draw()

    def drawSquare(self, color):
        size = random.choice((2, 3, 4))
        corner_x = random.randint(0, 5)
        corner_y = random.randint(0, 5)
        
        for x in range(corner_x, corner_x + size + 1):
            for y in range(corner_y, corner_y + size + 1):
                if x < 8 and y < 8:
                    pixel = self.wall.pixel(x, y)
                    pixel.hsv = color
        self.wall.draw()

    def run(self):
        for i in range(5 * len(self.colors)):
            #shape = random.choice((0, 1))
            shape = random.random()
            if shape < .75:
                self.drawLine(self.colors[i % len(self.colors)])
            else:
                self.drawSquare(self.colors[i % len(self.colors)])
            time.sleep(.2)
        time.sleep(1)

class Pinwheel(Effect):
    class Triangle(object):
        def __init__(self, dot_list, wall):
            self.dot_list = dot_list
            self.wall = wall

        def colorize(self):
            for dot in self.dot_list:
                pixel = self.wall.pixel(dot[0], dot[1])
                pixel.hsv = (self.hue, 1, 1)

    def _init(self, kw):
        self.tri1 = [(x, 0) for x in range(4)]
        self.tri1.extend([(x, 1) for x in range(1, 4)])
        self.tri1.extend([(x, 2) for x in range(2, 4)])
        self.tri1.extend([(x, 3) for x in range(3, 4)])
        
        self.tri2 = [(x, 0) for x in range(4,8)]
        self.tri2.extend([(x, 1) for x in range(4, 7)])
        self.tri2.extend([(x, 2) for x in range(4, 6)])
        self.tri2.extend([(x, 3) for x in range(4, 5)])

        self.s1 = [(x, 3) for x in range(5, 8)]
        self.s1.extend([(x, 2) for x in range(6, 8)])
        self.s1.extend([(x, 1) for x in range(7, 8)])

        self.s2 = [(x, 4) for x in range(5, 8)]
        self.s2.extend([(x, 5) for x in range(6, 8)])
        self.s2.extend([(x, 6) for x in range(7, 8)])

        self.tri3 = [(x, 7) for x in range(4,8)]
        self.tri3.extend([(x, 6) for x in range(4, 7)])
        self.tri3.extend([(x, 5) for x in range(4, 6)])
        self.tri3.extend([(x, 4) for x in range(4, 5)])

        self.tri4 = [(x, 7) for x in range(4)]
        self.tri4.extend([(x, 6) for x in range(1, 4)])
        self.tri4.extend([(x, 5) for x in range(2, 4)])
        self.tri4.extend([(x, 4) for x in range(3, 4)])

        self.s3 = [(x, 4) for x in range(0,3)]
        self.s3.extend([(x, 5) for x in range(0, 2)])
        self.s3.extend([(x, 6) for x in range(0, 1)])

        self.s4 = [(x, 3) for x in range(0, 3)]
        self.s4.extend([(x, 2) for x in range(0, 2)])
        self.s4.extend([(x, 1) for x in range(0, 1)])

        self.triangles = []
        for triangle in [self.tri1, self.tri2, self.s1, self.s2, self.tri3, self.tri4, self.s3, self.s4]:
            self.triangles.append(self.Triangle(triangle, self.wall))

        hue = random.random()
        self.colors = [hue + i * .05 for i in range(4)]
        self.colors.extend(self.colors)

    def shift(self):
        first = self.colors.pop(0)
        self.colors.append(first)

        counter = 0
        for triangle in self.triangles:
            triangle.hue = self.colors[counter]
            triangle.colorize()
            counter = counter + 1
        self.wall.draw()
        time.sleep(.1)

    def run(self):
        for i in range(50):
            self.shift()

class Diamonds(Effect):
    def _init(self, kw):
        self.foreground = [elt for elt in itertools.product([1, 3, 5, 7], [0, 1, 2, 3, 4, 5, 6, 7])]
        self.foreground.extend([elt for elt in itertools.product([0, 2, 4, 6], [1, 3, 5, 7])])

    def color(self):
        for x in range(0, 8):
            for y in range(0, 8):
                pixel = self.wall.pixel(x, y)
                pixel.hsv = (self.bhue + .05 * y, 1, 1)

        counter = 0
        for dot in self.foreground:
            pixel = self.wall.pixel(dot[0], dot[1])
            pixel.hsv = (self.fhue + (counter % 8) * .01, 1, 1)
            counter = counter + 1
        self.wall.draw()

        self.bhue = self.bhue + .01
        self.fhue = self.fhue + .01


    def shift(self):
        new_foreground = []
        for dot in self.foreground:
            new_x = dot[0] + 1
            if new_x > 7:
                new_x = 0
            new_y = dot[1] + 1
            if new_y > 7:
                new_y = 0
            new_foreground.append((new_x, new_y))
        self.foreground = new_foreground

    def run(self):
        self.fhue = random.random()
        self.bhue = (self.fhue + .1) % 1

        self.wall.draw()
        for i in range(50):
            self.shift()
            self.color()
            time.sleep(.5)

class Letters(Effect):
    def run(self):
        color = random.random()
        foreground = (color, 1, 1)
        background = ((color + .5) % 1, 1, 1)

        for ord in range(65, 123):
            self.wall.clear()
            ascii8x8.draw_chr(chr(ord), self.wall, foreground, background)
            self.wall.draw()
            time.sleep(1)
    
class Zig(Effect):
    class Pixel(object):
        def __init__(self, wall, hue):
            self.wall = wall
            self.hue = hue
            self.x = random.choice((0, 7))
    
            if self.x:
                self.horiz = 0 # left
            else:
                self.horiz = 1 # right
    
            self.vert = random.choice((0, 1)) # 1 = up
            self.y = random.randint(0, 7)
            self.tail = []
    
        def displayPixel(self):
            pixel = self.wall.pixel(self.x, self.y)
            pixel.hsv = (self.hue, 1, 1)
            intensity = 1.0
            for elt in self.tail:
                intensity = intensity - .3
                pixel = self.wall.pixel(elt[0], elt[1])
                pixel.hsv = (self.hue, 1, intensity)
            self.wall.draw()
            
        def movePixel(self):
            self.tail.insert(0, (self.x, self.y))
            if len(self.tail) > 3:
                self.tail.pop()

            if self.horiz:
                self.x = self.x + 1
            else:
                self.x = self.x - 1
            if self.vert:
                self.y = self.y + 1
            else:
                self.y = self.y - 1
    
            if self.x > 7:
                self.horiz = 0
                self.x = 6
            if self.x < 0:
                self.x = 1
                self.horiz = 1
            if self.y > 7:
                self.y = 6
                self.vert = 0
            if self.y < 0:
                self.y = 1
                self.vert = 1

        def move(self):
            self.displayPixel()
            self.movePixel()
        
    def run(self):
        master_hue = random.random()
        pixels = []
        counter = 0
        start_time = time.time()
        while time.time() - start_time < 10:
            for pixel in pixels:
                pixel.move()
            time.sleep(.2)
            self.wall.clear()
            
            if counter == 0 and len(pixels) < 3:
                pixels.append(self.Pixel(self.wall, master_hue + .1 * len(pixels)))
            counter = counter + 1
            counter = counter % 4

class Stars(Effect):
    def _init(self, kw):
#         self.star_parts = [
#             (3, 0),
#             (3, 1),
#             (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
#             (2, 3), (3, 3), (4, 3),
#             (1, 4), (2, 4), (3, 4), (4, 4), (5, 4),
#             (1, 5), (5, 5),
#             (0, 6), (6, 6)
#             ]
        self.star_parts = [
            (2, 0),
            (2, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
            (2, 3),
            (1, 4), (3, 4),
            (0, 5), (4, 5),
            ]
    
    def shift(self, star_hue):
        for i in range(50):
            for x in range(0, 8):
                for y in range(0, 8):
                    pixel = self.wall.pixel(x, y)
                    pixel.hsv = ((pixel.hsv[0] + .01) % 1, 1, 1)
                self.wall.draw()

    def run(self):
        x_offset = random.randint(0, 3)
        y_offset = random.randint(0, 2)
        star_hue = random.random()
        background = (star_hue + .5) % 1
    
        for x in range(0, 8):
            for y in range(0, 8):
                pixel = self.wall.pixel(x, y)
                pixel.hsv = (background + x * .01, 1, 1)
    
        for dot in self.star_parts:
            pixel = self.wall.pixel(dot[0] + x_offset, dot[1] + y_offset)
            pixel.hsv = (star_hue, 1, 1)            
    
        self.wall.draw()
        self.shift(star_hue)
        time.sleep(.5)
        self.wall.clear()
    
class Ripple(Effect):
    def _init(self, kw):
        self.widths = [0 for x in range(0,8)]
        self.directions = [1 for x in range(0,8)]
        self.hue = random.random()

    def run(self):
        while True:
            for y in range(0,8):
                width = self.widths[y]
                for x in range(3 - width, 3 + width + 1):
                    pixel = self.wall.pixel(x, y)
                    pixel.hsv = (self.hue, 1, 1)
                    self.wall.draw()


    def updateWidths(self):
        for x in self.widths:
            width = x + self.directions[x]
            self.widths[x] = width
            if width > 3:
                self.direction[width] = -1
            if width < 1:
                self.direction[width] = 1


class Droplets(Effect):
    class Droplet(object):
        def __init__(self, wall, droplets):
            self.wall = wall
            self.droplets = droplets
            self.x = 0
            self.y = 0
            self.decay = 0
            self.decaying = False
            self.on = False
            self.hue = random.random()

        def setX(self, x):
            self.x = x

        def setY(self, y):
            self.y = y

        def splash(self, decay, hue):
            print "in splash ", self.x, self.y, decay
            if not self.on:
                self.on = True
                self.decay = decay - 2
                self.hue = hue

            if self.decay < 0:
                self.on = False

        def drop(self):
            print "in drop ", self.x, self.y, "decay = ", self.decay
            self.tryOn()
            if self.on:
                pixel = self.wall.pixel(self.x, self.y)
                pixel.hsv = (self.hue, 1, self.decay * .1)
                changers = self.spread()
                return changers
            self.decayLight()
            return []

        def tryOn(self):
            if random.random() > 0:
                self.on = True
                self.decay = 10
        
        def decayLight(self):
            if self.on:
                self.decay = self.decay - 1

            if self.decay < 0:
                self.on = False

        def spread(self):
            below = above = left = right = None
            if self.x != 0:
                left = self.droplets[self.x - 1][self.y]
            if self.x != len(self.droplets[0]) - 1:
                right = self.droplets[self.x + 1][self.y]
            if self.y != 0:
                above = self.droplets[self.x][self.y - 1]
            if self.y != len(self.droplets) - 1:
                below = self.droplets[self.x][self.y + 1]

            changers = filter(lambda x: x != None, [below, above, left, right])
            print "changers = " + repr(changers)
            for star in changers:
                star.splash(self.decay, self.hue)
            return changers

    def _init(self, kw):
        self.droplets = []
        for x in range(0,8):
            row = [self.Droplet(self.wall, self.droplets) for x in range(0,8)]
            self.droplets.append(row)

        for x in range(len(self.droplets)):
            for y in range(len(self.droplets[0])):
                self.droplets[x][y].setX(x)
                self.droplets[x][y].setY(y)

    def run(self):
        start_time = time.time()
        queue = [self.droplets[3][3]]
        while time.time() - start_time < 10:
            changers = []
            while len(queue) > 0:
                print "queue = ", queue
                droplet = queue.pop()
                if droplet.drop():
                    changers.extend(droplet.drop())
                    changers = list(set(changers))
                    print "changers = ", changers
            self.wall.draw()
            time.sleep(1)
            queue = changers

class Twinkle(Effect):
    class Star(object):
        def __init__(self, wall, x, y):
            self.wall = wall
            self.x = x
            self.y = y
            self.decay = 0
            self.on = False
            self.hue = .65 + random.uniform(-1, 1) * .15
            

        def twinkle(self):
            self.tryOn()
            if self.on:
                pixel = self.wall.pixel(self.x, self.y)
                pixel.hsv = (self.hue, 1, self.decay*.1)
            self.decayLight()

        def tryOn(self):
            if random.random() > .95:
                self.on = True
                self.decay = 10
        
        def decayLight(self):
            if self.on:
                self.decay = self.decay - 1

            if self.decay == 0:
                self.on = False
            
    def _init(self, kw):
        self.stars = []
        for x in range(0,8):
            for y in range(0,8):
                self.stars.append(self.Star(self.wall, x, y))

    def run(self):
        start_time = time.time()
        while time.time() - start_time < 10:
            for star in self.stars:
                star.twinkle()
            self.wall.draw()
            time.sleep(.1)
            self.wall.clear()

class Droplets2(Effect):
    class Droplet(object):
        def __init__(self, wall, droplets):
            self.wall = wall
            self.droplets = droplets
            self.x = 0
            self.y = 0
            self.decay = 0
            self.decaying = False
            self.on = False
            self.hue = random.random()

        def setX(self, x):
            self.x = x

        def setY(self, y):
            self.y = y

        def splash(self, decay, hue):
            if not self.on:
                self.on = True
                self.decay = decay
                self.hue = hue

        def drop(self):
            self.tryOn()
            if self.on:
                pixel = self.wall.pixel(self.x, self.y)
                pixel.hsv = (self.hue, 1, self.decay * .1)
                self.spread()
            self.decayLight()

        def tryOn(self):
            if random.random() > .995:
                self.on = True
                self.decay = 10
        
        def decayLight(self):
            if self.on:
                self.decay = self.decay - 1

            if self.decay == 0:
                self.on = False

        def spread(self):
            below = above = left = right = None
            if self.x != 0:
                left = self.droplets[self.x - 1][self.y]
            if self.x != len(self.droplets[0]) - 1:
                right = self.droplets[self.x + 1][self.y]
            if self.y != 0:
                above = self.droplets[self.x][self.y - 1]
            if self.y != len(self.droplets) - 1:
                below = self.droplets[self.x][self.y + 1]

            changers = filter(lambda x: x != None, [below, above, left, right])
            for star in changers:
                star.splash(self.decay, self.hue + .01)

    def _init(self, kw):
        self.droplets = []
        for x in range(0,8):
            row = [self.Droplet(self.wall, self.droplets) for x in range(0,8)]
            self.droplets.append(row)

        for x in range(len(self.droplets)):
            for y in range(len(self.droplets[0])):
                self.droplets[x][y].setX(x)
                self.droplets[x][y].setY(y)

    def run(self):
        start_time = time.time()
        while time.time() - start_time < 10:
            for i in range(0, 8):
                for j in range(0,8):
                    self.droplets[i][j].drop()
            self.wall.draw()
            time.sleep(.1)
            self.wall.clear()


class Rings(Effect):
    class RingElement(object):
        def __init__(self, location):
            self.location = location
            self.hue = 0

        def setHue(self, hue):
            self.hue = hue

        def getHue(self):
            return self.hue

        def x(self):
            return self.location[0]
        
        def y(self):
            return self.location[1]

    def _init(self, kw):
        x_min = 0
        x_max = 7
        y_min = 0
        y_max = 7

        self.rings = [[], [], [], []]
        for ring in self.rings:
            for x in range(x_min, x_max + 1):
                ring.append(self.RingElement((x, y_min)))
            for y in range(y_min, y_max + 1):
                ring.append(self.RingElement((x_max, y)))
            for x in range(x_max, x_min - 1, -1):
                ring.append(self.RingElement((x, y_max)))
            for y in range(y_max, y_min, -1):
                ring.append(self.RingElement((x_min, y)))

            x_min = x_min + 1
            x_max = x_max - 1
            y_min = y_min + 1
            y_max = y_max - 1
        
    def run(self):
        self.wall.clear()
        hue = random.random()
        for i in range(10):
            for ring in self.rings:
                for elt in ring:
                    elt.setHue(hue)
                    pixel = self.wall.pixel(elt.x(), elt.y())
                    pixel.hsv = (elt.getHue(), 1, 1)
                self.wall.draw()
                time.sleep(.2)
                hue = hue + .1

class Spiral(Effect):
    def _init(self, kw):
        self.hue = random.random()
        self.tail = []

    def draw(self, x, y):

        self.tail.insert(0, (x, y))
        if len(self.tail) > 4:
            self.tail.pop()

        self.hue = self.hue + .003
        pixel = self.wall.pixel(x, y)
        pixel.hsv = (self.hue, 1, 1)

        intensity = 1.0
        for elt in self.tail:
            intensity = intensity - .2
            pixel = self.wall.pixel(elt[0], elt[1])
            pixel.hsv = (self.hue, 1, intensity)

        self.wall.draw()
        time.sleep(.01)
        self.wall.clear()

    def run(self):
        x_min = 0
        x_max = 7
        y_min = 0
        y_max = 7

        while x_max > x_min:
            for x in range(x_min, x_max + 1):
                self.draw(x, y_min)
            for y in range(y_min, y_max + 1):
                self.draw(x_max, y)
            for x in range(x_max, x_min - 1, -1):
                self.draw(x, y_max)
            for y in range(y_max, y_min, -1):
                self.draw(x_min, y)

            x_min = x_min + 1
            x_max = x_max - 1
            y_min = y_min + 1
            y_max = y_max - 1
    
class Test(Effect):
    def _init(self, kw):
        self.flow = 0
        self.v = [0.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, 0.0]
        self.hue = random.random()
        self.start_time = time.time()

    def run(self):
        while (time.time() - self.start_time) < 10:
            for i in range(7, -1, -1):
                for j in range(7, -1, -1):
                    pixel = self.wall.pixel(i, j)
                    pixel.hsv = (self.hue, 1, 1)
                    self.hue += .015
                time.sleep(.15)
                self.wall.draw()

            self.wall.clear()
            
            for i in range(0,8):
                for j in range(0,8):
                    pixel = self.wall.pixel(i, j)
                    pixel.hsv = (self.hue, 1, 1)
                    self.hue -= .015
                time.sleep(.15)
                self.wall.draw()

            self.wall.clear()

def effects():
    return [Twinkle, Rings, Spiral, Test, Zig, Droplets2, Pinwheel, Mondrian]