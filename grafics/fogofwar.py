import pygame as pg
import random

class SmokeParticle:
    """
    Обычная частица дыма: рождается в рамках ячейки, поднимается, растёт,
    теряет прозрачность и умирает.
    """
    def __init__(self, x, y, base_image, cell_size):
        """
        x, y — центр спавна (обычно центр клетки);
        base_image — Surface с изображением облака;
        cell_size — размер клетки (ширина/высота) для начального масштаба.
        """
        self.x = x
        self.y = y
        self.base_image = base_image


        self.scale_k = 1 + 0.4 * random.random()  # 0.2—0.3
        self.size = int(cell_size * self.scale_k)
        self.img = pg.transform.scale(self.base_image, (self.size, self.size))

        self.alpha = 240 + random.randint(0, 75)
        # self.alpha_rate = 0.5 + 0.3 * random.random()  # скорость падения alpha
        self.alpha_rate = 1.5 + 0.3 * random.random()

        self.alive = True

        # # движение вверх с небольшой «ветрушкой» вбок

        # self.vx = random.uniform(-0.5, 0.5)
        # self.vy = -(0.3 + random.random() * 0.7)
        # # небольшая дрожь/расширение горизонтального движения
        # self.k = 0.001 * random.random() * random.choice([-1, 1])

        self.vx = random.uniform(-0.3, 0.3)
        self.vy = -(0.3 + random.random() * 0.4)        # чуть помедленнее
        self.k = 0.0005 * random.random() * random.choice([-1, 1])

    def update(self):
        self.x += self.vx
        self.vx += self.k  # «дрожание» влево/вправо
        self.y += self.vy
        self.vy *= 0.97     # потихоньку замедляется движение вверх

        # Увеличиваем масштаб (частица «расширяется»)
        # self.scale_k += 0.002
        self.scale_k += 0.001
        new_size = int(self.base_image.get_width() * self.scale_k)
        new_size = max(new_size, 1)
        self.img = pg.transform.scale(self.base_image, (new_size, new_size))

        # Меняем прозрачность
        self.alpha -= self.alpha_rate
        if self.alpha <= 0:
            self.alpha = 0
            self.alive = False
        else:
            self.img.set_alpha(int(self.alpha))

    def draw(self, surface):
        rect = self.img.get_rect(center=(self.x, self.y))
        surface.blit(self.img, rect)


class FogOfWar:
    def __init__(self, maze_x, maze_y, grid_width, grid_height, cell_size, base_cloud_image):
        self.maze_x = maze_x
        self.maze_y = maze_y
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size

        # Общая поверхность, на которой «рисуется весь туман»
        width_px = grid_width * cell_size
        height_px = grid_height * cell_size
        self.surface = pg.Surface((width_px, height_px), flags=pg.SRCALPHA)

        # Заполняем его полностью «чёрным полупрозрачным» фоном (например, alpha=200)
        self.surface.fill((0, 0, 0, 200))

        # Базовое изображение облачка, которое будем масштабировать внутри SmokeParticle
        self.base_cloud_image = base_cloud_image

        # Список всех частиц дыма, привязанных к разным клеткам
        self.particles = []

        # Сколько кадров между спавном новых частиц в каждой невидимой клетке
        self.spawn_interval = 60
        self.frame_count = 0

        # Лимит на общее число активных частиц
        self.max_particles = 1000

        # Создаем начальные частицы для ВСЕХ клеток
        for row in range(grid_height):
            for col in range(grid_width):
                cell_center_x = col * self.cell_size + self.cell_size // 2
                cell_center_y = row * self.cell_size + self.cell_size // 2
                new_particle = SmokeParticle(
                    x=cell_center_x,
                    y=cell_center_y,
                    base_image=self.base_cloud_image,
                    cell_size=self.cell_size
                )
                self.particles.append(new_particle)



    def update(self, visibility_grid):
        """
        Обновляем все частицы, удаляем «мертвые» и, если пора,
        спавним новые во всех невидимых клетках.

        visibility_grid — двумерный список/массив размером [grid_height][grid_width]:
                          True если клетка **открыта** (игрок её увидел), False если ещё скрыта.
        """
        # убираем «мертвые» частицы
        self.particles = [p for p in self.particles if p.alive]
        # увеличиваем счётчик кадров
        self.frame_count += 1
        if self.frame_count >= self.spawn_interval:
            self.frame_count = 0
            # Проходим по всем клеткам; если cell закрыта (visibility_grid[row][col] == False),
            # то спавним в этой клетке ещё одну частицу (с центром посередине клетки или чуть случайно смещённым).
            for row in range(self.grid_height):
                for col in range(self.grid_width):
                    if not visibility_grid[row][col] and len(self.particles) < self.max_particles:
                        cell_center_x = col * self.cell_size + self.cell_size // 2
                        cell_center_y = row * self.cell_size + self.cell_size // 2
                        # создаём частицу в системе координат «относительно» левого верхнего угла maze (0,0)
                        new_particle = SmokeParticle(
                            x=cell_center_x,
                            y=cell_center_y,
                            base_image=self.base_cloud_image,
                            cell_size=self.cell_size
                        )
                        self.particles.append(new_particle)

        # Обновляем все частицы
        for p in self.particles:
            p.update()


    def render(self, target_surface, player_pos, reveal_radius):
         """
         Рисует слой тумана поверх target_surface.
         player_pos — (x, y) в глобальных координатах экрана,
         reveal_radius — радиус «окошка» вокруг игрока (в пикселях).
         """
         self.surface.fill((0, 0, 0, 240))

         for p in self.particles:
             p.draw(self.surface)

         #  «Пропечатываем» прозрачный круг вокруг игрока:
         #    сначала вычисляем координаты игрока внутри fog.surface:
         rel_x = player_pos[0] - self.maze_x
         rel_y = player_pos[1] - self.maze_y

         # Создаём вспомогательную поверхность той же величины, что и fog.surface:
         hole_surf = pg.Surface(self.surface.get_size(), flags=pg.SRCALPHA)
         #       — изначально она полностью прозрачная (чтобы вычитать именно область круга).
         hole_surf.fill((0, 0, 0, 0))


         pg.draw.circle(
             hole_surf,
             (0, 0, 0, 200),  # цвет: чёрный с alpha=200
             (int(rel_x), int(rel_y)),  # центр круга в системе fog.surface
             reveal_radius  # радиус круга
         )
         self.surface.blit(hole_surf, (0, 0), special_flags=pg.BLEND_RGBA_SUB)

         target_surface.blit(self.surface, (self.maze_x, self.maze_y))
