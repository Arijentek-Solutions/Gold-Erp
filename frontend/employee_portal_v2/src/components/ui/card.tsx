import React from 'react'
import { cn } from '@/lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    children: React.ReactNode
    className?: string
}

export function Card({ children, className, ...props }: CardProps) {
    return (
        <div
            className={cn(
                'rounded-xl border border-white/[0.06] bg-card/40 backdrop-blur-xl text-card-foreground shadow-sm transition-all duration-300',
                'hover:border-white/[0.1] hover:bg-card/60',
                className
            )}
            {...props}
        >
            {children}
        </div>
    )
}

export function CardHeader({ children, className, ...props }: CardProps) {
    return (
        <div className={cn('flex flex-col space-y-1.5 p-4', className)} {...props}>
            {children}
        </div>
    )
}

export function CardTitle({ children, className, ...props }: CardProps) {
    return (
        <h3 className={cn('font-semibold leading-none tracking-tight text-sm uppercase text-muted-foreground', className)} {...props}>
            {children}
        </h3>
    )
}

export function CardContent({ children, className, ...props }: CardProps) {
    return (
        <div className={cn('p-4 pt-0', className)} {...props}>
            {children}
        </div>
    )
}

export function CardFooter({ children, className, ...props }: CardProps) {
    return (
        <div className={cn('flex items-center p-4 pt-0', className)} {...props}>
            {children}
        </div>
    )
}