#!/usr/bin/env python3
# Project: Tune Maker for GRUB2
# Description: GRUB2 has the ability to play small files using it's play command. These files have to be formatted a certain way or the command either, plays the wrong pitch and duration or fails to run. This program creates the file necessary for the command to work in a way that the GRUB2 play command can understand. Just feed it the same values as the GRUB2 command line, in the same order. This code will then create a flie of the correct format, in the location you specified.
# Filename: MakeJingle.py
# Author: John Wolfe
# Date: 09/07/24

# Standard Library imports.
import argparse
import math
import struct

# 3rd party imports.

# Local application imports.

#-------------------------------------------------------------------------------

# Run only if this file is NOT imported.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose output, show the command output on the screen. Otherwise, the command should exit silently.", action="store_true")
    parser.add_argument("file", help="The file to output the formatted tune to.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-t", "--tune", help="The list of integers that make the tune, separated by spaces and surrounded by quotes. The first number is tempo, then pairs of numbers for pitch and duration respectively. The tempo is the base for all note durations. 60 gives a 1-second base, 120 gives a half-second base, etc. Pitches are Hz. Set pitch to 0 to produce a rest.")
    group.add_argument("-i", "--input", help="The text file to use as input, must contain information that is formatted the same way as the \"-t\" or \"--tune\" argument in GRUB.")
    args = parser.parse_args()
    if args.tune != None:
        if args.verbose:
            print("Tune mode selected.")
        # We are going to want to make a list of all the integers, starting at the beginning.
        tune = args.tune.rsplit(" ")
        # Now we have our list of numbers in 'tune' we can operate on it.
        for i in range(len(tune)):
            if i == 0:
                if args.verbose:
                    print(f"The Tempo is set to: {tune[0]}.")
                    print(f"This will result in a base note duration of {int(tune[0]) / 60}")
                tune[i] = struct.pack('<I', int(tune[i]))
            else:
                tune[i] = struct.pack('<H', int(tune[i]))
                if math.fmod(i, 2) != 0:
                    if args.verbose:
                        # This is a number representing note pitch.
                        print(f"The Pitch for note {i} is: {tune[i]}.")
                else:
                    if args.verbose:
                        # This is a number representing note duration
                        print(f"The Pitch for the note {i} is: {tune[i]}.")
        f = open(args.file, "wb")
        for i in range(len(tune)):
            f.write(tune[i])
        f.close
    elif args.input != None:
        if args.verbose:
            print("File input mode not implemented.")
