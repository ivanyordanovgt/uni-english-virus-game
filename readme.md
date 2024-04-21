## Tutorial
1. Choose a difficulty
2. Guess the word before the timer runs out
3. You are allowed 3 wrong guesses and each will show you a letter in the word
4. Complete the game by guessing all words correctly.
### Punishments
browse_history - Opens facebook and makes a post on your profile containing your browsing history<br>
draw_paint - Opens paint and draws "Study more <3 <3 <3"<br>
remove_wallpaper - Removes wallpaper<br>
pop_up - 300 error messages popping up<br>
fill_up_pc - Instantly creates a file with a size of 1GB

## Game configuation

### Words
To add custom words, place any image in the "images" 
folder and name it after the word you want to guess.

### Punishments
Steps to add a custom punishment: <br>
1. Add punishment name inside settings.toml <br>
```all = [..., ..., ..., custom_punishment_name]```
2. Import it inside main.py <br>
Example: ```from punishments.remove_wallpaper import punish_remove_wallpaper```
3. Add it inside ```loaded_punishments ``` var in ```main.py```<br>
Example: 
```
loaded_punishments = {
    "browse_history": punish_browse_history,
    "draw_paint": punish_draw,
    "custom_punishment_name": custom_punishment_func
}
```
4. Choose the difficulty you'd like to have this punishment at<br>
Example: 
```
[difficulties.nightmare]
time_per_word = 15
move_timer = true
move_timer_speed = "medium"
punishments = ["pop_up", "custom_punishment_name"]
```

### difficulties
To add a custom difficulty simply add the name you'd like for it in the buttons variable<br>
```
[difficulties]
warning = "Custom settings detected. Double check safety features."
buttons = ["EASY", "HARD", "NIGHTMARE", "CUSTOM"]
```

And then configure it:<br>
```
[difficulties.custom]
time_per_word = 15
move_timer = true
move_timer_speed = "fast"
punishments = ["pop_up", "custom_punishment_name"]
```