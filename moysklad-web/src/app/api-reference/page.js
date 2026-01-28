'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';

const API_GROUPS = [
    {
        title: 'Product Management V1',
        description: 'High-level normalized API for dashboard and external integrations.',
        endpoints: [
            {
                method: 'GET',
                path: '/api/v1/products',
                description: 'Search and list products from the enriched database.',
                params: [
                    { name: 'brand', type: 'string', desc: 'Case-insensitive brand filter' },
                    { name: 'limit', type: 'number', desc: 'Results per page (max 100)' },
                    { name: 'offset', type: 'number', desc: 'Pagination offset' }
                ],
                response: '{"data": [], "pagination": {}}'
            },
            {
                method: 'GET',
                path: '/api/v1/products/[id]',
                description: 'Fetch complete metadata for a single product by article.',
                response: '{"id": "...", "name": "...", "specs": {}}'
            },
            {
                method: 'PATCH',
                path: '/api/v1/products/[id]',
                description: 'Update product properties (e.g. custom names or prices).',
                payload: '{"name": "New Name", "price_kzt": 5000}',
                response: '{"success": true}'
            }
        ]
    },
    {
        title: 'Automation & Logistics',
        description: 'Control the parsing conveyor and MoySklad operations.',
        endpoints: [
            {
                method: 'POST',
                path: '/api/conveyor/run',
                description: 'Trigger the product synchronization conveyor.',
                payload: '{"dry_run": false}',
                response: '{"status": "started", "job_id": "..."}'
            },
            {
                method: 'GET',
                path: '/api/conveyor/status',
                description: 'Telemetry for the background conveyor process.',
                response: '{"active": true, "processed": 45, "errors": 0}'
            },
            {
                method: 'POST',
                path: '/api/oprihodovanie',
                description: 'Create a Stock Supply record in MoySklad.',
                payload: '{"product_id": "...", "quantity": 10}',
                response: '{"ms_id": "...", "doc_number": "001"}'
            }
        ]
    },
    {
        title: 'Market Intelligence',
        description: 'AI-driven analysis and multi-marketplace arbitrage tools.',
        endpoints: [
            {
                method: 'GET',
                path: '/api/scout',
                description: 'Discover trending products on Wildberries.',
                params: [{ name: 'query', type: 'string', desc: 'Niche search term' }],
                response: '[{"id": "...", "relevance": 0.98}]'
            },
            {
                method: 'GET',
                path: '/api/arbitrage',
                description: 'Compare multi-marketplace pricing for profit opportunities.',
                response: '{"opportunities": [{"profit_margin": "15%"}]}'
            }
        ]
    },
    {
        title: 'Content & AI Labs',
        description: 'Generative tools for visual and textual optimization.',
        endpoints: [
            {
                method: 'POST',
                path: '/api/content/generate-text',
                description: 'SEO-optimized product descriptions using Gemini/OpenAI.',
                payload: '{"article": "...", "style": "aggressive"}',
                response: '{"description": "..."}'
            },
            {
                method: 'POST',
                path: '/api/content/generate-image',
                description: 'AI Background removal or visual enhancement.',
                payload: '{"image_url": "...", "upscale": true}',
                response: '{"url": "..."}'
            }
        ]
    }
];

