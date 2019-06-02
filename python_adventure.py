# Example Python Adventure
# Copyright Tim Rogers 2019
#
# License: CC-BY
# Creative Commons Share-Alike
# https://creativecommons.org/licenses/by/4.0/
#

# A Note:
#       It turns out that Python performs function default parameter binding
#       exactly once, during initial definition of the function.  These defaults
#       are saved as internal variable and reused by the function every time it
#       is called.  This has lots of interesting effects, the currently
#       pertenent one being that all functions in this game needed to have all
#       defaults removed from the function definitions to avoid issues from
#       unrecognized language assumptions.


##### Data lookup functions

#  Define the helper functions so I don't have to remember how
#  I structured everything for every data lookup.

def GetRoomDescription( roomID, roomList ):
    ''' Returns the description string from the specified Room_ID in the RoomList list.'''
    return roomList[roomID][0]

def GetRoomExits( roomID, roomList ):
    ''' Returns the list of room connections from the specified Room_ID in the RoomList list.'''
    return roomList[roomID][1]

def GetObjectID( objectName, objectList ):
    '''
    This will try to find an object which has a Name or Alias matching the objectName input.
    If found, it will return the matching objectID.  Otherwise it will return -1.
    '''
    # We'll need to check each possible item in the object list...
    for itemNum in range(len(objectList)):
        # Is this the proper name of this item?
        if objectName == objectList[itemNum][0]:
            return itemNum
        # Maybe they typed an alias instead of the object's proper name?
        for alias in objectList[itemNum][1]:
            if objectName == alias:
                return itemNum
    # Didn't find it.  Return a non-valid index.
    return -1

def IsUsableObject( objectID, objectList ):
    '''
    Returns the boolean for if this object is a valid target for the "Use" command.
    '''
    return objectList[objectID][4]

def SetUsableObject( objectID, newValue, objectList ):
    '''
    Sets the boolean for if this object is a valid target for the "Use" command.
    For proper logic comparisons, this new value MUST be a boolean.
    '''
    objectList[objectID][4] = bool(newValue)

def GetUseMessage( objectID, objectList ):
    '''
    Returns the string to display if this object is "Used".
    '''
    return objectList[objectID][7]

def IsTakableObject( objectID, objectList ):
    '''
    Returns the boolean for if this object is a valid target for the "Take" command.
    '''
    return objectList[objectID][5]

def GetTakeMessage( objectID, objectList ):
    '''
    Returns the string to display if this object is "Taken".
    '''
    return objectList[objectID][8]

def GetObjectStatus( objectID, objectList ):
    '''
    Returns the numeric status for the given object.
    '''
    return objectList[objectID][6]

def SetObjectStatus( objectID, newStatus, objectList ):
    '''
    Sets the numeric status for the given object.
    Status values are always expected to be "int" types.
    '''
    objectList[objectID][6] = int(newStatus)

def GetObjectStatusMessage( objectID, objectList ):
    '''
    Returns the string to display if this object is "Taken".
    '''
    # Intentionally awkward variable name to ensure I don't accidentally
    # use it for something else elsewhere in the program.
    temp_current_object_status = GetObjectStatus(objectID,objectList)
    if temp_current_object_status > -1:
        return objectList[objectID][9][temp_current_object_status]
    return ""

def GetObjectLocation( objectID, objectList ):
    '''
    Returns the room (if any) where the given object is currently located.
    '''
    return objectList[objectID][3]

def SetObjectLocation( objectID, newLocation, objectList ):
    '''
    Sets the room (if any) where the given object is currently located.
    This is intentially required to be an "int" to avoid confusion with later use.
    '''
    objectList[objectID][3] = int(newLocation)

def GetObjectDescription( objectID, objectList ):
    '''
    Returns the description string for the specified object.
    '''
    return objectList[objectID][2]


##### Command handling

# I want a specific function for each command so I can easily follow the code paths later.

def CommandHelp():
    '''
    Prints the list of permitted commands.
    '''
    print('''
Commands:
  Help
  Inventory
  Look
  Examine <Object>
  Take <Object>
  Use <Object>
  N or North
  E or East
  S or South
  W or West
  Exit

''')

