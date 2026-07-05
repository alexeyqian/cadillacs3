
def draw(stage, screen):
    _draw_world(stage, screen)
    _draw_ui(stage, screen)

def _draw_world(stage, screen):
    camera = stage.camera
    stage.background.draw_far_and_mid(screen, camera.x)

def _draw_ui(stage, screen):
    pass