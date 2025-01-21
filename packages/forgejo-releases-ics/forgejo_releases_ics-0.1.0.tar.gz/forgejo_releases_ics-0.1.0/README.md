# forgejo-releases-ics – Get calendar of Forgejo releases
[![PyPI Version](https://img.shields.io/pypi/v/forgejo-releases-ics?color=00aa00)](https://pypi.org/project/forgejo-releases-ics)
[![PyPI License](https://img.shields.io/pypi/l/forgejo-releases-ics)](COPYING)

## Installation from PyPI

```sh
pip install forgejo-releases-ics
```

## Installation from source code

```sh
pip install .
```

## Usage as standalone program

```sh
forgejo-releases-ics -h
```

## Automated local calendar update

Add a cron job by using `crontab -e` with

```cron
# M  H  d  m  W  /path/command
  0  8  *  *  *  python -m forgejo-releases-ics -o ~/.forgejo-releases.ics
```

which will update the calendar on every day at 8 o’clock. It can then be added by programs such as Thunderbird as network calendar.

## Usage as python module

Currently not implemented.

## Copyright

Copyright 2025 Robert Wolff <mahlzahn@posteo.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
