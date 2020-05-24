

# import the libraries
import pygame
import random
import math
from matplotlib import pylab as plt


#initilize pygame
pygame.init()
pygame.font.init()

# enter
WIDTH, HEIGHT = 840, 840  #must be divided by three
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("COVID-19")


class Position:
    def __init__(self, x, y):
        self.x = x #x value of the position
        self.y = y #y value of the position

    def getX(self):
        # returns x position
        return self.x

    def getY(self):
        # returns y position
        return self.y

    def getNewPosition(self, angle, speed):
        # calculates the new position after one clock tick according to speed and angle

        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def getDistance(self, other):
        #returns the distance between two Point objects
        xDist = other.getX() - self.getX()
        yDist = other.getY() - self.getY()
        return math.sqrt(xDist ** 2 + yDist ** 2)

# Person class
class Person:


    RECOVER_TIME = 780 #number of frames it takes an infected person to die. (13 seconds with 60FPS)

    def __init__(self, speed, grid, spreadRadius, figureWidth, figureHeight):

        self.width = figureWidth   #the width of the person object in pixels
        self.height = figureHeight   #the height of the person object in pixels
        self.pos = grid.randomPos()   #Position object with a random placement
        self.speed = speed # pixels per frame
        self.direction = random.randint(0, 360)   #random angle is given
        self.grid = grid    #the grid person object is in
        self.isInfected = False    # state of being infectious
        self.spreadRadius = spreadRadius    # at most distance to be infected
        self.recoverTime = 0     #saving the time since being infected
        self.placeStayTime = 0     #saving the time since in common place

    def getPosition(self):
        # returns Position object
        return self.pos

    def getSpeed(self):
        # returns speed
        return self.speed

    def getDirection(self):
        # returns direction
        return self.direction

    def getGrid(self):
        #returns grid
        return self.grid

    def newDirection(self):
        #sets new direction
        self.direction = random.randrange(0, 360)

    def getSpreadRaidus(self):
        # returns the radius of infection zone
        return self.spreadRadius

    def getRecoverTime(self):
        # returns the time to recover
        return self.recoverTime

    def incrementRecover(self):
        # increments recover time
        self.recoverTime += 1

    def isPersonRecovered(self):
        # if the recover time has passed return true
        if self.getRecoverTime() >= self.RECOVER_TIME:
            return True
        return False

    def isInInfectionZone(self, otherPerson, spreadProb):
        # returns true if the person is infected, or false if its not

        distance = self.pos.getDistance(otherPerson.pos)
        prob = random.random()

        if distance <= self.getSpreadRaidus():
            if prob < spreadProb:
                return True
            else:
                return False
        else:
            return False

    def move(self):
        # updates the Person's position after one clock tick
        self.pos = self.getPosition().getNewPosition(self.direction, self.speed)

        if self.grid.isPosInGrid(self.pos, self.width, self.height) != True:
            while self.grid.isPosInGrid(self.pos, self.width, self.height) == False:
                self.newDirection()
                self.pos = self.getPosition().getNewPosition(self.direction, self.speed)

    def draw(self, window, color):
        # draws the person
        pygame.draw.rect(window, color,
        (self.getPosition().getX() - self.width / 2, self.getPosition().getY() - self.height / 2, self.width, self.height))
        pygame.draw.circle(window, (255, 0, 0), (self.getPosition().getX(), self.getPosition().getY()), 2)
        pygame.draw.circle(window, (255, 0, 0), (self.getPosition().getX(), self.getPosition().getY()),
                           self.width * 1.5, 1)

    def goCommonPlace(self, visitProb, currentFPS):
        #sets the position of the Person object equal to common place position if visit probability
        luck = random.random()
        visitProbFrame = visitProb / currentFPS  # visit prob per second
        if luck < visitProbFrame:
            self.pos.x = self.grid.width / 2
            self.pos.y = self.grid.height / 2
            self.placeStayTime += 1


# Person object of a community person in modes 3 and 4
# Inherited from Person class

