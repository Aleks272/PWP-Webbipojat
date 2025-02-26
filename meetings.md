# Meetings notes

## Meeting 1.
* **DATE:** 28.1.2025
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

Overall, the plan looks good and realistic. Improvements to wording of the text and diagram were discussed (these are included in action points below). The amount of resources (must be at least 5 according to [project requirements](https://lovelace.oulu.fi/ohjelmoitava-web/pwp-spring-2025/pwp-project-work-assignment/#restful-api)) for the API could end up being too low with the current description of users and lists. This should be taken into account in the implementation phase.

The process of adding movies and series to the database of the API was discussed. Using some external service here could be possible, from which the movies and series would be picked when adding a new entry to the user's list. However, this it not a mandatory feature.

### Action points
*List here the actions points discussed with assistants*
- Explain APIs reasoning more briefly, what it does, how it does it and why. aka motivation behind the project.
- Clarify the diagram and logic
- Improve description, is this mobile app, webapp? (Done)
- Find the link which justifies that client is using the API. (It actually read on the page behind on the link.)




## Meeting 2.
* **DATE:** 12.2.2025
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

Database documentation looks good, models are well defined, but `Content` is missing the genre-field defined in the plan. Instead of having two tables for public and private movie lists, it could be better to just have one model for list and set a private/public specifier for every list.

### Action points
*List here the actions points discussed with assistants*

- Instead of having PublicList and PrivateList separately, save movie/series entries to one list and have a boolean value specifying whether the list is public or private.
- Update previous plans in wiki according to changes made in later stages of the project.
- Include genre-field in Content-database model



## Meeting 3.
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




## Meeting 4.
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