export default function ApiReference() {
    const [activeTab, setActiveTab] = useState(API_GROUPS[0].title);
    const [searchQuery, setSearchQuery] = useState('');

    const filteredGroups = API_GROUPS.map(group => ({
        ...group,
        endpoints: group.endpoints.filter(e =>
            e.path.toLowerCase().includes(searchQuery.toLowerCase()) ||
            e.description.toLowerCase().includes(searchQuery.toLowerCase())
        )
    })).filter(group => group.endpoints.length > 0);

    return (
        <div style={{
            minHeight: '100vh',
            background: '#050505',
            color: '#fff',
            fontFamily: '"Outfit", "Inter", sans-serif',
            padding: '4rem 2rem'
        }}>
            {/* Ambient Background */}
            <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                height: '500px',
                background: 'radial-gradient(circle at 50% -20%, rgba(255, 179, 90, 0.15), transparent 70%)',
                pointerEvents: 'none',
                zIndex: 0
            }} />

            <div style={{ maxWidth: '1100px', margin: '0 auto', position: 'relative', zIndex: 1 }}>
                {/* Navigation Header */}
                <nav style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '4rem',
                    borderBottom: '1px solid rgba(255,255,255,0.05)',
                    paddingBottom: '2rem'
                }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <Link href="/" style={{ textDecoration: 'none' }}>
                            <h2 style={{
                                fontSize: '1.5rem',
                                fontWeight: '300',
                                letterSpacing: '0.2em',
                                color: '#fff',
                                margin: 0
                            }}>VELVETO <span style={{ color: '#ffb35a' }}>API</span></h2>
                        </Link>
                    </div>
                    <div style={{ display: 'flex', gap: '2rem' }}>
                        <Link href="/" style={{ color: 'rgba(255,255,255,0.5)', textDecoration: 'none', fontSize: '0.9rem' }}>Dashboard</Link>
                        <Link href="/settings" style={{ color: 'rgba(255,255,255,0.5)', textDecoration: 'none', fontSize: '0.9rem' }}>Settings</Link>
                    </div>
                </nav>

                {/* Hero Section */}
                <header style={{ marginBottom: '5rem', textAlign: 'center' }}>
                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        style={{
                            fontSize: '4.5rem',
                            fontWeight: '700',
                            letterSpacing: '-0.04em',
                            marginBottom: '1rem',
                            background: 'linear-gradient(135deg, #fff 0%, #ffb35a 100%)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent'
                        }}
                    >
                        Intelligence Infrastructure
                    </motion.h1>
                    <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.2 }}
                        style={{
                            fontSize: '1.25rem',
                            color: 'rgba(255,255,255,0.5)',
                            maxWidth: '700px',
                            margin: '0 auto',
                            lineHeight: 1.6
                        }}
                    >
                        Comprehensive API reference for multi-marketplace integration and automation control.
                    </motion.p>
                </header>

                {/* Search & Tabs Container */}
                <div style={{
                    background: 'rgba(255,255,255,0.02)',
                    backdropFilter: 'blur(20px)',
                    borderRadius: '24px',
                    border: '1px solid rgba(255,255,255,0.05)',
                    padding: '2rem',
                    marginBottom: '4rem'
                }}>
                    <div style={{ marginBottom: '2.5rem' }}>
                        <input
                            type="text"
                            placeholder="Find an endpoint (e.g. /products)..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            style={{
                                width: '100%',
                                background: 'rgba(0,0,0,0.3)',
                                border: '1px solid rgba(255,179,90,0.2)',
                                padding: '1.25rem 2rem',
                                borderRadius: '16px',
                                color: '#fff',
                                fontSize: '1.1rem',
                                outline: 'none',
                                transition: 'all 0.3s'
                            }}
                        />
                    </div>

                    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                        {API_GROUPS.map(group => (
                            <button
                                key={group.title}
                                onClick={() => setActiveTab(group.title)}
                                style={{
                                    padding: '0.75rem 1.5rem',
                                    borderRadius: '12px',
                                    border: '1px solid',
                                    borderColor: activeTab === group.title ? '#ffb35a' : 'rgba(255,255,255,0.1)',
                                    background: activeTab === group.title ? 'rgba(255,179,90,0.1)' : 'transparent',
                                    color: activeTab === group.title ? '#ffb35a' : 'rgba(255,255,255,0.4)',
                                    cursor: 'pointer',
                                    fontSize: '0.9rem',
                                    fontWeight: '600',
                                    transition: 'all 0.2s'
                                }}
                            >
                                {group.title}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Endpoints List */}
                <div style={{ display: 'grid', gap: '3rem' }}>
                    {filteredGroups.filter(g => activeTab === g.title || searchQuery).map((group, gIdx) => (
                        <motion.div
                            key={group.title}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ delay: gIdx * 0.1 }}
                        >
                            <div style={{ marginBottom: '2rem' }}>
                                <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#ffb35a', marginBottom: '0.5rem' }}>{group.title}</h2>
                                <p style={{ color: 'rgba(255,255,255,0.4)', fontSize: '1rem' }}>{group.description}</p>
                            </div>

                            <div style={{ display: 'grid', gap: '1.5rem' }}>
                                {group.endpoints.map((ep, eIdx) => (
                                    <EndpointCard key={ep.path} endpoint={ep} />
                                ))}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            <footer style={{ marginTop: '8rem', textAlign: 'center', color: 'rgba(255,255,255,0.2)', fontSize: '0.8rem' }}>
                &copy; 2026 VELVETO TECH INFRASTRUCTURE. ALL RIGHTS RESERVED.
            </footer>
        </div>
    );
}

function EndpointCard({ endpoint }) {
    const [isExpanded, setIsExpanded] = useState(false);

    const getBadgeColor = (method) => {
        switch (method) {
            case 'GET': return '#3b82f6';
            case 'POST': return '#10b981';
            case 'PATCH': return '#f59e0b';
            case 'DELETE': return '#ef4444';
            default: return '#71717a';
        }
    };

    return (
        <div
            onClick={() => setIsExpanded(!isExpanded)}
            style={{
                background: 'rgba(255,255,255,0.02)',
                borderRadius: '20px',
                border: '1px solid rgba(255,255,255,0.05)',
                overflow: 'hidden',
                cursor: 'pointer',
                transition: 'all 0.3s',
                ...(isExpanded ? { borderColor: 'rgba(255,179,90,0.3)', background: 'rgba(255,255,255,0.04)' } : {})
            }}
        >
            <div style={{ padding: '1.5rem 2rem', display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
                <span style={{
                    background: getBadgeColor(endpoint.method),
                    color: '#fff',
                    padding: '0.35rem 0.75rem',
                    borderRadius: '8px',
                    fontSize: '0.75rem',
                    fontWeight: '800'
                }}>{endpoint.method}</span>
                <code style={{ fontSize: '1.1rem', color: '#fff', fontWeight: '600', flex: 1 }}>{endpoint.path}</code>
                <span style={{ color: 'rgba(255,255,255,0.4)', fontSize: '0.9rem' }}>{endpoint.description}</span>
                <span style={{ color: '#ffb35a', transition: 'transform 0.3s', transform: isExpanded ? 'rotate(180deg)' : 'rotate(0deg)' }}>▼</span>
            </div>

            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        style={{ borderTop: '1px solid rgba(255,255,255,0.05)', padding: '2rem' }}
                    >
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '3rem' }}>
                            {endpoint.params && (
                                <div style={{ flex: 1 }}>
                                    <h4 style={{ color: '#ffb35a', fontSize: '0.9rem', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Parameters</h4>
                                    <div style={{ display: 'grid', gap: '1rem' }}>
                                        {endpoint.params.map(p => (
                                            <div key={p.name} style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                                                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                                    <span style={{ color: '#fff', fontWeight: '600' }}>{p.name}</span>
                                                    <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: '0.75rem' }}>({p.type})</span>
                                                </div>
                                                <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.85rem' }}>{p.desc}</span>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {endpoint.payload && (
                                <div style={{ flex: 1 }}>
                                    <h4 style={{ color: '#10b981', fontSize: '0.9rem', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Example Body</h4>
                                    <pre style={{
                                        background: '#0a0a0a',
                                        padding: '1.5rem',
                                        borderRadius: '12px',
                                        border: '1px solid rgba(16, 185, 129, 0.2)',
                                        color: '#10b981',
                                        fontSize: '0.85rem',
                                        margin: 0
                                    }}>{endpoint.payload}</pre>
                                </div>
                            )}

                            {endpoint.response && (
                                <div style={{ flex: 1 }}>
                                    <h4 style={{ color: '#3b82f6', fontSize: '0.9rem', marginBottom: '1rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Example Response</h4>
                                    <pre style={{
                                        background: '#0a0a0a',
                                        padding: '1.5rem',
                                        borderRadius: '12px',
                                        border: '1px solid rgba(59, 130, 246, 0.2)',
                                        color: '#3b82f6',
                                        fontSize: '0.85rem',
                                        margin: 0
                                    }}>{endpoint.response}</pre>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
