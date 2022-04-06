# Evennia Mudlet Mapper

A Mudlet mapping script to create simple mapping across your world

![image](https://user-images.githubusercontent.com/4159679/162091771-a781de84-224c-4c90-ae70-b7f69c64c2b8.png)

## 1. Import the script to Mudlet

Download the script here: [evennia-mapper.xml](https://raw.githubusercontent.com/RodRitter/Evennia-Doodads/main/Evennia%20Mudlet%20Mapper/evennia-mapper.xml)

## 2. Project Setup

### Prerequisites

1. Each room needs to have a `coord` attribute: `self.db.coord = (0,0,0)`
2. You will need to either manually set coordinates for rooms, or use a custom `tunnel` command to auto-generate coordinates. You can find a custom `tunnel` command here: [builder_cmds.py](https://github.com/RodRitter/Evennia-Doodads/blob/main/Evennia%20Mudlet%20Mapper/builder_cmds.py)
3. In this example, an "area" is the room which contains the regular "rooms".

```
# You are in Limbo
> dig City of Helmstead (ID: 2)
> dig Cobblestone Road (ID: 3)
> teleport #3 to #2

# Now you have "City of Helmstead" as your *area*, which contains a room
```

If you prefer, you can manually set an area at `area_name` in the GMCP object instead of having nested rooms.

### Step-by-step: The Mapper character

```
# characters.py

class Mapper(DefaultCharacter):
    """
    When this character runs around, it will send the appropriate
    data for the EvenniaMapper script to use for building the map
    """


    def get_exit_names(self):
        """
        This will return a rooms list of cardinal exits in their
        short form, along with the destination room ID's

        The format should be:
        room_exits = {
            e: 359,
            nw: 374,
        }
        """
        shortmap = {
            "north": "n",
            "south": "s",
            "east": "e",
            "west": "w",
            "northeast": "ne",
            "southeast": "se",
            "southwest": "sw",
            "northwest": "nw",
        }
        exit_names = {}
        for exit in self.location.exits:
            if exit.name in shortmap:
                exit_names[shortmap[exit.name]] = exit.destination.id
        return exit_names


    def prompt(self):
        char_prompt = "This prompt will trigger Mudlet Mapper"
        self.msg(prompt=char_prompt)


    def send_gmcp(self):
        """
        Here we will setup the location data and send it via GMCP
        """
        loc = self.location
        if loc.location:
            exit_names = self.get_exit_names()
            loc_gmcp = {
                "area_id": loc.location.id,
                "area_name": loc.location.name,
                "room_id": loc.id,
                "room_coord": "%s,%s,%s" % loc.db.coord, # Format: "x,y,z"
                "room_exits": exit_names
            }
            self.msg(location=(loc_gmcp))

    def at_after_move(self, source_location):
        super().at_after_move(source_location)
        self.send_gmcp() # Send GMCP data
        self.prompt()    # Prompt for Mudlet script to trigger
```
