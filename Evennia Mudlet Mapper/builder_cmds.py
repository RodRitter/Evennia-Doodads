
from evennia.commands.command import Command
from evennia.commands.default.building import CmdTunnel
from evennia import CmdSet, create_object, search_object

class CmdTunnel(CmdTunnel, Command):
    """
    Tunnel a room and maintain the "area" (parent room). Additionally
    this will also generate automatic coordinates and prevent
    overlapping rooms.

    Usage:
        tunnel <n/s/e/w> <room_name> <typeclass>
        tun <n/s/e/w> <room_name> <typeclass>
    """

    key = "tunnel"
    aliases = ["tun"]
    lock = "cmd:perm(Builders)"
    help_category = "Building"

    def parse(self):
        self.args_str = self.args.strip()
        self.args = self.args.strip().split()

    def func(self):
        if len(self.args) == 0:
            self.caller.msg("Usage: tunnel [n/s/e/w] [room_name]")
            return

        direction = None
        room_name = "Room" if len(self.args) == 1 else self.args[1]
        raw_dir = (0,0,0)

        if "=" in self.args_str:
            index = self.args_str.index("=")
            room_name = self.args_str[index+1:].strip()

        cardinal_arg = self.args[0].strip()

        if cardinal_arg == "n" or cardinal_arg == "north":
            direction = ("north", "n")
            raw_dir = (0,1,0)
        elif cardinal_arg == "s" or cardinal_arg == "south":
            direction = ("south", "s")
            raw_dir = (0,-1,0)
        elif cardinal_arg == "e" or cardinal_arg == "east":
            direction = ("east", "e")
            raw_dir = (1,0,0)
        elif cardinal_arg == "w" or cardinal_arg == "west":
            direction = ("west", "w")
            raw_dir = (-1,0,0)
        elif cardinal_arg == "ne" or cardinal_arg == "northeast":
            direction = ("northeast", "ne")
            raw_dir = (1,1,0)
        elif cardinal_arg == "se" or cardinal_arg == "southeast":
            direction = ("southeast", "se")
            raw_dir = (1,-1,0)
        elif cardinal_arg == "sw" or cardinal_arg == "southwest":
            direction = ("southwest", "sw")
            raw_dir = (-1,-1,0)
        elif cardinal_arg == "nw" or cardinal_arg == "northwest":
            direction = ("northwest", "nw")
            raw_dir = (-1,1,0)
        else:
            self.caller.msg("Not a valid direction")
            return

        current_room = self.caller.location

        # Search for target location
        curr_coord = current_room.db.coord
        target_coord = tuple(map(sum,zip(curr_coord,raw_dir)))
        rooms = search_object(target_coord,  attribute_name="coord")
        target_room = None if len(rooms) == 0 else rooms[0]

        
        if target_room != None:
            if direction[0] not in current_room.get_exit_names():
                create_object(typeclass="typeclasses.exits.Exit", key=direction[0], aliases=[direction[1]], location=current_room, destination=target_room)

                returning_dir = self.cardinal_opposite(direction[0])
                create_object(typeclass="typeclasses.exits.Exit", key=returning_dir[0], aliases=[returning_dir[1]], location=target_room, destination=current_room)
                
                self.caller.msg("Room already exists. Links between rooms created")
            else:
                self.caller.msg("Room already exists.")
            return

        elif direction[0] not in self.caller.location.exits and direction != None:
            room_typeclass = "typeclasses.rooms.Room" if len(self.args) < 3 else self.args[2]
            
            new_room = create_object(typeclass=room_typeclass, key=room_name, home=current_room.location, location=current_room.location)
            new_room.db.coord = target_coord
            # Exit from current_room to new_room
            create_object(typeclass="typeclasses.exits.Exit", key=direction[0], aliases=[direction[1]], location=current_room, destination=new_room)

            returning_dir = self.cardinal_opposite(direction[0])
            create_object(typeclass="typeclasses.exits.Exit", key=returning_dir[0], aliases=[returning_dir[1]], location=new_room, destination=current_room)
            self.caller.move_to(new_room, quiet=True)
            self.caller.msg("Room created!")
        else:
            self.caller.msg("There is already a room in that direction")
    
    def cardinal_opposite(self, dir):
        if dir == "n" or dir == "north":
            return ("south", "s")
        if dir == "s" or dir == "south":
            return ("north", "n")
        if dir == "e" or dir == "east":
            return ("west", "w")
        if dir == "w" or dir == "west":
            return ("east", "e")
        if dir == "ne" or dir == "northeast":
            return ("southwest", "sw")
        if dir == "se" or dir == "southeast":
            return ("northwest", "nw")
        if dir == "sw" or dir == "southwest":
            return ("northeast", "ne")
        if dir == "nw" or dir == "northwest":
            return ("southeast", "se")

class BuildersCmdSet(CmdSet):
    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdTunnel())