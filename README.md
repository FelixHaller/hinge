# Hinge


CLI-Tool/Indicator for working with convertible notebooks written in Python.

## ABOUT

This tool tries to help you in your daily work with your convertible notebook. It aims to be an easy to use software, but offers many advanced command line options as well.
You will be able to control important system features such as:

* Device orientation
* Wacom Input parameters
  * enable/disable touch
  * enable/disable stylus
  * enable/disable wacom hover click
* predefined modes for writing, regular working for easy switching

## INSTALLATION

To try it out you can download the sources into a directory of your choice and start:

    ./hinge

You can also install it via Debian .deb package (see below).

### UBUNTU

I you are an Ubuntu user, you can install the latest daily build by following the instructions of this ppa:

[ppa:felixhaller/hinge-daily](https://code.launchpad.net/~felixhaller/+archive/hinge-daily "hinge-daily ppa on launchpad")

### DEBIAN

If you are an Debian user, use the last Ubuntu LTS version. It should work with debian as well.
Just execute the following:

    echo "deb http://ppa.launchpad.net/felixhaller/hinge-daily/ubuntu precise main" >> /etc/apt/sources.list
    apt-get update
    apt-get install hinge

## USAGE

To use the tool there is an application indicator and also many command line options to bind special actions to specific hotkeys.

### Indicator

see screenshots (following soon)

### CLI

Currently the following options are available for the command line:

    -f, --flip                  flip the rotation (toggle normal/inverted)
    -T, --touch on,off          enable/disable finger touch input
    -t, --toggle-touch          toggle finger touch input
    -O, --hover-click on,off    enable/disable wacom hover click
    -o, --toggle-hover-click    toggle wacom hover click
    -n, --normal                reset settings to default
    -r, --rotate <orientation>  set a specific orientation (absolute), possible values: normal, left, right, inverted
    -W, --writing on,off        enables/disables writing-mode (turn to "inverted", disable touch input, enable hover click)
    -w, --toggle-writing        toggle writing-mode

#### Examples:

Turn your touch device off (if there is any)

    hinge -T off

Flip your screen and all of your devices (180°) and activate Hover-Click for the stylus.

    hinge -f -O on

## Bugs


If there are any problems while installing (dependencies, etc...) or while using the tool please file a bug or contact me.
