# Apparel For You 
A small scale project to familiarize myself with the web framework Django, a peak into deployment, play around with HTMX
and general navigation in the webspace.

## Thoughts

### Development stage 
- While I'm enjoying Django as a framework. The abstractions are a double edge sword in my case. I know what the framework 
is doing, but I don't know how it is doing it. Many of the smaller issue I have encountered become a dive into a rabbit
hole. Initially this was a minor frustration but the more times I embodied Ms. Liddell the faster I found myself 
implementing changes. 
- When creating the app models the first time I quickly realized it that planning the structure of the models is important
  - I know you're thinking "No **** Sherlock"  well I'm referring specifically the relationships between models;
    many-to-many, foreign key relationships. Having using Sqlite in most of my pet projects that knowledge was the building
    blocks that allowed the templating to be quite fun to navigate
  - The Django ORM seems to be very convenient. I currently have not come across a situation in which I needed to write
    raw SQL as its traversal between models, while complex at first make my usage a breeze. 
- I also used this project to dip my toes into the realm of frontend. Vanilla frontend that is. JavaScript, CSS, HTML and 
HTMX. I don't have much to say about that. I have included live search via HTMX but the rest of the website does not
follow the SPA meta 
- I have left out some features I want to add because I want to see what a production environment is like with feature
updates and how I will manage both the user point and the VCS point on my side 
- The auth included is very simple to use. It even offers both session and token based auth which is fairly easily.
  - From the docs rolling out an OAuth2 seems to be straight forward as well.
### Deployment
- Yet to be implemented
### The Future
- As I learn more about the web I'm excited to come back to this project and Django in general to see how the framework
works through it. 
#### potential features 
- integrating a dummy purchasing page 
- using a front end framework

