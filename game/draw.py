import pygame
from game.settings import SHOW_DEBUG_TEXT

_debug_font = None


def draw(stage, screen):
    _draw_world(stage, screen)
    _draw_ui(stage, screen)

def _draw_world(stage, screen):
    camera = stage.camera
    stage.background.draw_far_and_mid(screen, camera.x)
    characters = stage.get_all_characters()
    # depth sorting
    characters.sort(key=lambda c: c.z)
    for character in characters:
        character.draw(screen, camera.x)

def _draw_ui(stage, screen):
    if SHOW_DEBUG_TEXT:
        _draw_debug_attack_text(stage.player, screen)

def _draw_debug_attack_text(player, screen):
    global _debug_font
    if _debug_font is None:
        _debug_font = pygame.font.SysFont(None, 28)

    attack_name = player.current_attack.name if player.current_attack else "-"
    combo_text = "-"
    for i, attack in enumerate(player.combo_attacks):
        if attack is player.current_attack:
            combo_text = f"{i + 1}/{len(player.combo_attacks)}"
            break

    text = f"Attack: {attack_name}   Combo: {combo_text}"
    surface = _debug_font.render(text, True, (255, 255, 0))
    x = screen.get_width() - surface.get_width() - 10
    screen.blit(surface, (x, 10))
