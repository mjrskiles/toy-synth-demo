# toy synth

A __proof-of-concept__ synthesizer written in python

## Quick Start
---

### Project requirements & dependencies
---

This project requires python 3.10. It may work with python 3.11, but it has not been tested.

The synthesizer is controlled by MIDI, so you will need a MIDI controller as well, or some way of sending MIDI messages.

These instructions are written for Windows first, but effort has been made to make them as platform agnostic as possible.

NOTE to macOS users: wherever we run ```python```, you may need to run ```python3``` or even ```python3.10```. Check your python version with ```python --version```. If you don't have python3.10 installed, I recommend installing it with homebrew.

### Setting up the environment
---

Open a terminal and clone the repository into your projects directory:

```git clone https://github.com/mjrskiles/toy-synth-demo.git```

Navigate to the toy-synth-demo folder:

```cd toy-synth-demo```

Make sure you have the virtualenv python module installed on your machine. You can either run ```python -m virtualenv --version``` to check your version or ```pip install virtualenv``` to install it. (you may need to use ```pip3``` instead of ```pip```)

Now create a virtual environment:

```python -m virtualenv venv```

This should create a folder called venv. Activate the virtual environment:

Windows: ```.\venv\Scripts\activate```

Mac and Linux: ```source ./venv/bin/activate```

You should see ```(venv)``` appear in front of your shell prompt.

Now let's install the project dependencies:

```pip install -r requirements.txt```

### Setting up the synth
---

Now make sure your MIDI controller is plugged in to your computer and not attached to any other software such as a DAW.

Before we launch the synth, let's discover the name of the MIDI controller so we can attach to it. At your shell prompt with the virtual environment active:

```python```

This should open the python REPL. Now:

```
>>> import synth.midi as midi
>>> midi.get_available_controllers()
```

Should return something like 

```['MPK mini 3']```

where MPK mini 3 is replaced by the name of your controller. Copy the name of your controller, including the quotes (but not the array brackets).

You can now launch the program with ```python -m synth -p <controller-name>```.

If you'd like to set this controller to attach every time without passing a command line argument, you can. With the synth-demo project open in a text editor, open synth/settings.py. On the line with the ```auto_attach``` property, replace 'MPK mini 3' with your controller name.

Now we're ready to launch the program.

```python -m synth```

Should launch the synth and give an output like:

```
2023-07-04 19:11:40 [INFO] __main__ [<module>]:
    __
   |  |
 __|  |___             ______         __        __
/__    __/          __|______|__     |  |      |  |
   |  |            |  |      |  |    |__|______|  |
   |  |     __     |  |      |  |       |______   |
   |__|____|__|    |__|______|__|        ______|__|
      |____|          |______|          |______|

                                                            __              __
                                                           |  |            |  |
    _______         __        __      __    ____         __|  |___         |  |   ____
 __|_______|       |  |      |  |    |  |__|____|__     /__    __/         |  |__|____|__
|__|_______        |__|______|  |    |   __|    |  |       |  |            |   __|    |  |
   |_______|__        |______   |    |  |       |  |       |  |     __     |  |       |  |
 __________|__|        ______|__|    |  |       |  |       |__|____|__|    |  |       |  |
|__________|          |______|       |__|       |__|          |____|       |__|       |__|

2023-07-04 19:11:40 [INFO] __main__ [<module>]: Available MIDI ports: ['3- Focusrite USB MIDI 0', 'MPK mini 3 1']
2023-07-04 19:11:40 [INFO] __main__ [<module>]: Using MIDI port MPK mini 3 1
2023-07-04 19:11:40 [INFO] synthesizer [__init__]: Signal Chain Prototype:
--- Signal Chain ---
Delay#6468
  LowPassFilter#2980
    Mixer#5522
      Gain#4630
        SawtoothWaveOscillator#1995
      Gain#3090
        SquareWaveOscillator#9454

2023-07-04 19:11:40 [INFO] midi_listener [run]: Opened port MPK mini 3 1
```

At this point the synth is running and ready to make sound! Before you play, I'd highly recommend starting with the volume turned all the way down and adjusting it up slowly while playing a note.

### Setting up knobs/faders
---

With the synth running and your terminal in view try moving a knob or fader. You should get a log output like

```2023-07-01 09:53:47 [INFO] synthesizer [control_change_handler]: Control Change: channel 0, number 71, value 9```

The important segment here is ```number <num>```, where ```<num>``` is the CC number for the knob or fader you moved.

Now open synth/midi/implementation.py. You should see an Enum assigning integer values to synth-related properties. What you need to do is decide which knobs/faders you want to use for each property and use the method described above to determine the CC number to assign to that property. For example, I have CC number 71 assigned to the Low-pass filter cutoff.

Go ahead and assign MIDI CC numbers to each property in the Enum. Then we'll need to restart the synth for it to take effect.

Close the synth by pressing ctrl-C in the terminal and then hitting any key or control on your MIDI controller. (yeah, I know.)

You are officially set up! Go ahead and start the synth again and feel free to play around.