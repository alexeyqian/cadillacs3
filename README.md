# cadillacs3

1. Components (Data & Passive Logic)
2. Controllers (Active Logic & State Machines)
3. Managers (Global Systems)


1. Scene (The Technical Container)
What it is: A Scene is an engine-level concept. It represents everything currently loaded into the computer's memory and drawn on the screen.
Relationship: A scene contains the SceneManager, the Camera, the UIManager, the Player, and the current LevelManager.
Example: "Main Menu Scene", "Character Select Scene", "Gameplay Scene", "Game Over Scene".
Note: In our Python code, we don't explicitly swap Python files for scenes, but in engines like Unity or Godot, moving from the Main Menu to the Game involves loading a completely new Scene file.


# main loop order:
    - intention before movement
    - timers before movement
    - movement before combat
    - combat before reactions