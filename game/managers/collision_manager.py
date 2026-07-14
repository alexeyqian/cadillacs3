from game.components.collision_box_component import CollisionBoxComponent


class CollisionManager:
    """Keeps character bodies from overlapping. Runs after movement each
    frame (positions are already integrated) and before attacks/combat, so
    hitbox checks always see already-separated, physically valid positions -
    this is what stops a fast mover (e.g. a run attack) from sliding clean
    through another character instead of bumping into them."""

    #  character-vs-character collision
    # add other collisions later
    def resolve(self, characters):
        for i, a in enumerate(characters):
            if not a.alive:
                continue
            box_a = a.get_component(CollisionBoxComponent)
            if not box_a:
                continue

            for b in characters[i + 1:]:
                if not b.alive:
                    continue
                box_b = b.get_component(CollisionBoxComponent)
                if not box_b:
                    continue

                # A held target is deliberately kept right next to its
                # grabber (see GrabController) - pushing them apart here
                # would fight that every frame and drag both into a runaway
                # drift as each push gets immediately re-snapped back.
                if a.is_grabbed or b.is_grabbed:
                    continue

                self._separate(a, b, box_a.get_rect(), box_b.get_rect())

    def _separate(self, a, b, rect_a, rect_b):
        # Only ever push apart on x. The box's z-extent (depth/lane
        # thickness) is intentionally much smaller than its x-extent, so a
        # standard "push along the axis of least overlap" heuristic would
        # almost always pick z for two characters sharing a lane - which
        # does nothing to stop horizontal pass-through, the actual problem.
        if not rect_a.colliderect(rect_b):
            return

        overlap_x = min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left)
        if overlap_x <= 0:
            return

        push = overlap_x / 2
        if a.x <= b.x:
            a.x -= push
            b.x += push
        else:
            a.x += push
            b.x -= push