def CommandLook( roomID, roomList, objectList):
    '''
    Writes the specified room's description, the status of any objects in the room,
    and lists the exits from the specified room.
    '''
    # Print the room description.  We should always have one.
    print(GetRoomDescription(roomID,roomList))
    # Next we check for any items in this room.
    for item in range(len(objectList)):
        if GetObjectLocation(item,objectList) == roomID:
            # We have an item in this room.  Does it have a status message?
            # Checking the length should give a valid number even if the status doesn't exist.
            if len(GetObjectStatusMessage(item,objectList)) > 0:
                # We have a real message.  Print it.
                print(GetObjectStatusMessage(item,objectList))
    # We're done printing descriptions.  All that's left is to list the exits.
    localExits = GetRoomExits(roomID,roomList)
    # Parse out the individual directions for printing...
    exitString = "Exits are:  "
    if localExits[0] > -1:
        exitString += "North  "
    if localExits[1] > -1:
        exitString += "East  "
    if localExits[2] > -1:
        exitString += "South  "
    if localExits[3] > -1:
        exitString += "West  "
    # Last step is to print our list of exits.
    #Special case sanity check.  If there are no exits, print nothing.
    if len(exitString) > len("Exits are:  "):
        print(exitString)

def CommandExamine( objectName, roomID, roomList, objectList, playerInventory):
    '''
    Tries to examine the specified object.
    '''
    # Declaring the default failure string, that way players can't fish for item names.
    examineFailString = 'You do not see anything that is called that.'
    # Convert our input into a numeric ID that we can use.
    currentObjectID = GetObjectID(objectName,objectList)
    if currentObjectID < 0:
        # Doesn't match a defined object.  Print the failure string.
        print(examineFailString)
        return
    # It's a defined object.  Does the player have it with them?
    for item in playerInventory:
        if item == currentObjectID:
            # The player is holding it.
            # Print the object status (if any) and description (if any).
            if len(GetObjectStatusMessage(currentObjectID,objectList)) > 0:
                print(GetObjectStatusMessage(currentObjectID,objectList))
            if len(GetObjectDescription(currentObjectID,objectList)) > 0:
                print(GetObjectDescription(currentObjectID,objectList))
            # If the player was holding it, stop looking for the object.
            return
    # It wasn't in the player's inventory.  Maybe it's in the current room?
    if GetObjectLocation(currentObjectID,objectList) == roomID:
        # It's in the room.  Print the status and description.
        if len(GetObjectStatusMessage(currentObjectID,objectList)) > 0:
            print(GetObjectStatusMessage(currentObjectID,objectList))
        if len(GetObjectDescription(currentObjectID,objectList)) > 0:
            print(GetObjectDescription(currentObjectID,objectList))
        # We found the object.  Return to caller.
        return
    # We didn't find the object.  Print the failure string.
    print(examineFailString)

def CommandTake( objectName, roomID, roomList, objectList, playerInventory):
    '''
    Tries to take the named object.
    '''
    # Declaring the default failure string.
    takeFailString = 'You cannot take that.'
    # Convert our input into a numeric ID that we can use.
    currentObjectID = GetObjectID(objectName,objectList)
    if currentObjectID < 0:
        # Doesn't match a defined object.  Print the failure string.
        print(takeFailString)
        return
    # Is the object in the room?
    if GetObjectLocation(currentObjectID,objectList) == roomID:
        # Object is here.  Can it be taken?
        if IsTakableObject(currentObjectID,objectList):
            # It's takable.  Take it.
            # This involves removing it from the world, adding it to the
            #  player's inventory, and printing any special "take" message.
            SetObjectLocation(currentObjectID,-1,objectList)
            playerInventory += [currentObjectID]
            if len(GetTakeMessage(currentObjectID,objectList)) > 0:
                print(GetTakeMessage(currentObjectID,objectList))
            # Object is now "Taken".  Return to caller.
            return
        # Object not takable.  Default through...
    # Object not present or not takable.  Print failure string.
    print(takeFailString)

