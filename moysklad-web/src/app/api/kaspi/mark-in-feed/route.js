import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';

export async function POST(request) {
    try {
        const body = await request.json();
        const { productId } = body;

        if (!productId) {
            return NextResponse.json({ error: 'Product ID is required' }, { status: 400 });
        }

        // Update specs to include in_feed flag
        const { data: current, error: getError } = await supabase
            .from('wb_search_results')
            .select('specs')
            .eq('id', productId)
            .single();

        if (getError) throw getError;

        const specs = current.specs || {};
        specs.is_in_feed = true;

        const { error } = await supabase
            .from('wb_search_results')
            .update({
                specs,
                conveyor_status: 'in_feed'
            })
            .eq('id', productId);

        if (error) throw error;

        return NextResponse.json({ success: true, message: 'Added to XML feed bridge' });
    } catch (error) {
        console.error('Mark In Feed Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
