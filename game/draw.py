
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
    pass