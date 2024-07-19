+++
title="Local SSL Certs for your Homeserver with Caddy"
date=2024-07-18
template="post.html"
+++

In this post I would like to give an alternative implementation of the concepts shown in the following video by Wolfgang. We will achieve the same results, but using Caddy instead of Nginx Proxy Manager.

{{ youtube(id="qlcVx-k-02E", ratio="16/9") }}

I encourage you to watch the full video to have enough context. Also, some basic knowledge of Docker is expected for following this tutorial.

## A bit of context

Firstly, I will explain the different ways I have been accessing the services on my Homeserver through the years. If you are interested just on the Caddy implementation, jump to the [next section](#caddy-implementation)

### Before Wolfgang's video

For the first year or two of my Homeserver, I used to access the services directly by their IP and port. For example, I would write something like `http://192.168.0.40:500` to access Nextcloud.

As you can assume, remembering all the ports is rather cumbersome. That's why I used [Homer](https://github.com/bastienwirtz/homer/), a dashboard, to access all the services. By running it on port 80, I could just type `http://192.168.0.40` on the browser and, from there, click the corresponding icon.

This is much better, but it does not solve the annoying warning every time you enter the website[^1]. Just in time I was researching this topic, Wolfgang (amazing channel btw, worth subscribing) posted the video above.

By following the tutorial, I was left with a fully functioning implementation, and I was very happy about it. However, that did not last for long because of Nginx Proxy Manager.

### My issues with Nginx Proxy Manager

Don't get me wrong, Nginx Proxy Manager (NPM further on) is a great project that taught me quite a lot about how a Reverse Proxy (RP further on) works thanks to its GUI. Unfortunately, I had some issues with it which were forced me to switch.

Although it may seem a blessing at first, having such a critical part of the infrastructure configured via GUI felt like Damocles' sword, always ready to break my infrastructure.

The main problem was that, for some reason, restarting the container made NPM break sometimes in unexpected ways and blocked me access to the rest of my services.

To be clear, I am sure that these failures were my fault, but I sometimes did not manage to solve them, and it forced me to reconfigure everything. When having around 20 services, this means entering a lot of information via the GUI, it was like an hour-long process.

For this reason, I started to look for RPs with a config-based approach.

### Quick review of some Reverse Proxies

There are many popular candidate RPs. My main requirements were the following:

1. I don't care for top performance. I am willing to sacrifice some of it in favor of a simpler config.
2. I want to fully understand my configs, as this allows me to tweak them to my needs. If I can build it all by myself, better.
3. Small and easy to read documentation. I should be able to read it all in an afternoon and fully understand all the main features.

Now let's look at some popular options:

- Nginx: Although a pillar of the modern web, I did not have time to learn it fully at the moment. Fails on 1 and 3.
- SWAG: Great premade configs with Nginx. They are so well tweaked, in fact, that it fails on 2.
- Traefik: Great service, but too much overkill for my use-case. Fails on a 1 and 3.

This led me to Caddy, which meets all requirements. Caddy is a simpler RP that operates on a higher level of abstraction. Maybe the trivial configuration is not suited for very high traffic environments, but I don't have a problem with that.

## Implementing Wolfgang's video with Caddy {#caddy-implementation}

### Deploying Caddy with the rest of the services

Now let's tweak Wolfgang's video. Everything stays the same until *6:03*. At this moment, Wolfgang shows us a Compose file containing NPM, but we will change it for Caddy.

Caddy does not allow us to manage wildcard certificates with all providers out of the box. This feature is available in separate modules, which we can add to the base Caddy image.

#### Building the Caddy Image

To achieve that, we can make use of a `Dockerfile` like this one:

```
FROM caddy:builder AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/duckdns

FROM caddy

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```

Note that in this example, we are using the module for the DuckDNS provider. Many other providers are available, you have a complete list [here](https://caddyserver.com/download), by searching for *caddy-dns/*. You just have to replace the URL on line 4.

You can name the image however you want, in my case I will use `caddy-duckdns`. We can build it with a command like the following:

  docker build --tag caddy-duckdns .

#### Tweaking the Compose file

Now that we have the Caddy image tailored to our needs, we can use it for the Compose file used in the video. Note that we are only changing the `nginxproxymanager` service (now `caddy`), the rest may stay exactly the same:


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

After saving the `docker-compose.yml` file, you can run all the servers by simply using the following command:

    docker compose up -d

### Configuring the domains for our services

Continuing with Wolfgang's video, we will ignore the configuration of NPM (as we are not using it).

However, it is very important to configure DuckDNS (or our DNS provider of choice) as shown in the video between 7:12 and 7:37.

Now comes the fun part! Let's configure Caddy.

#### DNS Challenge with Caddy

Configuring the certificates for our domain with Caddy is quite straightforward. It's important to note that the configuration parameters depend on the provider. For this example, I will be using DuckDNS and the domain `mydomain.duckdns.org`.

Firstly, create a file named `Caddyfile` in `caddy/data/` (from the directory of your Compose file). This new file should be written to `/etc/caddy/Caddyfile` inside the container.

Secondly, copy the following contents into the file:

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

Don't forget to change `mydomain.duckdns.org` to your actual domain, and `DUCK_DNS_API_TOKEN` for the API Token visible on your DuckDNS account.

Finally, you can restart the Caddy container with:

  docker compose restart caddy

You should check for logs to monitor whether there are any issues. You can do that with:

  docker compose logs caddy

If everything worked correctly, you should see the message *Hello, world!* when connecting to your domain. You should also see that it uses HTTPS without any issue. The certificate should be verified by *Let's Encrypt* and HTTP traffic should be redirected to HTTPS.

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

- SERVICE: We would substitute this for the subdomain we want to use for accessing our service. We would use the same with NPM.
- MATCHER: This is only a "variable name", anything could be used as long as it does not collide with other services. To keep things tidy, I usually put the same as in SERVICE
- DESTINATION: This is where the request should be forwarded, as we would do with NPM. We may use the container name.

Finally, if none of the matchers above have succeeded for a given request, we have a final handle that will respond *This service does not exist!*.

To apply the changes, don't forget to restart the caddy container:

	docker compose restart caddy

We may want to run different services on your Homeserver, but in the example you can see how easy it is to expand Caddy's configuration by following the chunk above.

Best of all, you can save this configuration file as you desire and avoid retyping everything ever again.

### Going further

Hurray! Now we have finally achieved feature parity with Wolfgang's video, but using Caddy instead of NPM. Before finishing, though, there are a couple of extra concepts I would like to comment on.

#### Multiple Compose files

As Wolfgang says in his video: 

*I'm going to put \[NPM and the rest of the services\] on the same Compose file. This will ensure that all our containers are on the same Docker network and can communicate with each other easily.*

Putting everything on a single file is understandable for a tutorial, but with a lot of containers, it can have its drawbacks [^2]. That's why I would like to give some insight on how to communicate containers on different Compose files.

To make sure we are all on the same page, you should know that for each Compose file there is a `default` network which is automatically created and all containers inside the Compose file are added to it. That's why they can communicate with each other by default.

##### Single custom Network approach

First, we'll consider at the simplest approach. We'll create a single custom Docker Network called `caddy`, and all the services that we want to connect with the RP will be added to it.

We would need the following Compose file for the Caddy container:

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

- `default`: Where all the containers of the Compose file will be added, so they can communicate with each other.
- `caddy`: A custom network that we will use to communicate the RP with our services on other Compose files. We specify which container is added to this network by adding the content on lines 5 and 6.

Now, suppose we have a single Compose file for our Nextcloud container. It would look something like this:

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

Note that, apart from improving the management of the Compose files, we are improving a bit the security of our infrastructure. In the tutorial's implementation, all containers could communicate with each other. Now, only the ones that are added to the `caddy` network can communicate between them (apart from the ones on the same Compose file, of course).

##### Multiple Networks approach

Although the previous approach may be secure enough for many, there is technically a security flaw, as all containers between the `caddy` network can communicate with each other. For example, suppose we have Jellyfin and Nextcloud inside the Caddy network. If one is compromised, it can directly communicate to the other via the `caddy` network.

So now we will see an implementation that only allows connections from the RP to any service and vice versa, but not between services. We can visualize this idea as a star graph, with Caddy in the center.

{% mermaid() %}
mindmap
  Caddy
    Jellyfin
    Nextcloud
    Home Assistant
{% end %}

The implementation would not change much. The Compose file for Caddy would look like this:

```
version: '2.2' 
services:
  caddy:
    ...
    networks:
      - caddy-jellyfin
      - caddy-nextcloud
      - caddy-home
networks:
  default:
  caddy:
  caddy-jellyfin:
  caddy-home:
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

As you can see, this second approach achieves greater control over the communication between containers and greater security, but it makes configuration a bit more complicated to manage. It's up to you to determine if it's worth it or not.

### Implementing IP-based ACLs with Caddy

Finally, I would like to point out that NPM has some other great features which are not shown in the video by Wolfgang, as they are out of scope. All of them can be replicated using with Caddy on one way or another.

There is one in particular that I found very useful, and an easy and scalable Caddy implementation is not trivial: IP-range based ACLs. This is very useful when sharing access to your Homeserver to friends and family, as you can restrict the services available to each user.

I've had a reliable implementation of this feature for over a year. In some weeks I will write another post explaining it and I will link it here.

* * *

*For any suggestion on comment, don't hesitate to [contact me](mailto:contact@albertcanales.com)*

*Thanks for reading!*

[^1]: Actually, this is a side-effect of not using a trusted HTTPS connection. This may have other security concerns, but they were not important for me as I use Wireguard, which already encrypts the connection end-to-end

[^2]: I do not talk from experience here, as I run all my infrastructure on Docker Containers using Ansible. However, as someone with more than 20 containers running, I can imagine that navigating through a single file would be kind of a nightmare.
