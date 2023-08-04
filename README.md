# scenemap
Nerdy data vizualizations for your Spotify library

I started this project after becoming sort of fascinated at the breadth of
musical influence specifically of some involved in metalcore scene at the turn of
the millenium, and then a broader question of just how incestuous my musical
family treee was.

![An interesting cluster](./Figures/cluster_1.png)

How to try it:
- Grab an api key from developer.spotify.com
- Paste in `scenemap/.env` like so:
```
#!/usr/bin/env python3

client_secret = "YOURSECERT"
client_id = "YOURID"
redirect_uri = "https://localhost:8080"
```
- Run `python3 scenemap/spotify.py` and paste in the redirect when prompted
- Hopefully this will work for others; it seems Spotify has maybe changed
  auth to require your account to be on the developer dashboard, so reach out
  if you'd like to try it while I'm still developing.

