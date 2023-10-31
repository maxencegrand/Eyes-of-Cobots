class Step:
    def __init__(self, id, begin, duration):
        self.id = id
        self.begin = begin
        self.duration = duration
        self.end = self.begin = self.duration

    def __str__(self):
        return f"Step {self.id} begins at {self.begin} and lasts {self.duration}ms"
