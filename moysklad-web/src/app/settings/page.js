'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'

export default function Settings() {
    const [keys, setKeys] = useState(null)
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [message, setMessage] = useState({ type: '', text: '' })

    useEffect(() => {
        fetchKeys()
    }, [])

    const fetchKeys = async () => {
        setLoading(true)
        setMessage({ type: '', text: '' })
        try {
            const res = await fetch('/api/settings/keys')
            const data = await res.json()

            if (res.ok) {
                setKeys(data)
            } else {
                console.error('API error:', data.error)
                setMessage({ type: 'error', text: data.error || 'Failed to load settings from server. Check logs.' })
                setKeys(null)
            }
        } catch (error) {
            console.error('Fetch error:', error)
            setMessage({ type: 'error', text: 'Network error or server is down. Could not fetch settings.' })
        }
        setLoading(false)
    }

    const handleChange = (name, value) => {
        setKeys(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleSave = async () => {
        setSaving(true)
        setMessage({ type: '', text: '' })
        try {
            const res = await fetch('/api/settings/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(keys)
            })
            const result = await res.json()
            if (result.success) {
                setMessage({ type: 'success', text: 'Settings saved successfully!' })
                setTimeout(() => setMessage({ type: '', text: '' }), 3000)
                fetchKeys() // Refresh to get masked values back
            } else {
                setMessage({ type: 'error', text: result.error || 'Failed to save settings' })
            }
        } catch (error) {
            setMessage({ type: 'error', text: 'Error saving settings' })
        }
        setSaving(false)
    }

    return (
        <div style={{ minHeight: '100vh', background: 'var(--velveto-bg-primary)' }}>
            <header style={{
                padding: '1.5rem 3rem',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backdropFilter: 'blur(20px)',
                background: 'rgba(5, 8, 20, 0.8)',
                borderBottom: '1px solid rgba(255, 255, 255, 0.05)'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    <Link href="/">
                        <h1 style={{
                            fontSize: '1.5rem',
                            fontWeight: '300',
                            letterSpacing: '0.18em',
                            color: 'var(--velveto-text-primary)',
                            textTransform: 'uppercase',
                            cursor: 'pointer'
                        }}>
                            VELVETO
                        </h1>
                    </Link>
                </div>
                <div style={{ color: 'var(--velveto-text-secondary)', fontSize: '0.875rem', textTransform: 'uppercase' }}>
                    Settings & API Keys
                </div>
            </header>

            <main className="container" style={{ paddingTop: '4rem', maxWidth: '1000px', margin: '0 auto', paddingBottom: '4rem' }}>
                <div style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                    <div>
                        <Link href="/">
                            <div style={{ color: 'var(--velveto-accent-primary)', cursor: 'pointer', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                ← На главную
                            </div>
                        </Link>
                        <h2 style={{ fontSize: '2.5rem', fontWeight: '200', color: 'var(--velveto-text-primary)' }}>НАСТРОЙКИ</h2>
                    </div>

                    <button
                        onClick={handleSave}
                        disabled={saving || loading}
                        style={{
                            background: 'var(--velveto-accent-primary)',
                            color: '#000',
                            border: 'none',
                            padding: '0.8rem 2rem',
                            borderRadius: '4px',
                            fontWeight: '600',
                            cursor: (saving || loading) ? 'not-allowed' : 'pointer',
                            opacity: (saving || loading) ? 0.7 : 1,
                            transition: 'all 0.2s',
                            textTransform: 'uppercase',
                            letterSpacing: '0.1em'
                        }}
                    >
                        {saving ? 'Сохранение...' : 'Сохранить изменения'}
                    </button>
                </div>

                {message.text && (
                    <div style={{
                        padding: '1rem',
                        marginBottom: '2rem',
                        borderRadius: '4px',
                        background: message.type === 'success' ? 'rgba(76, 175, 80, 0.1)' : 'rgba(244, 67, 54, 0.1)',
                        border: `1px solid ${message.type === 'success' ? '#4CAF50' : '#F44336'}`,
                        color: message.type === 'success' ? '#4CAF50' : '#F44336',
                        textAlign: 'center'
                    }}>
                        {message.text}
                    </div>
                )}

                {loading ? (
                    <div style={{ color: 'var(--velveto-text-secondary)' }}>Загрузка...</div>
                ) : !keys ? (
                    <div style={{
                        padding: '3rem',
                        textAlign: 'center',
                        background: 'rgba(255,255,255,0.02)',
                        border: '1px dashed rgba(255,255,255,0.1)',
                        borderRadius: '8px'
                    }}>
                        <p style={{ color: 'var(--velveto-text-secondary)', marginBottom: '1.5rem' }}>
                            Не удалось загрузить настройки. Пожалуйста, проверьте подключение к базе данных.
                        </p>
                        <button
                            onClick={fetchKeys}
                            style={{
                                background: 'transparent',
                                border: '1px solid var(--velveto-accent-primary)',
                                color: 'var(--velveto-accent-primary)',
                                padding: '0.5rem 1.5rem',
                                borderRadius: '4px',
                                cursor: 'pointer'
                            }}
                        >
                            Повторить попытку
                        </button>
                    </div>
                ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        {Object.entries(keys).map(([name, value]) => (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                key={name}
                                className="velveto-card"
                                style={{
                                    padding: '1.5rem 2rem',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: '0.8rem',
                                    border: '1px solid rgba(255,255,255,0.03)'
                                }}
                            >
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <span style={{
                                        color: 'var(--velveto-accent-primary)',
                                        fontSize: '0.7rem',
                                        textTransform: 'uppercase',
                                        letterSpacing: '0.1em'
                                    }}>
                                        {name.replace(/_/g, ' ')}
                                    </span>
                                </div>
                                <div style={{ display: 'flex', gap: '0.8rem', alignItems: 'center' }}>
                                    <input
                                        type={name.includes('PASSWORD') || name.includes('TOKEN') || name.includes('KEY') ? "text" : "text"}
                                        value={value === 'Not Set' ? '' : value}
                                        placeholder={value === 'Not Set' ? 'Введите значение...' : ''}
                                        onChange={(e) => handleChange(name, e.target.value)}
                                        disabled={name === 'SUPABASE_URL'}
                                        style={{
                                            fontSize: '1rem',
                                            color: 'var(--velveto-text-primary)',
                                            fontFamily: 'monospace',
                                            background: 'rgba(0,0,0,0.3)',
                                            border: '1px solid rgba(255,255,255,0.1)',
                                            padding: '0.8rem',
                                            borderRadius: '4px',
                                            flex: 1,
                                            outline: 'none',
                                            transition: 'border-color 0.2s'
                                        }}
                                        onFocus={(e) => e.target.style.borderColor = 'var(--velveto-accent-primary)'}
                                        onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.1)'}
                                    />
                                    {value && value !== 'Not Set' && (
                                        <button
                                            onClick={() => {
                                                navigator.clipboard.writeText(value);
                                                // Minimal feedback
                                                const btn = document.getElementById(`copy-${name}`);
                                                if (btn) {
                                                    const oldText = btn.innerText;
                                                    btn.innerText = '✓';
                                                    btn.style.color = '#4CAF50';
                                                    setTimeout(() => {
                                                        btn.innerText = oldText;
                                                        btn.style.color = 'var(--velveto-text-secondary)';
                                                    }, 2000);
                                                }
                                            }}
                                            id={`copy-${name}`}
                                            title="Copy to clipboard"
                                            style={{
                                                background: 'rgba(255,255,255,0.05)',
                                                border: '1px solid rgba(255,255,255,0.1)',
                                                color: 'var(--velveto-text-secondary)',
                                                padding: '0.8rem 1rem',
                                                borderRadius: '4px',
                                                cursor: 'pointer',
                                                fontSize: '0.8rem',
                                                transition: 'all 0.2s'
                                            }}
                                            onMouseOver={(e) => e.target.style.background = 'rgba(255,255,255,0.1)'}
                                            onMouseOut={(e) => e.target.style.background = 'rgba(255,255,255,0.05)'}
                                        >
                                            COPY
                                        </button>
                                    )}
                                </div>
                                {name === 'SUPABASE_URL' && (
                                    <span style={{ fontSize: '0.6rem', color: 'var(--velveto-text-secondary)' }}>
                                        Системный параметр (только для чтения)
                                    </span>
                                )}
                            </motion.div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    )
}
