# FUT-LISTEN

```
  /`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`
  /`     ┏━╸╻ ╻╺┳╸   ╻  ╻┏━┓╺┳╸┏━╸┏┓╻     /`
  /`     ┣╸ ┃ ┃ ┃ ╺━╸┃  ┃┗━┓ ┃ ┣╸ ┃┗┫     /`
  /`     ╹  ┗━┛ ╹    ┗━╸╹┗━┛ ╹ ┗━╸╹ ╹     /`
  /`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`/`
```

A CLI Program to automate listening sections for tests.

### What it does

The default behavior is to search through the current working directory for *.mp3 files. It will sort the files in order, and then play them twice. There are instructions given (with TTS) and delays given throughout, with tones to indicate that the next portion will happen soon. It's basically an automated playlist.

The defaults probably work fine, but there are a lot of options. 

This program doesn't do any trimming of audio. If you need to do that, use another tool. 

### Requirements:

1. You should have a high-quality TTS voice downloaded. [Read here](https://support.apple.com/guide/mac-help/change-the-voice-your-mac-uses-to-speak-text-mchlp2290/mac) to find out more.
2. [mpv](https://mpv.io) is used for playing audio. Install it using homebrew: `brew install mpv`.
3. [sox](https://sourceforge.net/projects/sox/) is used to play tones. Install it using homebrew: `brew install sox`.

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
