import { NextResponse } from 'next/server';
import { execFile } from 'child_process';
import path from 'path';

export async function POST(request) {
    try {
        const body = await request.json();
        const { query, mode, page } = body;

        if (!query && mode !== 'top') {
            return NextResponse.json({ error: 'Query is required' }, { status: 400 });
        }

        const projectRoot = path.resolve(process.cwd(), '..');
        // Use the same venv as moysklad-automation
        // Use dynamic path to avoid Turbopack build-time validation of symlinks
        const venvPath = ['.venv', 'bin', 'python'].join(path.sep);
        const pythonPath = path.join(projectRoot, 'moysklad-automation', venvPath);
        const scriptPath = path.join(projectRoot, 'moysklad-automation', 'parse_wb_top.py');

        console.log('Executing WB Top Parser...');
        console.log('Query:', query, 'Mode:', mode, 'Page:', page);

        const args = [scriptPath];
        if (mode === 'top') {
            args.push('--mode', 'top');
        } else {
            args.push(query);
        }
        args.push('--limit', '40'); // Changed default limit to 40
        if (page) {
            args.push('--page', String(page));
        }

        return new Promise((resolve) => {
            execFile(pythonPath, args, { cwd: projectRoot }, (error, stdout, stderr) => {
                if (error) {
                    console.error('Error executing script:', error);
                    console.error('Stderr:', stderr);
                    resolve(NextResponse.json({ error: 'Failed to execute parser', details: stderr }, { status: 500 }));
                    return;
                }

                console.log('Parser output:', stdout);
                resolve(NextResponse.json({ success: true, message: 'Parser finished successfully' }));
            });
        });

    } catch (error) {
        console.error('API Error:', error);
        return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
    }
}
