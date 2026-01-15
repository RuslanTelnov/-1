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
