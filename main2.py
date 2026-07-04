def main():
    pygame.init()
    SCREEN_W, SCREEN_H = 800, 600
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    
    # Initialize Game State & Managers
    game_state = GameStateManager()
    audio_mgr = AudioManager()
    
    # Create Player & Enemy
    player = Player(400, 400)
    enemy = Enemy(600, 400, player)
    
    # UI needs reference to player
    ui_mgr = UIManager(player)
    
    # Start Game & Register Entities
    game_state.start_game(player)
    game_state.scene_mgr.register_entity(enemy)
    
    # Setup Event to trigger hitstop on hit
    hit_stop_timer = 0.0
    def on_hit(target, amount, kb):
        nonlocal hit_stop_timer
        hit_stop_timer = 0.05
    EventBus.subscribe("hit_landed", on_hit)
    
    running = True
    while running:
        raw_dt = clock.tick(60) / 1000.0
        raw_dt = min(raw_dt, 0.25)
        
        # 1. INPUT
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: game_state.toggle_pause()
                if event.key == pygame.K_g: 
                    player.get_component(GrabController).try_grab([enemy])
                if event.key == pygame.K_f:
                    grabber = player.get_component(GrabController)
                    if grabber.grabbed_target: grabber.throw_target()
        
        # 2. UPDATE (Only if Playing)
        if game_state.state == "Playing":
            if hit_stop_timer > 0:
                hit_stop_timer -= raw_dt
            else:
                # Player Input
                player.get_component(InputController).handle_input(keys)
                
                # Timers & Scene (Entities + Particles)
                TimerManager.update(raw_dt)
                game_state.scene_mgr.update(raw_dt)
        
        # 3. RENDERING
        screen.fill((30, 30, 40))
        if game_state.scene_mgr:
            # Depth sort
            entities = game_state.scene_mgr.entities
            entities.sort(key=lambda e: e.z)
            
            for ent in entities:
                # Simple 2.5D Draw
                sx, sy = ent.x, ent.z - ent.y
                pygame.draw.ellipse(screen, (0,0,0), (sx - 20, sy - 10, 40, 10)) # Shadow
                color = getattr(ent, 'color', (150, 150, 150))
                pygame.draw.rect(screen, color, (sx - 20, sy - 80, 40, 80)) # Body
                
                # Debug Hitbox
                hb = ent.get_component(HitboxComponent)
                if hb and hb.active:
                    pygame.draw.rect(screen, (255,100,100), (sx, sy-60, 30, 40), 2)
        
        if game_state.state == "Paused":
            font = pygame.font.SysFont("Arial", 50)
            text = font.render("PAUSED", True, (255, 255, 255))
            screen.blit(text, (SCREEN_W//2 - 80, SCREEN_H//2))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()