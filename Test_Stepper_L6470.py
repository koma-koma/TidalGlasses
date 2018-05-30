import stepperMotorL6470 as sm
import time

if __name__=="__main__":    
    L6470_init(0)

    try:
        while True:
            

    except KeyboardInterrupt:
        print("\nExit")
        sm.L6470_softstop(0)
        sm.L6470_softhiz(0)
        quit()