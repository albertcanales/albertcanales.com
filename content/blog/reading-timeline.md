+++
title="Reading Timeline"
date=2023-04-15
template="post.html"
+++


## Motivation

Last June, my friend and GeoGuessr enthusiast [Abel](https://abeldonate.github.io/) told me that, when looking for some information about maps, he stumbled with the website of the cartographer [Jeff Allen](http://jamaps.github.io). The geography part is not relevant for this project. In the *Words* section, however, lied a beautiful representation of a timeline for reading books. Abel, a passionate reader himself, was asking me if I was interested in making a program that would be ~~abel~~ able to generate a similar one automatically. I obviously said yes.


## How it works

The project's usage is quite simple, but open to improvements and building on top of it (as it will be discussed below). You may consider it more of a *backend* to a possible bigger application.

The program's installation is available on the included ``README.md`` file, and available options are shown with the *--help* argument.

In short, it is able to generate the said timeline using two input sources:

- ``data.yml``. Contains the actual data to be visualized (i.e. books and categories). The included example file should be self-explanatory of the different features.
- ``config.yml``. Contains the parameters to decide *how* to display the information. For example: colors, dimensions, fonts, etc.

It is expected for a general user to only modify the former, but anyone looking for a more customized version is welcomed to do as well for the latter. 

Once ready, the user can simply run the main program, automatically generating a timeline as such.

<figure>
    <img src="https://raw.githubusercontent.com/albertcanales/reading-timeline/main/example.svg" class="inlineimg">
    <figcaption>
        Timeline generated with the example data
    </figcaption>
</figure>


## Technologies

The project is fully implemented in Python. It is a language that I'm very familiar with, and its great libraries are really useful when treating different data formats.

For the input files (both data and configuration) I've decided to use YAML. I love YAML because it is really comfortable to read and write for both humans and machines. In my opinion, other formats like JSON and XML may be great one the latter, but definitely not on the former, which makes them impractical for this project. The program reads the YAML files through the [PyYAML](https://pypi.org/project/PyYAML/) library.

For exporting the Reading Timeline into an SVG, I had multiple library options. I finally chose [svgwrite](https://pypi.org/project/svgwrite/) as it did all I needed and seemed quite easy to use.


## Implementation

{% mermaid() %}
flowchart LR
    DaP([data.py]) --> PrP([processor.py])
    CoP([config.py]) --> PrP -->
    DrP([drawer.py])
    CoP --> DrP
    DaY[(data.yml)] --> DaP
    CoY[(config.yml)] --> CoP
{% end %}

As said before, the program is quite simple. It can be divided into three stages:

- **Getting input**. The data and configuration files are loaded into objects.
- **Processing the data**. Using the parameters specified in the configuration, the more complex attributes for drawing the data (books and categories) are calculated.
- **Drawing the timeline**. The resulting SVG is drawn using the previous parameters, both given in the input configuration and calculated on the processing stage.

The configurable nature of the project makes *config.py*, *processor.py* and above all, *drawer.py* quite dependent on the SVG format. This is not a problem as it is a standard format that could be easily converted to others if needed.

## Improvements

In the last few months, I've been sporadically adding the latest features that I would consider to be the core version of the program. However, since nearly the beginning I've had some parallel ideas which, although I would not consider them essential for the program's functioning, they would certainly be a great improvement.

### Dynamic Fit

Right now, the program takes a strict approach on date positioning in the timeline. That means that if two dates are really close together and the user finds it aesthetically unpleasing, it is advised to make the timeline taller or manually *separate* the dates (or a combination of the two) until satisfied.

It would be interesting to add an option to make the positioning more *flexible* (compromising on precision). That means that the program would automatically apply the minimum height that makes no dates collide (separating them a bit if necessary).

The definition is a bit fuzzy and should be worked on a bit more. However, it does not seem really complicated to implement, and I may add it myself in the near future.

### Import from Goodreads

I am aware that many readers use Goodreads to record their books (myself included), so an integration with it is more than obvious.

However, the tool for exporting the data from Goodreads' book library into a CSV does not include the *Date Started* field, which seems to be a bug, as the rest of the fields are present.

I contacted them over 6 months ago about the issue, but I sadly I have neither received an answer nor seen the issue resolved. So, I have the dilemma to implement a broken feature or to wait until it is resolved. Right now I am taking the second approach, but I may change my thoughts in the future.

### Interactive Frontend

As stated before, the core functionality of the project could be seen as the backend for a more polished graphical application. For deploying purposes, I think a web app would be the most appropriate.

The simplest version of this UI could just offer an online editor of the *data* and *config* files on a side-by-side view with a live preview of the timeline. This could be easily achieved, but I don't see a great improvement in usage apart from simplifying the installation process.

A more complex frontend could offer the tools to graphically enter all the data and configuration parameters. I find this option way more appealing, but frontend development is not really my thing (and this approach would require a lot of it), so I would not expect this implementation in a near future unless someone else joins the project (it could be you!).

### Packaging the program

As this project that may be used by non-programmers, I would like to simplify its installation and usage. Right now there is a small guide for downloading and running from source, but it is far from accessible for everyone.

For now, being a Python project, I think that it would be more than enough to develop a pip package, which would greatly simplify the installation and usage, although it would still require the use of the terminal. However, anything more complicated may be too much overkill for the project's scope.

Eventually, if some Web UI or similar is built, this process would only be relevant to developers or self-hosters, becoming less of a problem.


## Summary

Some friends of mine (Abel included!) have been using the program for some time and are quite happy with its results. Abel for example has even adventured to change the default appearance quite radically.

For my part, I am quite happy with how the project turned out. I managed to keep the project's scope and codebase small and clear, which is something quite important for future me (as I tend to forget my own implementations) or for anyone who wants to contribute. 

However, I sometimes feel like the project is incomplete due to the improvements mentioned above. As some of them are really easy, I may tackle their development on the next vacations.

As for the libraries used, I am quite happy with them. *PyYAML* worked like a charm, and *svgwrite* was also pretty intuitive. For the latter, I would argue that the documentation is a bit obtuse with terminology for someone who has not worked with SVGs before, but the given examples were great, and I could implement many features thanks to them.

Finally, if the project caught your attention, and you have questions or suggestions, tell me about them! I will be more than happy to listen to them.

* * *

*You can take a look at the source code of the project [here](https://github.com/albertcanales/reading-timeline). For any suggestion on comment, don't hesitate to [contact me](mailto:contact@albertcanales.com)*

*Thanks for reading!*