def CommandUse( objectName, roomID, roomList, objectList, playerInventory):
    '''
    Try to use an object.
    
    This command is full of special cases.  If this game/library were ever
    modified or extended, this function would likely need almost completely
    rewritten.

    Most player-caused special actions occur inside this function.
    '''
    # First we cover the usual basics, like if the thing can be used at all.
    # Declaring the default failure string.
    useFailString = 'You do not have that.'
    # Convert our input into a numeric ID that we can use.
    currentObjectID = GetObjectID(objectName,objectList)
    if currentObjectID < 0:
        # Doesn't match a defined object.  Print the failure string.
        print(useFailString)
        return
    # It's a defined object.  Does the player have it with them?
    # Adding a tracking variable here so the code doesn't get nested too deeply.
    tempPlayerHasObject = False
    for item in playerInventory:
        if item == currentObjectID:
            # The player is holding it.  Note this.
            tempPlayerHasObject = True
            # Break out of the for loop early for efficiency.
            break
    if not tempPlayerHasObject:
        # Player doesn't have the object.  Print the failure string and return.
        print(useFailString)
        return
    if not IsUsableObject(currentObjectID,objectList):
        # Player has the object but can't use it.  Print failure string and return.
        # This shouldn't happen in this game when unaltered.  Let's mention that.
        print("You can't use that.  This situation shouldn't happen.")
        return
    # At this point, we know the player both *has* and *can use* the object.

    ########
    #### Begin Special Case Handling
    ########

    # We'll start by gathering up our special items so we can identify what
    # we're tying to use.  We can't depend on a simple name check of each item
    # against the input objectName, so we'll be comparing numeric IDs.

    onionID = GetObjectID("Onion",objectList)
    keyID = GetObjectID("Key",objectList)
    # Now we check which one we're actually using.

    ## Onion
    if (onionID == currentObjectID):
        # I guess we're using the onion.
        # The onion only works if the Creature is present.  Let's check that.
        creatureID = GetObjectID("Creature",objectList)
        if GetObjectLocation(creatureID,objectList) == roomID:
            # The creature is present.  Magic can happen.
            # Remove the onion from the player's inventory.
            playerInventory.remove(onionID)
            # Print the onion's "use" message.
            print(GetUseMessage(onionID,objectList))
            # Remove the creature from the world.
            SetObjectLocation(creatureID,-1,objectList)
            # Add the key to the player's inventory.
            playerInventory += [keyID]
            # Print the key's "take" message.
            print(GetTakeMessage(keyID,objectList))
        else:
            # No creaure present.  Print an appropriate failure message.
            print("You can't use that here.")
        # Whether the onion was used or not, return to caller.
        return
    ## End Onion

    ## Key
    elif (keyID == currentObjectID):
        # The key only works if the gate is present.  Check for it.
        gateID = GetObjectID("Gate",objectList)
        if GetObjectLocation(gateID,objectList) == roomID:
            # We're in the room with the gate.  Use the key.
            # Remove the key from the player's inventory.
            playerInventory.remove(keyID)
            # Change the gate status to open.
            SetObjectStatus(gateID,1,objectList)
            # Set a new exit in the gate room
            roomList[roomID][1][1] = 7
            # Print the key's "use" message.
            print(GetUseMessage(keyID,objectList))
        else:
            # No gate present.  Print an appropriate failure message.
            print("You can't use that here.")
        # Whether the key was used or not, return to caller.
        return
    ## End Key

    ## ??? Unknown Usable Item
    # This should never be reached if the game is properly coded.
    # Print a meaningful message to the player.
    print("You don't know how to use that.  You should speak with the developer about this.")

    #### End of magic "Use" handler

