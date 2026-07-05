
def draw(stage, screen):
    _draw_world(stage, screen)
    _draw_ui(stage, screen)

def _draw_world(stage, screen):
    camera = stage.camera
    stage.background.draw_far_and_mid(screen, camera.x)
    entities = stage.get_all_entities()
    # depth sorting
    entities.sort(key=lambda e: e.z)
    for entity in entities:
        entity.draw(screen, camera.x)

def _draw_ui(stage, screen):
    pass