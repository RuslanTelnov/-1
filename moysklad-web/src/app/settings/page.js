'use client'
import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'

export default function Settings() {
    const [keys, setKeys] = useState(null)
    const [loading, setLoading] = useState(true)
    const [copied, setCopied] = useState(null)

    useEffect(() => {
        fetch('/api/settings/keys')
            .then(res => res.json())
            .then(data => {
                setKeys(data)
                setLoading(false)
            })
    }, [])

    const handleCopy = (key, value) => {
        navigator.clipboard.writeText(value)
        setCopied(key)
        setTimeout(() => setCopied(null), 2000)
    }

    return (
        <div style={{ minHeight: '100vh', background: 'var(--velveto-bg-primary)' }}>
            {/* Header */}
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

            <main className="container" style={{ paddingTop: '4rem', maxWidth: '1000px', margin: '0 auto' }}>
                <div style={{ marginBottom: '3rem' }}>
                    <Link href="/">
                        <div style={{ color: 'var(--velveto-accent-primary)', cursor: 'pointer', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            ← На главную
                        </div>
                    </Link>
                    <h2 style={{ fontSize: '2.5rem', fontWeight: '200', color: 'var(--velveto-text-primary)' }}>НАСТРОЙКИ</h2>
                </div>

                {loading ? (
                    <div style={{ color: 'var(--velveto-text-secondary)' }}>Загрузка...</div>
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
                                    gap: '0.5rem',
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
                                        {name}
                                    </span>
                                    <button
                                        onClick={() => handleCopy(name, value)}
                                        style={{
                                            background: 'rgba(255,255,255,0.05)',
                                            border: 'none',
                                            color: '#fff',
                                            padding: '4px 12px',
                                            borderRadius: '4px',
                                            fontSize: '0.7rem',
                                            cursor: 'pointer',
                                            transition: 'all 0.2s'
                                        }}
                                    >
                                        {copied === name ? '✓ Скопировано' : 'Копировать'}
                                    </button>
                                </div>
                                <div style={{
                                    fontSize: '1rem',
                                    color: 'var(--velveto-text-primary)',
                                    fontFamily: 'monospace',
                                    wordBreak: 'break-all',
                                    background: 'rgba(0,0,0,0.2)',
                                    padding: '0.5rem',
                                    borderRadius: '4px'
                                }}>
                                    {value}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    )
}
