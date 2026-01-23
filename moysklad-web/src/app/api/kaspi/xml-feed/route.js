import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import { XMLParser, XMLBuilder } from 'fast-xml-parser';

export const dynamic = 'force-dynamic';

export async function GET() {
    try {
        // 1. Fetch base XML from user's external link (Proxy mode)
        // If config is missing, default to the one we know or throw error
        const BASE_XML_URL = process.env.KASPI_BASE_XML_URL || 'https://mskaspi.fixhub.kz/xml/35fde8f355cd299f7a3e26cbe0e4f917.xml';

        const baseXmlResponse = await fetch(BASE_XML_URL, { cache: 'no-store' });
        if (!baseXmlResponse.ok) {
            throw new Error(`Failed to fetch base XML: ${baseXmlResponse.status}`);
        }
        const baseXmlText = await baseXmlResponse.text();

        // 2. Parse base XML
        const parser = new XMLParser({
            ignoreAttributes: false,
            attributeNamePrefix: "@_",
            parseAttributeValue: true
        });
        const jsonObj = parser.parse(baseXmlText);

        // Ensure structure exists
        if (!jsonObj.kaspi_catalog) jsonObj.kaspi_catalog = {};
        if (!jsonObj.kaspi_catalog.offers) jsonObj.kaspi_catalog.offers = { offer: [] };

        // Normalize offers to array
        let existingOffers = jsonObj.kaspi_catalog.offers.offer;
        if (!Array.isArray(existingOffers)) {
            existingOffers = existingOffers ? [existingOffers] : [];
        }

        // 3. Fetch new products from Supabase
        const { data: newProducts, error: dbError } = await supabase
            .from('wb_search_results')
            .select('*')
            .or('kaspi_created.eq.true,specs->>is_in_feed.eq.true');

        if (dbError) throw dbError;

        // 4. Merge new products into offers
        // Keep track of existing SKUs to avoid duplicates
        const existingSkus = new Set(existingOffers.map(o => String(o['@_sku'])));

        for (const product of newProducts) {
            const sku = `${product.id}-K`;

            // Skip if already in the base XML (to avoid double entries if user manually added them there)
            if (existingSkus.has(sku)) continue;

            const stock = product.specs?.stock || 0;
            const price = product.price_kzt || 0;
            const specs = product.specs || {};

            const newOffer = {
                "@_sku": sku,
                "model": product.name,
                "brand": product.brand || "Generic",
                "availabilities": {
                    "availability": {
                        "@_available": stock > 0 ? "yes" : "no",
                        "@_storeId": "PP1",
                        "@_stockCount": stock
                    }
                },
                "price": price
            };

            // Add Description
            const description = specs.description || product.description;
            if (description) {
                newOffer.description = description;
            }

            // Add Images (YML allows multiple picture tags)
            // Use specs.image_urls if available (array), else simple image_url
            let images = specs.image_urls;
            if (!images || !Array.isArray(images) || images.length === 0) {
                if (product.image_url) {
                    images = [product.image_url];
                } else {
                    images = [];
                }
            }
            if (images.length > 0) {
                newOffer.picture = images;
            }

            // Add Params (Attributes)
            const params = [];
            // NEW: Prefer strictly mapped Kaspi attributes if available
            if (specs.kaspi_attributes && typeof specs.kaspi_attributes === 'object') {
                // Handle dictionary format: { "Code": "Value" } or { "Code": ["Val1", "Val2"] }
                // (which is what Python saves)
                const attrs = Array.isArray(specs.kaspi_attributes) ? specs.kaspi_attributes : Object.entries(specs.kaspi_attributes).map(([code, value]) => ({ code, value }));

                for (const attr of attrs) {
                    // If it was already array of objects {code, value} (legacy/future proof), use it.
                    // If it came from Object.entries, attr is {code, value}

                    const values = Array.isArray(attr.value) ? attr.value : [attr.value];

                    for (const v of values) {
                        params.push({
                            "@_code": attr.code,
                            "@_name": attr.name || (attr.code ? attr.code.split('*').pop() : "Attribute"),
                            "#text": String(v)
                        });
                    }
                }
            } else {
                // FALLBACK: Old logic using raw specs keys
                const ignoredKeys = new Set([
                    'stock', 'is_closed', 'image_urls', 'is_in_feed', 'description',
                    'enriched', 'kaspi_created', 'kaspi_upload_status', 'kaspi_upload_id',
                    'kaspi_sku', 'wb_full_data', 'conveyor_log', 'ms_created', 'kaspi_attributes'
                ]);

                for (const [key, value] of Object.entries(specs)) {
                    if (ignoredKeys.has(key)) continue;
                    if (typeof value === 'object') continue; // Skip stored objects/arrays

                    // Sanitize key/value if needed, but XMLBuilder handles escaping usually
                    params.push({
                        "@_name": key,
                        "#text": String(value)
                    });
                }
            }

            if (params.length > 0) {
                newOffer.param = params;
            }

            existingOffers.push(newOffer);
        }

        // Update the JSON object with the merged list
        jsonObj.kaspi_catalog.offers.offer = existingOffers;

        // Update date to current
        jsonObj.kaspi_catalog['@_date'] = new Date().toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).replace(',', '');

        // 5. Re-bill XML
        const builder = new XMLBuilder({
            ignoreAttributes: false,
            attributeNamePrefix: "@_",
            format: true,
            indentBy: "  ",
            suppressEmptyNode: true,
            processEntities: true
        });

        const finalXml = `<?xml version="1.0" encoding="utf-8"?>\n${builder.build(jsonObj)}`;

        return new Response(finalXml, {
            headers: {
                'Content-Type': 'application/xml; charset=utf-8',
                'Cache-Control': 'no-store, max-age=0'
            }
        });

    } catch (error) {
        console.error('XML Feed Error:', error);
        return NextResponse.json({ error: error.message }, { status: 500 });
    }
}
