import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs))
}

export function formatDuration(hours: number): string {
    const h = Math.floor(hours)
    const m = Math.round((hours - h) * 60)
    return `${h}h ${m}m`
}

export function formatTime(date: string | Date): string {
    return new Date(date).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    })
}

export function formatDate(date: string | Date): string {
    return new Date(date).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    })
}

export function formatDateFull(date: string | Date): string {
    return new Date(date).toLocaleDateString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric'
    })
}

export function getInitials(name: string): string {
    return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .substring(0, 2)
        .toUpperCase()
}

export function getRelativeTime(date: string | Date): string {
    const now = new Date()
    const then = new Date(date)
    const diffInSeconds = Math.floor((now.getTime() - then.getTime()) / 1000)

    if (diffInSeconds < 60) return 'just now'
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
    return formatDate(date)
}

export function getStatusColor(status: string): string {
    const colors: Record<string, string> = {
        'Open': 'bg-blue-500',
        'In Progress': 'bg-amber-500',
        'Done': 'bg-emerald-500',
        'Closed': 'bg-emerald-500',
        'Resolved': 'bg-emerald-500',
        'Pending': 'bg-amber-500',
        'Approved': 'bg-emerald-500',
        'Rejected': 'bg-red-500',
        'Canceled': 'bg-gray-500',
        'Backlog': 'bg-slate-500',
        'Todo': 'bg-blue-500',
        'High': 'bg-red-500',
        'Medium': 'bg-amber-500',
        'Low': 'bg-blue-500',
        'Urgent': 'bg-red-600',
    }
    return colors[status] || 'bg-gray-500'
}

export function calculatePercentage(value: number, total: number): number {
    if (total === 0) return 0
    return Math.min(100, Math.round((value / total) * 100))
}