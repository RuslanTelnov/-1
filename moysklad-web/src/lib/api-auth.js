import { NextResponse } from 'next/server';

/**
 * Validates the X-API-KEY header against the REST_API_KEY environment variable.
 * @param {Request} request 
 * @returns {null|Response} Returns a 401 response if invalid, null if valid.
 */
export function validateApiKey(request) {
    const apiKey = request.headers.get('x-api-key');
    const validKey = process.env.REST_API_KEY;

    if (!validKey) {
        console.error('REST_API_KEY is not set in environment variables');
        return NextResponse.json({ error: 'System configuration error' }, { status: 500 });
    }

    if (!apiKey || apiKey !== validKey) {
        return NextResponse.json({ error: 'Unauthorized: Invalid API Key' }, { status: 401 });
    }

    return null;
}