class CommunityPerson(Person):
    RECOVER_TIME = 400000
    def __init__(self, speed, grid, spreadRadius, figureWidth, figureHeight):
        super().__init__(speed, grid, spreadRadius, figureWidth, figureHeight)

        self.destinationTuple = None
        self.onFlight = False
        self.infectionState = None
        self.arrivedState = None
        self.num = None
        self.commonPlaceWidth = 10
        self.commonPlaceHeight = 10


    def goCommonPlace(self, visitProb, currentFPS):
        luck = random.random()
        visitProbFrame = visitProb / currentFPS  # visit prob per second
        if luck < visitProbFrame:
            self.pos = self.grid.calculateMidPos()
            self.placeStayTime += 1


    def checkFlight(self, flyProb, currentFPS):
        #returns True if the person is going to fly otherwise false
        luck = random.random()
        flyProbFrame = flyProb / currentFPS  # visit prob per second
        if luck < flyProbFrame:
            self.onFlight = True
            return True
        return False

    def chooseAirport(self, grids):
        copyGrids = grids[:]
        copyGrids.remove(self.grid)
        return random.choice(copyGrids)

    def setDirection(self, path):
        #buraya bak
   #     print(self.num,path)
   #     print("")
        if path[1] > -self.commonPlaceWidth and path[1] < self.commonPlaceWidth:
            pass
        else:
            if path[1] < 0:
                self.direction = 360
            elif path[1] > 0:
                self.direction = 180

        if path[0] > -self.commonPlaceHeight and path[0] < self.commonPlaceHeight:
            pass
        else:
            if path[0] < 0:
                self.direction = 90

            elif path[0] > 0:
                self.direction = 270

    def checkArrived(self, path):
        if path[0] > -self.commonPlaceWidth and path[0] < self.commonPlaceWidth:
            if path[1] > -self.commonPlaceHeight and path[1] < self.commonPlaceHeight:
                return True
            return False
        return False

    def move(self):

        self.pos = self.getPosition().getNewPosition(self.direction, self.speed)
        if self.onFlight == False:
            if self.grid.isPosInGrid(self.pos, self.width, self.height) != True:
                while self.grid.isPosInGrid(self.pos, self.width, self.height) == False:
                    self.newDirection()
                    self.pos = self.getPosition().getNewPosition(self.direction, self.speed)

    def draw(self, window, color):
        # draws the person
        if self.onFlight:
            pygame.draw.circle(window, (255, 0, 0), (self.getPosition().getX(), self.getPosition().getY()), 2)
            pygame.draw.circle(window, (87, 89, 93), (self.getPosition().getX(), self.getPosition().getY()),
                               self.width * 1.5, 1)
            if self.infectionState:
                pygame.draw.rect(window, color,
                (self.getPosition().getX() - self.width / 2, self.getPosition().getY() - self.height / 2, self.width, self.height))

            else:
                pygame.draw.rect(window, (0,176,199),
                                 (self.getPosition().getX() - self.width / 2,
                                  self.getPosition().getY() - self.height / 2, self.width, self.height))

        else:
            pygame.draw.rect(window, color,
                             (self.getPosition().getX() - self.width / 2, self.getPosition().getY() - self.height / 2,
                              self.width, self.height))
            pygame.draw.circle(window, (255, 0, 0), (self.getPosition().getX(), self.getPosition().getY()), 2)
            pygame.draw.circle(window, (255, 0, 0), (self.getPosition().getX(), self.getPosition().getY()),
                               self.width * 1.5, 1)


class Grid:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def isPosInGrid(self, pos, width, height):
        # returns true if a position object is in the grid otherwise returns false
        if pos.getX() + width / 2 > self.width:
            return False
        if pos.getY() + height / 2 > self.height:
            return False
        if pos.getX() - width / 2 < 0:
            return False
        if pos.getY() - height / 2 < 0:
            return False
        return True

    def randomPos(self):
        # returns Position object with a random position

        randX = random.randrange(20, self.width - 20)
        randY = random.randrange(20, self.height - 20)

        newPos = Position(randX, randY)
        return newPos


