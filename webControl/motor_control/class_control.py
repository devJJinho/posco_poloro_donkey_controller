import motor

steer=motor.motorControl()

while True:
    dir=input("Which direction ? 'r','l','c','q','g' : ")
    # if dir in ['r','l']:
    #     angle=input("And how hard ? (0~10) : ")
    if dir=='r':
        steer.goRight(30)
    if dir=='l':
        steer.goLeft(20)
    if dir=='c':
        steer.cali()
    if dir=='g':
        steer.go()
    if dir=='q':
        steer.quit()
    if dir=='+':
        steer.go()
    if dir=='-':
        steer.stop()

# while True:
#     aa=input("degree?:")
#     steer.setAngle(int(aa))
