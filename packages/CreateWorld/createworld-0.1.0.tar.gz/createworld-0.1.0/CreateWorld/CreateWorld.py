import pygame
import sys
from multiprocessing import Process

class create2dworld:
    def __init__(self, width, height, name):
        self.width = width
        self.height = height
        self.name = name

    def window(self, mode='normal'):
        pygame.init()
        if mode == 'normal':
            screen = pygame.display.set_mode((int(self.width), int(self.height)))
        elif mode == 'no_frame':
            screen = pygame.display.set_mode((int(self.width), int(self.height)), pygame.NOFRAME)
        elif mode == 'full_screen':
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            raise ValueError("Invalid mode. Supported modes are 'normal', 'no_frame', and 'full_screen'.")
        
        pygame.display.set_caption(self.name)
        return screen

    def set_background(self, screen, color=None, image_path=None):
        if color:
            screen.fill(color)
        elif image_path:
            background_image = pygame.image.load(image_path)
            background_image = pygame.transform.scale(background_image, (self.width, self.height))
            screen.blit(background_image, (0, 0))
        else:
            raise ValueError("Either color or image_path must be provided.")

    def draw_shapes(self, screen, shapes):
        for shape in shapes:
            shape_type = shape['type']
            if shape_type == 'rectangle':
                pygame.draw.rect(screen, shape['color'], shape['rect'])
            elif shape_type == 'circle':
                pygame.draw.circle(screen, shape['color'], shape['center'], shape['radius'])
            elif shape_type == 'line':
                pygame.draw.line(screen, shape['color'], shape['start_pos'], shape['end_pos'], shape['width'])
            else:
                raise ValueError(f"Unsupported shape type: {shape_type}")

    def update_shapes(self, shapes, dt, control_func=None):
        for shape in shapes:
            if 'update_func' in shape:
                shape['update_func'](shape, dt)
        if control_func:
            control_func(shapes, dt)

    def run(self, mode='normal', color=None, image_path=None, draw_shapes=False, shapes=None, control_func=None):
        pygame.init()
        screen = self.window(mode)
        clock = pygame.time.Clock()  # 创建时钟对象
        running = True
        while running:
            dt = clock.tick(60) / 1000.0  # 获取时间间隔（秒）
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.set_background(screen, color, image_path)
            if draw_shapes and shapes:
                self.update_shapes(shapes, dt, control_func)  # 更新图形位置
                self.draw_shapes(screen, shapes)  # 重新绘制图形
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    @staticmethod
    def create_multiple_windows(window_configs):
        processes = []
        for config in window_configs:
            p = Process(target=create2dworld(*config[:3]).run, args=config[3:])
            processes.append(p)
            p.start()
        
        for p in processes:
            p.join()
