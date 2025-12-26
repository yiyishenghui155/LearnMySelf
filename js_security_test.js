function renderHtmlVulnerable(userInput) {
    const output = document.getElementById('user-content-area');
    if (output) {
        output.innerHTML = userInput;
    }
}

function renderHtmlSafe(userInput) {
    const output = document.getElementById('user-content-area');
    if (output) {
        output.textContent = userInput;
    }
}

function executeCodeVulnerable(userInput) {
    console.log("Executing vulnerable code...");
    eval(userInput);
}

function processDataSafe(userInput) {
    try {
        const data = JSON.parse(userInput);
        console.log("Safely processed data:", data);
    } catch (e) {
        console.error("Input is not valid JSON.");
    }
}

function checkRedosVulnerable(input) {
    const re = /^(a+)+$/;
    return re.test(input);
}

function checkRedosSafe(input) {
    const re = /^a+$/;
    return re.test(input);
}


function main() {
    const maliciousHtml = "<img src=x onerror=alert('XSS')>";
    const maliciousCode = "alert('Code Injection');";

    renderHtmlVulnerable(maliciousHtml);
    renderHtmlSafe(maliciousHtml);

    processDataSafe('{"status": "ok"}');

    checkRedosVulnerable("a".repeat(20) + "b");
    checkRedosSafe("a".repeat(20) + "b");
}

main();