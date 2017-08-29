import multiprocessing
from slowclap import (MicrophoneFeed, AmplitudeDetector,
RateLimitedDetector,VerboseFeed,Detector)


class MultiClapDetector(Detector):

        def __init__(self, d, rate_limit=1, num_of_claps=2):
                self.child=d
                self.last_clap = -rate_limit
                self.rate_limit = rate_limit
                self.num_of_claps = num_of_claps
                self.claps_per_rate = []

        def __iter__(self):
                for clap in self.child:
                        if clap.time - self.last_clap > self.rate_limit:
                                self.last_clap = clap.time
                                self.claps_per_rate = []
                        else:
                                self.claps_per_rate.append(clap.time)
                                if len(self.claps_per_rate)== self.num_of_claps:
                                        yield clap

def detect_one_clap(q):
        feed = MicrophoneFeed()

        value = 1
        detector = AmplitudeDetector(feed, 10000000)
        detector = RateLimitedDetector(detector, 1)

        for clap in detector:
            
                q.put(value)


def detect_two_claps(q):

        feed = MicrophoneFeed()

       
        detector = AmplitudeDetector(feed,10000000)
        
        detector = MultiClapDetector(detector)
        print(detector.last_clap)
        for clap in detector:
                q.put(value)
def main():

        q = multiprocessing.Queue()
        p1= multiprocessing.Process(target=detect_one_clap, args=(q,))
        p2= multiprocessing.Process(target=detect_two_claps, args=(q,) )

        p1.start()
        p2.start()
        while True:
                f = open("clapstatus.txt", "w")

                value= q.get()
                if value == 1:
                        print("Clap")
                        f.write("1")
                elif value == 2:
                        print("Claps")
                        f.write("2")
                else:
                        f.write("0")
        f.close()
        p1.terminate()
	p2.terminate()
main()





