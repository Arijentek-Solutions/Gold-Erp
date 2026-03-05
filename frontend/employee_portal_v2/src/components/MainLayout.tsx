import React from 'react'
import { Sidebar } from './layout/Sidebar'
import { Header } from './layout/Header'
import { Outlet } from 'react-router-dom'

export function MainLayout() {
    const [sidebarCollapsed, setSidebarCollapsed] = React.useState(false)

    return (
        <div className="flex h-screen w-full overflow-hidden bg-[#05070a] text-white selection:bg-amber-400/30">
            {/* Ambient Glows */}
            <div className="fixed top-[-10%] left-[-10%] w-[40%] h-[40%] bg-amber-400/[0.03] blur-[120px] rounded-full pointer-events-none" />
            <div className="fixed bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/[0.03] blur-[120px] rounded-full pointer-events-none" />

            {/* Sidebar */}
            <Sidebar
                collapsed={sidebarCollapsed}
                onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
            />

            {/* Main Content */}
            <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
                <Header />
                <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
                    <Outlet />
                </div>
            </main>
        </div>
    )
}