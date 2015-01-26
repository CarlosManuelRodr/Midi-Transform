#!/usr/bin/env python
#Encoding: utf-8

#========================================================================================
# title           : miditransform.py
# description     : Transform midi file.
# author          : CMRM.
# usage           : python miditransform.py [input file] [output file]
# python_version  : 2.7
# license         : Public domain.
#========================================================================================


import midi
import sys
import copy
import argparse

__version__ = "1.0.0"

class MidiFile:
    def __init__(self):
        self.tracks = []
        self.events = {'track_name': [],
                       'note_on':    [],
                       'note_off':   [],
                       'lyric':      [],
                       'marker':     [],
                       'tempo':      [],
                       'control_change':   [],
                       'program_change':   [],
                       'time_signature':   [],
                       'key_signature' :   [],
                       'smpte_offset'  :   [],
                       'text_meta'     :   []}

    def open(self, read, open_file=True):
        # Read file and organize events in dictionary.
        self.tracks = []
        if open_file:
            track_group = self.pattern = midi.read_midifile(read)
            resolution = track_group.resolution
        else:
            track_group = read

        total_times = []

        for track in track_group:
            bpm = 120
            time = 0

            # Clear dictionary values.
            for v in self.events.keys():
                self.events[v] = []

            # Events will be separeted to work with them individually.
            t = 0
            for event in track:
                if open_file:
                    t += event.tick
                    evt_type = event
                    evt_data = (t, event)
                else:
                    evt_type = event[1]
                    evt_data = event

                if isinstance(evt_type, midi.TrackNameEvent):
                    self.events["track_name"].append(evt_data)
                elif isinstance(evt_type, midi.NoteOnEvent):
                    self.events["note_on"].append(evt_data)
                elif isinstance(evt_type, midi.NoteOffEvent):
                    self.events["note_off"].append(evt_data)
                elif isinstance(evt_type, midi.LyricsEvent):
                    self.events["lyric"].append(evt_data)
                elif isinstance(evt_type, midi.MarkerEvent):
                    self.events["marker"].append(evt_data)
                elif isinstance(evt_type, midi.SetTempoEvent):
                    if open_file:
                        # Calculate elapsed time.
                        time += 60*t / (bpm * resolution)
                        bpm = event.get_bpm()
                    self.events["tempo"].append(evt_data)
                elif isinstance(evt_type, midi.ControlChangeEvent):
                    self.events["control_change"].append(evt_data)
                elif isinstance(evt_type, midi.ProgramChangeEvent):
                    self.events["program_change"].append(evt_data)
                elif isinstance(evt_type, midi.TimeSignatureEvent):
                    self.events["time_signature"].append(evt_data)
                elif isinstance(evt_type, midi.KeySignatureEvent):
                    self.events["key_signature"].append(evt_data)
                elif isinstance(evt_type, midi.SmpteOffsetEvent):
                    self.events["smpte_offset"].append(evt_data)
                elif isinstance(evt_type, midi.TextMetaEvent):
                    self.events["text_meta"].append(evt_data)
            self.tracks.append(self.events.copy())
            if open_file:
                time += 60*t / (bpm * resolution)
                total_times.append(time)
        if open_file:
            self.total_time = max(total_times)

    def save(self, midi_file, log=False):
        pattern = midi.Pattern(resolution=self.pattern.resolution, format=self.pattern.format)
        for track in self.tracks:
            # Put all events on a list.
            events = []
            for i in track["track_name"]:
                events.append(i)
            for i in track["text_meta"]:
                events.append(i)
            for i in track["program_change"]:
                events.append(i)
            for i in track["control_change"]:
                events.append(i)
            for i in track["time_signature"]:
                events.append(i)
            for i in track["key_signature"]:
                events.append(i)
            for i in track["smpte_offset"]:
                events.append(i)
            for i in track["tempo"]:
                events.append(i)
            for i in track["marker"]:
                events.append(i)
            for i in track["lyric"]:
                events.append(i)
            for i in track["note_on"]:
                events.append(i)
            for i in track["note_off"]:
                events.append(i)

            # Sort the list and dump it on the track.
            events.sort(key=lambda x: x[0])
            out_track = midi.Track()

            t_prev = 0
            t = 0
            for i in events:
                t = i[0]
                i[1].tick = t - t_prev
                t_prev = t
                out_track.append(i[1])

            # Write the file.
            eot = midi.EndOfTrackEvent(tick=0)
            out_track.append(eot)
            pattern.append(out_track)
        midi.write_midifile(midi_file, pattern)
        if log:
            open("Log.txt", "w").write(repr(pattern))

    def delay_event(self, track, new_track, event_type, max_time):
        event_times = [evt[0] for evt in track[event_type] if len(evt) != 0]
        if event_times:
            event_max_time = max(event_times)
        else:
            event_max_time = 0

        # Delay event or group of events.
        for i, evt in enumerate(track[event_type]):
            if evt[0] == event_max_time or i == len(track[event_type]) - 1:
                new_track.append((max_time, evt[1]))
            else:
                new_track.append((track[event_type][i+1][0], evt[1]))

    def revert(self):
        invertible_controllers = 64, 65, 66, 67, 68, 80, 81, 82, 83
        new_pattern = midi.Pattern(resolution=self.pattern.resolution, format=self.pattern.format)
        new_track_group = []
        times = [j[0] for track in self.tracks for i in track.keys() for j in track[i] if len(j) != 0]
        if times:
            max_time = max(times)
        else:
            max_time = 0

        for track_num, track in enumerate(self.tracks):
            notes_on = []
            controllers = []
            new_track = []

            # Change order of various events. E.g: 
            # delayevt1 -> noninvertevt1 -> delayevt2 -> noninvertevt2. will be 
            # changed to: noninvertevt1 -> delayevt1 -> noninvertevt2 -> delayevt2
            # so is easier to reverse.

            self.delay_event(track, new_track, "track_name", max_time)
            self.delay_event(track, new_track, "tempo", max_time)
            self.delay_event(track, new_track, "time_signature", max_time)
            self.delay_event(track, new_track, "key_signature", max_time)
            self.delay_event(track, new_track, "marker", max_time)
            self.delay_event(track, new_track, "program_change", max_time)
            self.delay_event(track, new_track, "text_meta", max_time)

            # Doc: The Controller Event signals the change in a MIDI channels state.
            # Controller events might be in pairs or just alone. Check both cases.
            # This inverts appeareance order. E.g:
            # noninvertevt1start -> evt1 -> noninvertevt1end -> noninvertevt2start -> evt2 -> noninvertevt2end
            # changes to: noninvertevt1end -> evt1 -> noninvertevt1start -> noninvertevt2end -> evt2 -> noninvertevt2start.
            for i, evt in enumerate(track['control_change']):
                # First check if the controller is invertible (like pedals).
                if evt[1].data[0] in invertible_controllers:
                    controller_found = False
                    # A value in the range 0 - 63 is off, and 64 - 127 is on.
                    if evt[1].data[1] >= 64 and evt[1].data[1] <= 127:
                        controllers.append(evt)
                        tmp = midi.ControlChangeEvent(tick=evt[1].tick, channel=evt[1].channel, data=[evt[1].data[0], 0])
                        new_track.append((evt[0], tmp))
                    else:
                        for j, controller in enumerate(controllers):
                            # Look for controller match.
                            if controller[1].data[0] == evt[1].data[0]:
                                new_track.append((evt[0], controller[1]))
                                controllers.pop(j)
                                controller_found = True
                                break

                            if not controller_found:
                                print("Warning: No matching controller found on invertible controller.")
                                tmp = midi.ControlChangeEvent(tick=evt[1].tick, channel=evt[1].channel, data=[evt[1].data[0], 127])
                                new_track.append((evt[0], tmp))

                # If it's not invertible just append it changing the order.
                else:
                    if i == len(track['control_change']) - 1:
                        new_track.append((max_time, evt[1]))
                    else:
                        new_track.append((track['control_change'][i+1][0], evt[1]))

            if len(controllers) != 0:
                # The unmatched ones are probably at the end of the track.
                print("Warning: Track " + str(track_num) + ", " + str(len(controllers)) + " controller event/s unmatched.")
                for c in controllers:
                    new_track.append((max_time, c))

            # Reverse notes (invert appearance order).
            for evt in track['note_on']:
                # Notes on.
                if evt[1].data[1] != 0:
                    notes_on.append(evt)
                    tmp = midi.NoteOnEvent(tick=evt[1].tick, channel=evt[1].channel, data=[evt[1].data[0], 0])
                    new_track.append((evt[0], tmp))

                # Notes off.
                else:
                    note_found = False
                    for i, note in enumerate(notes_on):
                        # Look for note match.
                        if note[1].data[0] == evt[1].data[0]:
                            new_track.append((evt[0], note[1]))
                            notes_on.pop(i)
                            note_found = True
                            break   

                    if not note_found:
                        print("Warning: No matching note found.")
                        tmp = midi.NoteOnEvent(tick=evt[1].tick, channel=evt[1].channel, data=[evt[1].data[0], 100])
                        new_track.append((evt[0], tmp))

            # The same as before.
            for evt in track['note_off']:
                note_found = False
                for i, note in enumerate(notes_on):
                    # Look for note match.
                    if note[1].data[0] == evt[1].data[0]:
                        new_track.append((evt[0], note[1]))
                        notes_on.pop(i)
                        note_found = True
                        break   

                if not note_found:
                    print("Warning: No matching note found.")
                    tmp = midi.NoteOnEvent(tick=evt[1].tick, channel=evt[1].channel, data=[evt[1].data[0], 100])
                    new_track.append((evt[0], tmp))

            if len(notes_on) != 0:
                print("Warning: Track " + str(track_num) + ", " + str(len(notes_on)) + " note/s unmatched.")

            # Lyrics won't be changed.
            for evt in track['lyric']:
                new_track.append(evt)

            # Sort and eliminate the empty time after the reversal.
            new_track.sort(key=lambda x: x[0], reverse=True)
            for i, evt in enumerate(new_track):
                t = max_time - evt[0]
                new_track[i] = (t, evt[1])
            new_track_group.append(list(new_track))

        # Find the time when the first note occurs.
        noteon_times = [evt[0] for track in new_track_group for evt in track if isinstance(evt[1], midi.NoteOnEvent)]
        if len(noteon_times) > 0:
            min_noteon = min(noteon_times)
            if min_noteon != 0:
                for i, evt in enumerate(new_track):
                    t = evt[0] - min_noteon
                    if t > 0:
                        new_track[i] = (t, evt[1])
        self.open(read=new_track_group, open_file=False)

    def change_pitch(self, pitch_var):
        # Add pitch_var to every note value.
        new_pattern = midi.Pattern(resolution=self.pattern.resolution, format=self.pattern.format)
        new_track_group = []
        times = [j[0] for track in self.tracks for i in track.keys() for j in track[i] if len(j) != 0]
        if times:
            max_time = max(times)
        else:
            max_time = 0

        for i, track in enumerate(self.tracks):
            for j, evt in enumerate(track['note_on']):
                tmp = list(evt[1].data)
                tmp[0] += pitch_var
                self.tracks[i]['note_on'][j][1].data = tuple(tmp)

            for j, evt in enumerate(track['note_off']):
                tmp = list(evt[1].data)
                tmp[0] += pitch_var
                self.tracks[i]['note_off'][j][1].data = tuple(tmp)

    def invert(self):
        # Change every note value to 127 - note value.
        new_pattern = midi.Pattern(resolution=self.pattern.resolution, format=self.pattern.format)
        new_track_group = []
        times = [j[0] for track in self.tracks for i in track.keys() for j in track[i] if len(j) != 0]
        if times:
            max_time = max(times)
        else:
            max_time = 0

        for i, track in enumerate(self.tracks):
            for j, evt in enumerate(track['note_on']):
                tmp = list(evt[1].data)
                tmp[0] = 127 - tmp[0]
                self.tracks[i]['note_on'][j][1].data = tuple(tmp)

            for j, evt in enumerate(track['note_off']):
                tmp = list(evt[1].data)
                tmp[0] = 127 - tmp[0]
                self.tracks[i]['note_off'][j][1].data = tuple(tmp)

    def get_length(self):
        return self.total_time

    def print_file(self, log_file):
        open(log_file, "w").write(repr(self.pattern))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", help="Input midi file.")
    parser.add_argument("outfile", help="Reversed output midi file.")
    parser.add_argument("-l", "--log", action="store_true", help="Write log to files.")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse midi file.")
    parser.add_argument("-i", "--invert", action="store_true", help="Invert notes on pentagram.")
    parser.add_argument("-c", "--change_pitch", metavar='<pitch_var>', type=int, help="Change pitch of midi file. Argument is pitch change. E.g: -c 2.", default=0)
    args = parser.parse_args()
    log = args.log
    change_pitch = args.change_pitch
    reverse = args.reverse
    invert = args.invert

    if change_pitch == 0 and not reverse and not invert:
        print("Please, introduce and option. Use -h to see a list of avalable options.")

    a = MidiFile()
    a.open(args.inputfile)
    if log:
        a.print_file("Original.txt")

    if reverse:
        a.revert()
    if invert:
        a.invert()
    if change_pitch != 0:
        a.change_pitch(change_pitch)

    a.save(args.outfile, log)
    print("Done.")