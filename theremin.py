
from gpiozero import DistanceSensor, TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
from rpi_lcd import LCD
from sortedcontainers import SortedDict
from threading import Thread
import board
import busio
import adafruit_vl53l0x


sd = SortedDict()
lcd = LCD()
#lcd.text("hi PETE", 1)
#sleep(0.1)
#lcd.clear
sleep(0.1)
i2c=busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

#uds = DistanceSensor(trigger=17, echo=27)
buzzer = TonalBuzzer(21, octaves=4)

#def string_for_hertz(hertz):

sd[123.4]= "B"
sd[130.8]= "C"
sd[138.5]= "C#"
sd[146.8]= "D"
sd[155.5]= "Eb"
sd[164.8]= "E"
sd[174.6]= "F"
sd[184.9]= "F#"
sd[195.9]= "G"
sd[207.6]= "Ab"
sd[220.0]= "A"
sd[233.0]= "Bb"
sd[246.9]= "B"
sd[261.6]= "C"
sd[277.1]= "C#"
sd[293.6]= "D"
sd[311.1]= "Eb"
sd[329.6]= "E"
sd[349.2]= "F"
sd[369.9]= "F#"
sd[391.9]= "G"
sd[415.3]= "Ab"
sd[440.0]= "A"
sd[466.1]= "Bb"
sd[493.8]= "B"
sd[523.2]= "C"
sd[554.3]= "C#"
sd[587.3]= "D"
sd[622.2]= "Eb"
sd[659.2]= "E"
sd[698.4]= "F"
sd[740.0]= "F#"
sd[784.0]= "G"
sd[830.6]= "Ab"
sd[880.0]= "A"
sd[932.3]= "Bb"
sd[987.7]= "B"
sd[1046.5]= "C"
sd[1108.7]= "C#"
sd[1174.7]= "D"
sd[1244.5]= "Eb"


def distance_to_tone2(distance_value):
    min_tone = buzzer.min_tone
    max_tone = buzzer.max_tone
    #20 is the min distance the device measures
    #500 is the max value the device can accurately measure
    #693-130 is the range of hertz we want to replicate
    #130 is the starting note
    scaled_distance = ((distance_value-20)/500.0)*(693-130)+130
    return min(max(scaled_distance, min_tone.frequency), max_tone.frequency)

samples_too_far = 0
last_sample_good = True
note_string = ""

def display_function2():
    while True:
        lcd.text(note_string, 1)
        sleep(0.15)

display_thread = Thread(target=display_function2, args=())
display_thread.start()

while True:
    distance_value = sensor.range
    if distance_value < 1700:
        samples_too_far = 0 #max(samples_too_far-1, 0)
        if last_sample_good == True:
            tone = distance_to_tone2(distance_value)
            note_index = sd.bisect_left(tone)
            note_index = min(note_index, len(sd)-1)
            note_string = sd.peekitem(note_index)[1]
            #print (tone)
            buzzer.play(Tone.from_frequency(tone))
        last_sample_good = True
    else:
        last_sample_good = False
        samples_too_far=samples_too_far+1
        if samples_too_far >= 15:
            buzzer.play(None)
            note_string = ""