+++
title = "Uses"
description = "Software that I use"
template="section.html"

[extra]
head_title = "Uses"
+++

Some of the Software that I use on my day to day and I could recommend.

Most except those marked with "⚠️" are OSS. In that case, I'll try to give an OSS alternative anyway.

## Email

- [Thunderbird](https://www.thunderbird.net/en-US/): My desktop email client of choice. I know that the UI used to be outdated and horrible, but it has come a long way recently. If you have not used it in the last couple of years, give it a try!
- [⚠️ PurelyMail](https://purelymail.com/): Email hosting service. The pricing model is simply divine: ridiculously cheap and no extra fees for arbitrary nonsense. My two main concerns is that it's all [run by a single guy](https://purelymail.com/about) (Hi Scott!) and that it's US-based (so no GDPR). I solve the former by having very good backups and the latter by not thinking about it. If those concern you anyways, [mailbox.org](https://mailbox.org/en/) and [Migadu](https://www.migadu.com/) looked really promising, although they fail on the "extra fees for arbitrary nonsense" aspect.
- [addy.io](https://addy.io/): Anonymous Email Forwarding service. If you are inside the [Proton](https://proton.me/) ecosystem, go with [SimpleLogin](https://simplelogin.io/), it'll be basically free. If not, it's clearly missing a "middle" tier in order to push customers into buying Premium, which I find pretty shady. Addy's pricing model avoids this nonsense.
- [mbsync](https://isync.sourceforge.io/mbsync.html): Command for downloading all my email into Maildir using IMAP, which is then backed up using [Borg](#backups). It requires an afternoon of reading man pages, but works like a charm. Might do a post going through the basic configuration in the future.

*"JuSt sElF-HoSt yOuR EmAiL In sOmE ChEaP VpS"* &ndash; No, thank you, I'm not that crazy.

## Backups

- [BorgBackup](https://www.borgbackup.org/): What does the heavy lifting in my backup setup. It has many commands with many arguments to learn. As my use case is pretty standard, and I'm not retired yet, I didn't bother learning to use it directly.
- [Borgmatic](https://torsion.org/borgmatic/): A config-based backup program built on top of Borg. This is *MUCH* nicer to use! The documentation has examples for everything, so in the end it's just a matter of taking bits from here-and-there. You can have everything working in a couple of hours.
- [⚠️ BorgBase](https://www.borgbase.com/): Where I host my client-encrypted offside backups. Cheap, GDPR-compliant and has a nice UI that does the job. Cannot ask for more.

## Monitoring

- [Uptime Kuma](https://uptime.kuma.pet/): Beautiful WebUI to monitor the websites and services I maintain. If you would love it to be config-based as me, check out [Gatus](https://gatus.io/). Last time I checked, its UI was still too limited and clunky for me though. 
- [Scrutiny](https://github.com/AnalogJ/scrutiny): Another WebUI to monitor, in this case, SSDs and HDDs health in my Home Server. If you don't use something alike, **do so right now**. I'm sadly talking from experience here...
- [DockProm](https://github.com/stefanprodan/dockprom): The monitoring Swiss Army knife for the lazy self-hoster. If you used Grafana before, you know how much of a pain is configuring all this. It's easier to start from here and tweak what's needed.

## Files

- [Nextcloud](https://nextcloud.com/): Where I store my files. If you installed it a few years ago maybe you don't know of [Nextcloud AIO](https://github.com/nextcloud/all-in-one). It's a pleasure to use.
- [TinyFileManager](https://tinyfilemanager.github.io/): An stupidly simple file manager webapp. A bit more clunky than [Filegator](https://filegator.io/) or [File Browser](https://filebrowser.org/), but it gets the job done. You could argue that I'd be better off with a basic SFTP server, and you'd be right.

## Books

- [Calibre Web](https://github.com/janeczku/calibre-web): Where I store my eBook collection. The WebUI is a bit rough sometimes, but I mostly use it to upload and retrieve eBooks, nothing complicated.
- [Calibre Desktop](https://calibre-ebook.com/): I use the Desktop program to send the eBooks to my Reader. An integration between Calibre Web, Calibre Server and Calibre Desktop would be a joy, but I never get around to do it.
- [Reading Timeline](https://github.com/albertcanales/reading-timeline): What a shameless plug, isn't it? In more seriousness, it's what I use to record the books I read (and get a nice diagram for free!).

## Music

- [Navidrome](https://www.navidrome.org/): Self-Hosted Music Streaming service. Pretty self-explanatory. If not, check out [the demo](https://demo.navidrome.org/app/#/login).
- [Maloja](https://github.com/krateng/maloja): WebUI to visualize your scrobbles (aka. the songs you've listened to). Simply put, like *Spotify Wrapped* but in a colossal scale. If you are curious, you can actually load all your Spotify history and see an absurd amount of statistics about *everything*, it's simple and quite fun.
- [Multiscrobbler](https://github.com/FoxxMD/multi-scrobbler): Allows me to scrobble simultaneously from Navidrome and Spotify into Maloja. Not needed if you just use one of the two.
- [⚠️ Symfonium](https://symfonium.app/): Amazingly good Music Player for Android. It's 6€ for life-long license, and it's well worth it. If you want something free (as in beer) and OSS, check [Tempo](https://github.com/CappielloAntonio/tempo), it's also very good.

## Tasks

I don't want fancy GTD features, just a task list with synchronization support.

- [Errands](https://apps.gnome.org/en-GB/List/): Simple Desktop Task Manager, part of [Gnome Circle](https://circle.gnome.org/).
- [Tasks.org](https://tasks.org/): Mobile Task Manager. At first the feature-cluttered UI drove me away. Thankfully everything can be disabled.
- [Nextcloud Tasks](https://apps.nextcloud.com/apps/tasks): Nextcloud App to keep both above in sync using CalDAV.
- [Mind](https://casvt.github.io/MIND/): Simple WebApp for setting reminders using push notifications or emails.

## Feeds

- [FreshRSS](https://freshrss.org/index.html): RSS Aggregator with a great WebUI. It can also be used as a Reader, although I prefer...
- [Newsflash](https://apps.gnome.org/en-GB/NewsFlash/): Desktop RSS Reader, part of [Gnome Circle](https://circle.gnome.org/).
- [Read You](https://github.com/Ashinch/ReadYou): Mobile RSS Reader (don't use it much, tbh).

## Notes

- [⚠️ Obsidian](https://obsidian.md/): Note-taking desktop and mobile app. Would love to recommend [Joplin](https://joplinapp.org/) in its place, but the UI/UX Obsidian is simply flawless. I don't use any of the fancy features of Obsidian either, it's mostly a pretty Markdown editor for me.
- [Syncthing](https://syncthing.net/): File syncing program I use for syncing the Markdown notes across devices.

## VCS

- [⚠️ GitHub](https://github.com/): Where I upload by public repos. I know that [GitLab](https://gitlab.com/) is OSS and has *many more* features. My problem is with the latter, it's just overengineered for my use case. Plus, I would need a GitHub account anyway, as I use it in part as a portfolio.
- [Gitea](https://about.gitea.com/): A Git-Hosting WebUI to manage my private repositories. Why don't use Github's? Because this way I can track TODOs with repo issues and be messy about it, without worrying about how it's gonna look when I make it public. Go wild on the discussions with yourself!
- [GitNext](https://gitnex.com/): Android client for accessing my Gitea instance. I'm always ready to file an issue for that pesky mantainer! (aka. myself).

## Home Server

A lot of what I host on my Home Server is scattered through the previous sections. Here you have some more:

- [Homer](https://github.com/bastienwirtz/homer/): A dead-simple config-based Homepage for my services. I actually don't use it much, as I have SSL on all my domains, and it's faster to write the URL (with browser autocomplete, of course). I have a tutorial how to do that [here](/blog/homeserver-ssl-with-caddy.md).
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/): Where I host my internal documentation for the Home Server with a nice WebUI. Is fully documenting an infrastructure that's just managed by myself too much overkill? Yes, of course. What were you expecting?
- [Tailscale](https://tailscale.com/): Main VPN to access the server remotely. It's more comfortable to use than [Wireguard](https://www.wireguard.com/) and less buggy than [ZeroTier](https://www.zerotier.com/). If you prefer going the Wireguard route, I can recommend [WG Easy](https://github.com/wg-easy/wg-easy) as a WebUI for your server or [wireguard-install](https://github.com/Nyr/wireguard-install) if you just want a quick headless installation.
- [ZeroTier](https://www.zerotier.com/): Backup and Guest VPN. At the time of installation, Tailscale Free Plan only included a handful of devices and modifying the given IP was not allowed. As needed both features for easily giving restricted access to friends and family to my server, so I chose ZeroTier for that. All in all, not so much of a recommendation, sorry :(.

## Website

- [Zola](https://www.getzola.org/): My SSG generator of choice. Very opinionated in its structure, which may be a bit confusing at first. However, once you understand it (quite easy thanks to great documentation), everything comes very natural and simple.
- [Hetzner](https://www.hetzner.com/): My VPS provider. Great prices and polished WebUI. They have datacenters in Europe, which is also a huge plus for me because of GDPR compliance.

## Other

- [Ansible](https://www.ansible.com/): My Infrastructure of Code tool of choice. I use it to orchestrate everything on my servers. I live peacefully knowing that I can erase one of my servers and have it back and running with a single command (and some backup restoration). Learning the basics is not hard thanks to [Jeff Geerling's course](https://www.youtube.com/playlist?list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN), which you can follow using [my notes](https://github.com/albertcanales/learning-notes/blob/main/courses/ansible-101.md).
- [Caddy](https://caddyserver.com/): As you can tell by [this](/blog/homeserver-ssl-with-caddy/) post, I'm in love with this Web Server. I slap it over all my web projects.
- [Dracula](https://draculatheme.com/): The theme I used everywhere during my Arch Linux ricing days. Apart from looking great, it has an amazing support. I also really liked [Catpuccin](https://catppuccin.com/), but I discovered it too late.
