

import time

class LucidDream:
    def __init__(self):
        self.awake = False
        self.meditation_time = 0

    def enter_lucid_dream(self):
        """Initiates the lucid dream."""
        self.awake = True
        return "You are now lucid dreaming!"

    def exit_lucid_dream(self):
        """Ends the lucid dream."""
        self.awake = False
        return "You have exited the lucid dream."

    def is_lucid(self):
        """Checks if currently lucid dreaming."""
        return self.awake

    def set_meditation_time(self, minutes):
        """Sets the meditation duration in minutes."""
        self.meditation_time = minutes
        return f"Meditation time set to {minutes} minutes."

    def meditate(self):
        """Guides the user through a meditation technique."""
        if self.meditation_time <= 0:
            return "Please set a meditation time before starting."

        print("Starting meditation...")
        for i in range(self.meditation_time):
            time.sleep(1)  # Simulate a minute passing (use shorter time for demonstration)
            print(f"Minute {i + 1}: Focus on your breathing and let go of distractions.")

        print("Meditation complete. You are relaxed and focused.")
        return "Meditation complete."

    def lucid_dream_technique(self):
        """Provides a built-in technique for enhancing lucid dreaming."""
        return (
            "To enhance your lucid dreaming experience, follow this technique:\n"
            "1. Relax your body completely before sleep.\n"
            "2. Focus on a specific intention, like flying or meeting someone.\n"
            "3. Use reality checks, such as pinching your nose and trying to breathe.\n"
            "4. Keep a dream journal to improve dream recall."
        )
