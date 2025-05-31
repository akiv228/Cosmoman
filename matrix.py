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

        # начальный масштаб относительно cell_size
        # self.scale_k = 0.4 + 0.2 * random.random()  # от 0.4 до 0.6
        # Начальный масштаб (меньше, чем раньше, чтобы быстрее пропадал)
        self.scale_k = 0.6 + 0.4 * random.random()  # 0.2—0.3
        self.size = int(cell_size * self.scale_k)
        self.img = pg.transform.scale(self.base_image, (self.size, self.size))

        self.alpha = 240 + random.randint(0, 75)   # начальная прозрачность (от 180 до 255)
        # self.alpha_rate = 0.5 + 0.3 * random.random()  # скорость падения alpha
        self.alpha_rate = 1.5 + 0.3 * random.random()
     #Уменьшить «время жизни» частицы (alpha_rate или скорость убывания прозрачности)
        self.alive = True

        # # движение вверх с небольшой «ветрушкой» вбок
        # self.vx = random.uniform(-0.5, 0.5)
        # self.vy = -(0.3 + random.random() * 0.7)
        #
        # # небольшая дрожь/расширение горизонтального движения
        # self.k = 0.001 * random.random() * random.choice([-1, 1])
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = -(0.3 + random.random() * 0.4)        # чуть помедленнее
        self.k = 0.0005 * random.random() * random.choice([-1, 1])

    def update(self):
        # Двигаем частицы
        self.x += self.vx
        self.vx += self.k  # «дрожание» влево/вправо
        self.y += self.vy
        self.vy *= 0.97 # потихоньку замедляется движение вверх

        # Увеличиваем масштаб (частица «расширяется»)
        # self.scale_k += 0.002
        # Меньший шаг роста
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
        """
        Рисуем частицу на заданную поверхность (surface).
        Позиционируем так, чтобы центр частицы совпадал с (self.x, self.y).
        """
        rect = self.img.get_rect(center=(self.x, self.y))
        surface.blit(self.img, rect)


class FogOfWar:
    def __init__(self, maze_x, maze_y, grid_width, grid_height, cell_size, base_cloud_image):
        """
        maze_x, maze_y — координаты левого верхнего угла лабиринта на экране;
        grid_width, grid_height — размеры сетки (количество клеток по x и y);
        cell_size — размер каждой клетки в пикселях;
        base_cloud_image — Surface с исходным изображением облака (одинаковое для всех частиц).
        """
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
        self.spawn_interval = 60  # раз в 15 кадров
        self.frame_count = 0

        # Частота появления новых частиц (раз в N кадров)
        self.spawn_interval = 40

        # Лимит на общее число активных частиц
        self.max_particles = 300

        # Максимум новых частиц за один «цикловый» spawn
        self.max_new_particles_per_spawn = 100

        self.frame_count = 0


    def update(self, visibility_grid):
        # 1) Очищаем «мертвые» частицы
        self.particles = [p for p in self.particles if p.alive]

        # 2) Спавним новые раз в spawn_interval, но не больше max_new_particles_per_spawn
        self.frame_count += 1
        if self.frame_count >= self.spawn_interval:
            self.frame_count = 0

            # Если уже достигли общего лимита, не создаём новых
            if len(self.particles) >= self.max_particles:
                return

            # Собираем список ВСЕХ закрытых клеток
            closed_cells = [
                (r, c)
                for r in range(self.grid_height)
                for c in range(self.grid_width)
                if not visibility_grid[r][c]
            ]
            if not closed_cells:
                return

            random.shuffle(closed_cells)
            num_to_spawn = min(self.max_new_particles_per_spawn,
                               self.max_particles - len(self.particles))

            for (r, c) in closed_cells[:num_to_spawn]:
                cx = c * self.cell_size + self.cell_size // 2
                cy = r * self.cell_size + self.cell_size // 2
                new_p = SmokeParticle(cx, cy, self.base_cloud_image, self.cell_size)
                self.particles.append(new_p)

        # 3) Обновляем все живые частицы
        for p in self.particles:
            p.update()



    def render(self, target_surface, player_pos, reveal_radius):
         """
         Рисует слой тумана поверх target_surface.
         player_pos — (x, y) в глобальных координатах экрана,
                      reveal_radius — радиус «окошка» вокруг игрока (в пикселях).
         """
         # 1) Полностью заливаем fog.surface полупрозрачным чёрным
         #    (RGBA = (0, 0, 0, 200) — 200 означает «почти непрозрачный» чёрный).
         self.surface.fill((0, 0, 0, 200))

         # 2) Рисуем все активные облачные частицы (SmokeParticle) на fog.surface
         for p in self.particles:
             p.draw(self.surface)

         # 3) «Пропечатываем» прозрачный круг вокруг игрока:
         #    a) Сначала вычисляем координаты игрока внутри fog.surface:
         rel_x = player_pos[0] - self.maze_x
         rel_y = player_pos[1] - self.maze_y

         #    b) Создаём вспомогательную поверхность той же величины, что и fog.surface:
         hole_surf = pg.Surface(self.surface.get_size(), flags=pg.SRCALPHA)
         #       — изначально она полностью прозрачная (чтобы вычитать именно область круга).
         hole_surf.fill((0, 0, 0, 0))

         #    c) Рисуем на hole_surf «круг заливки» чёрным полупрозрачным = (0,0,0,200).
         #       Внутри круга именно эта «альфа=200» и будет вычитаться из fog.surface.
         pg.draw.circle(
             hole_surf,
             (0, 0, 0, 200),  # цвет: чёрный с alpha=200
             (int(rel_x), int(rel_y)),  # центр круга в системе fog.surface
             reveal_radius  # радиус круга
         )

         #    d) Вычитаем hole_surf из fog.surface: BLEND_RGBA_SUB уменьшает каждый канал,
         #       поэтому внутри круга alpha мокнутого fog.surface (200) станет (200−200)=0,
         #       и там появится прозрачная «дырка». Вне круга hole_surf полностью прозрачен,
         #       так что fog.surface за пределами круга остаётся (0,0,0,200).
         self.surface.blit(hole_surf, (0, 0), special_flags=pg.BLEND_RGBA_SUB)

         # 4) Наконец, рисуем готовый fog.surface поверх целевой поверхности (лабиринта),
         #    смещая его по (maze_x, maze_y).
         target_surface.blit(self.surface, (self.maze_x, self.maze_y))
