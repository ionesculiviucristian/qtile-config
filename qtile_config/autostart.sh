function run {
    if ! pgrep $1 > /dev/null ;
    then
        $@&
    fi
}

nitrogen --restore &