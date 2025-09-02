# Hifzly – A Personalised Qur’an Memorisation Planner
#### [Video Demo](https://www.youtube.com/watch?v=eZeSXE0ZX70)
#### Description:

**Hifzly** is a custom-built web app designed to help users memorise the Qur’an in a structured, efficient, and personalised way. It generates day-by-day memorisation schedules based on the user’s preferences — including start point, daily ayah goal, and whether revision should be included — and presents it through a minimalist dashboard that prioritises ease of use.

The key motivation behind Hifzly was to remove the guesswork and lack of structure that often leads to inconsistency in Hifz (Qur’an memorisation). Many students and adults struggle to maintain progress due to scattered routines or difficulty knowing where to start. Hifzly solves this by automating the entire planning process.

---

## 🔍 How It Works

Once a user registers and logs in, they are prompted to create a personalised plan. They can select:

- **Starting Surah** (from a dropdown of all 114 Surahs)
- **Starting Ayah number**
- **Number of Ayahs per day**
- **Whether to include built-in revision**

Based on these inputs, the app generates a unique Hifz plan stored in the SQLite database. The dashboard displays each day’s lesson, tracks whether it’s complete, and intelligently includes revision if selected.

All data is persistent — so users can leave and come back to their current plan at any time.

---

## 🧾 File Breakdown and Roles

Below is an in-depth explanation of the core files and what each contributes to the system:

### `app.py`
This is the main Flask application file. It contains:

- Route definitions (`/`, `/login`, `/register`, `/form`, `/dashboard`, etc.)
- Session management via Flask's built-in `session` system
- Plan generation logic using helper functions
- SQL queries to store and retrieve user plans and progress
- Plan overwrite mechanism (users can regenerate plans anytime)

### `helpers.py`
This contains core logic for generating the Hifz plan based on user input. It:

- Validates Qur’anic range (ensuring the plan doesn’t go beyond 6236 ayahs)
- Generates the day-by-day ayah breakdown
- Adds revision lines if requested
- Converts JSON-style dictionaries into data suitable for SQL insertion

We chose to separate this logic for cleanliness and reusability.

### `schema.sql`
Defines the structure of the SQLite database. It includes:

- `users` table: Stores `id`, `email`, and password hash
- `plans` table: Stores individual lessons with day number, start and end ayahs, revision ayahs, and a `completed` Boolean (stored as `0` or `1`)

The structure is intentionally simple to keep performance fast and avoid relational overhead.

### `templates/`
Uses Flask’s Jinja2 engine for templating:

- `layout.html`: Shared base template with navigation, styling, and hero design
- `index.html`: Marketing landing page with call-to-action buttons
- `form.html`: Plan creation form using dropdowns and input fields
- `dashboard.html`: Displays the active plan day-by-day, allowing users to tick off lessons
- `login.html` and `register.html`: Handle user authentication flow

### `static/`
Contains Tailwind CSS builds and optional JavaScript for interactions. Tailwind was chosen for its utility-first classes and fast prototyping.

---

## 💡 Feature Deep Dive

### ✅ Customised Plan Generation
Rather than offering a fixed memorisation approach, Hifzly supports starting from *any* Surah and ayah. This allows for maximum flexibility — from Juz Amma beginners to users revising from Baqarah or further into the Qur’an.

The plan is generated instantly after form submission and stored securely under the user’s ID.

### 🔁 Built-in Revision (Optional)
When selected, Hifzly automatically adds revision ayahs from the previous day or two. This was implemented by adjusting the lesson generation logic to insert additional lines referencing previous ranges.

### 🗂️ Completion Tracking
Each day has a "Mark as complete" button that triggers an update to the `plans` table. The `completed` field is a Boolean represented by `0` (incomplete) or `1` (complete). This enables future visual elements like streaks, progress bars, or motivational messages.

### 📖 Start Anywhere Support
Users are not limited to standard progression through the Qur’an. Hifzly lets you start at Surah 1 or Surah 114, with any ayah range, making it ideal for revision, test preparation, or specific Juz targeting.

### 🔐 Authentication
Users register with an email and password, stored securely with Werkzeug's hashing system. Sessions ensure only the logged-in user can access their data.

---

## 🧠 Design Philosophy and Decisions

### Minimalism First
We intentionally kept the UI and UX minimal: clean forms, responsive design, and zero distractions. The dashboard contains only what the user needs — their current lesson, a completion checkbox, and access to their full plan.

### Instant Plan Replacement
Instead of adding complexity with multiple concurrent plans, Hifzly uses an overwrite model. Generating a new plan deletes the old one. This makes for a smooth, focused experience and simplifies backend queries.

### SQLite Simplicity
We used SQLite due to its simplicity, speed, and compatibility with CS50’s environment. Although not scalable for production, it was ideal for a single-user prototype.

---

## 🚧 Future Roadmap

This MVP lays the foundation for significantly more features, including:

- **Audio Playback**
  Each day's ayahs will be playable from integrated Qur'an recitations.

- **AI Recitation Feedback**
  Users will recite into their mic, and AI will evaluate fluency and tajweed accuracy.

- **Statistics Dashboard**
  Streaks, time spent, accuracy rate, and estimated completion dates.

- **Multi-Plan Support**
  Let users manage multiple memorisation goals simultaneously.

- **Progress Export + Reminders**
  Daily reminders, .pdf export of current plans, and mobile PWA support.

---

## 🎓 Project Summary

Hifzly was built as a final project for CS50, combining everything I’ve learned this year: backend logic, SQL queries, user authentication, frontend development, API thinking, and product design. It represents not just a working tool, but a vision for what structured Islamic learning can look like when powered by software.

