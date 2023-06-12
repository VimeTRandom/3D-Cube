import pygame
from math import *



pygame.init()


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
Cube_Distance = 10
Fov_Angle = 45
WIDTH, HEIGHT = 1300, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scale = 50
FOV = 300
points = []
Setpoints = []
ZFarDistance = 2
ZNearDistance = 2
Angle = 0

font = pygame.font.Font('freesansbold.ttf', 20)


# all the cube vertices 
#              x,   y,  z, w
points.append([-1, -1, 1])
points.append([1, -1, 1])
points.append([1,  1, 1])
points.append([-1, 1, 1])
points.append([-1, -1, -1])
points.append([1, -1, -1])
points.append([1, 1, -1])
points.append([-1, 1, -1])


def AddMatrix(Matrix):
    t=[]
    for i,v in enumerate(Matrix):
        num = 0
        for a,b in enumerate(v):
            num = num + b
            if a == len(v) - 1:
                t.insert(i, num)
    return t
Homogeneous_Matrix = [
    [1,0,0],
    [0,1,0],
    [0,0,1]
]

def AddFOV(Matrix):
    Matrix[0][0] =  (WIDTH/HEIGHT) * (1/ tan(FOV/2))
    Matrix[1][1] = 1/ tan(FOV/2)
    return Matrix

def AddPerspective(Matrix):
    Matrix[2][2] = ZFarDistance / (ZFarDistance - ZNearDistance)
    Matrix[2][3] = (-ZFarDistance * ZNearDistance) / (ZFarDistance - ZNearDistance)
    
    return Matrix
def MakePerspective(Matrix):
    print(Matrix)
    Matrix[0][0] = (WIDTH/HEIGHT) * (1/ tan(FOV/2))
    Matrix[1][1] = 1/ tan(FOV/2)
    Matrix[2][2] = ZFarDistance / (ZFarDistance - ZNearDistance)
    Matrix[2][3] = (-ZFarDistance * ZNearDistance) / (ZFarDistance - ZNearDistance)
    Matrix[3][2] = 1


    return Matrix




def MutiplyMatrix(Matrix, Coordinates):
    # __  ___            ___            ___
    #|   X   |          |  1     0      0  |
    #|       |          |                  |
    #|   Y   |          |  0     1      0  |
    #|       |    *     |                  |
    #|   Z   |          |  0     0      0  |
    #|__  ___|          |___            ___|


    #(X * 1) + (Y * 0) + (Z * 0)
    M = []
    for i,z in enumerate(Matrix):
        l = []
        for a,b in enumerate(Coordinates):
            l.insert(a, b * z[a])


            if a == len(z) - 1:
                M.insert(i, l)
    return M 


projected_points = [
    [n,n] for n in range(len(points))
]




def connect_points(i, j, points):
    pygame.draw.line(
        screen, (0, 37, 153), (points[i][0], points[i][1]), (points[j][0], points[j][1]))



#Rotation Maxtrix Tranformation
def RotateAround_Z(Angle):
    return [
        [cos(Angle), -sin(Angle), 0],
        [sin(Angle), cos(Angle), 0],
        [0, 0, 1],
    ]




def RotateAround_Y(Angle):
    return [
        [cos(Angle), 0, sin(Angle)],
        [0, 1, 0],
        [-sin(Angle), 0, cos(Angle)]
    ]




def RotateAround_X(Angle):
    return [
        [1, 0, 0],
        [0, cos(Angle), -sin(Angle)],
        [0, sin(Angle), cos(Angle)],
    ]


clock = pygame.time.Clock()


HoldDown_S = False
HoldDown_W = False
HoldDown_A = False
HoldDown_D = False
HoldDown_Q = False
HoldDown_E = False
S_Rotate = 0
while True:


    clock.tick(60)
    if HoldDown_S == True:
        ZFarDistance += 0.02


    if HoldDown_W == True:
        ZFarDistance -= 0.02


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_w:
                HoldDown_W = True
            if event.key == pygame.K_s:
                HoldDown_S = True
            
            if event.key == pygame.K_q:
                HoldDown_Q = True
            if event.key == pygame.K_e:
                HoldDown_E = True
            if event.key == pygame.K_a:
                HoldDown_A = True
            if event.key == pygame.K_d:
                HoldDown_D = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                HoldDown_W = False
            if event.key == pygame.K_s:
                HoldDown_S = False


            if event.key == pygame.K_a:
                HoldDown_A = False
            if event.key == pygame.K_d:
                HoldDown_D = False
            if event.key == pygame.K_q:
                HoldDown_Q = False
            if event.key == pygame.K_e:
                HoldDown_E = False


    screen.fill(WHITE)
    for i,p in enumerate(points):
        Rotate = None


        if S_Rotate != False:
            Rotate = AddMatrix(MutiplyMatrix(S_Rotate, p))
        else:
            Rotate = AddMatrix(MutiplyMatrix(Homogeneous_Matrix, p))


        if HoldDown_A == True:
            Angle -= 0.01
            Rotate = AddMatrix(MutiplyMatrix(RotateAround_Y(Angle), p))
            S_Rotate = RotateAround_Y(Angle)

        if HoldDown_D == True:
            Angle += 0.01
            Rotate = AddMatrix(MutiplyMatrix(RotateAround_Y(Angle), p))
            S_Rotate = RotateAround_Y(Angle)

        if HoldDown_Q == True:
            Angle -= 0.01
            Rotate = AddMatrix(MutiplyMatrix(RotateAround_X(Angle), p))
            S_Rotate = RotateAround_X(Angle)

        if HoldDown_E == True:
            Angle += 0.01
            Rotate = AddMatrix(MutiplyMatrix(RotateAround_Z(Angle), p))
            S_Rotate = RotateAround_Z(Angle)
            


        z = 1/ (ZFarDistance - Rotate[2])


        Homogeneous_Projection_Matrix = [
            [z, 0, 0],
            [0, z, 0],
            [0, 0, 0],
        ]

        #Homogeneous_Projection_Matrix = AddFOV(Homogeneous_Projection_Matrix)
        MTB = AddMatrix(MutiplyMatrix(Homogeneous_Projection_Matrix, Rotate))
        x = int(MTB[0] * scale) + (WIDTH/2)
        y = int(MTB[1] * scale) + (HEIGHT/2)
        projected_points[i] = [x, y]
        pygame.draw.circle(screen, BLACK, (x, y), 5)
        text = font.render(str(i), True, BLACK)
        screen.blit(text, (x,y))

    for p in range(4):
        #Triangle
        connect_points(1, 3, projected_points)
        connect_points(5, 7, projected_points)
        connect_points(6, 3, projected_points)
        connect_points(4, 1, projected_points)
        connect_points(0, 7, projected_points)
        connect_points(5, 2, projected_points)

        #Faces
        connect_points(p, (p+1) % 4, projected_points)
        connect_points(p+4, ((p+1) % 4) + 4, projected_points)
        connect_points(p, (p+4), projected_points)




    pygame.display.update()
