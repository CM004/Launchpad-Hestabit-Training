# HTML5 Learnings — README

## Overview

This README summarizes what we covered: **HTML5 page structure**, **semantic tags**, **metadata**, **forms & validation**, **accessibility basics (ARIA, `alt`, `tabindex`)**, **media & canvas**, and important **practical rules** and examples. Everything shown uses **pure HTML** unless noted.

---

# 1. Page structure (HTML5)

A modern HTML5 document uses semantic high-level skeleton:

```html
<!doctype html>
<html lang="en">
<head> ... metadata ... </head>
<body>
  <header> site header, logo, nav </header>
  <main> primary content </main>
  <aside> complementary content / sidebar </aside>
  <footer> site footer, copyright </footer>
</body>
</html>
```

Notes:

* Use **one** `<main>` per page. It contains the page’s primary content.
* Use `<header>` and `<footer>` for page or section headers/footers (both can appear inside articles/sections too).

---

# 2. Metadata (head)

Common `<head>` elements:

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Your page title</title>
<meta name="description" content="Short description">
<link rel="icon" href="favicon.ico">
```

Purpose:

* `charset` sets document encoding. Use UTF-8.
* `viewport` makes pages responsive on mobile.
* `title` appears in browser tabs and search results.
* Use `meta` description for SEO summaries.

---

# 3. Semantic tags and when to use them

* `<header>` – introductory content for a page or section.
* `<nav>` – navigation links (wrap a `<ul>` of `<li>` links). Use `aria-label` when multiple navs exist.
* `<main>` – main content (only one per page).
* `<section>` – a thematic grouping with (preferably) a heading. Use it when the group has a natural heading, e.g., "Latest Posts".
* `<article>` – a self-contained item (blog post, news story, comment) that could be syndicated.
* `<aside>` – tangential content like sidebars, author bio, ads.
* `<footer>` – footer of a page or section.
* `<figure>` + `<figcaption>` – image + caption pair.
* `<address>` – contact information.
* `<blockquote>`, `<cite>` – quoted content and its citation.

**Rule of thumb:** If a block should have its own heading, `section` is a good fit. If the block is a standalone item, use `article`.

---

# 4. Navigation & horizontal lists

Semantic navbar structure:

```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="#home">Home</a></li>
    <li><a href="#about">About</a></li>
  </ul>
</nav>
```

Pure-HTML horizontal nav (no CSS): use inline anchors inside `<nav>`:

```html
<nav>
  <a href="#home">Home</a> | <a href="#about">About</a>
</nav>
```

HTML alone cannot reliably force block-level elements (like `<h1>` and `<nav>`) to sit on the same line; use CSS or a table if you must keep them on one visual line without CSS.

---

# 5. Images, figures, and captions

* Use `alt` attributes for every meaningful image: `alt="Description"`.
* Group image + caption with `<figure>` and `<figcaption>`.

```html
<figure>
  <img src="mountain.jpg" alt="Snowy mountain and pine tree">
  <figcaption>Figure: mountain landscape.</figcaption>
</figure>
```

If you must display captions below images in a horizontal marquee (HTML-only), keep image+caption inline by wrapping both in an inline container such as `<a>` and use `<br>` or `<span>` (avoid block elements like `<figure>` inside marquee if it causes vertical stacking).

---

# 6. Forms, inputs, select, validation

Basic form elements:

```html
<form action="/subscribe" method="post">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required>

  <label for="country">Country</label>
  <select id="country" name="country">
    <option value="us">United States</option>
    <option value="uk">United Kingdom</option>
  </select>

  <button type="submit">Subscribe</button>
</form>
```

Validation & attributes:

* `required` enforces presence.
* `type="email"` does basic email format checking.
* `min`, `max`, `pattern`, `step` for numeric / pattern validation.
* Use `novalidate` on form to disable browser validation if needed.

Use `<fieldset>` + `<legend>` to group fields with an automatic border (handy when no CSS allowed).

---

# 7. Media: `audio`, `video`, `canvas`

* Embed video and audio semantically:

```html
<video controls width="640">
  <source src="video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

<audio controls>
  <source src="audio.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
```

* Use `<canvas>` for drawing; include fallback content for accessibility.

---

# 8. Accessibility basics

* Always include `alt` text for images.
* Use `<label for="id">` to connect labels and inputs.
* Use ARIA only when necessary: `role`, `aria-label`, `aria-labelledby`, `aria-describedby`.
* Use `tabindex="0"` to make non-focusable elements focusable when needed (avoid overuse).
* Use `aria-current="page"` for active nav link.
* Use semantic tags first; ARIA should augment semantics, not replace them.

---

# HTML Learnings — Notes & Cheat Sheet

This document summarizes all the key HTML concepts, tags, and techniques we covered so far, with examples and explanations.

---

# 9. 🧱 Basic HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Website</title>
</head>
<body>
  <!-- Your page content -->
</body>
</html>
```

### Key Elements

* `<head>` — metadata, links to styles/scripts, and the page title.
* `<body>` — main visible content.
* `<!DOCTYPE html>` — tells the browser you’re using HTML5.

---

## 🧭 Structure and Layout Tags

| Tag         | Purpose                                            |
| ----------- | -------------------------------------------------- |
| `<header>`  | Top section, usually includes logo or navigation   |
| `<nav>`     | Defines navigation links                           |
| `<main>`    | Main content area                                  |
| `<section>` | Groups related content                             |
| `<article>` | Represents self-contained content like a blog post |
| `<footer>`  | Bottom section of a page or article                |

---

## 📄 Text Formatting Tags

