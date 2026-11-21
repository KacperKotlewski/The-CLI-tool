---
author: Kacper Kotlewski
title: The CLI tool <br> <span>managing environment variables in projects</span>
subtitle: UNIVERSITY OF SILESIA IN KATOWICE FACULTY OF SCIENCE AND TECHNOLOGY,<br> AUGUST CHEŁKOWSKI INSTITUTE OF PHYSICS <br> Applied Computer Science
date: 'Supervisor: Dr Hab. Łukasz Machura'
---

# QUICK RECAP

---

## What is this project about?

![](https://storage.needpix.com/rsynced_images/question-1015308_1280.jpg)


<div style="font-size: 0.5em;">
<p>Photo from <strong><a href="https://www.needpix.com/photo/487659/question-question-mark-response-symbol-characters-help-request-note-punctuation-marks">needpix</a></strong></p>
</div>

---

## Command Line Interface and <br> environment variables - dotEnv

![](https://live.staticflickr.com/598/31673579214_9a3f86e237_c.jpg)

<div style="font-size: 0.5em;">
<p>Photo from <strong><a href="https://www.flickr.com/">flickr</a></strong></p>
</div>

---

### What is Command Line Interface?

![](https://live.staticflickr.com/7296/11863817035_53d6397056_z.jpg)

<div style="font-size: 0.5em;">
<p>Photo from <strong><a href="https://www.flickr.com/">flickr</a></strong></p>
</div>


---

### What is Environment variables?

![](https://live.staticflickr.com/525/31461522456_ee91b94636_m.jpg)

<div style="font-size: 0.5em;">
<p>Photo from <strong><a href="https://www.flickr.com/">flickr</a></strong></p>
</div>

---

### What is dotEnv?

<div>
    <div style = "display: flex; justify-content: center; gap: 50px;">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAh1BMVEXs1T8AAAD23kLz20Hp0j5QSBWHeiSQgiYsKAzMuDbUwDlZURgVEwXizDyDdiPv2EB8cCGZiinaxTpHQBOnlyyThSc9NxC0ojDBrjM3MQ4pJQtLRBQyLQ1DPRLSvjhiWBqfjyoLCgO6qDJWThewny8kIQobGQd1ah9pXxz840N9cSEgHQhnXRthazyAAAAEu0lEQVR4nO2aa1fbOBBAZSlhIRAEhFcp4dlNKN3///sWAolm9HC9aznknN77DWdi+1oTaUbGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4Ixh1Ihf/m/Mlp+92E9XE1ti/my785T7j3d7m2CJzOn+gv+JewzlmtnQP30LQta9uuP+/DZs9l5wuNhR/N800fwv+TMSUnsLXGDaT5IHHhsbehPCH9ImsTnna+tC+1PB78sQTQ3cRwuf5AXLzEHJXPUn7GTbn8SNPDFUKnuXuX0Z8qz+EPQ2b5HZjQ+NmIfo0JyCTNBvwtYbLKPEyhuch+jaXpvYyBBTmoq80bA504qWGZiSi06lJJWn6u65reHtYZHy+vrXY8FbnVcbQHmYeVEAm6Xn9eUYZ7v10RTaXjg2jJSBj6K+Kz2N1QjGT1i9otOFxl595YthM5YPPGBojgpPVQCbp/RBJWsFQ3VfO0C1DcLKiu4fw4dMQSVrBUJWSOUN/HWJ/xcNkRZIOIljDcPEbQ+MeQ3A894okPRlgMTRVDOUMmTc8bkoXkUlav61YUcNQVGNZQ9lgLPRFRJIuhhnCOobjza8ra2jcbYjVaToNHwzQVqyoYthcbWaVvKFoMNSvTSZppt6pQg/Dl3B3j+uP84ZyPjmSIjaU5ZcDDaGuaWwBcXFhOBEbIK+2zVA1GGJCkeZDtBWx4dF+gV8y4YLhmVjn1sVKyVA0GEtxMpGkQ7QVsWGZ16zhxN6HkLlrM5QzShOOiyQdpK3obnicN/Tyvj/a/ZKhbDBCcSa+P0hb0d9QZtlHY1AylA3Gy6ZgfYi+vXuGxoqF7sW2GKoGY3Pt75tD/wyWpD0N1Xbo+yRZNJQNxjpNp+mhnTM09iRE3bgWQ9lgfA6YTNKhlor+hir7LlxLlsoG42PARJIO1FbEho9HBWTJGBu6H0Jx6lsMRbl3tVIUSXowXJJ226cR10/G0D6HGz20ZUN/F+JW2wKiCrgZcAj71KUfhmpT+8kVDVWD8b422HExtCq9DVXj8NhmGG0biiTN7vbXor+h8eL10t6kaCgroGdrfEjSy+EWQ1PHUFbgYeJJUk9UoW91tphJC2/d/gPleaOKobGiU1yUDcWovVWxYkR7txWji1OFqh9qGKpXE2VD+csb/wy6z72TdBpdeikvXcVQtn8thrLbGoVF5kfveSY2PKluqF4+lA1lgyEm4L5+WzH0kyYhs8j5NEo0UzttaOxxE5N7k7ZMoqpsBG/D0PhFdJXsGF7HQW9FQoXVfjuGTx0MjT9KDF8rVGydDVue5maToWSodmKKhpn95BptRVfDVtbbmUVDH18mO4Z3UVCzX6Po3o6hqqxLhqrBKEftqGF893nD6DHUaSu2Zai2pQqGqptsarUV2zI0Vi13+fwTLcU7yb+N7bahrsDzhl6XsHXeVmzPUG1LFeYQ9RQO6/S+7b3FTdOJToYqBwuGssGo0FasGB1o1J25+3EXZus3J/5h9nlonpkG/dks+UYc8rQJGc+r+L2fNEJ96EqvRTXhfxHSQ/JSmW+UQwbdnwEAAAAAAAAAAIA/jX8Bd4tF8+9SMoUAAAAASUVORK5CYII="
        alt="dotEnv" style="width: 150px;">
        <img src="https://pbs.twimg.com/profile_images/689189555765784576/3wgIDj3j_400x400.png" alt="Heroku" style="width: 150px;">
    </div>
    <img src="../document/images/Screenshot 2024-03-06 201115.png" alt="file" style="width: 600px;">
</div>



# What is the problem?

---

## Public Repositories

![](https://c.pxhere.com/images/8c/1c/8f63e4cf7cd36305b8f6812e0b05-1444327.jpg!d)

<div style="font-size: 0.5em;">
<p>Photo by <strong><a href="https://pxhere.com/en/photographer/767067?utm_content=clipUser&utm_medium=referral&utm_source=pxhere">mohamed_hassan</a></strong> from <strong><a href="https://pxhere.com/en/photo/1444327?utm_content=clipUser&utm_medium=referral&utm_source=pxhere">PxHere</a></strong></p>
</div>

---

## Why that is a problem?

<span class="fragment fade-in"> <strong>Sensitive data</strong> in public repositories</span>

<center>
<ul style="width:50%;">
<li class="fragment fade-in"> <strong>Passwords</strong></li>
<li class="fragment fade-in"> <strong>API keys</strong></li>
<li class="fragment fade-in"> <strong>Database credentials</strong></li>
<li class="fragment fade-in"> <strong>Tokens</strong></li>
</ul>
</center>

---

## But wait...

there are .env.example file right?

![](./images/Screenshot%202024-03-07%20094823.png)


---

## Yes they are...

<div style = "display: flex; justify-content: center; gap: 10px; align-items: center;">
    <img src="../document/images/Screenshot 2024-03-07 095201.png" alt="" style="width: 300px; height:100px;">
    <img src="../document/images/Screenshot 2024-03-07 095217.png" alt="" style="height: 600px;">
</div>

---













# Solution - MVP

---

## Characteristics

<center>
<ul style="width:50%;">
<li class="fragment fade-in"> <strong>Secure</strong></li>
<li class="fragment fade-in"> <strong>Easy</strong></li>
<li class="fragment fade-in"> <strong>Fast</strong></li>
<li class="fragment fade-in"> <strong>Reliable</strong></li>
<li class="fragment fade-in"> <strong>Scalable</strong></li>
<li class="fragment fade-in"> <strong>Open Source</strong></li>
</ul>
</center>

---

## The CLI tool

![MVP](./images/Screenshot%202024-03-07%20095918.png)

---

## Not ideal but helpful

![.env.example](./images/Screenshot%202024-03-07%20100053.png)

[github.com/KacperKotlewski/strapi_postgres_docker](https://github.com/KacperKotlewski/strapi_postgres_docker)

---

## Summary of MVP

<center>
<ul style="width:50%;">
<li class="fragment fade-in"> <strong>Secure?</strong> <span class="fragment fade-in">Yes</span></li>
<li class="fragment fade-in"> <strong>Easy?</strong> <span class="fragment fade-in">To use as CLI,<br> not to implement</span></li>
<li class="fragment fade-in"> <strong>Fast?</strong> <span class="fragment fade-in">Yes</span></li>
<li class="fragment fade-in"> <strong>Reliable</strong> <span class="fragment fade-in">No</span></li>
<li class="fragment fade-in"> <strong>Scalable</strong> <span class="fragment fade-in">Maybe</span></li>
<li class="fragment fade-in"> <strong>Open Source?</strong> <span class="fragment fade-in">Not realy</span></li>
</ul>
</center>










# Solution

---

## New approach

<center>
<ul style="width:50%;">
<li class="fragment fade-in"> <strong>New "schema" format</strong></li>
<li class="fragment fade-in"> <strong>Better CLI tool</strong>
    <ul style="">
    <li class="fragment fade-in"> <strong>Create .env from "schema"</strong></li>
    <li class="fragment fade-in"> <strong>Create "schema" from .env</strong></li>
    </ul>
</li>
<li class="fragment fade-in"> <strong>Open Source</strong></li>
</ul>

---

## Schema format

<img src="../document/images/Screenshot 2024-03-07 101930.png" alt="schema" style="height: 1000px;">


---

## New CLI tool

![](./images/Screenshot%202024-03-07%20102337.png)

---

## New Framework

![](./images/Screenshot%202024-03-07%20102518.png)









# Why new CLI framework?

---

## Because it is not

![](./images/Screenshot%202024-03-07%20102635.png)

## GUI one day

![](./images/Screenshot%202024-03-07%20105506.png)

---

## How to implement?
### Command

![](./images/Screenshot%202024-03-07%20110528.png)

---

## How to implement?
### Interface

![](./images/Screenshot%202024-03-07%20110709.png)






# What about tool?

---

## Create .env from "schema"

![](./images/Screenshot%202024-03-07%20111222.png)

---

![](./images/Screenshot%202024-03-07%20111516.png)

---

### Results

![](./images/Screenshot%202024-03-07%20111618.png)


---

## Create "schema" from .env

![](./images/Screenshot%202024-03-07%20111855.png)

---

![](./images/Screenshot%202024-02-28%20235850.png)


---

![](./images/Screenshot%202024-03-07%20112120.png)

---

![](./images/Screenshot%202024-03-07%20112144.png)

---

![](./images/Screenshot%202024-03-07%20112250.png)

---

![](./images/Screenshot%202024-03-07%20112610.png)

---

![](./images/Screenshot%202024-03-07%20112641.png)

---

![](./images/Screenshot%202024-03-07%20113231.png)





# Summary

---

## New CLI tool is

<center>
<ul style="width:50%;">
<li class="fragment fade-in"> <strong>Secure</strong></li>
<li class="fragment fade-in"> <strong>Easy</strong></li>
<li class="fragment fade-in"> <strong>Fast</strong></li>
<li class="fragment fade-in"> <strong>Reliable</strong></li>
<li class="fragment fade-in"> <strong>Scalable</strong></li>
<li class="fragment fade-in"> <strong>Open Source</strong></li>
</ul>
</center>


<div class="fragment fade-in"> All objectives of the work were achieved and implemented, and an additional advantage not planned at the beginning of the work's creation was the forum added to the application. </div>

---

## Questions?


![](https://storage.needpix.com/rsynced_images/question-1015308_1280.jpg)


<div style="font-size: 0.5em;">
<p>Photo from <strong><a href="https://www.needpix.com/photo/487659/question-question-mark-response-symbol-characters-help-request-note-punctuation-marks">needpix</a></strong></p>
</div>

---

![](https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTA1L2pvYjk2NC0xMDVhLXYuanBn.jpg)


<div style="font-size: 0.5em;">
<p>Photo from <strong><a href="https://www.rawpixel.com/search/thanks%20you?page=1&path=_topics&sort=curated">rawpixel</a></strong></p>

UNIVERSITY OF SILESIA IN KATOWICE FACULTY OF SCIENCE AND TECHNOLOGY,<br> AUGUST CHEŁKOWSKI INSTITUTE OF PHYSICS <br> Applied Computer Science
</div>

**Kacper Kotlewski**