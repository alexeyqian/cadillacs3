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

Other places that touch x/z (hitbox/hurtbox components, distance checks, depth-sort in draw.py) stay as-is — those operate in world space for gameplay logic (collision, sorting), not screen pixels, so they don't need this conversion.

Complete each phase for all entities before starting the next. Never interleave — if you did entity.update_intention(); entity.update_movement() per entity in one loop, an enemy's AI could read the player's already-moved position this frame instead of last frame's, making behavior depend on entity list order.

update_movement must never read another entity's live state — it only touches the entity's own vx/vz/x/z. That's what makes it safe to run in any order.

GameObject — the generic, engine-level concept: "a thing that exists in the world with a position, and can hold components." It carries no assumption about whether the thing is alive, active, or gameplay-relevant. A camera rig, a background layer, a spawn-point marker, a static wall, and a player character could all be GameObjects. This is the Unity sense of the word — deliberately minimal.

Entity — the gameplay-relevant subset: something with identity and agency in the simulation — it updates every frame, has state that changes, and usually participates in combat/interaction (can deal or take damage, gets iterated by AI/physics/combat systems). In classic ECS architecture "Entity" is stripped down even further to just an ID with no behavior at all, but in most brawler codebases (not strict ECS) it informally means "an active participant," as opposed to passive scenery.

The practical dividing line in a 2D beat-em-up specifically: does it need to be iterated by gameplay systems every frame (movement, AI, combat resolution), or is it just there to be drawn/collided with once? Player, enemies, projectiles, pickups, breakable props → entities. Background art, camera, static tile geometry → GameObjects (or not even that — often just rendering data with no update loop).


Combo attack:
InputReader.attack_pressed is now edge-triggered (true only the frame J is newly pressed, not while held) — holding the button no longer auto-chains through the combo; each hit needs its own distinct press.
Character.combo_window_timer starts counting down the moment a hit finishes (= current_attack.combo_window); a press within that window continues to the next hit, a press after it expires resets to hit 1.
Doesn't loop past 3: combo_index is clamped (min(combo_index + 1, len - 1)), and hit 3 has combo_window=0, so there's nothing to advance into.