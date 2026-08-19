from mfrc522 import SimpleMFRC522
from time import sleep
import vlc
from gpiozero import PWMOutputDevice, DigitalOutputDevice

AIN1 = DigitalOutputDevice(31)
AIN2 = DigitalOutputDevice(29)
PWMA = PWMOutputDevice(12)
STBY = DigitalOutputDevice(18)

STBY.on()

nfc_reader = SimpleMFRC522()

# Add your songs here
# id (written on the nfc chip): vlc.MediaPlayer("path to your mp3")


songs = {

    123456789: vlc.MediaPlayer("file:///home/qwatrum/piano1.mp3"), 
    87654321: vlc.MediaPlayer("file:///home/qwatrum/piano2.mp3")

    }

read_attempt = 0
current_song = None

try:
    while True:
        id, txt = nfc_reader.read_no_block()

        if id in songs:
            if id != current_song:
                for song in songs.values():
                    song.stop()
                songs[id].play()
                current_song = id
                read_attempt = 0
                AIN1.on()
                AIN2.off()
                PWMA.value = 0.2
        else:
            if current_song != None:
                read_attempt += 1

                if read_attempt > 3:
                    for song in songs.values:
                        song.stop()
                    read_attempt = 0
                    PWMA.value = 0
                    AIN1.off()
                    AIN2.off()

                    current_song = None
        sleep(0.1)

except KeyboardInterrupt:
    PWMA.value = 0
    AIN1.off()
    AIN2.off()

    STBY.off()