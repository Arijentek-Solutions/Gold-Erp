import { useEffect, useState } from 'react'
import { useEmployeeStore } from '@/stores/employeeStore'
import { useTasksStore } from '@/stores/tasksStore'
import type { Task } from '@/types'
import { formatDuration } from '@/lib/utils'
import { Card } from '@/components/ui/card'
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels'
import {
    Clock,
    Calendar,
    CheckCircle2,
    FileText,
    Activity,
    User,
    MoreVertical,
} from 'lucide-react'

// Custom Resize Handle
const ResizeHandle = ({ direction = "horizontal" }) => {
    return (
        <PanelResizeHandle className={`flex items-center justify-center transition-colors hover:bg-amber-400/20 active:bg-amber-400/30 ${direction === 'horizontal' ? 'w-3' : 'h-3'}`}>
            <div className={`rounded-full bg-white/20 ${direction === 'horizontal' ? 'w-1 h-8' : 'h-1 w-8'}`} />
        </PanelResizeHandle>
    )
}

function ClockWidget() {
    const { attendance, clockIn, clockOut, isLoading } = useEmployeeStore()
    const [currentTime, setCurrentTime] = useState(new Date())

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000)
        return () => clearInterval(timer)
    }, [])

    const hours = currentTime.getHours()
    const minutes = currentTime.getMinutes()
    const isCheckedIn = attendance?.checked_in
    const totalHours = attendance?.total_hours_today || 0

    return (
        <Card className="h-full flex flex-col p-5 relative overflow-hidden group border-white/10 bg-[#111420]/80">
            <div className="absolute inset-0 bg-gradient-to-br from-amber-400/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="relative z-10 flex flex-col h-full">
                <div className="flex items-center justify-between mb-4">
                    <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                        <Clock className="w-3.5 h-3.5" />
                        Time Tracker
                    </span>
                    <div className={`w-2 h-2 rounded-full ${isCheckedIn ? 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.6)]' : 'bg-gray-500'}`} />
                </div>
                <div className="flex-1 flex flex-col items-center justify-center">
                    <div className="text-5xl font-bold tracking-tight font-mono text-white">
                        {hours.toString().padStart(2, '0')}:{minutes.toString().padStart(2, '0')}
                    </div>
                    <div className="text-sm text-gray-400 mt-2 font-medium">
                        {isCheckedIn ? `Checked In: ${formatDuration(totalHours)}` : 'Not checked in'}
                    </div>
                </div>
                <div className="flex gap-2 mt-6">
                    <button
                        onClick={clockIn}
                        disabled={isCheckedIn || isLoading}
                        className={`flex-1 py-3 justify-center rounded-xl text-sm font-bold transition-all ${isCheckedIn
                            ? 'bg-white/5 text-gray-500 cursor-not-allowed'
                            : 'bg-amber-400 text-black shadow-[0_0_15px_rgba(251,191,36,0.3)] hover:shadow-[0_0_20px_rgba(251,191,36,0.5)]'
                            }`}
                    >
                        Clock In
                    </button>
                    <button
                        onClick={clockOut}
                        disabled={!isCheckedIn || isLoading}
                        className={`flex-1 py-3 justify-center rounded-xl text-sm font-bold transition-all ${!isCheckedIn
                            ? 'bg-white/5 text-gray-500 cursor-not-allowed'
                            : 'bg-red-500/10 text-red-400 border border-red-500/20 hover:bg-red-500/20'
                            }`}
                    >
                        Clock Out
                    </button>
                </div>
            </div>
        </Card>
    )
}

function ProfileWidget() {
    const { employee } = useEmployeeStore()

    return (
        <Card className="h-full flex flex-col p-5 border-white/10 bg-[#111420]/80 group relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-amber-400/5 rounded-full blur-3xl" />
            <div className="relative z-10 flex flex-col h-full justify-between">
                <div>
                    <div className="flex items-center justify-between mb-4">
                        <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                            <User className="w-3.5 h-3.5" />
                            My Profile
                        </span>
                    </div>
                    <h3 className="text-xl font-bold text-white mb-1">{employee?.employee_name || "Employee"}</h3>
                    <p className="text-sm text-amber-400 font-medium">{employee?.designation || "Staff"}</p>
                </div>

                <div className="mt-6 pt-4 border-t border-white/5">
                    <p className="text-xs text-gray-500 uppercase font-semibold mb-2">Reporting To</p>
                    <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center text-blue-400 font-bold text-xs">RM</div>
                        <div>
                            <p className="text-sm text-white font-medium">{employee?.reports_to || "Reporting Manager"}</p>
                            <p className="text-xs text-gray-500">Manager</p>
                        </div>
                    </div>
                </div>
            </div>
        </Card>
    )
}

