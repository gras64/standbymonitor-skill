# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/desktop.svg" card_color="#40DBB0" width="50" height="50" style="vertical-align:bottom"/> Standbymonitor
Monitor Standby

## About
the skill switches the monitor off after a short time to save electricity when mycroft is not used. With "hey mycroft" the monitor is switched on again.you can set the time and the automatic mode under "home.mycroft".
the skill supports the following methods:auto,xset dpms force,7 Zoll pi Display,DLP2000,tvservice,vcgencmd,CEC,mark 1,mark 2

## Examples
* "Monitor activate"
* "Monitor deaktivate"
* "Monitor automatic"

## Credits
gras64

## ToDo
multiple monitor setup support
more intents
## For sudo on Raspberry

    sudo crontab -e
and add
    
    @reboot /usr/bin/sudo /bin/chmod 777 /sys/class/backlight/rpi_backlight/bl_power
    @reboot /usr/bin/sudo /bin/chmod 777 /sys/class/backlight/rpi_backlight/brightness

## Category
**Daily**

## Tags
#Monitor
#automatic