class subGrid(Grid):

    def __init__(self, width, height, gridNo, gridNum):
        super().__init__(width, height)

        self.infectedList = []
        self.susceptibleList = []
        self.recoveredList = []
        self.infectedNumList = []
        self.susceptibleNumList = []
        self.recoveredNumList = []
        self.totalList = []
        self.basicRList = []
        self.gridNo = gridNo
        self.gridNum = gridNum

        if self.gridNo < gridNum / 2:
            self.xTL = self.width * self.gridNo
            self.yTL = 0
        else:
            self.xTL = self.width * (self.gridNo - 3)
            self.yTL = self.height

    def isPosInGrid(self, pos, objWidth, objHeight):
        # returns true if a position object is in the grid otherwise returns false
        if pos.getX() + 2*objWidth > self.xTL + self.width:
            return False
        if pos.getY() + 2*objHeight > self.yTL + self.height:
            return False
        if pos.getX() - 2*objWidth < 0 + self.xTL:
            return False
        if pos.getY() - 2*objHeight < 0 + self.yTL:
            return False
        return True

    def randomPos(self):

        randX = random.randrange(self.xTL + 20, self.xTL + self.width - 20)
        randY = random.randrange(self.yTL + 20, self.yTL + self.height - 20)

        newPos = Position(randX, randY)
        return newPos

    def calculateMidPos(self):
        xMid = self.xTL + self.width / 2
        yMid = self.yTL + self.height / 2

        midPos = Position(xMid, yMid)
        return midPos


def calculateR(currentInfectionNum, preInfectionNum, susceptibleNum):
    if susceptibleNum > 0:
        try:
            return round(currentInfectionNum / preInfectionNum, 2)
        except ZeroDivisionError:
            return None
    else:
        return None

class simpleAirway:



    def __init__(self, gridList, flightSpeed):

        self.gridList = gridList
        self.passengerDict = {}
        self.passengerList = []
        self.counter = 0
        self.flightSpeed = flightSpeed
        self.speed = None

    def addPassenger(self, person, destination):

        self.speed = person.speed
        self.passengerDict[person] = self.setPath(person,destination)
        self.passengerList.append(person)
        person.destinationTuple = (destination.calculateMidPos().getX(),destination.calculateMidPos().getY())
        person.onFlight = True
        person.arrivedState = False
        person.num = self.counter
        self.counter += 1

    def setPath(self, person, destination):

        currentPos = person.pos
        destPos = destination.calculateMidPos()


        pathX = currentPos.getX() - destPos.getX()
        pathY = currentPos.getY() - destPos.getY()

        return (pathX,pathY)

    def updatePath(self, passenger, destination):


        pathX = passenger.pos.getX() - destination[0]
        pathY = passenger.pos.getY() - destination[1]
   #     print(passenger.num, "exact position", passenger.pos.getX(), passenger.pos.getY())
        return (pathX,pathY)

    def fly(self):

        for passenger in self.passengerList:
            passenger.speed = self.flightSpeed
            passenger.spreadRadius = 0
            newPath = self.updatePath(passenger, passenger.destinationTuple)
            passenger.setDirection(newPath)

            if passenger.checkArrived(newPath):
                self.ifArrived(passenger)
                continue

            passenger.move()



    def ifArrived(self, passenger):
            self.passengerList.remove(passenger)
            del self.passengerDict[passenger]
            passenger.onFlight = False
            passenger.arrivedState = True
       #     print("works")
            for grid in self.gridList:
                gridX = grid.calculateMidPos().getX()
                gridY = grid.calculateMidPos().getY()
                personX = passenger.pos.getX()
                personY = passenger.pos.getY()


                if gridX + gridY - (personX + personY) < 50 and gridX + gridY - (personX + personY) > -50:

                    passenger.speed = self.speed
                    if passenger.infectionState:
                        newPerson = CommunityPerson(self.speed,grid,passenger.spreadRadius,passenger.width, passenger.height)
                        newPerson.pos = passenger.pos
                        grid.infectedList.append(newPerson)
                        break
                    else:
                        newPerson = CommunityPerson(self.speed, grid, passenger.spreadRadius, passenger.width,
                                                    passenger.height)
                        newPerson.pos = passenger.pos
                        grid.susceptibleList.append(newPerson)
                        break



