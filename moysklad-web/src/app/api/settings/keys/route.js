import { NextResponse } from 'next/server';
import { getSettings } from '@/lib/settings-service';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        const settings = await getSettings();

        // Add cache status header if it's hit/miss (optional, since getSettings handles it internally but we can't easily see it here without modifying getSettings to return more info)
        // For simplicity, we just return the settings.

        return NextResponse.json(settings, {
            headers: {
                'Cache-Control': 'no-store, max-age=0, must-revalidate',
            }
        });
    } catch (error) {
        console.error('Settings API Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}

