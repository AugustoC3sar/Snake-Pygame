import pygame
import config as cfg


class Window:
    def __init__(self):
        self._window = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    
    def draw_snake(self, snake):
        for segment in snake.body():
            pygame.draw.rect(self._window, segment.color(), segment.hitbox())

    def draw_fruit(self, fruit):
        pygame.draw.rect(self._window, cfg.FRUIT_COLOR, fruit)

    def draw_info(self, score, highscore):
        pygame.draw.rect(self._window, cfg.INFO_BG_COLOR, pygame.Rect(0,0,cfg.WIDTH,cfg.MARGIN))
        score_label = cfg.FONT.render(f'Score: {score}', False, cfg.FONT_COLOR)
        highscole_label = cfg.FONT.render(f'Highscore: {highscore}', False, cfg.FONT_COLOR)
        self._window.blit(score_label, (5,5))
        self._window.blit(highscole_label, (cfg.WIDTH-(highscole_label.get_rect().width)-5,5))

    def draw_end_game_screen(self):
        pygame.draw.rect(self._window, cfg.INFO_BG_COLOR, pygame.Rect(0,0,cfg.WIDTH,cfg.HEIGHT))
        lose_info = cfg.FONT.render('YOU LOSE!', False, cfg.FONT_COLOR)
        lose_rect = lose_info.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)-50))
        
        restart = cfg.FONT.render('Press R to restart',False, cfg.FONT_COLOR)
        restart_rect = restart.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))
        
        game_quit = cfg.FONT.render('Press Q to quit',False, cfg.FONT_COLOR)
        game_quit_rect = game_quit.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)+50))

        self._window.blit(lose_info, lose_rect)
        self._window.blit(restart, restart_rect)
        self._window.blit(game_quit, game_quit_rect)

    def draw_pause_screen(self):
        bg = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA)
        bg.fill((0,0,0,128))
        
        pause = cfg.FONT.render('PAUSED', False, cfg.FONT_COLOR)
        pause_rect = pause.get_rect(center=(cfg.WIDTH/2, (cfg.HEIGHT/2)))

        self._window.blit(bg, (0,0))
        self._window.blit(pause, pause_rect)

    def display(self, snake, fruit, score, highscore, game_in_progress, paused):
        if game_in_progress:
            self._window.fill(cfg.MAZE_COLOR)
            self.draw_snake(snake)
            self.draw_fruit(fruit)
            self.draw_info(score, highscore)
            if paused:
                self.draw_pause_screen()
        else:
            self.draw_end_game_screen()
        pygame.display.update()
            
