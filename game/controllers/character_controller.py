class CharacterController:
    """The Master State Machine. Prevents illegal actions."""
    def __init__(self):
        self.state = "idle"
        
    def can_act(self):
        return self.state in ["idle", "walk", "run", "jump", "attack", "chase"]
    
    def set_state(self, new_state: str):
        if self.state == "dead": return
        self.state = new_state