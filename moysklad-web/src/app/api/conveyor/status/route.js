import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';

export async function GET() {
    try {
        const logPath = path.resolve(process.cwd(), '../moysklad-automation/conveyor.log');
        let logs = 'No logs yet.';

        if (fs.existsSync(logPath)) {
            const content = fs.readFileSync(logPath, 'utf-8');
            // Return last 50 lines
            logs = content.split('\n').slice(-50).join('\n');
        }

        // Check if python process is running
        // This is a naive check. Ideally we track the PID we started.
        // Or we check `ps aux | grep process_conveyor.py`
        return new Promise((resolve) => {
            exec('pgrep -f "process_conveyor.py"', (err, stdout) => {
                const isRunning = !!stdout && stdout.trim().length > 0;
                resolve(NextResponse.json({
                    running: isRunning,
                    logs: logs
                }));
            });
        });

    } catch (error) {
        return NextResponse.json({ error: 'Failed to read status' }, { status: 500 });
    }
}
