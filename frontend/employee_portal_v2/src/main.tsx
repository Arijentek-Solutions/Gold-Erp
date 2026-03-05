import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// Add error handling
class ErrorBoundary extends React.Component<
    { children: React.ReactNode },
    { hasError: boolean; error: Error | null }
> {
    constructor(props: { children: React.ReactNode }) {
        super(props)
        this.state = { hasError: false, error: null }
    }

    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error }
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        console.error('App Error:', error, errorInfo)
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{
                    padding: '20px',
                    color: 'white',
                    background: '#0a0c1a',
                    minHeight: '100vh',
                    fontFamily: 'system-ui'
                }}>
                    <h1 style={{ color: '#ef4444' }}>Something went wrong</h1>
                    <pre style={{
                        background: '#111420',
                        padding: '10px',
                        borderRadius: '8px',
                        overflow: 'auto'
                    }}>
                        {this.state.error?.toString()}
                    </pre>
                </div>
            )
        }
        return this.props.children
    }
}

const root = document.getElementById('root')
if (!root) {
    console.error('Root element not found!')
} else {
    ReactDOM.createRoot(root).render(
        <React.StrictMode>
            <ErrorBoundary>
                <App />
            </ErrorBoundary>
        </React.StrictMode>,
    )
}