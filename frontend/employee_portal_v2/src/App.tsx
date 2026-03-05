import React, { Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { MainLayout } from '@/components/MainLayout'
import Dashboard from '@/pages/Dashboard'
import { useAuthStore } from '@/stores/authStore'

// Simple fallback loader
function PageLoader() {
    return (
        <div className="h-screen w-full flex items-center justify-center bg-[#05070a]">
            <div className="flex flex-col items-center gap-4">
                <div className="w-8 h-8 border-2 border-amber-400 border-t-transparent rounded-full animate-spin" />
                <p className="text-gray-400 text-sm">Loading...</p>
            </div>
        </div>
    )
}

// Simple placeholder pages
function TasksPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4 text-white">Tasks</h1>
            <p className="text-gray-400">Manage your tasks and track progress.</p>
        </div>
    )
}

function AttendancePage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4 text-white">Attendance</h1>
            <p className="text-gray-400">View your attendance history and clock in/out.</p>
        </div>
    )
}

function LeavePage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4 text-white">Leave Management</h1>
            <p className="text-gray-400">Apply for leave and view your leave balance.</p>
        </div>
    )
}

function ExpensePage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4 text-white">Expense Claims</h1>
            <p className="text-gray-400">Submit and track your expense claims.</p>
        </div>
    )
}

function PayrollPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4 text-white">Payroll</h1>
            <p className="text-gray-400">View your payslips and salary information.</p>
        </div>
    )
}

function SupportPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4 text-white">Support</h1>
            <p className="text-gray-400">Get help and raise support tickets.</p>
        </div>
    )
}

function OpenDeskPage() {
    React.useEffect(() => {
        window.location.href = '/app'
    }, [])
    return null
}

function AppContent() {
    const { fetchUser, isLoading } = useAuthStore()

    React.useEffect(() => {
        console.log('App mounted, fetching user...')
        fetchUser().catch(err => console.error('Failed to fetch user:', err))
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    if (isLoading) {
        return <PageLoader />
    }

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<MainLayout />}>
                    <Route index element={<Dashboard />} />
                    <Route path="tasks" element={<TasksPage />} />
                    <Route path="attendance" element={<AttendancePage />} />
                    <Route path="leave" element={<LeavePage />} />
                    <Route path="expense" element={<ExpensePage />} />
                    <Route path="payroll" element={<PayrollPage />} />
                    <Route path="support" element={<SupportPage />} />
                    <Route path="open-desk" element={<OpenDeskPage />} />
                </Route>
            </Routes>
        </BrowserRouter>
    )
}

function App() {
    return (
        <Suspense fallback={<PageLoader />}>
            <AppContent />
        </Suspense>
    )
}

export default App