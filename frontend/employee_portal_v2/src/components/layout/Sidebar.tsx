import React from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/stores/authStore'
import { getInitials } from '@/lib/utils'
import {
    LayoutDashboard,
    CheckCircle2,
    Calendar,
    Umbrella,
    Receipt,
    Wallet,
    HelpCircle,
    ExternalLink,
    ChevronLeft,
    Building2,
} from 'lucide-react'

interface NavItem {
    to: string
    icon: React.ElementType
    label: string
    badge?: number
}

const navItems: NavItem[] = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/tasks', icon: CheckCircle2, label: 'Tasks' },
    { to: '/attendance', icon: Calendar, label: 'Attendance' },
    { to: '/leave', icon: Umbrella, label: 'Leave' },
    { to: '/expense', icon: Receipt, label: 'Expense' },
    { to: '/payroll', icon: Wallet, label: 'Payroll' },
    { to: '/support', icon: HelpCircle, label: 'Support' },
    { to: '/open-desk', icon: ExternalLink, label: 'Open Desk' },
]

interface SidebarProps {
    collapsed: boolean
    onToggle: () => void
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
    const location = useLocation()
    const { user } = useAuthStore()
    const initials = getInitials(user?.full_name || 'User')

    return (
        <aside
            className={cn(
                'flex flex-col bg-[#0a0c1a] border-r border-white/[0.06] transition-all duration-300 ease-in-out z-20',
                collapsed ? 'w-20' : 'w-64'
            )}
        >
            {/* Logo */}
            <div className={cn('p-4', collapsed ? 'px-3' : 'px-4')}>
                <div className="flex items-center gap-3 bg-[#111420] p-2.5 rounded-xl border border-white/[0.06]">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center shrink-0">
                        <Building2 className="w-4 h-4 text-black" />
                    </div>
                    {!collapsed && (
                        <span className="font-bold text-white tracking-wide text-sm">Zevar</span>
                    )}
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 px-3 space-y-1 overflow-y-auto custom-scrollbar">
                {navItems.map((item) => {
                    const Icon = item.icon
                    const isActive = location.pathname === item.to

                    return (
                        <NavLink
                            key={item.to}
                            to={item.to}
                            className={cn(
                                'flex items-center rounded-xl transition-all duration-200 group relative',
                                isActive
                                    ? 'bg-[#111822] text-amber-400'
                                    : 'text-gray-400 hover:text-white hover:bg-white/[0.04]',
                                collapsed ? 'justify-center px-2 py-3' : 'justify-between px-3 py-2.5'
                            )}
                        >
                            <div className="flex items-center gap-3">
                                <Icon className="w-[18px] h-[18px] shrink-0" />
                                {!collapsed && (
                                    <span className="text-sm font-medium">{item.label}</span>
                                )}
                            </div>
                            {isActive && !collapsed && (
                                <div className="w-1 h-1 rounded-full bg-amber-400" />
                            )}
                        </NavLink>
                    )
                })}
            </nav>

            {/* Collapse Toggle */}
            <div className="p-3">
                <button
                    onClick={onToggle}
                    className={cn(
                        'w-full py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/[0.06] transition-all duration-200 flex items-center border border-white/[0.06]',
                        collapsed ? 'justify-center px-2' : 'justify-center gap-2 px-4'
                    )}
                >
                    <ChevronLeft
                        className={cn(
                            'w-4 h-4 transition-transform duration-300',
                            collapsed && 'rotate-180'
                        )}
                    />
                    {!collapsed && <span className="text-xs font-medium">Collapse</span>}
                </button>
            </div>

            {/* User Profile Mini */}
            <div className={cn('p-3 border-t border-white/[0.06]', collapsed && 'px-2')}>
                <div
                    className={cn(
                        'flex items-center gap-3 p-2 rounded-xl bg-white/[0.02] border border-white/[0.06]',
                        collapsed && 'justify-center'
                    )}
                >
                    <div className="w-8 h-8 rounded-full bg-amber-400/10 flex items-center justify-center text-amber-400 font-bold text-xs shrink-0">
                        {initials}
                    </div>
                    {!collapsed && (
                        <div className="min-w-0">
                            <p className="text-sm font-medium text-white truncate">
                                {user?.full_name || 'User'}
                            </p>
                            <p className="text-xs text-gray-500 truncate">
                                {user?.email || 'user@zevar.com'}
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </aside>
    )
}