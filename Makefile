VERSION=v0.20.0

pull:
	docker pull ghcr.io/getzola/zola:$(VERSION)

build:
	docker run -u "$$(id -u):$$(id -g)" -v $$PWD:/app --workdir /app ghcr.io/getzola/zola:$(VERSION) build

serve:
	docker run -u "$$(id -u):$$(id -g)" -v $$PWD:/app --workdir /app -p 1111:1111 ghcr.io/getzola/zola:$(VERSION) serve --interface 0.0.0.0 --base-url localhost
