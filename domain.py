class Activity():
    def __init__(self, activityName,activityEarliestStartTime,activityLatestStartTime,activityEarliestEndTime,activityLatestEndTime,activityDuration):
        self.__activityName=activityName
        self.__activityEarliestStartTime=activityEarliestStartTime
        self.__activityLatestStartTime=activityLatestStartTime
        self.__activityEarliestEndTime=activityEarliestEndTime
        self.__activityLatestEndTime=activityLatestEndTime
        self.__activityDuration=activityDuration

    def set_activity_name(self, value):
        self.__activityName = value


    def set_activity_earliest_start_time(self, value):
        self.__activityEarliestStartTime = value


    def set_activity_latest_start_time(self, value):
        self.__activityLatestStartTime = value


    def set_activity_earliest_end_time(self, value):
        self.__activityEarliestEndTime = value


    def set_activity_latest_end_time(self, value):
        self.__activityLatestEndTime = value


    def get_activity_name(self):
        return self.__activityName


    def get_activity_earliest_start_time(self):
        return self.__activityEarliestStartTime


    def get_activity_latest_start_time(self):
        return self.__activityLatestStartTime


    def get_activity_earliest_end_time(self):
        return self.__activityEarliestEndTime


    def get_activity_latest_end_time(self):
        return self.__activityLatestEndTime


    def get_activity_duration(self):
        return self.__activityDuration
    

    activityName = property(get_activity_name, None, None, None)
    activityEarliestStartTime = property(get_activity_earliest_start_time, None, None, None)
    activityLatestStartTime = property(get_activity_latest_start_time, None, None, None)
    activityEarliestEndTime = property(get_activity_earliest_end_time, None, None, None)
    activityLatestEndTime = property(get_activity_latest_end_time, None, None, None)
    activityDuration = property(get_activity_duration, None, None, None)
    activityName = property(None, set_activity_name, None, None)
    activityEarliestStartTime = property(None, set_activity_earliest_start_time, None, None)
    activityLatestStartTime = property(None, set_activity_latest_start_time, None, None)
    activityEarliestEndTime = property(None, set_activity_earliest_end_time, None, None)
    activityLatestEndTime = property(None, set_activity_latest_end_time, None, None)
        