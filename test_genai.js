const { GoogleGenerativeAI } = require("@google/generative-ai");
require('dotenv').config({ path: 'moysklad-web/.env.local' });

const apiKey = process.env.GOOGLE_API_KEY;
if (!apiKey) {
    console.error("No API KEY");
    process.exit(1);
}

const genAI = new GoogleGenerativeAI(apiKey);

async function testModel(modelName) {
    console.log(`Testing ${modelName}...`);
    try {
        const model = genAI.getGenerativeModel({ model: modelName });
        const result = await model.generateContent("Hello");
        const response = await result.response;
        console.log(`✅ ${modelName} SUCCESS:`, response.text());
        return true;
    } catch (e) {
        console.error(`❌ ${modelName} FAILED:`, e.message);
        return false;
    }
}

async function run() {
    // Try reliable models
    const models = ["gemini-1.5-flash", "gemini-pro", "gemini-1.5-pro", "gemini-2.0-flash-exp"];

    for (const m of models) {
        if (await testModel(m)) break;
    }
}

run();
