import time

class BlinkProcessor:

    def __init__(self):

        self.blink_start=None
        self.last_blink_time=0
        self.cooldown=0.5
        self.morse=""

    def detect(self,eye_closed):

        current=time.time()

        if eye_closed:

            if self.blink_start is None and current-self.last_blink_time>self.cooldown:

                self.blink_start=current

        else:

            if self.blink_start is not None:

                duration=current-self.blink_start

                if duration<0.4:
                    self.morse+="."
                    print("DOT")

                else:
                    self.morse+="-"
                    print("DASH")

                self.last_blink_time=current
                self.blink_start=None

    def reset_letter(self):

        self.morse=""