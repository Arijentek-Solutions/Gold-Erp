# Zevar Employee Portal V2

A modern, premium React-based employee portal for Frappe/ERPNext with elegant UI/UX design.

## Features

### Design
- **Premium Dark Theme**: Elegant dark interface with amber/gold accents
- **Bento Grid Dashboard**: Compact, organized widget layout
- **Glass-morphism Cards**: Modern translucent card design with subtle borders
- **Smooth Animations**: Premium hover effects and transitions
- **Proper Alignment**: Clean spacing and grid system

### Integrated Systems
- **HRMS**: Leave management, attendance tracking, payroll info
- **Gameplan**: Task management integration
- **Helpdesk**: Support ticket management

### Widgets
1. **Clock Widget**: Real-time time tracking with check-in/out
2. **Attendance Summary**: Weekly attendance visualization
3. **Leave Balance**: Leave days tracking with breakdown
4. **Tasks Widget**: Gameplan task list with status
5. **Support Tickets**: Helpdesk ticket overview
6. **Quick Actions**: Fast access to common actions

## Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Routing**: React Router DOM
- **Icons**: Lucide React
- **UI Components**: Custom + Radix UI primitives

## Project Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx       # Collapsible navigation sidebar
│   │   └── Header.tsx        # Top header with user menu
│   ├── ui/
│   │   └── card.tsx          # Reusable card component
│   └── MainLayout.tsx        # Main app layout wrapper
├── pages/
│   └── Dashboard.tsx         # Bento grid dashboard
├── stores/
│   ├── authStore.ts          # Authentication state
│   ├── employeeStore.ts      # Employee & attendance data
│   ├── tasksStore.ts         # Gameplan tasks
│   └── helpdeskStore.ts      # Helpdesk tickets
├── types/
│   └── index.ts              # TypeScript types
├── utils/
│   └── frappe.ts             # Frappe API utilities
├── lib/
│   └── utils.ts              # Utility functions (cn, formatters)
├── App.tsx                   # Main app component
├── main.tsx                  # Entry point
└── index.css                 # Global styles + custom CSS
```

## Setup & Installation

### 1. Install Dependencies

```bash
cd frappe-bench/apps/zevar_core/frontend/employee_portal_v2
npm install
```

### 2. Development Server

```bash
npm run dev
```

The app will run at `http://localhost:8080`

### 3. Production Build

```bash
npm run build
```

Builds to `../zevar_core/public/employee_portal_v2`

## Frappe Integration

The portal integrates with the following Frappe apps:

### API Endpoints Used

**Attendance & Employee:**
- `zevar_core.api.attendance.get_current_employee`
- `zevar_core.api.attendance.get_today_checkin_status`
- `zevar_core.api.attendance.clock_in`
- `zevar_core.api.attendance.clock_out`

**HRMS:**
- `hrms.api.get_leave_balance_map`
- `hrms.api.get_leave_applications`

**Gameplan (Tasks):**
- `zevar_core.api.tasks.get_employee_tasks`
- `zevar_core.api.tasks.get_task_stats`

**Helpdesk:**
- `zevar_core.api.helpdesk.get_employee_tickets`
- `zevar_core.api.helpdesk.get_ticket_stats`

### Frappe Page Setup

To serve this portal from Frappe, create a new page in your app:

```python
# zevar_core/www/employee-portal-v2.py
import frappe

def get_context(context):
    context.no_cache = 1
    return context
```

```html
<!-- zevar_core/www/employee-portal-v2.html -->
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <title>Employee Portal</title>
    <link rel="stylesheet" href="/assets/zevar_core/employee_portal_v2/assets/index.css">
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/assets/zevar_core/employee_portal_v2/assets/index.js"></script>
</body>
</html>
```

## Customization

### Theme Colors

Edit the CSS variables in `src/index.css`:

```css
.dark {
  --background: 222 47% 6%;
  --primary: 45 93% 61%;  /* Amber/Gold */
  /* ... */
}
```

### Adding New Widgets

1. Create widget component in `src/pages/Dashboard.tsx`
2. Add to the Bento Grid layout
3. Connect to store if data is needed

### Sidebar Items

Edit the `navItems` array in `src/components/layout/Sidebar.tsx`:

```typescript
const navItems: NavItem[] = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  // Add new items here
]
```

## Key Design Principles

1. **Compact & Elegant**: Smaller widgets, tight spacing, premium feel
2. **Consistent Spacing**: 4px base unit, consistent gaps
3. **Subtle Borders**: Very light borders (`border-white/[0.06]`)
4. **Glass Effect**: Backdrop blur with translucent backgrounds
5. **Hover States**: Subtle brightness/contrast changes on hover

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## License

Proprietary - Zevar