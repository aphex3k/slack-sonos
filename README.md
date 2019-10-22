<b style="color: white;background-color: black">&nbsp;SONOS&nbsp;</b>&nbsp;+&nbsp;<b style="color: #1383de">Slack</b>

Add this bot to your Slack channel to ask it what song is currently playing on you Sonos sound system.

<img src="https://github.com/aphex3k/slack-sonos/blob/master/.images/sonos-slack.png?raw=true"/>

# Installation

After checking out the repository locally, install the dependencies by running

    pip3 install -r requirements.txt

or 

    python3 -m pip install -r requirements.txt

# Usage

Before starting the script, you need to export the following 3 variables to your environment:

1. GOOGLE_API_TOKEN="..."
    - This is the API token for the google image search (album art)
1. GOOGLE_CX_TOKEN="..."
    - This is the context token for you custom google image search
1. SLACK_API_TOKEN="..."
    - This is the API token for the slack bot integration

[![Build Status](https://travis-ci.org/aphex3k/slack-sonos.svg?branch=master)](https://travis-ci.org/aphex3k/slack-sonos)
