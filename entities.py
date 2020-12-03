# Contains all of the hostile entities, that subclass the Entity class
# Entity class is subclassed from Tile for center and proximity methods

from tiles import *

class Entity(Tile):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)

class UpwardSpike(Entity):
    def __init__(self, x, y, size):
        super().__init__(x,y, size)
        self.boundingBoxes = self.createBoundingBoxes()

    def createBoundingBoxes(self):
        boxes = []
        x = self.x + self.size / 2
        y = self.y
        size = self.size
        index = 1
        while(y < self.y + size):
            boxes.append((x - size / 8 * index, y, x + size / 8 * index, 
                            y + size / 4))
            y += size / 4
            index += 1
        return boxes

    def centerOfTile(self):
        return (self.x + self.size / 2, self.y + self.size / 2)

    def isTouching(self, boundingBoxes):
        playerBox = boundingBoxes["bot"]
        for spikeBox in self.boundingBoxes:
            if (boxesIntersect(spikeBox, playerBox)):
                return True
        return False
            

    def draw(self, canvas):
        x = self.x
        y = self.y
        size = self.size
        for box in self.boundingBoxes:
            x0, y0, x1, y1 = box
            canvas.create_rectangle(x0, y0, x1, y1)
        canvas.create_line(x + size / 2, y, x, y + size)
        canvas.create_line(x + size / 2, y, x + size, y + size)
        canvas.create_line(x, y + size, x + size, y + size)
