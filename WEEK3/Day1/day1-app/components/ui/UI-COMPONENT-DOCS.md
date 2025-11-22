# UI Component Library Documentation

## Overview

This is a lightweight UI component library built with **Tailwind CSS** for Next.js applications. The library includes five core components designed to be simple, composable, and flexible.

### Components Included
- **Button** - Action buttons with size and type variants
- **Input** - Form input fields with full prop forwarding
- **Card** - Content containers with optional icons and actions
- **Badge** - Status indicators with color variants
- **Modal** - Overlay dialogs for focused content

---

```

### Importing Components

Using the Next.js default `@/` alias:
```jsx
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Modal from "@/components/ui/Modal";
```

Or with relative paths if alias is not configured:
```jsx
import Button from "../components/ui/Button";
```

---

### Button

**File**: `/components/ui/Button.jsx`

#### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | `"sm"` \| `"lg"` | `"sm"` | Button size variant |
| `type` | `"primary"` \| `"basic"` \| `"delete"` | `"primary"` | Button style variant |
| `className` | `string` | - | Additional Tailwind classes |
| `onClick` | `function` | - | Click event handler |
| `children` | `ReactNode` | - | Button content |

#### Usage
```jsx
<Button size="sm" type="primary">Save</Button>
<Button size="lg" type="delete" className="ml-2">Delete</Button>
<Button type="basic" onClick={() => console.log('clicked')}>Cancel</Button>
```

---

### Input

**File**: `/components/ui/Input.jsx`

#### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `string` | `"text"` | HTML input type |
| `placeholder` | `string` | - | Placeholder text |
| `value` | `string` | - | Controlled input value |
| `onChange` | `function` | - | Change event handler |
| `className` | `string` | - | Additional Tailwind classes |
| `...rest` | `any` | - | All standard input attributes |

#### Usage
```jsx
<Input placeholder="Search..." className="max-w-sm" />
<Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
<Input type="password" placeholder="Password" />
```
---

### Card

**File**: `/components/ui/Card.jsx`

#### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | - | Card header title |
| `content` | `string` | - | Short description text |
| `icon` | `ReactNode` | - | Optional icon (e.g., from `react-icons`) |
| `className` | `string` | - | Additional classes for card wrapper |
| `children` | `ReactNode` | - | Custom content inside card |

#### Usage
```jsx
<Card title="Revenue" content="$12,345">
  <Button size="sm">View Details</Button>
</Card>

<Card 
  title="Users" 
  icon={<FaUser />} 
  className="bg-blue-100"
>
  <p>Active: 1,024</p>
</Card>

<Card title="Analytics">
  <div className="space-y-2">
    <Badge color="green">Live</Badge>
    <p className="text-gray-600">Real-time data</p>
  </div>
</Card>
```

---

### Badge

**File**: `/components/ui/Badge.jsx`

#### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `color` | `"red"` \| `"green"` \| `"blue"` \| `"yellow"` \| `"gray"` | `"blue"` | Badge color variant |
| `className` | `string` | - | Additional Tailwind classes |
| `children` | `ReactNode` | - | Badge content |

#### Usage
```jsx
<Badge>Default</Badge>
<Badge color="green">Active</Badge>
<Badge color="red" className="px-3 py-1">Error</Badge>
<Badge color="yellow">Pending</Badge>
```

---

### Modal

**File**: `/components/ui/Modal.jsx`

#### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | - | Controls modal visibility |
| `onClose` | `function` | - | Called when modal should close |
| `title` | `string` | - | Modal header title |
| `children` | `ReactNode` | - | Modal body content |

#### Usage
```jsx
const [open, setOpen] = useState(false);

<Button onClick={() => setOpen(true)}>Open Modal</Button>

<Modal 
  isOpen={open} 
  onClose={() => setOpen(false)} 
  title="Confirmation"
>
  <p>Are you sure you want to proceed?</p>
  <div className="mt-4 flex gap-2">
    <Button type="primary" onClick={() => setOpen(false)}>Confirm</Button>
    <Button type="basic" onClick={() => setOpen(false)}>Cancel</Button>
  </div>
</Modal>
```
---