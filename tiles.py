import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, im, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(im).convert_alpha()
        self.hit_box = self.image.get_rect()
        self.hit_box.x, self.hit_box.y = x, y
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.hit_box.x, self.hit_box.y))

class TileMap():
    def __init__(self, filename, stpx, stpy):
        self.tile_size = 32
        self.start_x, self.start_y = stpx, stpy
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()
        pygame.image.save(self.map_surface, 'mapa.png')

    def draw_map(self, surface, stpx, stpy):

        surface.blit(self.map_surface, (stpx, stpy))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, mapname):
        map = []
        with open(os.path.join('Maps/{}.csv'.format(mapname))) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:

                if tile == '-1':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                else:
                    for i in range(0, 18):
                        if tile == str(i):

                            tiles.append(Tile('Graphics/level_' + filename + '/tiles_' +filename+'_'+str(i+1)+'.png', x * self.tile_size, y * self.tile_size))
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

