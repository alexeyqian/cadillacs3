# cadillacs3

A a 2D side-scrolling beat-em-up based on game: cadillacs and dinosaurs.
using pygame.

1. Components (Data & Passive Logic)
2. Controllers (Active Logic & State Machines)
3. Managers (Global Systems)

# main loop order:
    - intention before movement
    - timers before movement
    - movement before combat
    - combat before reactions

1. collect input
2. update player intent
3. update enemy AI intent
4. move entities
5. clamp to arena / lane / world bounds
6. resolve body collisions
7. resolve attacks and hitboxes
8. apply damage / hitstun / knockback
9. update waves and spawn logic
10. update camera lock / camera position
11. update effects, floating text, loot
12. remove dead or expired objects
13. draw background
14. draw stage objects behind characters
15. draw characters sorted by feet_y
16. draw front props
17. draw effects
18. draw UI
19. flip display