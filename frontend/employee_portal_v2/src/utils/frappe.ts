// Frappe API utilities
const API_BASE = '/api/method'

async function getCSRFToken(): Promise<string> {
    // Try to get from cookie
    const cookies = document.cookie.split(';')
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=')
        if (name === 'csrf_token' || name === 'sid') {
            return value || ''
        }
    }
    // Fallback: try to get from window object (Frappe sets this)
    if ((window as unknown as Record<string, string>).csrf_token) {
        return (window as unknown as Record<string, string>).csrf_token
    }
    return ''
}

export async function frappeCall<T = unknown>(
    method: string,
    args?: Record<string, unknown>
): Promise<T> {
    const csrfToken = await getCSRFToken()

    const response = await fetch(`${API_BASE}/${method}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Frappe-CSRF-Token': csrfToken,
        },
        credentials: 'include',
        body: JSON.stringify({ args }),
    })

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || 'API call failed')
    }

    const data = await response.json()
    return data.message as T
}

export async function frappeGetCall<T = unknown>(
    method: string,
    params?: Record<string, string | number | boolean>
): Promise<T> {
    const csrfToken = await getCSRFToken()
    const queryString = params
        ? '?' + new URLSearchParams(params as Record<string, string>).toString()
        : ''

    const response = await fetch(`${API_BASE}/${method}${queryString}`, {
        method: 'GET',
        headers: {
            'X-Frappe-CSRF-Token': csrfToken,
        },
        credentials: 'include',
    })

    if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || 'API call failed')
    }

    const data = await response.json()
    return data.message as T
}

export async function getCurrentUser(): Promise<{ full_name: string; email: string } | null> {
    try {
        const response = await frappeGetCall<string>('frappe.auth.get_logged_user')
        if (response) {
            const userInfo = await frappeGetCall<{ full_name: string; email: string }>('frappe.client.get_value', {
                doctype: 'User',
                filters: JSON.stringify({ name: response }),
                fieldname: 'full_name,email',
            })
            return userInfo?.full_name ? userInfo : { full_name: response, email: response }
        }
        return null
    } catch {
        return null
    }
}