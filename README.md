# DistantSpace2 Save Editor

Simple tool to modify your DistantSpace2 game save file.

### The file "savedata.sav" included is at level 29 (final boss) with 200,000 HP and 100% shield.

## How to Use

*You need [Python](https://www.python.org/downloads/) installed on your computer.*

0. **Close the game**: Make sure DistantSpace2 is not running
1. **Find your save file**: Your save is located in `%localappdata%/DistantSpace`. File name : `savedata.sav`
2. **Copy the script**: Put `savedata_modifier.py` in the same folder as your save file
3. **Run the script**: Double-click the script or run `python savedata_modifier.py`
4. **Choose what to modify**: Follow the menu options
5. **Save changes**: Select option 5 to save your changes
6. **Start the game**: Launch DistantSpace2 and enjoy!

## What You Can Change

- **Level**: Set any level you want. Final boss : level 29
- **HP**: Your health points
- **Shield**: Your shield points  
- **Custom values**: Sound volume, music settings, etc.

## Important Warnings

⚠️ **Shield limit**: Don't set shield above 100 - the game might crash  
⚠️ **HP limit**: Don't set HP above 200,000 - not necessary and might cause problems  
⚠️ **Achievements**: Changing your level won't unlock all achievements automatically  
⚠️ **Backup**: The script creates a backup automatically, but make your own copy to be safe

## Tips

- Start with small changes first
- Test the game after each modification  
- If the game crashes, restore from backup
- The script shows your current values before you change them

## Backup Location

Your backup file will be saved as `savedata.sav.backup` in the same folder. Remove the ".backup" extension to restore it.

---


*This tool modifies your save file. Use at your own risk. I'm not responsible for any damage caused by using this tool.*
