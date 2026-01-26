import { NextResponse } from 'next/server';

export async function GET() {
    try {
        // Whitelist of public/semi-public keys to show in settings
        // We do NOT return the full process.env for security reasons.
        const keys = {
            REST_API_KEY: process.env.REST_API_KEY || 'Not Set',
            SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL || 'Not Set',
            KASPI_BASE_XML_URL: process.env.KASPI_BASE_XML_URL || 'Not Set',
            RETAIL_DIVISOR: process.env.RETAIL_DIVISOR || '0.3',
            MIN_PRICE_DIVISOR: process.env.MIN_PRICE_DIVISOR || '0.45',
            // Mask very sensitive ones even in settings, only showing prefix for verification
            OPENAI_API_KEY: process.env.OPENAI_API_KEY ? `${process.env.OPENAI_API_KEY.substring(0, 8)}...` : 'Not Set',
            GOOGLE_API_KEY: process.env.GOOGLE_API_KEY ? `${process.env.GOOGLE_API_KEY.substring(0, 8)}...` : 'Not Set',
        };

        return NextResponse.json(keys);
    } catch (error) {
        return NextResponse.json({ error: 'Failed to fetch settings' }, { status: 500 });
    }
}
