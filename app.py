from collections import deque

class Room:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.exits = {}

    def connect(self, direction, other_room):
        self.exits[direction] = other_room

    def describe(self):
        lines = [f"\n📍 You are in the {self.name}.", self.desc]
        if self.exits:
            lines.append("🚪 Exits: " + ", ".join(f"{d} -> {r.name}" for d, r in self.exits.items()))
        else:
            lines.append("No exits from here.")
        return "\n".join(lines)

class Game:
    def __init__(self):
        self.rooms = {}
        self.create_world()
        self.player_room = self.rooms['Entrance']

    def create_world(self):
        # Create rooms
        r = lambda n, d: Room(n, d)
        entrance = r("Entrance", "An old wooden door creaks behind you. The hall lies ahead.")
        hall = r("Hall", "Portraits of knights watch silently.")
        kitchen = r("Kitchen", "You smell something burnt. A rusty knife lies on the counter.")
        library = r("Library", "Dusty books line the shelves. Something glimmers between them.")
        garden = r("Garden", "Overgrown vines cover the walls.")
        tower = r("Tower", "A spiral staircase winds upward.")
        treasure = r("Treasure Room", "💎 You found the treasure chest filled with gold!")

        # Connect rooms (graph edges)
        entrance.connect('north', hall); hall.connect('south', entrance)
        hall.connect('east', kitchen); kitchen.connect('west', hall)
        hall.connect('west', library); library.connect('east', hall)
        hall.connect('north', garden); garden.connect('south', hall)
        garden.connect('up', tower); tower.connect('down', garden)
        tower.connect('north', treasure); treasure.connect('south', tower)

        for room in [entrance, hall, kitchen, library, garden, tower, treasure]:
            self.rooms[room.name] = room

    def bfs_shortest_path(self, start_name, goal_name):
        """Find shortest path using BFS"""
        start, goal = self.rooms[start_name], self.rooms[goal_name]
        queue = deque([start])
        parent = {start.name: None}
        visited = {start.name}

        while queue:
            current = queue.popleft()
            if current.name == goal.name:
                path = []
                while current:
                    path.append(current.name)
                    current = self.rooms[parent[current.name]] if parent[current.name] else None
                return path[::-1]
            for direction, neighbor in current.exits.items():
                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    parent[neighbor.name] = current.name
                    queue.append(neighbor)
        return None

    def play(self):
        print("🎮 Welcome to the Adventure Game!")
        print("Type directions (north, south, east, west, up, down) to move.")
        print("Type 'auto' to find the shortest path to the treasure.")
        print("Type 'exit' to quit.\n")

        while True:
            print(self.player_room.describe())
            command = input("\n➡️ What do you want to do? ").strip().lower()

            if command == "exit":
                print("👋 Thanks for playing! Goodbye!")
                break

            elif command == "auto":
                path = self.bfs_shortest_path(self.player_room.name, "Treasure Room")
                print("\n🧭 BFS Path to Treasure:")
                print(" -> ".join(path))
                if self.player_room.name != "Treasure Room":
                    print("\nFollowing the path automatically...")
                    for step in path[1:]:
                        print(f"Moving to {step}...")
                    print("\n💎 Congratulations! You reached the Treasure Room!")
                    break

            elif command in self.player_room.exits:
                self.player_room = self.player_room.exits[command]
                if self.player_room.name == "Treasure Room":
                    print("\n💎 You found the Treasure Room! Game Over!")
                    break
            else:
                print(" Invalid command! Try a valid direction or 'auto'.")

# Run the game
if __name__ == "__main__":
    game = Game()
    game.play()
