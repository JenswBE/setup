#!/usr/bin/python
from subprocess import call
import RPi.GPIO as GPIO
import time

# ===== SETTINGS =====
base_dir = '/tmp/radio/'
speech_dir = base_dir + 'speech/'
stations = [
    {
        'name': 'MNM',
        'url': 'http://mp3.streampower.be/mnm-high.mp3',
        },
    {
        'name': 'MNM Hits',
        'url': 'http://mp3.streampower.be/mnm_hits-high.mp3',
        },
    {
        'name': 'RGR FM',
        'url': 'http://5.255.85.19/rgrfm',
        },
    {
        'name': 'Studio Brussels',
        'url': 'http://mp3.streampower.be/stubru-high.mp3',
        },
    {
        'name': 'Q Music',
        'url': 'http://icecast-qmusic.cdp.triple-it.nl:80/Qmusic_be_live_96.mp3',
        },
    {
        'name': 'Joe FM',
        'url': 'http://icecast-qmusic.cdp.triple-it.nl:80/JOEfm_be_live_128.mp3',
        },
    {
        'name': 'Nostalgia',
        'url': 'http://nostalgiewhatafeeling.ice.infomaniak.ch/nostalgiewhatafeeling-128.mp3',
        },
    {
        'name': 'Radio 2',
        'url': 'http://mp3.streampower.be/ra2ant-high.mp3',
    },
    {
        'name': 'Ketnet Radio',
        'url': 'http://mp3.streampower.be/ketnetradio-high.mp3',
        }
]
station_count = len(stations)
current_station = 0
playing = True

# ===== SETUP GPIO =====

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# ===== HELPER FUNCTIONS =====


def mpc_pause():
    call('sudo mpc pause', shell=True)
    global playing
    playing = False


def mpc_stop():
    call('sudo mpc stop', shell=True)
    global playing
    playing = False


def mpc_play(station=-1):
    mpc_stop()
    if station < 0:
        call('sudo mpc play', shell=True)
    else: 
        call('espeak "%s" --stdout | aplay' % stations[station]['name'], shell=True)
        call('sudo mpc play %d' % (station + 1), shell=True)
        global playing
    playing = True

# ===== MAIN PROGRAM =====

# === Init ===
# Clear list and add stations
call('sudo mpc clear', shell=True)
for station in stations:
    call('sudo mpc add %s' % station['url'], shell=True)

# Start station
mpc_play(current_station)

# === Program loop

while True:
    input_state18 = GPIO.input(18)
    if input_state18:
        was_playing = playing
        if was_playing:
            mpc_stop()

        call('date \'+%A %-d %B\' | espeak --stdout | aplay', shell=True)

        if was_playing:
            mpc_play()

    # Prev
    input_state21 = GPIO.input(21)
    if input_state21:
        current_station -= 1
        if current_station < 0:
            current_station = station_count - 1
        mpc_play(current_station)
     
    # Stop/play
    input_state22 = GPIO.input(22)
    if input_state22:
        if playing:
            mpc_stop()
        else:
            mpc_play()

    # Next
    input_state23 = GPIO.input(23)
    if input_state23:
        current_station += 1
        if not current_station < station_count:
            current_station = 0
        mpc_play(current_station)


while True:
    # Get input
    cmd = str.lower(raw_input("> "))

    # Parse input
    if cmd == 'play':
        mpc_play()

    elif cmd == 'pause':
        mpc_pause()

    elif cmd == 'next':
        current_station += 1
        if not current_station < station_count:
            current_station = 0
        mpc_play(current_station)

    elif cmd == 'prev':
        current_station -= 1
        if current_station < 0:
            current_station = station_count - 1
        mpc_play(current_station)

    elif cmd == 'exit':
        exit()
