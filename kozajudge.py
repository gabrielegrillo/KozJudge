import subprocess, os, glob, configparser, sys
from pathlib import Path

nameProblem = ""
pathEx = ''
pathSol = ''
timeLimit = 20

def makeConfig(pathExercises: str, pathSolutions: str) -> None:
    config = configparser.ConfigParser()
    config['PATHS'] = {'exercises': f"{pathExercises}", 'solutions': f"{pathSolutions}"}
    # config['VALUES']['timelimit'] = 20

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def loadConfig() -> None:
    config = configparser.ConfigParser()
    config.read('config.ini')
    if (os.path.exists(config['PATHS']['exercises']) and os.path.exists(config['PATHS']['solutions'])):
        global pathEx, pathSol
        pathEx = f"{config['PATHS']['exercises']}"
        pathSol = f"{config['PATHS']['solutions']}"
    else:
        print("Error! Check the config file")

# TODO: Adjust paths
def loadDomjudgeConfig(path) -> None:
    config = configparser.ConfigParser()
    if (os.path.exists(os.path.join(path, "domjudge-problem.ini"))):
        with open(os.path.join(path, "domjudge-problem.ini")) as stream:
            # Little trick to cheat the parser. 
            config.read_string("[top]\n" + stream.read())
            timeLimit = config["top"]["timelimit"]

def loadTestCases(exercise: str) -> list[str]:
    Testcases = []
    try:
        os.chdir(os.path.join(pathSol, exercise))
    except FileNotFoundError:
        return Testcases
    
    for file in glob.glob(f"{exercise}_*.in"):
        Testcases.append(file)
    return Testcases

def startJudging(exercise, tc):
    count_tc_passed = 0 
    print("------------------------------------------------------------------")
    print("Testing:", exercise)
    for i in range(len(tc)):
        file_in = os.path.join(pathSol, exercise, tc[i])
        file_out = file_in[:-2] + "out"

        with open(file_in) as f1:
            inn = f1.readlines()

        innt = ""
        for j in range(len(inn)):
            innt += inn[j] 
        # Get the path of python and run it
        p = subprocess.Popen([os.environ['_'], os.path.join(pathEx, f"{exercise}.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        
        try:
            stdout, stderr = p.communicate(input=innt, timeout=timeLimit)
        except subprocess.TimeoutExpired:
            p.kill()
            print("Testcase:", tc[i], "- TIMEOUT EXPIRED ⏰")
            continue
        
        if (p.returncode != 0):
            print("Testcase:",tc[i], "- ERROR ❗ \n", "Actual output:", str(stdout), "Error raised: ", str(p.returncode))
            continue

        
        with open(file_out) as f2:
            out = f2.readlines()

        outt = ""
        for j in range(len(out)):
            outt += out[j] 
        
        if (stdout == outt):
            count_tc_passed += 1
            print("Testcase:",tc[i], "- CORRECT ✅ ")
        else:
            print("Testcase:",tc[i], "- WRONG ❌ \n", "Expected output:", str(outt), "Actual output:", str(stdout))
        #print("Testcase:",tc[j], stdout == outt)
    print("""------------------------------------------------------------------\n""")
    if (count_tc_passed == len(tc)):
        print("ALL TESTCASE PASSED! 🥳")
    else:
        print("NOT ALL TESTCASE PASSED! 😱")

def startProgram(ex="") -> None:
    print(""" 
██╗░░██╗░█████╗░███████╗░█████╗░░░░░░██╗██╗░░░██╗██████╗░░██████╗░███████╗
██║░██╔╝██╔══██╗╚════██║██╔══██╗░░░░░██║██║░░░██║██╔══██╗██╔════╝░██╔════╝
█████═╝░██║░░██║░░███╔═╝███████║░░░░░██║██║░░░██║██║░░██║██║░░██╗░█████╗░░
██╔═██╗░██║░░██║██╔══╝░░██╔══██║██╗░░██║██║░░░██║██║░░██║██║░░╚██╗██╔══╝░░
██║░╚██╗╚█████╔╝███████╗██║░░██║╚█████╔╝╚██████╔╝██████╔╝╚██████╔╝███████╗
╚═╝░░╚═╝░╚════╝░╚══════╝╚═╝░░╚═╝░╚════╝░░╚═════╝░╚═════╝░░╚═════╝░╚══════╝\n""")
    
    if (ex == ""):
        file = input("Welcome to KozaJudge!\nPlease insert the name of the exercise: ")
    else:
        file = ex
    testcase = loadTestCases(file)
    if (testcase != []):
        startJudging(file,testcase)
    else:
        print("Testcase were not found and/or Folder with the excercise not found. Please check the folders")

def main():
    if (os.path.exists("config.ini")):
        loadConfig()
        if (len(sys.argv) > 1):
            startProgram(sys.argv[1])
        else:
            startProgram()
    else:
        print("Welcome to KozaJudge, follow the instructions below:")
        pathEx = Path(input("Please insert the path where your exercises are located: "))
        pathSol = Path(input("Please insert the path where your solutions are located: "))
        print()
        makeConfig(pathEx, pathSol)
        loadConfig()
        startProgram()


main()
