---
layout: post
title: "How to Write a Great GitHub Issue: A Guide for Open Source Contributors"
date: 2026-03-12 07:00:00 -0400
author: gunthercox
excerpt: "Open source software thrives on collaboration. Every time someone reports a bug, suggests a feature, or asks a well-formulated question, the project takes a step forward. For projects like ChatterBot, the GitHub issue tracker is the central hub for this collaboration."
categories: community
tags:
  - open-source
image: /img/articles/05-circuit.jpg
image_alt: Abstract article image showing wires and a circuit board connected together.
---

Open source software thrives on collaboration. Every time someone reports a bug, suggests a feature, or asks a well-formulated question, the project takes a step forward. For projects like ChatterBot, the GitHub issue tracker is the central hub for this collaboration.

However, writing a good GitHub issue is a skill. A well-written ticket gives maintainers exactly what they need to understand, reproduce, and fix the problem. A poorly written ticket, on the other hand, can lead to endless back-and-forth threads, frustration, and delayed fixes.

Whether you are a seasoned developer or a first-time contributor, here is a guide on the best ways to open GitHub issues, along with a few examples of what to avoid.

## What Not to Do: The Anti-Patterns

Before diving into the perfect issue template, let's look at a few common pitfalls. Maintainers often sift through a high volume of tickets, and certain types of messages make it nearly impossible to provide help.

**The "Out of Scope" Ticket**

> "Help, I can't install Python."

This is a generalized example of a common anti-pattern. Without knowing the operating system, the Python version, the exact code being run, the full error traceback, or what steps have already been taken to try and fix it, maintainers are left guessing.

When project trackers are flooded with vague, low-effort tickets, it takes a heavy toll on the people volunteering their time to manage them. Fostering a sustainable environment where maintainers and contributors can collaborate effectively is crucial for the health of any project. If you are interested in how the community can build a more positive and sustainable ecosystem moving forward, check out this perspective on [an optimistic outlook for the future of open source](https://blog.salvius.org/2026/01/an-optimistic-outlook-for-future-of.html).

## The Anatomy of a Great Issue

To ensure your issue gets the attention it deserves, always include the following elements:

1. Search First: Before clicking "New Issue," briefly search the existing open and closed issues. Someone else may have already reported the same problem or found a workaround.

2. A Descriptive Title: Summarize the problem clearly. Instead of "Database broken," use "SQLite OperationalError when initializing ChatBot in Python 3.12."

3. Environment Details: Always list your Operating System, the project version you are using, and your language version (e.g., Python 3.13).

4. Steps to Reproduce: Provide a minimal, reproducible example. What exact steps or code snippet will cause the error to appear?

5. Expected vs. Actual Behavior: Explain what you thought was going to happen, and what actually happened instead.

6. Troubleshooting Steps Taken: Share what you have already tried to do to solve the issue. This saves maintainers from suggesting fixes you've already ruled out.

While **all** of these pieces of information are certainly never an absolute requirement, considering if these elements should be included in a GitHub issue _is_.

## Examples of Great Issues

### Example 1: The Bug Report

**Title:** `TypeError in TimeLogicAdapter when passing custom datetime object`

**Description:**  
Environment:  
OS: Ubuntu 22.04  
Python Version: 3.11  
ChatterBot Version: 1.1.x  

**Expected Behavior:**  
The `TimeLogicAdapter` should return a response containing the current time when triggered, even if a custom localized datetime object is passed in the kwargs.

**Actual Behavior:**  
The bot crashes with a TypeError: can't compare offset-naive and offset-aware datetimes.

**Steps to Reproduce:**

```python
from chatterbot import ChatBot
import datetime
import pytz

chatbot = ChatBot(
    'TestBot',
    logic_adapters=['chatterbot.logic.TimeLogicAdapter']
)

# Passing a timezone-aware datetime causes the crash
custom_time = datetime.datetime.now(pytz.UTC)
chatbot.get_response("What time is it?", additional_kwargs={'time': custom_time})
```

**What I've Tried:**

I traced the error to line 42 in `time_adapter.py`. I tried stripping the timezone info before passing it, which acts as a temporary workaround, but the adapter should probably handle both naive and aware datetimes natively. I'd be happy to submit a Pull Request if you agree with this approach!

### Example 2: The Feature Request

**Title:** `Add support for PostgreSQL JSONB fields in storage adapter`

**Description:**

Currently, the SQL storage adapter handles statement metadata by serializing it. For users scaling ChatterBot on PostgreSQL databases, leveraging native JSONB columns for metadata would significantly improve search performance and allow for more complex filtering.

**Proposed Solution:**

Introduce a check in the SQLAlchemy models that detects if the dialect is PostgreSQL, and if so, utilizes `JSONB` for the `tags` and `in_response_to` fields rather than standard text.

**Alternatives Considered:**

I considered writing a completely separate `PostgresStorageAdapter`, but integrating it into the existing SQL storage adapter via dialect checks seems cleaner and easier to maintain.

***

By taking a few extra minutes to provide context, code snippets, and troubleshooting history, you respect the maintainers' time and dramatically increase the chances of your issue being resolved quickly. Open source is a team effort, and a great GitHub issue is the best way to start the conversation.
