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



In this codebase's convention: x = left/right, z = depth (the character's position on the ground plane, up/down within the walkable "lane" band), y = height above the ground (jump elevation, 0 when standing). This matches the standard 3D "Y-up" convention (Unity/Godot use the same: X-right, Y-up, Z-forward).
The screen, however, is flat — pygame only has one vertical axis, and pixel 0 is the top of the window. So rendering has to project the 3D-ish world position down onto that single screen axis: a character's vertical pixel position is "how far into the lane they are" (z, larger = lower on screen/closer to camera) minus "how high they've jumped" (y, jumping should move the sprite up on screen, i.e. to a smaller pixel value). Hence screen_y = z - y. It's not a meaningful "z minus y" in an abstract sense — it's the collapse of two separate world axes (depth and height) into pygame's one screen-vertical axis, with jump height subtracted because "up" in the world is "down" in pixel-value terms.

That formula is a conversion between coordinate spaces (world → screen), so it deserves one canonical function rather than being reimplemented inline wherever a sprite gets drawn.