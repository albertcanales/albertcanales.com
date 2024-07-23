+++
title="Local SSL Certs for your Homeserver with Caddy"
date=2024-07-18
template="post.html"
+++

In this post, I would like to give an alternative implementation of the concepts shown in the following video by Wolfgang. We will achieve the same results, but using Caddy instead of Nginx Proxy Manager.

{{ youtube(id="qlcVx-k-02E", ratio="16/9") }}

I encourage you to watch the full video to have enough context. Also, some basic knowledge of Docker is expected for following this tutorial.

## A bit of context

Firstly, I will explain the different ways I have been accessing the services on my Homeserver through the years. If you are interested just on the Caddy implementation, jump to the [next section](#caddy-implementation)

### Before Wolfgang's video

For the first year or two of my Homeserver, I used to access the services directly by their IP and port. For example, I would write something like `http://192.168.0.40:500` to access Nextcloud.

As you can assume, remembering all the ports is rather cumbersome. That's why I used [Homer](https://github.com/bastienwirtz/homer/), a dashboard, to access all the services. By running it on port 80, I could just type `http://192.168.0.40` on the browser and, from there, click the corresponding icon.

This is much better, but it does not solve the annoying warning every time you enter the website[^1]. Just in time I was researching this topic, Wolfgang (amazing channel, worth subscribing) posted the video above.

By following the tutorial, I was left with nice URLs with HTTPS for my services, and I was very happy. Because of Nginx Proxy Manager, however, this did not last for long.

### My issues with Nginx Proxy Manager

Don't get me wrong, Nginx Proxy Manager (NPM further on) is a great project that taught me quite a lot about how a Reverse Proxy (RP further on). Its simple GUI is great. Unfortunately, I had some issues with it which were forced me to switch.

Although the GUI may seem a blessing at first, having such a critical part of the infrastructure configured using it felt like Damocles' sword, always ready to break it all.

The main problem was that, for some reason, sometimes restarting the container made NPM break in unexpected ways and blocked me access to the rest of my services.

Just to be clear, I am sure that these failures were my fault, but solving them using the logs took a good amount of time and, on a couple of cases, it was easier to start fresh and reconfigure everything.

Configuring a couple of services via the GUI for the tutorial is fairly quick. However, configuring my 20-ish services was like a half an hour long and very repetitive process.

For this reason, I started to look for RPs with a config-based approach, as I assumed they would have better logs when failing and, if I had to start anew, I would not have to reenter all the endpoints.

### Quick review of some Reverse Proxies

There were many popular candidates for the RP. My main requirements were the following:

1. I don't care for top performance (there are a handful of users on my Homeserver). I am willing to sacrifice some optimizations it in favor of a simpler config.
2. I want to fully understand my configs, as this allows me to tweak them as I please. If I can build them all from the ground up by myself, better.
3. Small and easy to read documentation. I should be able to read it all in an afternoon and fully understand all the main features.

Now let's look at some popular options:

- Nginx: Although a pillar of the modern web, I did not have time to learn it fully at the moment (as I would like to do in the future). Fails a bit on 1 and 3.
- SWAG: Great premade configs with Nginx. They are so well tweaked and optimized, in fact, that it fails on 2.
- Traefik: Great service, but too much overkill for my use-case. Fails on a 1 and 3.

This led me to Caddy, which meets all requirements. Caddy is a simpler RP that operates on a higher level of abstraction. Maybe the trivial configuration is not suited for very high traffic environments, but I don't have a problem with that.

## Implementing Wolfgang's video with Caddy {#caddy-implementation}

### Deploying Caddy with the rest of the services

Now let's tweak Wolfgang's video. Everything stays the same until *6:03*. At this moment, Wolfgang shows us a Compose file containing NPM. We will change it for Caddy.

Caddy does not allow us to manage wildcard certificates with all providers out of the box. This feature is available in separate plugins, which we can add to the base Caddy image.

#### Building the Caddy Image

To achieve that, we can make use of a `Dockerfile` like this one:

```
FROM caddy:builder AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/duckdns

FROM caddy

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```

Note that, in this example, we are using the plugin for the DuckDNS provider. Many other providers are available, you have a complete list [here](https://caddyserver.com/download) (by searching *caddy-dns*). If you use another provider, you just have to change line 4.

You can name the image however you want, in my case I will use `caddy-duckdns`. We can build it with the following command[^2]:

    docker build --tag caddy-duckdns .

#### Tweaking the Compose file

We now have a Caddy image that can manage domains for our chosen provider. Let's tweak Wolfgang's Compose file to use it instead of NPM.

The modified Compose file is the following. Note that we are only changing the `nginxproxymanager` service (now `caddy`), the rest stays exactly the same:

```
version: '2.2' 
services:
  caddy:
    image: caddy-duckdns 
    container_name: caddy
    restart: unless-stopped 
    ports:
      - '80:80'
      - '443:443'
      - '443:443/udp'
    volumes:
      - ./caddy/config:/config
      - ./caddy/configuration:/etc/caddy
      - ./caddy/data:/data 

  nextcloud:
    image: lscr.io/linuxserver/nextcloud:latest
    container_name: nextcloud
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin 
    volumes:
      - ./nextcloud/appdata:/config 
      - ./nextcloud/data:/data
    restart: unless-stopped 

  homeassistant:
    image: lscr.io/linuxserver/homeassistant:latest
    container_name: homeassistant 
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin 
    volumes:
      - ./hass/config:/config 
    restart: unless-stopped

  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin 
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Berlin 
    volumes:
      - ./jellyfin/config:/config
      - ./jellyfin/tvshows:/data/tvshows
      - ./jellyfin/movies:/data/movies 
    restart: unless-stopped
```

After saving the `docker-compose.yml` file, you can run all the servers by simply using the following command (like in the video):

    docker compose up -d

### Configuring the domains for our services

We will ignore the configuration of NPM that follows on Wolfgang's video, as we are not using it.

However, it is very important to configure DuckDNS (or our DNS provider of choice) as shown in the video between 7:12 and 7:37.

Now comes the fun part! Let's configure Caddy.

#### DNS Challenge with Caddy

Configuring the certificates for our domain is quite straightforward with Caddy. It's important to note that the configuration parameters depend on the provider. For this example, I will be showing how to configure DuckDNS. You can find the other provider's configuration on their respective GitHub repositories.

Firstly, create a file named `Caddyfile` in the directory `caddy/data/`. The file should have the following content:

```
mydomain.duckdns.org, *.mydomain.duckdns.org {
	tls {
		dns duckdns DUCK_DNS_API_TOKEN
	}

	handle {
		respond "Hello, world!"
	}
}
```

You just have to change `mydomain.duckdns.org` to your actual DuckDNS domain, and `DUCK_DNS_API_TOKEN` for the API Token visible on your DuckDNS account.

Finally, you can restart the Caddy container with:

    docker compose restart caddy

You should check for logs to monitor whether there are any issues. You can do that with:

    docker compose logs caddy

If everything worked correctly, waiting a few seconds you should see the message *Hello, world!* when connecting to your domain. You should also see that it uses HTTPS without any issue. The certificate should be verified by *Let's Encrypt* and HTTP traffic should be redirected to HTTPS.

If that is not the case, check the logs and the DuckDNS configuration, you should be able to troubleshoot the problem fairly quickly.

#### Configuring the services

We may have been able to establish a secure connection, but we have not yet configured access to our services as shown in the video. The virtue of Caddy is making this step really easy.

We will just need to update our `Caddyfile` to the following content:

```
mydomain.duckdns.org, *.mydomain.duckdns.org {
	tls {
		dns duckdns DUCK_DNS_API_TOKEN
	}

	@nextcloud host nextcloud.mydomain.duckdns.org
	handle @nextcloud {
		reverse_proxy https://nextcloud:443
	}

	@jellyfin host jellyfin.mydomain.duckdns.org
	handle @jellyfin {
		reverse_proxy http://jellyfin:8096
	}

	@home host home.mydomain.duckdns.org
	handle @home {
		reverse_proxy http://homeassistant:8123
	}

	# In case any of the above match
	handle {
		respond "This service does not exist!"
	}
}
```

Let's break down the changes. The provider configuration stays exactly the same. After that, we assign a subdomain to each of our services. We will use the URL to distinguish the appropriate destination for each request.

We will take a look at the chunk corresponding to a single service to understand the configuration:

```
@MATCHER host SERVICE.mydomain.duckdns.org
  handle @MATCHER {
    reverse_proxy DESTINATION
  }
```

- SERVICE: We would replace this for the subdomain we want to use for accessing our service.
- MATCHER: This is only a "variable name", anything could be used as long as it does not collide between services. To keep things tidy, I usually put the same as in SERVICE
- DESTINATION: This is where the request should be forwarded, as we would do with NPM. We may use the container name.

Finally, if none of the matchers above have succeeded for a given request (that means, we have accessed a subdomain that has doesn't have a service attached), we have a final handle that will respond *This service does not exist!*.

To apply the changes, don't forget to restart the caddy container:

	docker compose restart caddy

You may want to run other services on your Homeserver but, as you can see, expanding this configuration file to your needs is really easy. Also, you can save this file and avoid retyping everything ever again!

### Going further

Hurray! We have finally achieved feature parity with Wolfgang's video, using Caddy instead of NPM. Before finishing, though, there are a couple of extra concepts I would like to comment on.

#### Multiple Compose files

As Wolfgang says in his video: 

*I'm going to put \[NPM and the rest of the services\] on the same Compose file. This will ensure that all our containers are on the same Docker network and can communicate with each other easily.*

Putting everything on a single file is understandable for a tutorial, but with a lot of containers, it can have its drawbacks [^3]. That's why I would like to give you some insight on how to communicate containers on different Compose files.

To make sure we are all on the same page, you should know that for each Compose file there is a `default` network which is automatically created and all containers inside the Compose file are added to it. That's why they can communicate with each other by using the container name.

##### Single custom Network approach

First, we'll consider at the simplest approach. We'll create a single custom Docker Network called `caddy`, and all the services that we want to connect with the RP will be added to it. By doing this, they will be able to communicate even if they are in different Compose files.

We would need to add the following to the Compose file for the Caddy service (supposing we want it separately):

```
version: '2.2'
services:
  caddy:
    ...
    networks:
      - caddy

networks:
  default:
  caddy:
```

Note that we have a new `networks` section where we are creating two networks:

- `default`: Where all the containers of the Compose file will be added, so they can communicate with each other (will do nothing if there is only a single service).
- `caddy`: A custom network that we will use to communicate the RP with our services on other Compose files. We specify which container is added to this network by adding the content on lines 5 and 6.

Now, suppose we have a separate Compose file for our Nextcloud service. It would look something like this:

```
version: '2.2' 
services:
  nextcloud:
    ...
    networks:
      - caddy

networks:
  default:
  caddy:
    external: true
```

This is the same as before, except for the last line. This line is very important, as we are telling Docker Compose that it should not create a new `caddy` network, as it has already been created before.

Note that, by using this implementation, we are forced to run the Compose files in a certain order. If we try to run the Nextcloud before the Caddy one, the `caddy` network won't exist and we will get an error.

Also note that, apart from improving the management of the Compose files, we are improving a bit the security of our infrastructure. In the tutorial's implementation, all containers could communicate with each other. Now, only the ones that are added to the `caddy` network can communicate between them (apart from the ones on the same Compose file, of course).

##### Multiple Networks approach

Although the previous approach may be secure enough for many, there is technically a security improvement possible, as all containers between the `caddy` network can communicate with each other. For example, suppose we have Jellyfin and Nextcloud inside the `caddy` network. If one is compromised, it can directly communicate to the other via the `caddy` network.

Now, we will see an implementation that only allows connections from the RP to the needed  services and vice versa, but not between services. We can visualize this idea as a star graph, with Caddy in the center.

{% mermaid() %}
mindmap
  Caddy
    Jellyfin
    Nextcloud
    Home Assistant
{% end %}

The implementation would not change much. The Compose file for the Caddy service would look like this:

```
version: '2.2' 
services:
  caddy:
    ...
    networks:
      - caddy-home
      - caddy-jellyfin
      - caddy-nextcloud
networks:
  default:
  caddy-home:
  caddy-jellyfin:
  caddy-nextcloud:
```

And the Compose file for the rest of services would look like this (we'll use Nextcloud as an example):

```
version: '2.2' 
services:
  nextcloud:
    ...
    networks:
      - caddy-nextcloud

networks:
  default:
  caddy-nextcloud:
    external: true
```

You can see that, for communicating Caddy with Nextcloud, we are creating a network `caddy-nextcloud` that will only be added to both of them. As we repeat this with all the services, Caddy will be able to access all, but the services will only be able to access Caddy.

As you can see, this approach achieves greater control over the communication between services and greater security, but it makes configuration a bit more complicated to manage. It's up to you to determine if it's worth the extra effort.

### Implementing IP-based ACLs with Caddy

Finally, I would like to point out that NPM has some other great features not shown in the video by Wolfgang, as they are out of scope. All of them can be replicated using with Caddy in one way or another.

There is one in particular that I found very useful, IP-range based ACLs. This is very useful when sharing access to your Homeserver to friends and family, as you can restrict the services available to each group of users.

Unfortunately, an easy and scalable Caddy implementation is not trivial. A few weeks after configuring Caddy for the first time, I did an implementation which has been working perfectly ever since. I will write about it in the following weeks.

* * *

[^1]: More precisely, this is a side-effect of not using a trusted HTTPS connection. This may have other security concerns, but they were not of much importance for me as I use Wireguard to connect to my services, which already encrypts and verifies the connection end-to-end.

[^2]: Alternatively, we can avoid this step by using the `build` subsection instead of `image` on the next Compose file.

[^3]: I do not talk from experience here, as I run all my infrastructure on Docker Containers using Ansible. However, as someone with more than 20 containers running, I can imagine that navigating through a single file would be kind of a nightmare.

* * *

*For any suggestion on comment, don't hesitate to [contact me](mailto:contact@albertcanales.com)*

*Thanks for reading!*
