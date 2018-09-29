class SCNTime:
    def __init__(self, start_time: str, sunset_time: str, sunrise_time: str):
        self.start_time = datetime.time()
        self.sunset_time = sunset_time
        self.sunrise_time = sunrise_time
