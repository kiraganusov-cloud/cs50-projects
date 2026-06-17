# StudentSphere

#### Video Demo: (https://youtu.be/BSHU22D9aEc)

#### Description

StudentSphere is a Flask web application that gives high-school students a single place to connect with one another, share opportunities, build out a personal academic profile, and plan the milestones they want to hit before they graduate.
The idea grew out of a simple observation: information that matters to students — internships, club events, scholarship deadlines, and the small questions everyone is afraid to ask — tends to scatter across group chats, flyers, and word of
mouth. This project pulls that activity into one feed and surrounds it with the tools a student actually needs to stay organized over four years of high school.

At its core the app has three pillars. The first is a shared **post feed** where any logged-in user can publish a post tagged as an opportunity, an event, or a question, optionally attaching a location. Other students can reply to any post
through a threaded comment system, which turns the feed into an ongoing conversation rather than a static bulletin board. The second pillar is a personal **profile/account page**, where each student records their grade, SAT and ACT scores,
and a running list of courses, extracurriculars, and awards. The third is a four-year **planning dashboard** that lets students set goals for grades 9 through 12 so they can see the whole arc of their high-school career laid out at once.

#### Files

**`app.py`** is the heart of the project and contains every route. After configuring Flask, a filesystem-backed session, and a CS50 `SQL` connection to `project.db`, it defines the application's logic. The `/` route (named `main`) handles
both reading and writing the feed: a `GET` request loads every post newest-first, joins each one against the `users` table to attach an author username and emoji, and then runs a second query per post to gather its comments; a `POST` request
validates the four required fields and inserts a new post. The `/comment` route inserts a reply tied to a specific post and user. The `/account` and `/editprofile` and `/add_item` and `/delete_item` routes together manage the profile page —
reading the user's record and their categorized profile items, and updating scores, grade, or list entries. The `/planning`, `/addgoal`, and `/delete_goal` routes power the four-year dashboard, bucketing goals by grade level. Finally, `/
login`, `/logout`, and `/register` handle authentication using Werkzeug's password hashing so that plaintext passwords are never stored.

**`helpers.py`** holds two small but important utilities borrowed and adapted from CS50 Finance. `apology()` renders a friendly error page with an escaped message, and `login_required` is a decorator that redirects any unauthenticated visitor
to the login page. Wrapping nearly every route in `@login_required` is what keeps the app private to registered students.

**`project.db`** is the SQLite database. It defines five tables: `users` (credentials, an emoji avatar, grade, and test scores), `posts`, `comments`, `profile_items` (courses, extracurriculars, and awards distinguished by a `category`
column), and `dashboard_items` (planning goals keyed by `grade_level`). Foreign keys tie posts, comments, profile items, and goals back to the user who created them.

The **templates** folder holds the Jinja2/Bootstrap 5 views, all of which extend a common base. `layout.html` is that base: it loads Bootstrap and the stylesheet, defines the StudentSphere navbar, and switches the navigation links depending
on whether a user is logged in (Account and Planner when authenticated, Register and Log In when not). `main.html` renders the post feed — each post is a Bootstrap card showing the author, type, and location badges, its title and body, and
the thread of comments, with a reply box beneath. It also holds a floating "+" button that opens a modal containing the new-post form (type dropdown, location, title, and text). `account.html` builds the profile page: a header with the
username, grade, and SAT/ACT scores, three columns for courses, awards, and extracurriculars, and several modals for adding items or editing scores. It includes a small script that powers the "edit" modal, where clicking Grade, SAT, or ACT
sets a hidden category field and reveals the text input. `planning.html` lays out the four-year goal board as four grade columns (9th–12th), each goal expandable to reveal a delete button, plus an "Add a goal" modal driven by the same
button-to-hidden-field script. `login.html` and `register.html` are the authentication forms, and both (like every page) display flashed error messages. `apology.html` renders the fallback error page used by the `apology()` helper.

`styles.css` (in the **static** folder) supplies the app's identity: a light-green background, the two-tone orange-and-yellow "StudentSphere" wordmark, custom orange primary buttons and green secondary badges, and themed modals and focus
states. Keeping all of this in one stylesheet rather than scattering inline styles made the color scheme easy to adjust in a single place.

#### Design Choices

A few decisions are worth explaining. I chose to store post **type** as a free text column with a small set of expected values (`opportunity`, `event`, `question`) rather than splitting posts into separate tables. Three near-identical tables
would have meant three near-identical feeds, whereas one `posts` table with a type tag keeps the feed unified and makes future filtering trivial. Similarly, I collapsed courses, awards, and extracurriculars into a single `profile_items` table
separated by a `category` column instead of three tables, which let one pair of `add_item`/`delete_item` routes serve all of them.

I also deliberately left some schema headroom for features I planned but had not yet wired up. The `is_anonymous` flag on users, posts, and comments and the `completed` flag on dashboard goals exist in the database so that anonymous posting
and a check-off "done" state can be added without a migration. Finally, I used CS50's `SQL` library with parameterized queries throughout to guard against SQL injection, and filesystem sessions rather than signed cookies so that login state
survives more reliably during development.
