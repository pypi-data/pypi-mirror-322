#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
#
# Copyright 2025 Robert Wolff <mahlzahn@posteo.de>
# SPDX-License-Identifier: GPL-3.0-or-later


import argparse
import datetime
import hashlib
import json
import urllib.request
import uuid

import icalendar

# Optional dependencies
try:
    import argcomplete
except ModuleNotFoundError:
    argcomplete = None


def parse_args():
    parser = argparse.ArgumentParser(
            prog='forgejo_releases_calender',
            description='Get calendar of Forgejo releases',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--cut', action='store_true',
                        help='include dates of release feature cuts')
    parser.add_argument('-s', '--span', action='store_true',
                        help='span release events from release to EOL date')
    parser.add_argument('-n', '--omit-eol', action='store_true',
                        help="omit events for EOL dates, ignored if '--span' "
                        'is specified')
    parser.add_argument('-a', '--alarm', nargs='+', default=[],
                        help='time in hours or duration string formatted '
                        'according to RFC5545 for triggers or path to file '
                        'with VALARM specification for reminder(s) of events, '
                        'may be specified multiple times')
    parser.add_argument('-o', '--output',
                        help='output icalendar file instead of stdout')
    parser.add_argument('-u', '--url-release-schedule',
                        default='https://codeberg.org/forgejo/docs/raw/branch/'
                        'next/release-schedule.json',
                        help='URL of the release schedule JSON file')
    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    return parser.parse_args()


def main():
    args = parse_args()
    cal = icalendar.Calendar(version=2.0,
                             prodid='-//mahlzahn//forgejo-releases-calendar//EN')
    namespace = uuid.UUID(hex=hashlib.sha1(cal['PRODID'].encode()).hexdigest()[:32])
    with urllib.request.urlopen(args.url_release_schedule) as response:
        release_schedule = json.loads(response.read())
    events = get_events(release_schedule, span=args.span, cut=args.cut,
                        eol=not args.omit_eol)
    vevents = get_vevents(events, namespace=namespace)
    valarms = get_valarms(args.alarm)
    for vevent in vevents:
        for valarm in valarms:
            vevent.add_component(valarm)
        cal.add_component(vevent)
    if args.output:
        with open(args.output, 'wb') as f:
            f.write(cal.to_ical())
    else:
        print(cal.to_ical().decode())


class Event(argparse.Namespace):
    ...


def get_events(release_schedule, span=False, cut=False, eol=True):
    events = []
    for release in release_schedule:
        version = f"{release['major']}.{release['minor']}"
        if release['lts']:
            version += ' (LTS)'
        if span:
            events.append(
                    Event(summary=f'Forgejo {version} release',
                          start=release['release'],
                          end=release['eol']))
        else:
            events.append(
                    Event(summary=f'Forgejo {version} release',
                          start=release['release']))
            if eol:
                events.append(                        
                        Event(summary=f'Forgejo {version} EOL',
                              start=release['eol']))
        if cut:
            events.append(
                    Event(summary=f'Forgejo {version} feature cut',
                          start=release['cut']))
    return events


def get_vevents(events, namespace):
    dtstamp = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
    vevents = []
    for i, event in enumerate(events):
        vevent = icalendar.Event()
        vevent.add('summary', event.summary)
        vevent.add('dtstamp', dtstamp)
        #TODO determined UID
        vevent.add('uid', uuid.uuid5(namespace, event.summary + event.start))
        vevent.add('dtstart', datetime.date.fromisoformat(event.start))
        if hasattr(event, 'end'):
            vevent.add('dtend', datetime.date.fromisoformat(event.end))
        else:
            vevent.add('duration', datetime.timedelta(days=1))
        vevents.append(vevent)
    return vevents


def get_valarms(alarms):
    valarms = []
    for alarm in alarms:
        try:
            valarms.append(icalendar.Alarm(
                trigger=icalendar.vDuration(-datetime.timedelta(hours=int(alarm))),
                action='DISPLAY'))
        except ValueError:
            try:
                valarms.append(icalendar.Alarm(
                    trigger=icalendar.vDuration(icalendar.vDuration.from_ical(alarm)),
                    action='DISPLAY'))
            except ValueError:
                with open(alarm) as f:
                    valarms.extend(icalendar.Calendar.from_ical(
                        f'BEGIN:VEVENT\n{f.read()}\nEND:VEVENT').subcomponents)
    return valarms


if __name__ == '__main__':
    main()
