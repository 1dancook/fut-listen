# FUT-LISTEN

```
          -// ┏━╸╻ ╻╺┳╸   ╻  ╻┏━┓╺┳╸┏━╸┏┓╻ \\-               
       -+=||  ┣╸ ┃ ┃ ┃ ╺━╸┃  ┃┗━┓ ┃ ┣╸ ┃┗┫  ||=+-            
          -\\ ╹  ┗━┛ ╹    ┗━╸╹┗━┛ ╹ ┗━╸╹ ╹ //-               
```

A CLI Program to automate listening sections for tests.

### What it does

The default behavior is to search through the current working directory for *.mp3 files. It will sort the files in order, and then play them twice. There are instructions given (with TTS) and delays given throughout, with tones to indicate that the next portion will happen soon. It's basically an automated playlist.

The defaults probably work fine, but there are a lot of options. 

This program doesn't do any trimming of audio. If you need to do that, use another tool. 

**Note:** Currently this is only tested to work on MacOS.

### Requirements:

- [mpv](https://mpv.io) is used for playing audio. Install it using homebrew: `brew install mpv`.

### Installation

It's best to use [pipx](https://pypa.github.io/pipx/):

```
pipx install fut-listen
```

Alternatively, install with pip:

```
pip install fut-listen
```

### Usage

```
# navigate to directory
fut-listen

# See options
fut-listen --help
```

### Generating Audio requirements (development)

1. High quality TTS voice to use for `say` on MacOS
2. sox (for generating tones)
