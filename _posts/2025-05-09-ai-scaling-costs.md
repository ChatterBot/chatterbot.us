---
layout: post
title: "Handling AI Scaling and Reducing Costs"
date: 2025-05-09 07:03:03 +0000
author: gunthercox
categories: infrastructure deployment
tags:
  - chatterbot
  - Celery
  - Docker
image: /img/articles/03-acorn.jpg
image_alt: Abstract article image showing an acorn resting on a rock
---

When it comes to the programming adage "Speed, Quality, Price: Choose Two" I tend to prefer low price. Perhaps it's the influence that the [Zen of Python](https://peps.python.org/pep-0020/) has had on me, or perhaps it's simply the trend of software to outpace hardware when it comes to improving efficiency.

> Now is better than never.
> Although never is often better than *right* now.
> 
> ~ Zen of Python

Regardless, the case I'll make here is that we can demonstrate a method to handle simple AI tasks at scale favoring queued results that complete eventually over immediate results that require adding resources each time scaling is needed.

## Scaling using a queue

![Scaling using a queue](/img/diagrams/scaling-using-a-queue.svg)

The idea here is to handle tasks submitted by users by adding them to a queue, then a task executor takes items from the queue (processing one task at a time). This makes it so that the primary limitation to the number of tasks that can be handled is the queue itself. However, it is less expensive to add storage to our queue than it is to add additional task executors.

This highlights the contrast between the queued design vs physically scaling by adding an additional task executor for each additional user. Of course the users in the example on the right benefit from getting immediate results as they don't have to wait their turn in a queue. One way we can begin to remedy this is to then scale our queueing infrastructure:

![Scaling horizontally](/img/diagrams/horizontal-scaling.svg)

## An example using Redis and Celery

Diving into a practical example, we can create a queue using [Redis](https://github.com/redis/redis), and a task executor using [Celery](https://docs.celeryq.dev/en/stable/).

The following files will be needed:

```dockerfile
# Dockerfile

{% include articles/chatterbot-celery/Dockerfile %}
```

```yaml
# docker-compose.yml

{% include articles/chatterbot-celery/docker-compose.yml %}
```

```
# requirements.txt

{% include articles/chatterbot-celery/requirements.txt %}
```

```python
# tasks.py

{% include articles/chatterbot-celery/tasks.py %}
```

### Running the example

Next, use docker to start your services.

```bash
sudo docker compose up -d
```

You can check to make sure the expected services are running using the `ps` subcommand. You should see output similar to the following:

```bash
sudo docker compose ps

NAME                           IMAGE                      COMMAND                  SERVICE    CREATED              STATUS              PORTS
chatterbot-celery-celery-1     chatterbot-celery-celery   "celery -A tasks wor…"   celery     7 seconds ago        Up 6 seconds        
chatterbot-celery-rabbitmq-1   rabbitmq:4.1               "docker-entrypoint.s…"   rabbitmq   About a minute ago   Up About a minute   4369/tcp, 5671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:5672->5672/tcp, [::]:5672->5672/tcp
```

Next, we can simulate a user submitting a task to the queue. Celery will then detect this task and start running it.

```bash
sudo docker compose exec celery python

Python 3.11.12 (main, Apr 28 2025, 22:10:55) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tasks import solve
>>> solve.delay(1, 'What is 50 divided by 2?')
<AsyncResult: 984463f9-603b-4242-b3f5-8d626dc4f7a6>
```

Now if we inspect the contents of the `data` directory, we should see the a new file named `1-response.txt` containing the solved equation:

```text
50 divided by 2 = 25
```

## Scaling horizontally

We can horizontally scale the task executor (Celery) layer of our infrastructure. The following command will create a new instance of our `celery` container so we have 2 total running.

```bash
sudo docker compose up -d --scale celery=2

[+] Running 3/3
 ✔ Container chatterbot-celery-rabbitmq-1  Running    0.0s 
 ✔ Container chatterbot-celery-celery-1    Running    0.0s 
 ✔ Container chatterbot-celery-celery-2    Started 
```

Once the scaling is complete, both Celery workers will run in parallel, each able to take a task out of the queue for processing.

## Final notes and musings

There is a time and a place for delayed processing in the method that has been described here. Actions such as conversing with AI likely require more real-time strategies for returning responses promptly. Tasks better suited to the strategy described in this post might include long running tasks such as AI image generation or analysis, or generating summaries of relatively static data.

As noted in [my Earth Day post](/2025/04/codecarbon/) from a few weeks back, AI models can consume a large amount of power to generate output. I think an interesting experiment to consider might be to set up a queue, and use a Raspberry Pi connected to a solar panel to process tasks. Perhaps in some use cases the initial investment in hardware could provide some level of ROI compared to purchasing cloud services.

If you _do_ happen to be using a Raspberry Pi running on solar power, a relevant note might be the use of a `rabbitmq` container over an alternative such as `redis`. Per the [Celery docs](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html#redis) redis is more susceptible to data loss in the event of abrupt power failures.
