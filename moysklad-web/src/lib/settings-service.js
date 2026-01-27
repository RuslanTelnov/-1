import { createClient } from '@supabase/supabase-js';

let cachedSettings = null;
let lastFetchTime = 0;
const CACHE_DURATION = 60000; // 1 minute

export async function getSettings(forceRefresh = false) {
    const now = Date.now();

    if (!forceRefresh && cachedSettings && (now - lastFetchTime < CACHE_DURATION)) {
        return cachedSettings;
    }

    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || process.env.SUPABASE_URL;
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || process.env.SUPABASE_KEY;

    if (!supabaseUrl || !supabaseKey) {
        throw new Error('Supabase configuration missing');
    }

    const supabase = createClient(supabaseUrl, supabaseKey);
    const { data, error } = await supabase.from('client_configs').select('*').limit(1).single();

    if (error && error.code !== 'PGRST116') {
        throw new Error(`Database error: ${error.message}`);
    }

    const dbKeys = data || {};

    const settings = {
        REST_API_KEY: dbKeys.rest_api_key || process.env.REST_API_KEY || 'Not Set',
        SUPABASE_URL: supabaseUrl || 'Not Set',
        KASPI_BASE_XML_URL: dbKeys.kaspi_xml_url || process.env.KASPI_BASE_XML_URL || 'Not Set',
        RETAIL_DIVISOR: dbKeys.retail_divisor || process.env.RETAIL_DIVISOR || '0.3',
        MIN_PRICE_DIVISOR: dbKeys.min_price_divisor || process.env.MIN_PRICE_DIVISOR || '0.45',
        OPENAI_API_KEY: dbKeys.openai_key || process.env.OPENAI_API_KEY || 'Not Set',
        MOYSKLAD_LOGIN: dbKeys.moysklad_login || process.env.MOYSKLAD_LOGIN || 'Not Set',
        MOYSKLAD_PASSWORD: dbKeys.moysklad_password || process.env.MOYSKLAD_PASSWORD || 'Not Set',
        KASPI_API_TOKEN: dbKeys.kaspi_token || process.env.KASPI_API_TOKEN || 'Not Set',
    };

    cachedSettings = settings;
    lastFetchTime = now;

    return settings;
}

export function clearSettingsCache() {
    cachedSettings = null;
    lastFetchTime = 0;
}
