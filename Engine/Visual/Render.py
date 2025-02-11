from Engine.Constants import UPDATE_LIMIT, DEFAULT_COLOR, MOUSE_CLICK_LEFT
from Engine.Visual.Efffect import Effect, Information
import pygame.display


class Render:
    def __init__(self, handler):
        self.handler = handler

    def update_effects(self):
        if self.handler.camera.mouse_click[2] and int(self.handler.camera.mouse_click[3]) == MOUSE_CLICK_LEFT:
            if not self.handler.pressed:
                self.handler.pressed = True
                # self.effects.append(Effect((self.camera.mouse_click[0], self.camera.mouse_click[1]), self.textures.effects['mouse1']))
        else:
            self.handler.pressed = False
        for i in [_ for _ in self.handler.effects if isinstance(_, Effect)]:
            i.draw(self.handler.screen)
            if not i.update(self.handler.camera.move):
                self.handler.effects.remove(i)
        for i in [_ for _ in self.handler.effects if isinstance(_, Information)]:
            i.draw(self.handler.screen)
            if not i.update(self.handler.camera.move):
                self.handler.effects.remove(i)
            break

    def update_titles(self):
        fps_text = self.handler.textures.font.render(f'fps: {int(self.handler.clock.get_fps())}', False, DEFAULT_COLOR)
        r = self.handler.textures.resizer
        # handler.screen.blit(handler.version, (10 * r, 10 * r))
        self.handler.screen.blit(fps_text, (10, 10 * r))

    def rendering(self):
        c = self.handler.click_handler()
        try:
            for interface in self.handler.interfaces.values():
                interface.surface.update(self.handler.camera.mouse_click, self.handler.screen, c)
                self.handler.last_interface = interface
        except Exception:
            pass
        self.update_effects()
        point_pos = (self.handler.camera.mouse_click[0] - 10, self.handler.camera.mouse_click[1] - 10)
        # handler.screen.blit(handler.textures.point, point_pos)
        self.update_titles()
        pygame.display.flip()
