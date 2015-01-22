import cx_Freeze
 
executables = [cx_Freeze.Executable("main.py")]
 

    
if __name__ == '__main__':
    cx_Freeze.setup(
        name="x86trial",
        version = "1.1",
        options={"build_exe": {"packages":["pygame"]}},
        executables = executables)
    raw_input("Press any key to continue") #Pause to let user see that things ends 