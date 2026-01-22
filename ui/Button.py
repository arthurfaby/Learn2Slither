import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, action=None, background_color=(70, 70, 70),  hover_background_color=(100, 100, 100), text_color=(255, 255, 255), hover_text_color=(255, 255, 255), border_color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.background_color = background_color
        self.hover_background_color = hover_background_color
        self.current_background_color = background_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.current_text_color = text_color
        self.border_color = border_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_background_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2) # Bordure

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        if not self.action:
            return
        if self.rect.collidepoint(mouse_pos):
            self.current_background_color = self.hover_background_color
            self.current_text_color = self.hover_text_color
        else:
            self.current_background_color = self.background_color
            self.current_text_color = self.text_color

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()