def ParseCommand( command, roomList, objectList, playerInventory, roomID, gameTurn ):
    '''
    Attempts to parse the provided string for a valid command.
    If the command is recognized, this will further attempt to process the command.
    '''
    # Set default return for a fresh look around.
    newLook = False
    # Split the command string into "'command' 'object'" if a space is present.
    separator_index = -1
    for position in range(len(command)):
        if command[position] == ' ':
            separator_index = position
            break
    if separator_index < 0:
        # No space, so the command isn't trying to target something.
        localCommand = command
        localObject = None
    else:
        # There's a space.  The first word is our command.  Anything after
        # is assumed to be the object.
        localCommand = command[:separator_index] # Everything before first space
        localObject = command[separator_index+1:] # Everything after first space

    ### Command handling

    # Help
    if (localCommand == "Help") or (localCommand == "HELP") or (localCommand == "help") or \
       (localCommand == "H") or (localCommand == "h") or (localCommand == "?"):
        CommandHelp()
        # Getting the list of commands does not advance game time.
    # Look
    elif (localCommand == "Look") or (localCommand == "LOOK") or (localCommand == "look") or \
         (localCommand == "L") or (localCommand == "l"):
        # Request a look from the calling function to ensure proper timing.
        newLook = True
        gameTurn +=1
    # Examine
    elif (localCommand == "Examine") or (localCommand == "EXAMINE") or (localCommand == "examine") or \
         (localCommand == "Ex") or (localCommand == "EX") or (localCommand == "ex") or \
         (localCommand == "X") or (localCommand == "x"):
        # This command only really works with a target.
        if localObject == None:
            print("You carefully examine nothing.  There was nothing worth noting.")
        else:
            CommandExamine(localObject,roomID,roomList,objectList,playerInventory)
        gameTurn +=1
    # Take
    elif (localCommand == "Take") or (localCommand == "TAKE") or (localCommand == "take") or \
         (localCommand == "T") or (localCommand == "t"):
        # This command also only works with a target.
        if localObject == None:
            print("You grasp at air, but fail to hold on to anything.")
        else:
            CommandTake(localObject,roomID,roomList,objectList,playerInventory)
        gameTurn +=1
    # Use
    elif (localCommand == "Use") or (localCommand == "USE") or (localCommand == "use") or \
         (localCommand == "U") or (localCommand == "u"):
        # Yet another command that only works with a target.
        if localObject == None:
            print("You succesfully use nothing.  There was no effect.")
        else:
            CommandUse(localObject,roomID,roomList,objectList,playerInventory)
        gameTurn +=1
    # Inventory
    elif (localCommand == "Inventory") or (localCommand == "INVENTORY") or (localCommand == "inventory") or \
         (localCommand == "Inv") or (localCommand == "INV") or (localCommand == "inv") or \
         (localCommand == "I") or (localCommand == "i"):
        print("You are carrying: ")
        if len(playerInventory) > 0:
            for item in playerInventory:
                print(objectList[item][0])
        else:
            print("  Nothing")

    ## Movement directions
    # North
    elif (localCommand == "North") or (localCommand == "NORTH") or (localCommand == "north") or \
         (localCommand == "N") or (localCommand == "n"):
        # Check for a path in this direction.
        localExits = GetRoomExits(roomID,roomList)
        if localExits[0] > -1:
            # There's a path this way.  Move the player.
            roomID = localExits[0]
            newLook = True
        else:
            print("You see no way to go that direction.")
        gameTurn +=1
    # East
    elif (localCommand == "East") or (localCommand == "EAST") or (localCommand == "east") or \
         (localCommand == "E") or (localCommand == "e"):
        # Check for a path in this direction.
        localExits = GetRoomExits(roomID,roomList)
        if localExits[1] > -1:
            # There's a path this way.  Move the player.
            roomID = localExits[1]
            newLook = True
        else:
            print("You see no way to go that direction.")
        gameTurn +=1
    # South
    elif (localCommand == "South") or (localCommand == "SOUTH") or (localCommand == "south") or \
         (localCommand == "S") or (localCommand == "s"):
        # Check for a path in this direction.
        localExits = GetRoomExits(roomID,roomList)
        if localExits[2] > -1:
            # There's a path this way.  Move the player.
            roomID = localExits[2]
            newLook = True
        else:
            print("You see no way to go that direction.")
        gameTurn +=1
    # West
    elif (localCommand == "West") or (localCommand == "WEST") or (localCommand == "west") or \
         (localCommand == "W") or (localCommand == "w"):
        # Check for a path in this direction.
        localExits = GetRoomExits(roomID,roomList)
        if localExits[3] > -1:
            # There's a path this way.  Move the player.
            roomID = localExits[3]
            newLook = True
        else:
            print("You see no way to go that direction.")
        gameTurn +=1
    #Exit
    elif (localCommand == "Exit") or (localCommand == "EXIT") or (localCommand == "exit"):
        # Implementing this as an arbitrary <0 check in the caller.
        gameTurn = -5

    ### End handling of known commands

    else:
        print("I don't understand that command.  Please ask for HELP to see what commands are available.")

    ### End command parsing and processing

    # Return the new roomID and gameTurn to the caller.
    return [roomID, gameTurn, newLook]


