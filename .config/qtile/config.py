# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"
terminal = "alacritty"

def muteVol(qtile):
    os.system('bash ~/.config/qtile/scripts/volume.sh mute')
    
def lowerVol(qtile):
    os.system('bash ~/.config/qtile/scripts/volume.sh down')
    
def raiseVol(qtile):
    os.system('bash ~/.config/qtile/scripts/volume.sh up')
    
def fullScreenScreenshot(qtile):
    os.system('scrot ~/Pictures/screenshots/%m-%d-%Y-%T-screenshot.png')
    os.system('notify-send "Fullscreen screenshot taken."')
        
def selectScreenshot(qtile):
    os.system('scrot ~/Pictures/screenshots/%m-%d-%Y-%T-screenshot.png --select --line mode=edge')
    os.system('notify-send "Select screenshot taken."')
    
def windowScreenshot(qtile):
    os.system('scrot ~/Pictures/screenshots/%m-%d-%Y-%T-screenshot.png --focused')
    os.system('notify-send "Window screenshot taken."')
    
def browserSearch(qtile):
    os.system('bash ~/.config/rofi/scripts/rofi-surfraw')

keys = [
    # launch applications
    Key([mod], "b", lazy.spawn("brave")),
    Key([mod], "p", lazy.spawn("pavucontrol")),
    Key([mod], "f", lazy.spawn("thunar")),
    Key([mod], "s", lazy.function(browserSearch)),
    Key(["mod1"], "space", lazy.spawn("rofi -show drun")),
    Key(["mod1"], "Tab", lazy.spawn("rofi -show window")),
    Key([mod], "e", lazy.spawn("rofi -show emoji")),
    Key([mod], "c", lazy.spawn("rofi -show calc -modi calc -no-show-match -no-sort")),    
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.next_layout(), desc="Move window focus to other window"),
    Key([mod], "Down", lazy.layout.shuffle_down()),
    Key([mod], "Up", lazy.layout.shuffle_up()),
    Key([mod], "Left", lazy.layout.shuffle_left()),
    Key([mod], "Right", lazy.layout.shuffle_right()),
    
    Key([mod], "t", lazy.window.toggle_floating(), desc='Toggle floating'),
    
    # Resize modes
    KeyChord([mod], "w", [
        Key([], "g", lazy.layout.grow()),
        Key([], "s", lazy.layout.shrink()),
        Key([], "r", lazy.layout.reset()),
        Key([], "m", lazy.window.toggle_minimize()),
        Key(["shift"], "m", lazy.window.toggle_maximize()),
        Key([], "f", lazy.window.toggle_fullscreen())],
        mode="Windows"
    ),
    
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.function(muteVol)),
    Key([], "XF86AudioLowerVolume", lazy.function(lowerVol)),
    Key([], "XF86AudioRaiseVolume", lazy.function(raiseVol)),
    
    # Screenshots
    Key([], "F3", lazy.function(fullScreenScreenshot)),
    Key([], "F4", lazy.function(selectScreenshot)),
    Key([], "F5", lazy.function(windowScreenshot)),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

def init_layout_theme():
    return {"margin":10,
            "border_width":2,
            "border_focus": "#009dc4",
            "border_normal": "#ffffff"
            }

layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(margin=16, border_width=2, border_focus="#009dc4", border_normal="#ffffff"),
    layout.MonadWide(margin=16, border_width=2, border_focus="#009dc4", border_normal="#ffffff"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Stack(**layout_theme),
    layout.Tile(**layout_theme),
    layout.TreeTab(
        sections=['FIRST', 'SECOND'],
        bg_color = '#141414',
        active_bg = '#0000ff',
        inactive_bg = '#1e90ff',
        padding_y =5,
        section_top =10,
        panel_width = 280),
    layout.VerticalTile(**layout_theme),
    layout.Zoomy(**layout_theme)
]

widget_defaults = dict(
    font='Ubuntu',
    fontsize=16,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth=1,
            padding=1,
            background="#191970",
            foreground="#191970"
        ),
        widget.Image(
            background="#191970",
            filename="~/.config/qtile/icons/arch_linux.png",
            margin=3
        ),
        widget.GroupBox(
            font='Ubuntu',
            background="#191970",
            fontsize = 18,
            margin_y = 3,
            margin_x = 2,
            padding_y = 5,
            padding_x = 4,
            borderwidth = 3,
            active="#add8e6",
            inactive="#ffffff",
            rounded= True,
            highlight_method='border',
            urgent_alert_method='block',
            this_current_screen_border="#add8e6",
            disable_drag=True
        ),
        widget.TaskList(
            highlight_method ='border', 
            margin_y = 3,
            margin_x = 5,
            icon_size=20,
            max_title_width=500,
            rounded=True,
            fontsize = 16,
            border="#add8e6",
            borderwidth = 3,
            background="#a202ff"
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
            foreground = "#ffffff",
            background = "#191970",
            padding = 0,
            scale = 0.8,
        ),
        widget.CurrentLayout(
            font = "Ubuntu Bold",
            fontsize = 18,
            foreground = "#ffffff",
            background = "#191970"
        ),
        widget.Net(
            font="Ubuntu",
            fontsize=18,
            # Here enter your network name
            interface=["enp0s31f6"],
            format = '{down} ↓↑ {up}',
            foreground = "#ffffff",
            background = "#e820e5",
            padding = 10,
        ),
        widget.CPU(
            font="Ubuntu",
            #format = '{MemUsed}M/{MemTotal}M',
            update_interval = 1,
            fontsize = 18,
            foreground = "#ffffff",
            background = "#06ab81",
            mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(terminal + ' -e htop')},
        ),
        widget.Memory(
            font="Ubuntu",
            format = '{MemUsed: .2f}GB /{MemTotal: .2f}GB',
            update_interval = 1,
            fontsize = 18,
            measure_mem = 'G',
            foreground = "#ffffff",
            background = "#0683ab",
            mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(terminal + ' -e htop')},
        ),
        widget.Clock(
            foreground = "#ffffff",
            background = "c3a613",
            fontsize = 18,
            format="%a, %m/%d/%y, %I:%M%p"
        ),
        widget.TextBox(
            font="Ubuntu",
            fontsize=18,
            text="Reboot",
            fmt='{:^24s}',
            padding=0,
            background="#f07b00",
            mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('reboot')}
        ),
        widget.TextBox(
            font="Ubuntu",
            fontsize=18,
            text="Shutdown",
            fmt='{:^24s}',
            padding=0,
            background="#bf1d46",
            mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('shutdown -h now')}
        )
    ]
    return widgets_list

widgets_list = init_widgets_list()

screens = [Screen(top=bar.Bar(widgets=widgets_list, size=30, opacity=0.85, background= "000000"))]
    
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    # works best when dragging bottom right hand corner
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.set_size_floating(1000,750), start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.enter_chord
def notification(chord):
    os.system('notify-send -t 0 -u critical "Window management mode"')
    
@hook.subscribe.leave_chord
def notification():
    os.system('killall dunst')

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
