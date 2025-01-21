# F.A.N.G. (Find a Number Game)

<p align="center" >
  <img src="https://raw.githubusercontent.com/armartirosyan/find-a-number-game/refs/heads/main/assets/fang_icon.png" style="width: 35%; height: 35%" />
</p>
</br>
Find a Number Game (FANG) is a game that can played with friends and family, featuring simple rules and an easy setup.

## Game setup

Access the [FANG Grid](https://docs.google.com/document/d/1-2hvNXohJWNpOWQj82NXgcLfX7S2L9YQ/edit?usp=sharing&ouid=110117817908775633071&rtpof=true&sd=true) document and print the required number of copies, ensuring it matches the number of players.
Open your terminal and install fang on your computer

```shell
$ pip install find-a-number-game
```
After installation, generate PDFs with randomized numbers on it.

> NOTE: By default the `fang` will generate 4 PDFs. If there are more players, use the `-p X` command where `X` is the number of players.</br>

> ANOTHER NOTE: You can generate a colored version by using the `-c True` option. option. Be aware that this may increase the difficulty
> in finding the numbers, as the colors can be very light and barely visible.

```shell
$ fang
```

This will generate 4 PDFs in the directory where the command was executed.

## Game Play

Recommended number of players: 4-6
The first player chooses a number on his paper, put
