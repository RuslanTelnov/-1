import { createClient } from '@supabase/supabase-js';
import { NextResponse } from 'next/server';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

export async function POST(request) {
    try {
        const body = await request.json();
        const { id, price_kzt, name, brand } = body;

        if (!id) {
            return NextResponse.json({ error: 'Product ID is required' }, { status: 400 });
        }

        const updateData = {
            updated_at: new Date().toISOString(),
        };

        if (price_kzt) updateData.price_kzt = price_kzt;
        if (name) updateData.name = name;
        if (brand) updateData.brand = brand;

        const { error } = await supabase
            .from('wb_search_results')
            .update(updateData)
            .eq('id', id);

        if (error) throw error;

        return NextResponse.json({ success: true });
    } catch (error) {
        console.error('Error saving price:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
