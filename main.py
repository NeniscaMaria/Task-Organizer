from meniu import printMeniu
from graph import DirectedGraph,Edge
from domain import Activity

class UI:
    def __init__(self):
        self.activities={}
        self.activitiesGraph=0
        self.noActivites=0
        self.dependecy={} #a dictionary which has as keys the activityID of an activity and as values the list of activtyID's of the activities that need to be finished before that task begins
        self.sortedTopo=[]
        
    def checkChoice(self,choice):
        if choice.isdigit()==False:
            raise ValueError("Not a digit. Please insert a digit between 1 and 5!")
        if int(choice) not in [1,2,3,4,5,6]:
            raise ValueError("Please insert a digit between 1 and 5!")
    def checkActivityName(self,activityName):
        if activityName.isdigit()==True:
            raise ValueError("Activity name must contain letters.")
    def checkDuration(self, activityDuration):
        if activityDuration.isdigit()==False:
            raise ValueError("Duration must be a digit.")
    def getPrerequisites(self):
        print("Prerequisites: for each activity, you must specify the previous activity by their activityID (to mark the end, insert 0)")
        lst=[]
        while True:
            try:
                element=input(">>")
                if int(element)==0:
                    break
                if element.isdigit()==False:
                    raise ValueError("Prerequisite must be an activityId(digit).")
                element=int(element)
                lst.append(element)
            except ValueError as ve:
                print(ve)
        return lst
    def printGraph(self):
        for origin in self.activitiesGraph.parseVertices():
                print("The vertex "+str(origin)+" has "+str(len(self.activitiesGraph.parseOutboundNeighbors(origin)))+" outbound neighbor(s):")
                for target in self.activitiesGraph.parseOutboundNeighbors(origin):
                    print(str(origin)+" ---> "+str(target))
    def createGraph(self):
        self.activitiesGraph=DirectedGraph(self.noActivites+1,0)
        for i in self.dependecy.keys():
            if self.dependecy[i]==[]:
                edge=Edge(0,i)
                cost=0
                self.activitiesGraph._addEdge(edge, cost)
            else:
                for j in self.dependecy[i]:
                    edge=Edge(j,i)
                    cost=0
                    self.activitiesGraph._addEdge(edge, cost)
        for vertex in self.activitiesGraph.parseVertices():
            if self.activitiesGraph._getOutdegree(vertex)==0 and vertex!=self.noActivites:
                edge=Edge(vertex,self.noActivites)
                cost=0
                self.activitiesGraph._addEdge(edge, cost)
        self.printGraph()
    def getActivities(self):
        if self.activities!={}:
            raise ValueError("Activities already inserted!")
        self.activities[0]=Activity("0","","","","",0) #fictive activity
        activityID=1;
        while True:
            try:
                activityName=input("Activity name: ")
                if activityName=='0':
                    break
                self.checkActivityName(activityName)
                activityDuration=input("Activity duration: ")
                self.checkDuration(activityDuration)
                activityDuration=int(activityDuration)
                prerequisites=self.getPrerequisites()
                self.dependecy[activityID]=prerequisites
                print(activityID)
                self.activities[activityID]=Activity( activityName,"","","","",activityDuration)
                activityID+=1
            except ValueError as ve:
                print(ve)
        self.activities[activityID]=Activity("","","","","",0)#fictiveActivity
        self.noActivites=activityID
        self.createGraph()

    def topoSortDFS(self, vertex, sorted, fullyProcessed, inProcess):
        inProcess.add(vertex)
        for y in self.activitiesGraph.parseInboundNeighbors(vertex):
            if y in inProcess:
                return False
            elif y not in fullyProcessed:
                ok=self.topoSortDFS(y, sorted, fullyProcessed, inProcess)
                if not ok:
                    return False
        inProcess.remove(vertex)
        sorted.append(vertex)
        fullyProcessed.add(vertex)
        return True
    def TarjanAlgorithm(self):
        sorted=[]
        fullyProcessed=set()
        inProcess=set()
        for vertex in self.activitiesGraph.parseVertices():
            if vertex not in fullyProcessed:
                ok=self.topoSortDFS(vertex,sorted,fullyProcessed,inProcess)
                if not ok:
                    sorted=[]
                    return sorted
        return sorted
    def checkDAG(self):
        if self.activities=={}:
            raise ValueError("Please insert activities first!")
        if self.activitiesGraph==0:
            raise ValueError("Please form the graph of activities first!")
        sorted = self.TarjanAlgorithm()
        if sorted==[]:
            print("The graph is not DAG!")
        else:
            print("The graph is DAG!")
            self.sortedTopo=sorted
    

    def getEarliestTimes(self):
        self.activities[0].set_activity_earliest_start_time(0)
        self.activities[0].set_activity_earliest_end_time(0)
        for i in self.sortedTopo:
            self.activities[i].set_activity_earliest_start_time(0)
            self.activities[i].set_activity_earliest_end_time(0)
            for i in range(1,self.noActivites+1):
                tmax=0;
                for vertex in self.activitiesGraph.parseInboundNeighbors(i):
                    tmax=max(tmax,int(self.activities[vertex].get_activity_earliest_end_time()))
                self.activities[i].set_activity_earliest_start_time(tmax)
                self.activities[i].set_activity_earliest_end_time(tmax+self.activities[i].get_activity_duration())
    def getLatestTimes(self):
        self.activities[self.noActivites].set_activity_latest_end_time(self.activities[self.noActivites].get_activity_earliest_end_time())
        self.activities[self.noActivites].set_activity_latest_start_time(self.activities[self.noActivites].get_activity_latest_end_time()-self.activities[self.noActivites].get_activity_duration())
        for i in (len(self.sortedTopo)-1,0):
            vertex=self.sortedTopo[i]
            self.activities[vertex].set_activity_latest_end_time(self.activities[vertex].get_activity_earliest_end_time())
            self.activities[vertex].set_activity_latest_start_time(self.activities[vertex].get_activity_latest_end_time()-self.activities[vertex].get_activity_duration())
            for j in range(self.noActivites-1,0,-1):
                tmin=1000
                for k in self.activitiesGraph.parseOutboundNeighbors(j):
                    tmin=min(tmin,self.activities[k].get_activity_latest_start_time())
                self.activities[j].set_activity_latest_end_time(tmin)  
                self.activities[j].set_activity_latest_start_time(tmin-self.activities[j].get_activity_duration())
    def printTimes(self):
        for i in self.sortedTopo:
            if i!=0 and i!=self.noActivites:
                activity=self.activities[i]
                print("Activity: "+activity.get_activity_name()+":")
                print("\tEarliest start time: "+ str(activity.get_activity_earliest_start_time()))
                print("\tEarliest end time: "+ str(activity.get_activity_earliest_end_time()))
                print("\tLatest start time: "+ str(activity.get_activity_latest_start_time()))
                print("\tLatest end time: " + str(activity.get_activity_latest_end_time()))
    def getTotalTime(self):
        print("Total time: "+str(self.activities[self.noActivites].get_activity_latest_end_time()))    
    def getSchedule(self):
        if self.activities=={}:
            raise ValueError("Please insert activities first!")
        if self.activitiesGraph==0:
            raise ValueError("Please form the graph of activities first!")
        if self.sortedTopo==[]:
            self.sortedTopo=self.TarjanAlgorithm()
        if self.sortedTopo==[]:
            raise ValueError("The graph is not DAG!")
        self.getEarliestTimes()
        self.getLatestTimes()
        self.getTotalTime()
        self.printTimes()
        
    
    def getCriticalActivities(self):
        if self.activities=={}:
            raise ValueError("Please insert activities first!")
        if self.activitiesGraph==0:
            raise ValueError("Please form the graph of activities first!")
        if self.sortedTopo==[]:
            self.sortedTopo=self.TarjanAlgorithm()
        if self.sortedTopo==[]:
            raise ValueError("The graph is not DAG!")
        self.getEarliestTimes()
        self.getLatestTimes()
        criticalActivitiesID=[]
        for i in self.activities.keys():
            if i!=0 or i!=self.noActivites:
                activity=self.activities[i]
                earliestStartTime=activity.get_activity_earliest_start_time()
                latestStartTime=activity.get_activity_latest_start_time()
                if earliestStartTime==latestStartTime:
                    criticalActivitiesID.append(i)
        print("The critical activities are:",)
        for i in criticalActivitiesID:
            if self.activities[i].get_activity_name() not in ['0','']:
                print("->"+self.activities[i].get_activity_name()+"") 
    
    def baseActivites(self):
        #read from file
        #'''
        self.activities[0]=Activity("0","","","","",0) #fictive activity
        activityID=1;
        self.activities[activityID]=Activity("A","","","","",2)
        self.dependecy[activityID]=[]
        activityID+=1
        self.activities[activityID]=Activity("B","","","","",3)
        self.dependecy[activityID]=[]
        activityID+=1
        self.activities[activityID]=Activity("C","","","","",5)
        self.dependecy[activityID]=[2]
        activityID+=1
        self.activities[activityID]=Activity("D","","","","",3)
        self.dependecy[activityID]=[1]
        activityID+=1
        self.activities[activityID]=Activity("E","","","","",3)
        self.dependecy[activityID]=[1]
        activityID+=1
        self.activities[activityID]=Activity("F","","","","",3)
        self.dependecy[activityID]=[3,4,5]
        activityID+=1
        self.activities[activityID]=Activity("G","","","","",2)
        self.dependecy[activityID]=[3,6]
        activityID+=1
        self.activities[activityID]=Activity("","","","","",0)#fictive activity
        '''
        #if you want to not be a DAG
        self.activities[0]=Activity("0","","","","",0) #fictive activity
        activityID=1;
        self.activities[activityID]=Activity("A","","","","",2)
        self.dependecy[activityID]=[]
        activityID+=1
        self.activities[activityID]=Activity("B","","","","",3)
        self.dependecy[activityID]=[]
        activityID+=1
        self.activities[activityID]=Activity("C","","","","",5)
        self.dependecy[activityID]=[2,7]
        activityID+=1
        self.activities[activityID]=Activity("D","","","","",3)
        self.dependecy[activityID]=[1]
        activityID+=1
        self.activities[activityID]=Activity("E","","","","",3)
        self.dependecy[activityID]=[1]
        activityID+=1
        self.activities[activityID]=Activity("F","","","","",3)
        self.dependecy[activityID]=[3,4,5]
        activityID+=1
        self.activities[activityID]=Activity("G","","","","",2)
        self.dependecy[activityID]=[6]
        activityID+=1
        self.activities[activityID]=Activity("","","","","",0)#fictive activity
        '''
        self.noActivites=activityID
        self.createGraph()
    
    def main(self):
        while True:
            try:
                printMeniu()
                choice=input(">>")
                self.checkChoice(choice)
                choice=int(choice)
                if choice==1:
                    self.getActivities()
                if choice==2:
                    self.checkDAG()
                if choice==3:
                    self.getSchedule()
                if choice==4:
                    self.getCriticalActivities()
                if choice==5:
                    break
                if choice==6:
                    self.baseActivites()
            except ValueError as ve:
                print(ve)
            
ui=UI()
ui.main()