| Tag             | Description                                  |
| --------------- | -------------------------------------------- |
| `<h1>` – `<h6>` | Headings; `<h1>` is largest, `<h6>` smallest |
| `<p>`           | Paragraph of text                            |
| `<em>`          | Emphasized text (italic by default)          |
| `<strong>`      | Important text (bold by default)             |
| `<br>`          | Line break                                   |
| `<small>`       | Smaller text size                            |
| `<hr>`          | Horizontal rule/divider                      |

💡 **Tip:** Headings are block elements; they start on new lines.

---

## 🧩 Buttons and Links

```html
<button type="submit">Submit</button>
<button type="button">Click Me</button>
<a href="file.pdf" download><button type="button">Download</button></a>
```

### Button Types

* `type="button"` → normal clickable button
* `type="submit"` → submits form data
* `type="reset"` → resets a form

---

## 🖼️ Images and Accessibility

```html
<img src="image.jpg" alt="Description of the image" width="400" height="250">
```

* `alt` — text shown if the image fails to load, and read by screen readers.
* `width` / `height` — control dimensions.
* Always include an `alt` for accessibility.

---

## 🧱 Fieldset and Legend

Used to group related form elements visually and semantically.

```html
<fieldset>
  <legend>Subscribe</legend>
  <h3>Newsletter</h3>
  <button type="button">Subscribe</button>
</fieldset>
```

`<fieldset>` is a block element — so it appears on its own line. You can control its width using inline style:

```html
<fieldset style="width:50%;">
```

---

## 🧭 Navigation Example (No CSS)

```html
<header style="display:flex; justify-content:space-between; align-items:center;">
  <h1>My Website</h1>
  <nav>
    <a href="#home">Home</a>
    <a href="#about">About</a>
    <a href="#services">Services</a>
    <a href="#contact">Contact</a>
  </nav>
</header>
```

Avoid using too many `&nbsp;` for spacing — use layout techniques instead.

---

## 📦 Tables in HTML

Tables are used to display data in a grid of rows and columns.

### Basic Table Structure

```html
<table border="1">
  <tr>
    <th>Name</th>
    <th>Age</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alice</td>
    <td>25</td>
    <td>USA</td>
  </tr>
  <tr>
    <td>Bob</td>
    <td>30</td>
    <td>UK</td>
  </tr>
</table>
```

### Tags Explained

| Tag       | Description                                    |
| --------- | ---------------------------------------------- |
| `<table>` | Defines the table container                    |
| `<tr>`    | Table row                                      |
| `<td>`    | Table data cell                                |
| `<th>`    | Table header cell (bold + centered by default) |

### Table Auto Layout Algorithm

The **auto layout algorithm** defines how column widths are calculated in a table without CSS rules like `table-layout: fixed;`.

* The browser analyzes the content in each column to decide width.
* The widest cell in a column defines that column’s width.
* The table expands or shrinks depending on its content and parent container.
* You can control it manually with CSS property:
  `table { table-layout: fixed; width: 100%; }`  → evenly distributes columns.

Without CSS, HTML’s default layout is `table-layout: auto` — responsive but unpredictable for uneven data.

---

## ⚙️ ARIA Labels and Accessibility

| Attribute         | Description                                    |
| ----------------- | ---------------------------------------------- |
| `aria-label`      | Provides an accessible name for screen readers |
| `aria-labelledby` | Links an element to a visible label            |
| `tabindex`        | Controls keyboard navigation order             |

Example:

```html
<nav aria-label="Main Navigation">
  <a href="#home" tabindex="1">Home</a>
  <a href="#about" tabindex="2">About</a>
</nav>
```

---

## 🧠 Extra Notes

* Block elements (like `<div>`, `<h1>`, `<p>`, `<section>`) take full width by default.
* Inline elements (like `<a>`, `<em>`, `<strong>`, `<img>`) stay in line with text.
* Use `<br>` for small breaks, not for layout.
* Avoid too many non-breaking spaces (`&nbsp;`).
* Always use semantic HTML for better accessibility and SEO.

---

**End of README — HTML Learnings Summary**

---

# 10. HTML-only layout tricks & limitations

**What you can do in pure HTML:**

* Use `<table>` to create reliable multi-column layouts (works everywhere) — useful when CSS is not allowed.
* Use `<fieldset>` to get a bordered box for grouping content.
* Use inline elements (`<a>`, `<span>`) and `&nbsp;` to add spacing.
* Use `align` attributes (deprecated but still supported) and HTML attributes like `width` on images and table cells.

**What HTML cannot do (without CSS/JS):**

* Precise layout control (margins, padding, flex/grid, exact positioning).
* Smooth animations, interactive controls, and event-driven behaviors (needs JavaScript).
* Modern responsive fine-tuning and visual styling — CSS is required.

**Marquee notes:** `<marquee>` is deprecated. It still works in many browsers but is non-standard and not accessible.

---

# Quick Reference: Useful tags & attributes

* Structural: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`
* Grouping: `<figure>`, `<figcaption>`, `<fieldset>`, `<legend>`, `<details>`, `<summary>`
* Forms: `<form>`, `<label>`, `<input>`, `<select>`, `<option>`, `<textarea>`, `<button>`
* Media: `<img>`, `<audio>`, `<video>`, `<canvas>`
* Accessibility attributes: `alt`, `aria-label`, `aria-labelledby`, `aria-describedby`, `role`, `tabindex`, `aria-current`

---

# Final tips

* Favor semantic tags over generic `<div>` where appropriate.
* Keep HTML valid and accessible: proper heading order, labels, alt text, and roles.
* Use HTML layout tricks (tables, fieldsets) only when CSS is not allowed.
* Learn basic CSS next — it will unlock proper visual layout and responsive design while keeping semantic HTML intact.

---
