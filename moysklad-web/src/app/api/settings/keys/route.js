import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export async function GET() {
    console.log("--- Settings API Debug Start ---");
    try {
        const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
        console.log("Supabase URL in Env:", supabaseUrl);

        let dbKeys = {};
        try {
            console.log("Checking Supabase client...");
            const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_KEY;

            if (!supabaseUrl || !supabaseKey) {
                console.error("Supabase URL or Key missing in env!");
            } else {
                // Ensure we have a valid client. Initialize locally if the import is problematic.
                const { createClient } = require('@supabase/supabase-js');
                const client = createClient(supabaseUrl, supabaseKey);

                console.log("Attempting to fetch from client_configs table...");
                const { data, error } = await client.table('client_configs').select('*').limit(1).single();

                if (error) {
                    console.error("Supabase Error:", error.message);
                } else if (data) {
                    console.log("Data found in DB. Record ID:", data.id);
                    dbKeys = data;
                } else {
                    console.warn("No data returned from client_configs.");
                }
            }
        } catch (e) {
            console.error("Database access exception:", e.message);
        }

        const keys = {
            REST_API_KEY: dbKeys.rest_api_key || process.env.REST_API_KEY || 'Not Set',
            SUPABASE_URL: supabaseUrl || 'Not Set',
            KASPI_BASE_XML_URL: dbKeys.kaspi_xml_url || process.env.KASPI_BASE_XML_URL || 'Not Set',
            RETAIL_DIVISOR: dbKeys.retail_divisor || process.env.RETAIL_DIVISOR || '0.3',
            MIN_PRICE_DIVISOR: dbKeys.min_price_divisor || process.env.MIN_PRICE_DIVISOR || '0.45',
            OPENAI_API_KEY: (dbKeys.openai_key || process.env.OPENAI_API_KEY) ? `${(dbKeys.openai_key || process.env.OPENAI_API_KEY).substring(0, 8)}...` : 'Not Set',
            MOYSKLAD_LOGIN: dbKeys.moysklad_login || process.env.MOYSKLAD_LOGIN || 'Not Set',
            KASPI_API_TOKEN: (dbKeys.kaspi_token || process.env.KASPI_API_TOKEN) ? 'Connected ✅' : 'Not Set',
        };

        console.log("Final keys result mapping complete.");
        console.log("--- Settings API Debug End ---");
        return NextResponse.json(keys);
    } catch (error) {
        console.error("Critical Settings API Error:", error);
        return NextResponse.json({ error: 'Failed' }, { status: 500 });
    }
}
