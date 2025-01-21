#main repair code
from self_healing.data.detail import details, yes
from self_healing.data.values import reset_font, font, error
from self_healing.data.fixes import error_fixes, detailed_error_fixes

def get_message(error, details= details):
    code_path = []
    error_type = {}
    path = ""
    i = 0
    while i <= len(error):
        if error[i:(i+4)] == "File":
            while error[i:(i+1)] != "\n":
                path += error[i]
                i += 1
            if details["line"]:
                if details["file"]:
                    code_path.append(f"{str(path).split(",")[1].strip()} on {str(path).split(",")[0].strip()}")
                else:
                    code_path.append(f"{str(path).split(",")[1].strip()}")
            else:
                if details["file"]:
                    code_path.append(f"{str(path).split(",")[0].strip()}")
            path = ""
            i += 1
        
        elif ":" in error[i:] and "\n" not in error[i:]:
            name = (error[i:].split(":", 1))[0].strip()
            detail = ((error[i:].split(":", 1))[1]).strip()
            error_type[name]= detail
            break
        else: 
            i += 1
    return code_path, error_type

class healer:
    def __init__(self, error, detail=details):
        self.error = error
        self.details = detail
    
    def heal(self):
        error_path, error_type = get_message(self.error, self.details)
        error_fix = ""
        setup = False
        if list(error_type.keys())[0] in list(error_fixes.keys()):
            error_fix = error_fixes.get(list(error_type.keys())[0])
        else:
            error_fix = f"{font.red}Error is not supported yet...{font.white}"
        out_error = ""
        for i in range(len(error_path)):
            if setup:
                if (i+1) < len(error_path):
                    out_error += f"{font.white}called {font.yellow}from {font.white}{(error_path[::-1])[i]}, "
                else:
                    out_error += f"{font.white}called {font.yellow}from {font.white}{(error_path[::-1])[i]}.\n"
            else:
                if (i+1) < len(error_path):
                    out_error += f"{font.red}{list(error_type.values())[0]}{font.yellow} at {font.white}{(error_path[::-1])[i]}, "
                    setup = True
                else:
                    out_error += f"{font.red}{list(error_type.values())[0]}{font.yellow} at {font.white}{(error_path[::-1])[i]}.\n"
        print(out_error, end="")
        print(f"{font.green}How to fix {error}{font.white}:{font.bold} {error_fix}")
        if not details["detailed"]:
            print(f"do you want more specific details?")
            reset_font()
            user_answer = input()
        if user_answer in yes: details["detailed"] = True
        if details["detailed"]:
            print(f"Error name: {list(error_type.keys())[0]}")
            print(f"Error detail: {out_error}")
            print(f"Fix way: {detailed_error_fixes[list(error_type.keys())[0]]}")