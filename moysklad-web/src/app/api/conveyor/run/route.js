import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

let conveyorProcess = null;

export async function POST() {
    if (conveyorProcess) {
        return NextResponse.json({ message: 'Conveyor is already running', status: 'running' });
    }

    try {
        const scriptPath = path.join(process.cwd(), 'automation', 'moysklad', 'process_conveyor.py');
        const pythonCommand = 'python3';

        console.log(`Starting conveyor: ${pythonCommand} ${scriptPath}`);

        conveyorProcess = spawn(pythonCommand, [scriptPath], {
            cwd: path.dirname(scriptPath),
            detached: true,
            stdio: 'ignore' // or 'pipe' if we want to capture logs here, but script writes to file
        });

        conveyorProcess.unref();

        // Reset variable on exit (though detached process might outlive this variable if node restarts)
        conveyorProcess.on('exit', () => {
            conveyorProcess = null;
        });

        return NextResponse.json({ message: 'Conveyor started', status: 'running' });
    } catch (error) {
        console.error('Failed to start conveyor:', error);
        return NextResponse.json({ error: 'Failed to start conveyor' }, { status: 500 });
    }
}

export async function DELETE() {
    if (conveyorProcess) {
        conveyorProcess.kill();
        conveyorProcess = null;
        return NextResponse.json({ message: 'Conveyor stopped' });
    }
    return NextResponse.json({ message: 'Conveyor was not running' });
}
