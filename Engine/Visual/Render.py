from Engine.Constants import UPDATE_LIMIT, DEFAULT_COLOR, MOUSE_CLICK_LEFT
from Engine.Visual.Efffect import Effect, Information
import pygame.display


def update_effects(self):
    if self.camera.mouse_click[2] and int(self.camera.mouse_click[3]) == MOUSE_CLICK_LEFT:
        if not self.pressed:
            self.pressed = True
            # self.effects.append(Effect((self.camera.mouse_click[0], self.camera.mouse_click[1]), self.textures.effects['mouse1']))
    else:
        self.pressed = False
    for i in [_ for _ in self.effects if isinstance(_, Effect)]:
        i.draw(self.screen)
        if not i.update(self.camera.move):
            self.effects.remove(i)
    for i in [_ for _ in self.effects if isinstance(_, Information)]:
        i.draw(self.screen)
        if not i.update(self.camera.move):
            self.effects.remove(i)
        break


def update_titles(handler):
    fps_text = handler.textures.font.render(f'fps: {int(handler.clock.get_fps())}', False, DEFAULT_COLOR)
    r = handler.textures.resizer
    # handler.screen.blit(handler.version, (10 * r, 10 * r))
    handler.screen.blit(fps_text, (10, 10 * r))


def rendering(handler, scene):
    c = handler.click_handler()
    try:
        for interface in handler.interfaces.values():
            interface.surface.update(handler.camera.mouse_click, handler.screen, c)
            handler.last_interface = interface
    except Exception:
        pass
    update_effects(handler)
    point_pos = (handler.camera.mouse_click[0] - 10, handler.camera.mouse_click[1] - 10)
    # handler.screen.blit(handler.textures.point, point_pos)
    update_titles(handler)
    pygame.display.flip()
