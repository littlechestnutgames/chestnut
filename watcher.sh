#!/bin/zsh
source /home/lumpywizard/.profile
source ~/.oh-my-zsh/oh-my-zsh.sh
source /home/lumpywizard/.zshrc
inotifywait -m -e modify -r ~/Projects/Python/chestnut/ --include '\.nuts$' | 
while read path action file; do
    if [[ "$file" == *.nuts ]]; then
        echo "Change detected in .nuts file: $path$file"
        /usr/bin/python3.13 chestnut examples/span.nuts
    fi
done
