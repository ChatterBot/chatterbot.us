---
layout: page
title: "Measuring Chatbot Climate Impact with CodeCarbon"
date: 2025-04-29 07:03:03 +0000
author: gunthercox
categories: libraries
tags:
  - climate
  - libraries
og_image: /img/articles/01-field.jpg
og_image_alt: Abstract article image showing a fractal pattern in cauliflower
---

{% picture /img/articles/01-field.jpg --alt Abstract article image showing a fractal pattern in cauliflower %}

<div class="text-muted">
    Article by <a href="https://github.com/gunthercox/" target="_blank">Gunther Cox</a>
</div>
<div class="text-muted mb-3">
    Posted {{ page.date | date: "%B %-d, %Y" }}
</div>

This past [Earth Day](https://en.wikipedia.org/wiki/Earth_Day) GitHub shared their [Climate Action Plan for Developers](https://github.com/social-impact/focus-areas/environmental-sustainability/climate-action-plan-for-developers), a collection of resources designed to create tangible steps that developers can use to improve how software impacts the planet.

This concept has become increasingly relevant as of late with the increasing use of generative AI. A trend in recent news has been to point out the sometimes staggering statistics around the use of water for cooling the hardware on which many AI systems run, as well as the use of electricity. A <a href="https://www.washingtonpost.com/technology/2024/09/18/energy-ai-use-electricity-water-data-centers/">2024 article from The Washington Post</a> reports estimates that models such as GPT-4 require approximately 1 bottle's worth of water (519 milliliters) to write a 100-word email. That same email also consumes roughly the same amount of energy as turning on 14 LED light bulbs for 1 hour (0.14 kilowatt-hours).

Highlighted amidst GitHub's list of environmental impact tools was a project called **CodeCarbon**, a Python library designed to allow developers to estimate the carbon footprint of their work in the form of kilograms of CO₂-equivalents (CO₂eq). Their [documentation](https://mlco2.github.io/codecarbon/motivation.html) dives further into the motivation and methodology used to implement their statistics.

To test out `codecarbon` we put the following example together, demonstrating the initialization of a simple chat bot, with a small amount of training data.

## Code Setup

```bash
pip install codecarbon
```

Our example code will be as follows:

```python
# codecarbon-example.py

{% include articles/2025-04-codecarbon.py %}
```

## Results

Next, running the code using `python codecarbon-example.py` yields the analyzed run for our chat bot. Let's take a look at some of the results:

```
The below tracking methods have been set up:
    RAM Tracking Method: RAM power estimation model
    CPU Tracking Method: cpu_load
    GPU Tracking Method: Unspecified

>>> Tracker's metadata:
  Python version: 3.12.2
  CodeCarbon version: 3.0.0
  Available RAM : 30.541 GB
  CPU count: 4 thread(s) in 1 physical CPU(s)
  CPU model: Intel(R) Core(TM) i7

Energy consumed for RAM : 0.000009 kWh. RAM Power : 10.0 W
Delta energy consumed for CPU with cpu_load : 0.000010 kWh, power : 10.89 W
Energy consumed for All CPU : 0.000010 kWh
0.000018 kWh of electricity used since the beginning.
Carbon emissions from computation: 0.0068 g CO2eq
```

ChatterBot's resource usage is relatively low in this example, likely for a few reasons. Since we used a small amount of training data fewer resources are required to process it. This example is also using ChatterBot's default search-based response generation (designed to run efficiently on smaller devices such as the Raspberry Pi), which is less processing intensive in most cases compared to using generative models.

Check out CodeCarbon's [Quickstart guide](https://mlco2.github.io/codecarbon/usage.html) for more examples of ways their library can be used. Likewise the documentation for ChatterBot can be found at [docs.chatterbot.us](https://docs.chatterbot.us/)