########
### Begin game data
########

# Rooms
#
#   This is a list of rooms, where each "room" is just a list containing the
#   description and a list of exits.  The exits are always ordered [N, E, S, W].
#   An room with no exit in a direction will list "-1" in that index.
#
#   eg. A room's description will always be found at:
#       roomList[room_number][0]
#
#   eg. A room's South exit will always be found at:
#       roomList[room_number][1][2]
#

roomList = [
    [
        #Room 0
        "You are in a small stone room with no furnishings.  Near the doorway is a tablet with writing on it.",
        [-1,1,-1,-1]
    ],
    [
        #Room 1
        "You are in a small clearing at the bottom of a steep valley.  There appear to be a few small stone houses in the area, and a path leading off to the east.",
        [2,4,3,0]
    ],
    [
        #Room 2
        "You are in what appears to have been a small herb garden in front of a crumbling structure.  A few plants are still growing, but much of the area has been overgrown with weeds.",
        [-1,-1,1,-1]
    ],
    [
        #Room 3
        "You are in a small stone room with no furnishings.",
        [1,-1,-1,-1]
    ],
    [
        #Room 4
        "You are on a path through some dense woods.  There is a fork in the path here.",
        [-1,5,6,1]
    ],
    [
        #Room 5
        "You are standing before a large stone archway with a gate set in it.",
        [-1,-1,-1,4]
    ],
    [
        #Room 6
        "You are at the edge of a small lake in the valley.  The water appears to be clear and calm.",
        [4,-1,-1,-1]
    ],
    [
        #Room 7 - Placeholder
        "",
        [-1,-1,-1,-1]
    ]]

# Objects
#
#   This is a list of anything which the player can interact with.  It's a
#   relatively complicated list of lists to keep track of each object's
#   properties and status.
#
#   Each item in the list represents a single object, structered thusly:
#  - List: Object_Data (Ordered list of individual data items for each object.)
#    - String: Object_Name
#    - List: Aliases (List of strings that are also acceptable names for this object.)
#    - String: Description
#    - Int: Current_Room_ID
#    - Boolean: Usable?
#    - Boolean: Takable?
#    - Int: Status
#    - String: Use_String
#    - String: Take_String
#    - List: Status_Strings (Ordered list of strings for each status used by this item in the `Status` Int above.)
#

