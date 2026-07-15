import pygame
from game.settings import (
    SHOW_DEBUG_INFO,
    NO_IMAGES_FOR_STAGE,
    SCREEN_WIDTH,
    PLAYER_EXTRA_LIFE_SCORE_BASE,
    PLAYER_EXTRA_LIFE_SCORE_STEP,
)
from game.colors import *
from game.components.health_component import HealthComponent

_debug_font = None
_hud_font = None
_warning_font = None

# How many equal-height lanes to divide the ground's walkable z-range into
# when NO_IMAGES_FOR_STAGE is on.
_LANE_COUNT = 4


def draw(stage, screen):
    _draw_world(stage, screen)
    _draw_ui(stage, screen)

def _draw_world(stage, screen):
    camera = stage.camera
    stage.background.draw_background(screen, camera.x)
    if NO_IMAGES_FOR_STAGE:
        _draw_lanes(stage, screen)
    stage.exit.draw(screen, camera.x)
    _draw_exit_arrow(stage, screen, camera.x)
    characters = stage.get_all_characters()
    # depth sorting
    characters.sort(key=lambda c: c.z)
    for character in characters:
        character.draw(screen, camera.x)
    stage.floating_text_manager.draw(screen, camera.x)
    # Foreground decoration, drawn last so it can pass in front of characters.
    stage.background.draw_front(screen, camera.x)

def _draw_lanes(stage, screen):
    """Debug overlay dividing the walkable z-range (lane_top/lane_bottom)
    into _LANE_COUNT equal lanes - z maps straight to screen y with no
    camera scroll on that axis, so these are just horizontal lines
    spanning the full screen width."""
    pygame.draw.line(screen, WHITE_COLOR, (0, stage.lane_top), (SCREEN_WIDTH, stage.lane_top), 2)
    pygame.draw.line(screen, WHITE_COLOR, (0, stage.lane_bottom), (SCREEN_WIDTH, stage.lane_bottom), 2)
    lane_height = (stage.lane_bottom - stage.lane_top) / _LANE_COUNT
    for i in range(1, _LANE_COUNT):
        y = stage.lane_top + i * lane_height
        pygame.draw.line(screen, (200, 200, 200), (0, y), (SCREEN_WIDTH, y), 1)

# todo: in future, just show an png file as arrow
def _draw_exit_arrow(stage, screen, camera_x):
    """Points down at the stage exit so it's easy to spot regardless of
    what its current sprite looks like."""
    rect = stage.exit.rect
    center_x = rect.x + rect.width // 2 - camera_x
    tip_y = rect.y - 10
    arrow_width, arrow_height = 24, 20
    points = [
        (center_x, tip_y),
        (center_x - arrow_width // 2, tip_y - arrow_height),
        (center_x + arrow_width // 2, tip_y - arrow_height),
    ]
    pygame.draw.polygon(screen, YELLOW_COLOR, points)

def _draw_ui(stage, screen):
    _draw_player_hud(stage.player, screen)
    if SHOW_DEBUG_INFO:
        _draw_debug_attack_text(stage.player, screen)
    if stage.warning_manager.active:
        _draw_warning(stage.warning_manager, screen)

def _draw_player_hud(player, screen):
    global _hud_font
    if _hud_font is None:
        _hud_font = pygame.font.SysFont(None, 36)

    x, y = 32, 32
    bar_width, bar_height = 200, 24

    health = player.get_component(HealthComponent)
    hp_ratio = max(0.0, health.health / health.max_health) if health.max_health else 0.0
    pygame.draw.rect(screen, (80, 80, 80), (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, (200, 30, 30), (x, y, int(bar_width * hp_ratio), bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    next_extra_life_score = _get_next_extra_life_score(player.score)
    score_surface = _hud_font.render(
        f"Score: {player.score}   Lives: {player.lives}   Next Life: {next_extra_life_score}",
        True, (255, 255, 255))
    screen.blit(score_surface, (x, y + bar_height + 6))

def _get_next_extra_life_score(score):
    if score < PLAYER_EXTRA_LIFE_SCORE_BASE:
        return PLAYER_EXTRA_LIFE_SCORE_BASE
    milestones_passed = (score - PLAYER_EXTRA_LIFE_SCORE_BASE) // PLAYER_EXTRA_LIFE_SCORE_STEP
    return PLAYER_EXTRA_LIFE_SCORE_BASE + (milestones_passed + 1) * PLAYER_EXTRA_LIFE_SCORE_STEP

def _draw_warning(warning_manager, screen):
    global _warning_font
    if _warning_font is None:
        _warning_font = pygame.font.SysFont(None, 48, bold=True)

    surface = _warning_font.render(warning_manager.message, True, YELLOW_COLOR)
    x = screen.get_width() // 2 - surface.get_width() // 2
    y = screen.get_height() // 2 - surface.get_height() // 2
    screen.blit(surface, (x, y))

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
