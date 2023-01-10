import json

# import GameObjects.json
def welcome_message():
    print(
        """Welcome to the Escape Room Game!
In this game, you will be locked in a room and must find the three-digit code to escape.
You will have a limited number of attempts to guess the code.
You can interact with various objects in the room to gather clues about the code.
Good luck, and have fun trying to escape!
"""
    )


class GameObject:
    def __init__(self, name, appearance, feel, smell):
        self.name = name
        self.appearance = appearance
        self.feel = feel
        self.smell = smell

    def look(self):
        return f"You look at the {self.name}. {self.appearance}\n"

    def touch(self):
        return f"You touch the {self.name}. {self.feel}\n"

    def sniff(self):
        return f"You sniff at the {self.name}. {self.smell}\n"


class Room:
    escape_code = 0
    game_objects = []

    def __init__(self, escape_code, game_objects):
        self.escape_code = escape_code
        self.game_objects = game_objects

    # Returns whether the code of the room matches the code entered by the player
    def check_code(self, code):
        return self.escape_code == code

    # Returns a list with all the names of the objects we have in our room
    def get_game_object_names(self):
        names = []
        for object in self.game_objects:
            names.append(object.name)
        return names


class Game:
    def __init__(self):
        # Number of attempts the player has made on the escape code of the room
        self.attempts = 0

        with open("GameObjects.json") as f:
            data = json.load(f)
        objects = []
        for obj in data["game_objects"]:
            objects.append(
                GameObject(obj["name"], obj["appearance"], obj["feel"], obj["smell"])
            )
        self.escape_code = data["escape_code"]
        self.room = Room(self.escape_code, objects)

    def take_turn(self):
        prompt = self.get_room_prompt()
        selection = input(prompt)
        if selection == "q":
            print("Cheeky!! You are trapped in a mysterious room, with no idea how you got there. The only way out is to find the secret code")
            self.take_turn()
        else:
            selection = int(selection)
        if selection >= 1 and selection <= 5:
            self.select_object(selection - 1)
            self.take_turn()
        
        else:
            is_code_correct = self.guess_code(selection)
            if is_code_correct:
                print("Congratulations!! You Win!!")
            else:
                if self.attempts == 3:
                    print(
                        "\nGame Over!! You ran out of guesses. Better luck next time!\n"
                    )
                else:
                    print(f"\n Incorrect. You have used {self.attempts}/3 attempts.\n")
                    self.take_turn()

    def get_room_prompt(self):
        prompt = "Enter 3 digit lock code or choose an item to interact with: \n"
        names = self.room.get_game_object_names()
        index = 1
        for name in names:
            prompt += f"{index} . {name}\n"
            index += 1
        return prompt

    def select_object(self, index):
        selected_object = self.room.game_objects[index]
        prompt = self.get_object_interaction_string(selected_object.name)
        interaction = input(prompt)
        clue = self.interact_with_object(selected_object, interaction)
        print(clue)

    def get_object_interaction_string(self, name):
        return f"How do you want to interact with the {name}?\n1. Look\n2. Touch\n3. Smell\n"

    def interact_with_object(self, object, interaction):
        
         if interaction == "1":
             return object.look()
         elif interaction == "2":
             return object.touch()
         elif interaction == "3":
             return object.sniff()
         else:
             return "Enter a Valid interaction.\nReturning back to Object Selection\n"
                
            

    def guess_code(self, code):
        if self.room.check_code(code):
            return True
        else:
            self.attempts += 1
            return False


game = Game()
welcome_message()
game.take_turn()
