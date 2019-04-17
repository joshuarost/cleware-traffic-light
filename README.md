# cleware-traffic-light
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://stash.intranet.roche.com/stash/users/rostj1/repos/cleware-traffic-light/browse/LICENSE )
[![PyPI version](https://badge.fury.io/py/cleware-traffic-light.svg)](https://badge.fury.io/py/cleware-traffic-light)

**cleware-traffic-light** an easy to use CLI tool written in Python3 to control the cleware USB [traffic light](http://www.cleware-shop.de/USB-MiniTrafficLight-EN).
It supports multiple traffic light control and the usage as a module in your own Python application.

## Usage

### Module

```python
from cleware-traffic-light import ClewareTrafficLight, Color, State

ClewareTrafficLight().red_on()
ClewareTrafficLight().yellow_off()

# with address for specific light
ClewareTrafficLight(21).green_on()
```

### CLI

```bash
ctl --red on
ctl -r on
ctl --red on --green off
ctl --red off --green on --address 19
```

## Installation

use **pip** to install **cleware-traffic-light**

```bash
pip3 install cleware-traffic-light
```

### Help

```bash
usage: traffic_light [-h] [-r {on,off}] [-y {on,off}] [-g {on,off}]
                     [-a ADDRESS]

Turns the led of the cleware traffic light on or off

optional arguments:
  -h, --help            show this help message and exit
  -r {on,off}, --red {on,off}
                        Controlls the red led
  -y {on,off}, --yellow {on,off}
                        Controlls the yellow led
  -g {on,off}, --green {on,off}
                        Controlls the green led
  -a ADDRESS, --address ADDRESS
                        Specifies which traffic light should be used
```
