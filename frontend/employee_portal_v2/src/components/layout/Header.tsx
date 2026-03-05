import React from 'react'
import { useAuthStore } from '@/stores/authStore'
import { getInitials } from '@/lib/utils'
import { Bell, Search, ChevronDown, LogOut, User, Moon, Lock } from 'lucide-react'
import { cn } from '@/lib/utils'

interface HeaderProps {
    className?: string
}

export function Header({ className }: HeaderProps) {
    const { user, logout } = useAuthStore()
    const [isMenuOpen, setIsMenuOpen] = React.useState(false)
    const menuRef = React.useRef<HTMLDivElement>(null)
    const initials = getInitials(user?.full_name || 'User')

    // Close menu when clicking outside
    React.useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setIsMenuOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    return (
        <header
            className={cn(
                'flex items-center justify-between px-6 py-3 border-b border-white/[0.06] bg-[#0a0c1a]/80 backdrop-blur-xl shrink-0',
                className
            )}
        >
            {/* Search */}
            <div className="relative max-w-md w-96 hidden md:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
                <input
                    type="text"
                    placeholder="Search..."
                    className="w-full pl-10 pr-4 py-2 bg-white/[0.03] border border-white/[0.06] rounded-lg text-sm text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-amber-400/20 focus:border-amber-400/30 transition-all"
                />
            </div>

            {/* Right Section */}
            <div className="flex items-center gap-4 ml-auto">
                {/* Notifications */}
                <button className="relative p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/[0.06] transition-colors">
                    <Bell className="w-5 h-5" />
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-amber-400 rounded-full" />
                </button>

                {/* User Menu */}
                <div className="relative" ref={menuRef}>
                    <button
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        className="flex items-center gap-3 pl-2 pr-3 py-1.5 rounded-xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.06] hover:border-white/[0.1] transition-all"
                    >
                        <div className="w-8 h-8 rounded-full bg-amber-400/10 flex items-center justify-center text-amber-400 font-bold text-xs">
                            {initials}
                        </div>
                        <div className="hidden sm:block text-left">
                            <p className="text-sm font-medium text-white leading-tight">
                                {user?.full_name || 'User'}
                            </p>
                            <p className="text-xs text-gray-500 leading-tight">
                                {user?.email || 'user@zevar.com'}
                            </p>
                        </div>
                        <ChevronDown
                            className={cn(
                                'w-4 h-4 text-gray-500 transition-transform duration-200',
                                isMenuOpen && 'rotate-180'
                            )}
                        />
                    </button>

                    {/* Dropdown */}
                    {isMenuOpen && (
                        <div className="absolute right-0 top-full mt-2 w-56 bg-[#111420] border border-white/[0.08] rounded-xl shadow-2xl py-2 z-50">
                            <div className="px-4 py-3 border-b border-white/[0.06] mb-1">
                                <p className="text-white font-medium text-sm">{user?.full_name || 'User'}</p>
                                <p className="text-xs text-gray-500 mt-0.5">{user?.email || 'user@zevar.com'}</p>
                            </div>

                            <button className="w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-white/[0.04] transition-colors flex items-center gap-3 text-sm">
                                <User className="w-4 h-4" />
                                Profile
                            </button>

                            <button className="w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-white/[0.04] transition-colors flex items-center justify-between text-sm">
                                <div className="flex items-center gap-3">
                                    <Moon className="w-4 h-4" />
                                    Dark Mode
                                </div>
                                <div className="w-8 h-4 bg-amber-400/20 rounded-full relative flex items-center">
                                    <div className="w-3 h-3 bg-amber-400 rounded-full absolute right-0.5" />
                                </div>
                            </button>

                            <button className="w-full text-left px-4 py-2.5 text-gray-400 hover:text-white hover:bg-white/[0.04] transition-colors flex items-center gap-3 text-sm">
                                <Lock className="w-4 h-4" />
                                Change Password
                            </button>

                            <div className="h-px w-full bg-white/[0.06] my-1" />

                            <button
                                onClick={logout}
                                className="w-full text-left px-4 py-2.5 text-red-400 hover:text-red-300 hover:bg-red-400/10 transition-colors flex items-center gap-3 text-sm"
                            >
                                <LogOut className="w-4 h-4" />
                                Logout
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header>
    )
}