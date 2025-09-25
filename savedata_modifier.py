import base64
import json
import os
import sys
import shutil
from typing import Dict, Any

class SavedataModifier:
    """modifier for savedata.sav file"""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.prefix_data = ""
        self.game_data = {}
        
    def load_savedata(self) -> bool:
        """load and decode savedata file"""
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
            
            # find base64 part (try different patterns)
            base64_patterns = ['eyA', 'eyJ', 'ey']
            base64_start = -1
            for pattern in base64_patterns:
                base64_start = content.find(pattern)
                if base64_start != -1:
                    break
            
            if base64_start == -1:
                print("error: no base64 data found")
                return False
            
            # split prefix and base64 data
            self.prefix_data = content[:base64_start]
            base64_data = content[base64_start:].rstrip('\x00').rstrip('=') + '=='
            
            print(f"prefix length: {len(self.prefix_data)} chars")
            print(f"base64 data length: {len(base64_data)} chars")
            
            # decode base64
            decoded_bytes = base64.b64decode(base64_data)
            decoded_str = decoded_bytes.decode('utf-8')
            print(decoded_str)
            
            # extract json part manually
            json_start = decoded_str.find('{')
            json_end = decoded_str.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_part = decoded_str[json_start:json_end]
                self.game_data = json.loads(json_part)
                print("decoded game data successfully")
                return True
            else:
                print("error: no json data found in decoded string")
                return False
                
        except Exception as e:
            print(f"error reading file: {e}")
            return False
    
    def show_current_data(self):
        """display current game data"""
        print("\ncurrent game data:")
        for key, value in self.game_data.items():
            print(f"  {key}: {value}")
    
    def modify_level(self, new_level: int):
        """modify player level"""
        old_level = self.game_data.get('level', 0)
        self.game_data['level'] = float(new_level)
        print(f"level changed: {old_level} -> {new_level}")
    
    def modify_value(self, key: str, value: float):
        """modify any game value"""
        if key in self.game_data:
            old_value = self.game_data[key]
            self.game_data[key] = value
            print(f"{key} changed: {old_value} -> {value}")
            return True
        else:
            print(f"error: key '{key}' not found")
            return False
    
    def save_modified_data(self, backup: bool = True) -> bool:
        """save modified data to file"""
        try:
            # create backup if requested
            if backup and os.path.exists(self.filepath):
                backup_path = f"{self.filepath}.backup"
                if not os.path.exists(backup_path):
                    shutil.copy2(self.filepath, backup_path)
                    print(f"backup created: {backup_path}")
            
            # encode data back to base64
            json_str = json.dumps(self.game_data)
            base64_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
            
            # reconstruct file content
            new_content = self.prefix_data + base64_data + '\x00'
            
            # save file
            with open(self.filepath, 'wb') as f:
                f.write(new_content.encode('utf-8'))
            
            print("file saved successfully")
            return True
            
        except Exception as e:
            print(f"error saving file: {e}")
            return False

def main():

    
    savedata_path = "savedata.sav"
    
    if not os.path.exists(savedata_path):
        print(f"error: file {savedata_path} not found")
        sys.exit(1)
    
    modifier = SavedataModifier(savedata_path)
    
    # load current data
    if not modifier.load_savedata():
        print("failed to load savedata")
        sys.exit(1)
    
    # interactive menu
    while True:
        modifier.show_current_data()
        
        print("\nOptions:")
        print("1. modify level")
        print("2. modify hp")
        print("3. modify shield")
        print("4. modify custom value")
        print("5. save and exit")
        print("6. exit without saving")
        
        try:
            choice = input("\nchoose option (1-6): ").strip()
            
            if choice == '1':
                new_level = int(float(input(f"enter new level (current: {modifier.game_data.get('level', 0)}): ")))
                if new_level < 1:
                    print("error: level must be >= 1")
                    continue
                modifier.modify_level(new_level)
                
            elif choice == '2':
                new_hp = float(input(f"enter new hp (current: {modifier.game_data.get('hp', 0)}): "))
                modifier.modify_value('hp', new_hp)
                
            elif choice == '3':
                new_shield = float(input(f"enter new shield (current: {modifier.game_data.get('shield', 0)}): "))
                modifier.modify_value('shield', new_shield)
                
            elif choice == '4':
                print("available keys:", list(modifier.game_data.keys()))
                key = input("enter key to modify: ").strip()
                if key in modifier.game_data:
                    new_value = float(input(f"enter new value for {key} (current: {modifier.game_data.get(key, 0)}): "))
                    modifier.modify_value(key, new_value)
                else:
                    print(f"key '{key}' not found")
                    
            elif choice == '5':
                confirm = input("save changes? (y/n): ").lower().strip()
                if confirm in ['y', 'yes', 'o', 'oui']:
                    if modifier.save_modified_data():
                        print("modifications saved successfully!")
                        break
                    else:
                        print("failed to save modifications")
                else:
                    print("save cancelled")
                    
            elif choice == '6':
                print("exiting without saving")
                break
                
            else:
                print("invalid choice")
                
        except KeyboardInterrupt:
            print("\nexiting...")
            break
        except ValueError:
            print("error: invalid input")
        except Exception as e:
            print(f"error: {e}")

if __name__ == "__main__":
    main()