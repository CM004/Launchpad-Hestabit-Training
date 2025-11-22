# UI Component Library Documentation

## Overview

This is a lightweight UI component library I built with **Tailwind CSS** for Next.js. All components are small, composable, and simple so I can easily reuse and override styles whenever needed.

### Components I've Built

* **Button** — Action buttons with size and type variants
* **Input** — Form input fields with full prop forwarding
* **Card** — Content container with optional icon and header
* **Badge** — Status indicator with color variants
* **Modal** — Overlay dialog for focused content
* **DataTable** — Small control/header block I use inside cards (project-specific)

---

## How to Import

I'm using the project alias (`@`) 

```jsx
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Modal from "@/components/ui/Modal";
import DataTable from "@/components/ui/DataTable";
```

If you don't have aliases set up, just use relative paths:

```jsx
import Button from "../components/ui/Button";
```

---

## Button

**File:** `/components/ui/Button.jsx`

### Props

* `size` ("sm" | "lg") — default: `sm` — controls padding/text size
* `type` ("primary" | "secondary" | "basic" | "delete") — default: `primary` — visual variant
* `className` (string) — additional Tailwind classes to append
* `onClick` (function) — click handler
* `children` (ReactNode)


### Usage

```jsx
<Button size="sm" type="primary">Save</Button>
<Button size="lg" type="delete" className="ml-2">Delete</Button>
<Button type="basic" onClick={() => console.log('clicked')}>Cancel</Button>
```

---

## Input

**File:** `/components/ui/Input.jsx`

### Props

* `type` (string) — default: `text`
* `placeholder` (string)
* `value` (string) — controlled value
* `onChange` (function)
* `className` (string)
* `...rest` — forwarded attributes

### Usage

```jsx
<Input placeholder="Search..." className="max-w-sm" />
<Input type="email" placeholder="Email" value={email} onChange={(e)=>setEmail(e.target.value)} />
```

---

## Card

**File:** `/components/ui/Card.jsx`

### Props

* `title` (string) — header text (optional)
* `icon` (ReactNode) — optional icon element
* `content` (string) — short description (optional)
* `className` (string) — additional classes for the card wrapper
* `children` (ReactNode)


### Usage

```jsx
<Card title="Revenue" content="$12,345">
  <Button size="sm">View Details</Button>
</Card>

<Card title="Area Chart Example" icon={<FaChartArea />} className="bg-white" >
  <div className="h-64 w-full">
    <AreaChart />
  </div>
</Card>
```

---

## Badge

**File:** `/components/ui/Badge.jsx`

### Props

* `color` ("red" | "green" | "blue" | "yellow" | "gray") — default `blue`
* `className` (string)
* `children` (ReactNode)

### Usage

```jsx
<Badge>Default</Badge>
<Badge color="green">Active</Badge>
```

---

## Modal

**File:** `/components/ui/Modal.jsx`

### Props

* `isOpen` (boolean) — show/hide
* `onClose` (function)
* `title` (string)
* `children` (ReactNode)

### Usage

```jsx
const [open,setOpen] = useState(false);
<Button onClick={()=>setOpen(true)}>Open</Button>
<Modal isOpen={open} onClose={()=>setOpen(false)} title="Confirm">
  <p>Do you want to proceed?</p>
</Modal>
```

---

## DataTable (UI header + controls)

**File:** `/components/ui/DataTable.jsx`

This is a small, layout-only component I use inside cards to provide the table header and controls (show entries, search input). 

### Usage

I wrap it in a Card. For a flush look (no left/right/bottom gutters), I use negative margins on the wrapper div.

Example:

```jsx
<Card title="Data Table" icon={<FaTable />} className="bg-gray-300">
  <div className="-mx-4 -mb-4 -my-4">
    <DataTable />
  </div>
</Card>
```

---

## Charts (Area / Bar)

Charts are client components (I'm using Chart.js via `react-chartjs-2`). Important rules I follow:

* Chart files are marked with `"use client"` because they use hooks and `window`-dependent libs


### Example Usage

```jsx
<Card title="Area Chart Example" icon={<FaChartArea />} className="bg-purple-600">
  <div className="h-64 flex justify-center bg-white">
    <AreaChart />
  </div>
</Card>
```

* I keep primitives small and prefer composition over large props lists
* `className` always comes last so I can override any default styles
