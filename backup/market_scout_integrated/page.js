'use client';

import { useState } from 'react';
import styles from './page.module.css';

export default function MarketScoutPage() {
    const [query, setQuery] = useState('');
    const [targetImage, setTargetImage] = useState('');
    const [targetPrice, setTargetPrice] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query) return;

        setLoading(true);
        setError(null);
        setResults([]);

        try {
            const response = await fetch('/api/scout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    msName: query, // Use the query as MS Name
                    title: query,  // Also send as title fallback
                    price: parseFloat(targetPrice) || 0,
                    imageUrl: targetImage,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Search failed');
            }

            setResults(data.results || []);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            {/* Header */}
            <header style={{
                padding: '1rem 2rem',
                position: 'sticky',
                top: 0,
                zIndex: 100,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                backdropFilter: 'blur(20px)',
                background: 'rgba(11, 14, 20, 0.8)',
                borderBottom: '1px solid var(--border-subtle)',
                marginBottom: '2rem'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <a href="/" style={{ textDecoration: 'none' }}>
                            <h1 style={{
                                fontSize: '1.5rem',
                                fontWeight: '900',
                                letterSpacing: '1px',
                                color: 'var(--text-primary)',
                                cursor: 'pointer',
                                margin: 0
                            }}>
                                VELVETO
                            </h1>
                        </a>
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem', letterSpacing: '0.1em', textTransform: 'uppercase' }}>CONTROL PANEL</span>
                    </div>

                    {/* Navigation Tabs */}
                    <nav style={{ display: 'flex', gap: '1rem' }}>
                        <a href="/" style={{
                            color: 'var(--text-muted)',
                            fontWeight: '500',
                            fontSize: '0.9rem',
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            textDecoration: 'none',
                            transition: 'all 0.2s'
                        }}>
                            Главная
                        </a>
                        <a href="/ms-products" style={{
                            color: 'var(--text-muted)',
                            fontWeight: '500',
                            fontSize: '0.9rem',
                            padding: '0.5rem 1rem',
                            borderRadius: '8px',
                            textDecoration: 'none',
                            transition: 'all 0.2s'
                        }}>
                            Номенклатуры
                        </a>
                        <a href="/market-scout" style={{
                            color: 'var(--text-primary)',
                            fontWeight: '600',
                            fontSize: '0.9rem',
                            padding: '0.5rem 1rem',
                            background: 'rgba(245, 158, 11, 0.1)',
                            borderRadius: '8px',
                            border: '1px solid rgba(245, 158, 11, 0.3)',
                            textDecoration: 'none'
                        }}>
                            Market Scout
                        </a>
                    </nav>
                </div>
                <div style={{ color: 'var(--text-primary)', fontSize: '0.875rem', fontWeight: '500' }}>
                    Admin
                </div>
            </header>

            <h1 className={styles.title}>Market Scout</h1>

            <form onSubmit={handleSearch} className={styles.searchForm}>
                <div className={styles.formGroup}>
                    <label className={styles.label}>MoySklad Product Name</label>
                    <input
                        type="text"
                        className={styles.input}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="e.g. Панама"
                        required
                    />
                    <small style={{ color: '#888', marginTop: '4px', display: 'block' }}>
                        System will search MoySklad for this name, get the photo, and then scout marketplaces.
                    </small>
                </div>

                <div className={styles.formGroup}>
                    <label className={styles.label}>Target Price (Optional)</label>
                    <input
                        type="number"
                        className={styles.input}
                        value={targetPrice}
                        onChange={(e) => setTargetPrice(e.target.value)}
                        placeholder="e.g. 5000"
                    />
                </div>

                <div className={styles.formGroup}>
                    <label className={styles.label}>Target Image URL (Optional)</label>
                    <input
                        type="text"
                        className={styles.input}
                        value={targetImage}
                        onChange={(e) => setTargetImage(e.target.value)}
                        placeholder="http://..."
                    />
                </div>

                <button type="submit" className={styles.button} disabled={loading}>
                    {loading ? 'Scouting...' : 'Search'}
                </button>
            </form>

            {error && <div className={styles.error}>{error}</div>}

            {loading && <div className={styles.loading}>Searching Marketplaces... This may take 20-30 seconds.</div>}

            <div className={styles.resultsGrid}>
                {results.map((item, index) => (
                    <div key={index} className={styles.card}>
                        <div className={styles.imageContainer}>
                            {item.image_url ? (
                                <img src={item.image_url} alt={item.title} className={styles.productImage} />
                            ) : (
                                <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#555' }}>No Image</div>
                            )}
                        </div>
                        <div className={styles.cardContent}>
                            <div className={styles.productTitle} title={item.title}>{item.title}</div>

                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <div className={styles.price}>
                                    {item.price} ₽
                                    {item.is_best_price && <span style={{ fontSize: '0.8rem', background: '#4caf50', color: 'white', padding: '2px 6px', borderRadius: '4px', marginLeft: '8px' }}>Best Price</span>}
                                </div>
                                <div style={{ fontSize: '0.8rem', fontWeight: 'bold', color: item.source === 'ozon' ? '#005bff' : '#cb11ab' }}>
                                    {item.source === 'ozon' ? 'OZON' : 'WB'}
                                </div>
                            </div>

                            <div className={styles.score}>
                                <span className={item.match_score > 0.8 ? styles.highScore : ''}>
                                    Match: {(item.match_score * 100).toFixed(0)}%
                                </span>
                                <a href={item.url} target="_blank" rel="noopener noreferrer" className={styles.link}>View</a>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {!loading && results.length === 0 && query && !error && (
                <div className={styles.loading}>No results found.</div>
            )}
        </div>
    );
}
