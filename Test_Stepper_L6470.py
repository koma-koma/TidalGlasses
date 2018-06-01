import stepperMotorL6470 as sm
import time

if __name__=="__main__":    
    sm.L6470_init(0)

    try:
        while True:
            print("input command")
            input_command = str(input(">>> "))
            command = input_command.split()
            print(command[0])
            if command[0] == "run":
                print("*** run speed %d ***" % int(command[1]))
                sm.L6470_run(0, int(command[1]))
                time.sleep(1)

            elif command[0] == "move":
                print("*** run %d steps ***" % int(command[1]))
                sm.L6470_move(0, int(command[1]))
                time.sleep(1)

            if input_command == "stop":
                print("*** stop ***")
                sm.L6470_softstop(0)
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nExit")
        sm.L6470_softstop(0)
        sm.L6470_softhiz(0)
        quit()