# Evennia Mudlet Mapper

A Mudlet mapping script to create simple mapping across your world

## 1. Import the script to Mudlet

Download the script here: [evennia-mapper.xml](https://github.com/RodRitter/Evennia-Doodads/blob/main/Evennia%20Mudlet%20Mapper/evennia-mapper.xml)

## 2. Project Setup

### Overview

- We will use the hook: `Character:at_after_move()`
- `self.msg(location=location_data)`
  - This will send data via OOB comms (GMCP)
- `self.msg(prompt=f"{self.hp} HP, {self.mana} MP")`
  - This will trigger the script to use the data above to create a room in Mudlet Mapper

### Step-by-step Setup

#### Prerequisites

1. The "area" is the room which contains the regular "rooms"

```
# You are in Limbo
> dig City of Helmstead (ID: 2)
> dig Cobblestone Road (ID: 3)
> teleport #3 to #2

# Now you have "City of Helmstead" as your *area*, which contains a room
```

#### Step-by-step Code

```
# characters.py

class Mapper(DefaultCharacter):
    """
    When this character runs around, it will send the appropriate
    data to for the EvenniaMapper script to use for building the map
    """

    def get_exit_names(self):
        """
        This will return a rooms list of cardinal exits
        in their short form
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
        loc = self.location
        if loc.location:
            exit_names = self.get_exit_names()
            loc_gmcp = {
                "area_id": loc.location.id,
                "area_name": loc.location.name,
                "room_id": loc.id,
                "room_coord": "%s,%s,%s" % loc.db.coord,
                "room_exits": exit_names
            }
            self.msg(location=(loc_gmcp))

    def at_after_move(self, source_location):
        super().at_after_move(source_location)
        self.send_gmcp() # Send GMCP data
        self.prompt()    # Prompt for Mudlet script to trigger
```
