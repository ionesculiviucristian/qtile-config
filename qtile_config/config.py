from libqtile import bar, layout, widget
from libqtile.config import hook, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import subprocess
import os

# https://github.com/qtile/qtile-examples

# sudo reflector --latest 50 --protocol https --sort score --save /etc/pacman.d/mirrorlist;
# sudo pacman -Syu python-psutil python-dbus-next alacritty nitrogen;

# https://www.nerdfonts.com/cheat-sheet
# https://github.com/ryanoasis/nerd-fonts

# sudo mkdir -p /usr/share/fonts/nerd-fonts/FiraCode;
# sudo curl -L --output-dir /usr/share/fonts/nerd-fonts/FiraCode https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/FiraCode/Regular/FiraCodeNerdFont-Regular.ttf -o "FiraCodeNerdFont Regular.ttf";
# sudo fc-cache -vf;
# shutdown -r now;

# cp -R qtile_config/* ~/.config/qtile/ && qtile cmd-obj -o cmd -f reload_config

# nitrogen ~/.config/qtile/assets/backgrounds;

# https://docs.qtile.org/en/stable/manual/config/default.html#default-config-file

mod = "mod4"
terminal = guess_terminal()

# https://docs.qtile.org/en/v0.22.1/manual/config/index.html#configuration-variables

auto_fullscreen = True
bring_front_click = False
cursor_warp = False
dgroups_key_binder = None
dgroups_app_rules = []
focus_on_window_activation = 'smart'
follow_mouse_focus = True
widget_defaults = dict(
    font="FiraCodeNerdFont Regular",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()
reconfigure_screens = True
wmname = 'LG3D'
auto_minimize = True

# https://docs.qtile.org/en/v0.22.1/manual/config/keys.html#keys

keys = [
    Key([mod, "shift"], "Tab", lazy.layout.down()),
    Key([mod], "Tab", lazy.layout.up()),


    # Layout hotkeys
    Key([mod], "h", lazy.layout.shrink_main()),
    Key([mod], "l", lazy.layout.grow_main()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),

    # Window hotkeys
    Key([mod], "space", lazy.window.toggle_fullscreen()),
    Key([mod], "x", lazy.window.kill()),
    Key([mod, "shift"], "c", lazy.window.kill()),

    # Spec hotkeys
    Key([mod], "return", lazy.spawn(terminal)),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),

    # Media hotkeys
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pulseaudio-ctl up 5')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pulseaudio-ctl down 5')),
    Key([], 'XF86AudioMute', lazy.spawn('pulseaudio-ctl set 1')),
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
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# https://docs.qtile.org/en/stable/manual/config/layouts.html#layouts
# https://docs.qtile.org/en/v0.22.1/manual/ref/layouts.html#built-in-layouts

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

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

# https://docs.qtile.org/en/stable/manual/config/screens.html#screens
# https://docs.qtile.org/en/v0.22.1/manual/ref/widgets.html#built-in-widgets

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(padding=10),
                widget.WindowName(),
                widget.Mpris2(
                    scroll=False,
                    objname="org.mpris.MediaPlayer2.spotify",
                    display_metadata=["xesam:artist", "xesam:title"],
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Memory(fmt="󰍛 {}", measure_mem="M"),
                widget.Sep(padding=10),
                widget.PulseVolume(step=5, fmt=" {}", limit_max_volume=True),
                widget.Sep(padding=10),
                widget.Clock(fmt="󰅐 {}", format="%a, %b %d %Y, %H:%M%p"),
                widget.Sep(padding=10),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
