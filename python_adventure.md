Start Planning Time:        2019-05-25  00:15

End first planning session: 2019-05-25  01:45

Start first research session:  2019-05-25  14:17

End first research session:  2019-05-25  14:19

Start Second planning session:  2019-05-25  22:16

End Second planning session: 2019-05-25  23:21


Total Planning Time:  2hrs 35mins

----

## Room and Action descriptions

#### Intro:
You wake up on a dirt floor with no recolection of how you came to be here.
`<Continue with "Look" in Room_ID=0>`

#### Room 0:
You are in a small stone room with no furnishings.  Near the doorway is a tablet with writing on it.
`<Tablet object lives here.>`


#### Room 1:
You are in a small clearing at the bottom of a steep valley.  There appear to be a few small stone houses in the area, and a path leading off to the east.


#### Room 2:
You are in what appears to have been a small herb garden.  Few plants are still growing, and much of the area has been overgrown with weeds.
`<Onion object lives here.>`


#### Room 3:
You are in a small stone room with no furnishings.


#### Room 4:
You are on a path through some dense woods.  There is a fork in the path here.


#### Room 5:
You are standing before a large stone archway with a gate set in it.
`<Gate object lives here.  Write Gate status>`

#### Room 6:
You are at the edge of a small lake in the valley.  The water appears to be clear and calm.
```
<Creature object starts here.>
<Water object lives here.>
```

#### Room 7: \[END]
*Placeholder room for end of game.*

-----

### Map

```
       RM2
        |
        |
RM0 -- RM1 -- RM4 -- RM5 [] END
        |      |
        |      |
       RM3    RM6
```


-----

### Function planning

`Get_Room_Description(int Room_ID)` -- Return string description of specified Room_ID

`Get_Room_Exits(int Room_ID)` -- Return ordered list of connected Room_ID: (North,East,South,West)

`Parse_Command(string Command)` -- Extract first word as command, then call related function with remainder of string as parameter?
  - --> Default:  "I don't understand that command."
  - --! Remember to include a "Help" function to list permitted commands!

`GetObjectID(string Name)` -- Int.  Find object which matches `Name` in the object list and return that object's ID.  Returns `-1` if not found.

`IsUsable(int Object_ID)` -- Boolean.  Look up if the given object works with the `Use` command.

`IsTakable(int Object_ID)` -- Boolean.  Look up if the given object works with the `Take` command.

`GetTakeMessage(int Object_ID)` -- String. Returns the string description for taking the given object.

`GetObjectStatus(int Object_ID)` -- Int.  Look up the current status of an object.  What this means varies by object.

`GetStatusMessage(int Object_ID)` -- String.  Returns the status string for the given object's current status.

`GetObjectRoom(int Object_ID)` -- Int.  Returns the `Room_ID` where the object currently is.



-----

### Other design thoughts

Tracking objects intelligently:
- Have each important/interactable object keep it's current Room_ID location?
  - **Iterate through list of notable objects during each "Look" command to see what additional text to display.**
- "Creature" object moves around once turn_count > 6 (10?)
- "Creature" object gets actively hungry and will eat (and maybe hunt?) player after turn_count > 24
- Game ends when the gate is opened or when player gets eaten.

-----

### Commands

- `Look`
- `Examine <Object>`
- `Take <Object>`
- `Use <Object>`
- Directions
  - `N` or `North`
  - `E` or `East`
  - `S` or `South`
  - `W` or `West`
- `Help`

-----

### List of objects for tracking

1. Tablet
   - Flags:
     - Usable? False
	 - Takable?  False
   - Description: `As each eon comes to a close an individual is chosen to open the gate to prosperity for posterity.  As you now read this, know that you have been selected for this task.  Seek ye the gate and the key and pass through, that those who come after may follow.`
   - Status:  ``
1. Gate
   - Flags:
     - Usable? **True**
	 - Takable?  False
   - Description: `The gate is formed of some gleaming metal and appears to be polished to a high luster.`
   - Status:
     - Locked: `The gate is locked.`
     - Unlocked: `The gate is unlocked.`
1. Garden
   - Flags:
     - Usable? False
	 - Takable?  False
   - Description: `The garden is almost completely overgrown with weeds.  There appear to still be some onions growing off to one side.`
   - Status:  ``
1. Onion
   - Flags:
     - Usable? **True** (Only from inventory)
       - Use_Message:  `You offer the onion to the creature, which accepts it with a broad smile.  The creature removes the shiny object hanging from its neck and hands it to you before wandering off to eat`
	 - Takable?  **True**
	   - Take_Message:  `You dig up a fresh onion and take it with you.`
   - Description: ``
   - Status:  ``
1. Creature
   - Flags:
     - Usable? False
	 - Takable?  False
   - Description: `The creature walks in a constant slouch and still stands nearly twice your height.  There is a shiny object hanging by a thong from its neck. It seems hungry.`
   - Status:
     - Friendly: `There is a large bipedal creature here.  You hear it mumble about needing something to eat.`
	 - Hostile: `There is a large bipedal creature here.  It has a hungry look in its eyes when it sees you.`
1. Water
   - Flags:
     - Usable? False
	 - Takable?  False
   - Description: `The water appears to be clean and clear.`
   - Status:  ``
1. Key?
   - Flags:
     - Usable? **True**
	 - Takable?  False
	   - Take_Message:  `You have received a key.`
   - Description: `It looks like a gleaming brass key.`
   - Status:  ``

-----

### Data structure

#### Rooms:

- List: Room_ID (Each room gets a slot in the list.  Room_ID == index_in_list)
  - List: Room_data (The actual content of each index in the `Rooms` list is a list containing ordered data for the respective room.)
    - String: Description
    - List: Connected_Rooms (Ordered size 4 list of rooms reachable from this room. Only lists `Room_ID` for the room in the given direction.  `-1` if no connection. Ordered as `North`,`East`,`South`,`West`.)
    
#### Objects:

- List: Object_ID (ID of each object is not really used in program, but is just the index of the object within this list.)
  - List: Object_Data (Ordered list of individual data items for each object.)
    - String: Object_Name
    - String: Description
    - Int: Current_Room_ID
    - Boolean: Usable?
    - Boolean: Takable?
    - Int: Status
    - String: Use_String
    - String: Take_String
    - List: Status_Strings (Ordered list of strings for each status used by this item in the `Status` Int above.)

#### "Global" variables:

- *Player_Room* - Int.  `Room_ID` where Player currently is.
- *Inventory* - List \[Int].  List of objects Player currently has.
- *Turn_Count* - Int.  How many turns/actions have passed since the starting the game.
- *Win_Message* - String.  Message to display when Player wins.
- *Lose_Message* - String.  Message to display when Player loses.