def communitySimulation(airwayOn=False):

    myGrids = []

    gridNum = 6
    subGridWidth = WIDTH / (gridNum / 2)
    subGridHeight = HEIGHT / 2

    run = True
    commonPlace = True

    FPS = 60 # at most FPS
    speed = 0.5 # Speed of community person
    airwaySpeed = 3 # Speed of passengers
    personNum = 35

    spreadProbSecond = 0.12  # Infection probability in 1 second
    flightProb = 0.05 # Flight probability in 1 second
    counter = 0
    figureWidth = 10
    figureHeight = 10
    spreadRadius = figureWidth*4
    dayCounter = 0

    placeWidth = 30
    placeHeight = 30
    visitProb = 0.05  # per second
    placeStayTime = 0.1 #place stay time in seconds
    clock = pygame.time.Clock()
    infected_font = pygame.font.SysFont("comicsans", 23)
    R_font = pygame.font.SysFont("comicsans", 25)
    dayCount_font = pygame.font.SysFont("comicsans", 20)

    def redrawWindow(commonPlace):
        WIN.fill((0, 0, 0))
        infectedNumLableList = []
        dayCountLabelList = []
        rLableList = []

        for i in range(gridNum):
            infectedNumLabel = infected_font.render(f"Infected people num: {len(myGrids[i].infectedList)}", 1,
                                                    (255, 255, 255))
            dayCountLabel = dayCount_font.render(f"Day num: {dayCounter}", 1, (255, 255, 255))
            infectedNumLableList.append(infectedNumLabel)
            dayCountLabelList.append(dayCountLabel)

            pygame.draw.rect(WIN,(255,255,255),(int(myGrids[i].xTL),int(myGrids[i].yTL), int(myGrids[i].width), int(myGrids[i].height)), 2)
            #draw the airline
            if airwayOn:
                pygame.draw.rect(WIN,(0,255,0),(int(myGrids[0].calculateMidPos().getX()), int(myGrids[0].calculateMidPos().getY()), int(myGrids[0].width)*2, int(myGrids[0].height)), 3)
                pygame.draw.line(WIN, (0,255,0), (int(myGrids[1].calculateMidPos().getX()), int(myGrids[1].calculateMidPos().getY())), (int(myGrids[1].calculateMidPos().getX()),int(myGrids[1].calculateMidPos().getY() + myGrids[1].height)), 3)

            if commonPlace:
                pygame.draw.rect(WIN, (255, 255, 255),
                                 (myGrids[i].calculateMidPos().getX() - placeWidth / 2,
                                  myGrids[i].calculateMidPos().getY() - placeHeight / 2, placeWidth, placeHeight), 2)

            for p in myGrids[i].susceptibleList:
                p.draw(WIN, (0, 0, 255))

            for d in myGrids[i].infectedList:
                d.draw(WIN, (255, 0, 0))

            for k in myGrids[i].recoveredList:
                k.draw(WIN, (55, 55, 55))

            if dayCounter > 2:

                RLabel = R_font.render(f"R: {myGrids[i].basicRList[dayCounter-3]}", 1, (255, 255, 255))
                rLableList.append(RLabel)

                WIN.blit(RLabel, (myGrids[i].xTL + RLabel.get_width() / 2, myGrids[i].yTL + myGrids[i].height - 30))
            WIN.blit(dayCountLabel, (WIDTH - WIDTH / 16 - dayCountLabel.get_width() / 2, HEIGHT - dayCountLabel.get_height() - 10))

            WIN.blit(infectedNumLabel, (myGrids[i].xTL + (myGrids[i].width / 2) - infectedNumLabel.get_width() / 2, myGrids[i].yTL + 10))

        if airwayOn:
            for passenger in airway.passengerList:
                passenger.draw(WIN, (217, 49, 255))

        pygame.display.update()


    for i in range(gridNum):
        grid = subGrid(subGridWidth, subGridHeight, i, gridNum)
        myGrids.append(grid)

    if airwayOn:
        airway = simpleAirway(myGrids, airwaySpeed)

    for area in myGrids:
        for i in range(personNum):
            if i == personNum-1:

                civilian = CommunityPerson(speed, area, spreadRadius, figureWidth, figureHeight)
                area.infectedList.append(civilian)
            civilian = CommunityPerson(speed, area, spreadRadius, figureWidth, figureHeight)
            area.susceptibleList.append(civilian)

        area.infectedNumList = [len(area.infectedList)]
        area.susceptibleNumList = [len(area.susceptibleList)]
        area.recoveredNumList = [len(area.recoveredList)]

    daysList = [0]

    while run:


        dt = clock.tick(FPS)
        currentFPS = 1000 / dt

        redrawWindow(commonPlace)

       # totalList = susceptibleList + infectedList
        counter+= 1

        #creating the data for the plot
        if counter%60 == 0:
            dayCounter += 1
            daysList.append(counter//60)
            for area in myGrids:
             #   print(len(area.infectedList))
                area.infectedNumList.append(len(area.infectedList))
                area.susceptibleNumList.append(len(area.susceptibleList))
                area.recoveredNumList.append(len(area.recoveredList))

                if dayCounter > 2:
                    basicR = calculateR(area.infectedNumList[dayCounter],area.infectedNumList[dayCounter-2], area.susceptibleNumList[dayCounter])
                    area.basicRList.append(basicR)


        for area in myGrids:
            area.totalList = area.infectedList + area.susceptibleList
            for person in area.totalList:

                if commonPlace:
                    person.goCommonPlace(visitProb,currentFPS)

                if airwayOn:
                    if person.checkFlight(flightProb, currentFPS):

                        person.pos = area.calculateMidPos()
                        destination = person.chooseAirport(myGrids)

                        try:

                            area.infectedList.remove(person)
                            person.infectionState = True

                        except ValueError:

                            area.susceptibleList.remove(person)
                            person.infectionState = False

                        airway.addPassenger(person, destination)



                if person.placeStayTime > 0:
                    person.placeStayTime += 1
                    if person.placeStayTime == FPS*placeStayTime:
                        person.placeStayTime = 0
                    continue

                person.move()


        if airwayOn:
            airway.fly()





        spreadProbReal = spreadProbSecond / currentFPS
        countryFinish = False
        for area in myGrids:
            for patient in area.infectedList:

                patient.incrementRecover()
                if patient.isPersonRecovered():
                    area.recoveredList.append(patient)
                    area.infectedList.remove(patient)

                for citizen in area.susceptibleList:
                    if patient.isInInfectionZone(citizen, spreadProbReal):

                        area.infectedList.append(citizen)
                        area.susceptibleList.remove(citizen)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if len(area.infectedList) > 0:
                countryFinish = True


        if countryFinish == False:
            run = False


    for area in myGrids:
        plt.figure()
        plt.plot(daysList, area.infectedNumList, label="Infected Num")
        plt.plot(daysList, area.susceptibleNumList, label="Susceptible Num")
        plt.plot(daysList, area.recoveredNumList, label="Recovered Num")
        plt.legend(loc='upper left')
        plt.xlabel("Day")
        plt.ylabel("Person Number")
        plt.title(f"Covid-19 Simulation area number:{area.gridNo}")

        plt.figure()
        plt.plot(daysList[3:], area.basicRList, label="Basic Reproduction number")
        plt.legend(loc='upper left')
        plt.xlabel("Day")
        plt.ylabel("R Value")
        plt.title(f"Covid-19 Simulation area number:{area.gridNo}")

    plt.figure()
    plt.plot(daysList[3:], area.basicRList, label="Basic Reproduction number")
    plt.legend(loc='upper left')
    plt.xlabel("Day")
    plt.ylabel("R Value")
    plt.title("Covid-19 Simulation")
    plt.show()



def runSimulation(commonPlace=False):
    run = True


    FPS = 60
    speed = 0.5
    personNum = 100
    infectedList = []
    susceptibleList = []
    recoveredList = []
    spreadProbSecond = 0.25  # 0.25 probabilty of being infected in 1 second
    counter = 0
    figureWidth = 15
    figureHeight = 15
    spreadRadius = figureWidth*4
    dayCounter = 0
    RList = []
    placeWidth = 40
    placeHeight = 40
    visitProb = 0.04  # probability of visiting common place in 1 second
    placeStayTime = 0.5 #place stay time in seconds

    clock = pygame.time.Clock()
    infected_font = pygame.font.SysFont("comicsans", 25)
    R_font = pygame.font.SysFont("comicsans", 25)
    dayCount_font = pygame.font.SysFont("comicsans", 25)

    def redrawWindow(susceptibleList, infectedList, commonPlace):
        WIN.fill((0,0,0))
        infectedNumLabel = infected_font.render(f"Infected people num: {len(infectedList)}", 1, (255,255,255))
        dayCountLabel = dayCount_font.render(f"Day num: {dayCounter}", 1, (255,255,255))

        if commonPlace:
            pygame.draw.rect(WIN,(255,255,255), (WIDTH/2 - placeWidth/2, HEIGHT/2 - placeHeight/2, placeWidth, placeHeight), 2)

        for p in susceptibleList:
            p.draw(WIN,(0,0,255))

        for d in infectedList:
            d.draw(WIN,(255,0,0))

        for k in recoveredList:
            k.draw(WIN,(55,55,55))

        if dayCounter > 3:
            RLabel = R_font.render(f"R: {basicR}", 1, (255,255,255))
            WIN.blit(RLabel, (WIDTH / 8 - RLabel.get_width() / 2, 10))
        WIN.blit(dayCountLabel, (WIDTH - WIDTH/6 - dayCountLabel.get_width() / 2, 10))

        WIN.blit(infectedNumLabel, (WIDTH / 2 - infectedNumLabel.get_width() / 2, 10))
        pygame.display.update()

    grid = Grid(WIDTH, HEIGHT)

    for i in range(personNum):
        if i == 59:
            civilian = Person(speed, grid, spreadRadius, figureWidth, figureHeight)
            infectedList.append(civilian)
        civilian = Person(speed, grid, spreadRadius, figureWidth, figureHeight)
        susceptibleList.append(civilian)

    daysList = [0]
    infectedNumList = [1]
    susceptibleNumList = [personNum]
    recoveredNumList = [0]

    while run:


        dt = clock.tick(FPS)
        currentFPS = 1000 / dt

        redrawWindow(susceptibleList,infectedList, commonPlace)

        totalList = susceptibleList + infectedList
        counter+= 1

        #creating the data for the plot
        if counter%60 == 0:
            dayCounter += 1
            daysList.append(counter//60)
            infectedNumList.append(len(infectedList))
            susceptibleNumList.append(len(susceptibleList))
            recoveredNumList.append(len(recoveredList))

            if dayCounter > 2:

                basicR = calculateR(infectedNumList[dayCounter],infectedNumList[dayCounter-2], susceptibleNumList[dayCounter])
                RList.append(basicR)


        for person in totalList:
            if commonPlace:
                person.goCommonPlace(visitProb,currentFPS)
            if person.placeStayTime > 0:
                person.placeStayTime += 1
                if person.placeStayTime == FPS*placeStayTime:
                    person.placeStayTime = 0
                continue

            person.move()


        spreadProbReal = spreadProbSecond / currentFPS

        for patient in infectedList:

            patient.incrementRecover()
            if patient.isPersonRecovered():
                recoveredList.append(patient)
                infectedList.remove(patient)

            for citizen in susceptibleList:
                if patient.isInInfectionZone(citizen, spreadProbReal):

                    infectedList.append(citizen)
                    susceptibleList.remove(citizen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if len(infectedList) == 0:
            redrawWindow(susceptibleList, infectedList, commonPlace)
            run = False


    plt.figure()
    plt.plot(daysList, infectedNumList, label="Infected Num")
    plt.plot(daysList, susceptibleNumList, label="Susceptible Num")
    plt.plot(daysList, recoveredNumList, label="Recovered Num")
    plt.legend(loc='upper left')
    plt.xlabel("Day")
    plt.ylabel("Person Number")
    plt.title("Covid-19 Simulation")

    plt.figure()
    plt.plot(daysList[3:], RList, label="Basic Reproduction Number")
    plt.legend(loc='upper left')
    plt.xlabel("Day")
    plt.ylabel("R Value")
    plt.title("Covid-19 Simulation")
    plt.show()




#-----------------------------------------------



#-----------------------------------------------




def main_menu():
    title_font = pygame.font.SysFont("comicsans", 60)
    description_font = pygame.font.SysFont("comicsans", 40)

    descriptionList = [
                        "Press 1 for normal simulation",
                        "Press 2 for common place simulation",
                        "Press 3 for communities simulation",
                        "Press 4 for enabling the air transportation"
                        ]
    open = True
    while open:
        WIN.fill((0,0,0))
        titleLabel = title_font.render("Welcome to simulation!", 1, (255, 255, 255))
        WIN.blit(titleLabel, (WIDTH / 2 - titleLabel.get_width() / 2, 125))
        for i,text in enumerate(descriptionList):
            descriptionLabel = description_font.render(text, 1, (255, 255, 255))
            WIN.blit(descriptionLabel, (WIDTH / 2 - descriptionLabel.get_width() / 2, 220 + 80 * (i + 1)))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                open = False
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_1:
                    runSimulation()
                 if event.key == pygame.K_2:
                    runSimulation(commonPlace=True)
                 if event.key == pygame.K_3:
                    communitySimulation()
                 if event.key == pygame.K_4:
                    communitySimulation(airwayOn=True)

main_menu()


