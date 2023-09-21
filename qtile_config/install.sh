sudo pacman -Syu python-psutil;
sudo pacman -Syu python-dbus-next;
sudo pacman -Syu alacritty;
sudo pacman -Syu nitrogen;

sudo mkdir -p ~/.local/share/backgrounds;


# https://www.nerdfonts.com/cheat-sheet
# https://github.com/ryanoasis/nerd-fonts

sudo mkdir -p /usr/share/fonts/nerd-fonts/FiraCode;
sudo curl -L --output-dir /usr/share/fonts/nerd-fonts/FiraCode https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/FiraCode/Regular/FiraCodeNerdFont-Regular.ttf -o "FiraCodeNerdFont Regular.ttf";
sudo fc-cache -vf;
shutdown -r now;