function TasksWidget() {
    const { tasks, fetchTasks } = useTasksStore()

    useEffect(() => {
        fetchTasks()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const pending = tasks.filter((t: Task) => t.status === 'Todo' || t.status === 'In Progress')

    return (
        <Card className="h-full flex flex-col p-5 border-white/10 bg-[#111420]/80">
            <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Pending Tasks
                </span>
                <span className="px-2 py-0.5 rounded-full bg-amber-400/10 text-amber-400 text-xs font-bold">
                    {pending.length}
                </span>
            </div>

            <div className="flex-1 overflow-y-auto pr-2 space-y-2 custom-scrollbar">
                {pending.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-2">
                        <CheckCircle2 className="w-8 h-8 opacity-20" />
                        <p className="text-sm">No pending tasks</p>
                    </div>
                ) : pending.slice(0, 5).map((task: Task) => (
                    <div key={task.id} className="p-3 bg-white/5 hover:bg-white/10 rounded-xl border border-white/5 group transition-colors cursor-pointer">
                        <div className="flex items-start gap-3">
                            <button className="w-4 h-4 mt-0.5 rounded border border-gray-500 hover:border-amber-400 flex items-center justify-center bg-black/20">
                                <CheckCircle2 className="w-3 h-3 text-transparent group-hover:text-amber-400" />
                            </button>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm text-gray-300 group-hover:text-white transition-colors truncate">{task.description || task.title}</p>
                                <p className="text-xs text-gray-500 mt-1">{task.due_date}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    )
}

function ActivityWidget() {
    const { attendance } = useEmployeeStore()

    interface ActivityLog {
        type: 'IN' | 'OUT'
        time: string
    }

    const logs: ActivityLog[] = []
    if (attendance?.check_in_time) logs.push({ type: 'IN', time: attendance.check_in_time })
    if (attendance?.check_out_time) logs.push({ type: 'OUT', time: attendance.check_out_time })

    return (
        <Card className="h-full flex flex-col p-5 border-white/10 bg-[#111420]/80">
            <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                    <Activity className="w-3.5 h-3.5" />
                    Recent Activity
                </span>
            </div>

            <div className="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar">
                {logs.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-gray-500 space-y-2">
                        <Activity className="w-8 h-8 opacity-20" />
                        <p className="text-sm">No activity today</p>
                    </div>
                ) : logs.map((log, i) => (
                    <div key={i} className="flex items-center gap-4">
                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${log.type === 'IN' ? 'bg-amber-400/10 text-amber-400 border border-amber-400/20' : 'bg-red-500/10 text-red-500 border border-red-500/20'}`}>
                            <Clock className="w-4 h-4" />
                        </div>
                        <div>
                            <p className="text-sm text-gray-300 font-medium">Clocked {log.type === 'IN' ? 'In' : 'Out'}</p>
                            <p className="text-xs text-gray-500">{new Date(log.time).toLocaleTimeString()}</p>
                        </div>
                    </div>
                ))}
            </div>
        </Card>
    )
}

function LeavesWidget() {
    const { leaveBalances } = useEmployeeStore()
    const totalBalance = leaveBalances.reduce((sum, lb) => sum + (lb.balance || 0), 0)
    const totalAllocated = leaveBalances.reduce((sum, lb) => sum + (lb.total_leaves || 0), 0)

    return (
        <Card className="h-full flex flex-col p-5 border-white/10 bg-[#111420]/80">
            <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                    <Calendar className="w-3.5 h-3.5" />
                    Leave Balance
                </span>
            </div>

            <div className="flex-1 flex items-center justify-center relative">
                <div className="absolute inset-0 bg-gradient-to-t from-emerald-500/5 to-transparent blur-xl" />
                <div className="text-center">
                    <h2 className="text-4xl font-bold text-white mb-1">{totalBalance}</h2>
                    <p className="text-sm text-gray-400">Days Available</p>
                    <div className="mt-4 px-3 py-1 bg-white/5 rounded-full text-xs text-gray-300 inline-flex items-center gap-2">
                        <span>Allocated: {totalAllocated}</span>
                    </div>
                </div>
            </div>
        </Card>
    )
}

function PayrollWidget() {
    return (
        <Card className="h-full flex flex-col p-5 border-white/10 bg-[#111420]/80">
            <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                    <FileText className="w-3.5 h-3.5" />
                    Latest Payslip
                </span>
            </div>
            <div className="flex-1 flex flex-col justify-center text-center">
                <div className="w-12 h-12 bg-white/5 rounded-full flex items-center justify-center mx-auto mb-3">
                    <FileText className="w-5 h-5 text-gray-400" />
                </div>
                <p className="text-gray-400 text-sm">No recent payslips found</p>
            </div>
        </Card>
    )
}

function SupportWidget() {
    return (
        <Card className="h-full flex flex-col p-5 border-white/10 bg-[#111420]/80">
            <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                    <MoreVertical className="w-3.5 h-3.5" />
                    Team Board
                </span>
            </div>
            <div className="flex-1 flex flex-col justify-center text-center">
                <p className="text-gray-400 text-sm">Review team performance stats here</p>
            </div>
        </Card>
    )
}

export default function Dashboard() {
    return (
        <div className="h-full w-full p-4 lg:p-6 overflow-hidden flex flex-col mx-auto max-w-screen-2xl">
            <div className="mb-6 shrink-0">
                <h1 className="text-2xl font-bold font-display text-white mb-1">Overview Dashboard</h1>
                <p className="text-sm text-gray-400">Adjust the widgets by dragging the borders between them.</p>
            </div>

            <div className="flex-1 relative rounded-xl overflow-hidden shadow-2xl">
                <PanelGroup direction="horizontal">

                    {/* Side 2 grid (Clock & Profile) */}
                    <Panel defaultSize={30} minSize={20}>
                        <PanelGroup direction="vertical">
                            <Panel defaultSize={50} minSize={30}>
                                <div className="p-2 h-full"><ClockWidget /></div>
                            </Panel>
                            <ResizeHandle direction="vertical" />
                            <Panel defaultSize={50} minSize={30}>
                                <div className="p-2 h-full"><ProfileWidget /></div>
                            </Panel>
                        </PanelGroup>
                    </Panel>

                    <ResizeHandle direction="horizontal" />

                    {/* Main Grid containing Top and Bottom sections */}
                    <Panel defaultSize={70} minSize={40}>
                        <PanelGroup direction="vertical">

                            {/* Top part of Main Grid (Tasks & Activity) */}
                            <Panel defaultSize={60} minSize={30}>
                                <PanelGroup direction="horizontal">
                                    <Panel defaultSize={60} minSize={30}>
                                        <div className="p-2 h-full"><TasksWidget /></div>
                                    </Panel>
                                    <ResizeHandle direction="horizontal" />
                                    <Panel defaultSize={40} minSize={30}>
                                        <div className="p-2 h-full"><ActivityWidget /></div>
                                    </Panel>
                                </PanelGroup>
                            </Panel>

                            <ResizeHandle direction="vertical" />

                            {/* Bottom 3 Grid */}
                            <Panel defaultSize={40} minSize={20}>
                                <PanelGroup direction="horizontal">
                                    <Panel defaultSize={33} minSize={20}>
                                        <div className="p-2 h-full"><LeavesWidget /></div>
                                    </Panel>
                                    <ResizeHandle direction="horizontal" />
                                    <Panel defaultSize={33} minSize={20}>
                                        <div className="p-2 h-full"><PayrollWidget /></div>
                                    </Panel>
                                    <ResizeHandle direction="horizontal" />
                                    <Panel defaultSize={34} minSize={20}>
                                        <div className="p-2 h-full"><SupportWidget /></div>
                                    </Panel>
                                </PanelGroup>
                            </Panel>

                        </PanelGroup>
                    </Panel>

                </PanelGroup>
            </div>
        </div>
    )
}