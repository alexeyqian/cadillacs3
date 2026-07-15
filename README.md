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

Most classic beat-em-ups (Streets of Rage, Final Fight, Double Dragon) don't model hitbox-vs-hitbox collision at all — hitboxes only test against hurtboxes, so if both attacks are active on the same frame, both land and both take damage (a straightforward "trade")

flanking and attacker-slot limiting
Genre convention is less about real pathfinding (arenas are simple x/z lanes, no navmesh needed) and more about two specific tricks: (1) capping simultaneous attackers — only a few enemies (e.g. 2–4) are ever allowed to actively close in and attack at once, the rest hang back circling/faking so the player isn't overwhelmed instantly, and (2) flanking instead of direct-chase — each enemy targets an offset position around the player (spread across x and lane/z) rather than the player's exact coordinates, so they surround rather than stack into a single-file conga line.

Exit stage flow:
clear waves → attack the door → it opens → walk into it → stage advances.

Backgrounds:

4-5 layers is the practical sweet spot for this genre, and the breakdown you listed maps almost exactly onto genre convention (Streets of Rage 4, Final Fight): sky/far (near-static or barely moving), far-mid (softened/blurred secondary buildings), near background (sharp detail right behind the playable lane), playable ground (moves 1:1 with characters), and foreground decoration (scrolls faster than the player — railings/plants passing in front, occluding characters briefly for a strong depth cue). Going beyond 5 has diminishing returns — more art to produce and maintain, more draw calls, and it gets hard to keep a consistent art direction across that many independent layers.

Split into 3 (or more) source images: a begin tile (the entry, with the door on the left), a middle tile (one repeatable arch/column/window unit — needs to be cropped so its right edge tiles seamlessly against its own left edge), and an end tile (the staircase section on the right). Each stays small in memory regardless of how long the stage is.

chasing on z axis
Avoids the "conga line" — if every chasing enemy beelines onto the player's exact Z, they all converge onto the same row and visually stack/queue single-file as they close in, which reads as robotic. Loose Z during the chase lets each enemy approach on more of a diagonal from wherever they started, arriving at slightly different Z rows
Reduces jitter — the player's Z wobbles constantly during normal movement; without a deadzone, every chasing enemy's move_z flickers direction in response, which is visible as twitchy back-and-forth micro-corrections.