objectList = [
    [
        "Tablet", #Object Name
        [   #Aliases
            "TABLET",
            "tablet",
            "Tab",
            "TAB",
            "tab"],
        #Description string
        "As each eon comes to a close an individual is chosen to open the gate to prosperity for posterity.  As you now read this, know that you have been selected for this task.  Seek ye the gate and the key and pass through, that those who come after may follow.",
        0,      #Room
        False,  #Usable?
        False,  #Takable?
        -1,     #Status number
        "",     #"Use" message
        "",     #"Take" message
        []      #List of status messages
    ],
    [
        "Gate",
        ["GATE","gate"],
        "The gate is formed of some gleaming metal and appears to be polished to a high luster.",
        5,
        False,
        False,
        0,
        "",
        "",
        [
            "The gate is locked.",
            "The gate is unlocked."
        ]
    ],
    [
        "Garden",
        [   "GARDEN", "garden",
            "Plant", "PLANT", "plant",
            "Plants", "PLANTS", "plants",
            "Herb", "HERB", "herb",
            "Herbs", "HERBS", "herbs",
            "Weeds", "WEEDS", "weeds"
            ],
        "The garden is almost completely overgrown with weeds.  There appear to still be some onions growing off to one side.",
        2,
        False,
        False,
        -1,
        "",
        "",
        []
    ],
    [
        "Onion",
        ["ONION", "onion", "Onions", "ONIONS", "onions"],
        "It's a fresh onion.",
        2,
        True,
        True,
        -1,
        "You offer the onion to the creature, which accepts it with a broad smile.  The creature removes the shiny object hanging from its neck and hands it to you before wandering off to eat.",
        "You dig up a fresh onion and take it with you.",
        []
    ],
    [
        "Key",
        ["KEY","key"],
        "It looks like a gleaming brass key.",
        -1,
        True,
        False,
        -1,
        "You unlock the gate with the key.",
        "You have received a key.",
        []
    ],
    [
        "Water",
        ["WATER","water","Lake","LAKE","lake"],
        "The water appears to be calm and clear.",
        6,
        False,
        False,
        -1,
        "",
        "",
        []
    ],
    [
        "Creature",
        ["CREATURE","creature"],
        "The creature walks in a constant slouch and still stands nearly twice your height.  There is a shiny object hanging by a thong from its neck. It seems hungry.",
        6,
        False,
        False,
        0,
        "",
        "",
        ["There is a large bipedal creature here.  You hear it mumble about needing something to eat.",
         "There is a large bipedal creature here.  It has a hungry look in its eyes when it sees you."]
    ]]




########
### Begin game execution
########
import random

# Initial variables
#   These are our "global" tracking variables that get passed around among functions.
playerRoom = 0
playerInventory = []
gameTurn = 0

encounter = False
creatureID = GetObjectID("Creature",objectList)


print("\n\n\n\n")
print("You wake up on a dirt floor with no recolection of how you came to be here.")
newLook = True

# Main loop
while True:
    # Check win/lose conditions.
    if playerRoom == 7:
        print("\n\nCongradulations!  You have successfully opened the gate and stepped out into the world once more!\n")
        break

    # Creature becomes hostile after 25 game turns.
    if gameTurn > 24:
        SetObjectStatus(creatureID,1,objectList)

    # If the creature is hostile and you stay in the same room as it, you lose.
    if encounter & (GetObjectLocation(creatureID,objectList) == playerRoom):
        print("\n\nThe creature attacked you in the throes of its hunger.  Defenseless, you stood no chance.  You have died and failed.\n")
        break

    if newLook:
        CommandLook(playerRoom,roomList,objectList)

    #Prompt for action    
    print("\n\n\n")
    action = input('["?" for Help]  Action>  ')

    #When we call the command parsing function, it returns our new roomID and gameTurn.
    commandReturn = ParseCommand(action, roomList, objectList, playerInventory, playerRoom, gameTurn)
    playerRoom = commandReturn[0]
    gameTurn = commandReturn[1]
    newLook = commandReturn[2]
    
    if gameTurn < 0:
        print("Exiting game...")
        break

    # Creature begins moving around after 10 game turns.
    if gameTurn > 9:
        creatureLocation = GetObjectLocation(creatureID,objectList)
        # Skip trying to move the creature if it's already gone.
        if creatureLocation > -1:
            creatureMoveTo = -1
            if (GetObjectStatus(creatureID,objectList) > 0):
                # Hostile creature.  Will hunt nearby player if able.
                if (creatureLocation == playerRoom):
                    encounter = True
                    creatureMoveTo = creatureLocation
                else:
                    encounter = False
                    creatureExits = GetRoomExits(creatureLocation,roomList)
                    for path in creatureExits:
                        if path == playerRoom:
                            creatureMoveTo = path
            moveChoices = [creatureLocation] + GetRoomExits(creatureLocation,roomList)
            while creatureMoveTo == -1:
                # If the creature doesn't already have somewhere to go, select at random.
                creatureMoveTo = random.choice(moveChoices)
            SetObjectLocation(creatureID,creatureMoveTo,objectList)
    # End creature movement segment


