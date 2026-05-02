/**
 * AI IDE Assistant — VS Code Extension
 *
 * Captures all code before the cursor in a Java file, sends it to the local
 * FastAPI backend, and inserts the AI-predicted completion at the cursor.
 *
 * Tools used:
 *   • VS Code Extension API  — editor integration
 *   • TypeScript 5           — type-safe extension logic
 *   • Fetch API              — HTTP calls to FastAPI backend
 *
 * Author: Naram Prashanth Goud
 * GitHub: https://github.com/prashanth9968
 */

import * as vscode from 'vscode';

const BACKEND_URL = 'http://127.0.0.1:8000/complete';

export function activate(context: vscode.ExtensionContext) {
    console.log('AI IDE Assistant activated.');

    const disposable = vscode.commands.registerCommand(
        'ai-ide-assistant.analyzeJava',
        async () => {
            const editor = vscode.window.activeTextEditor;

            if (!editor) {
                vscode.window.showErrorMessage('AI IDE Assistant: No active editor found.');
                return;
            }

            if (editor.document.languageId !== 'java') {
                vscode.window.showWarningMessage(
                    'AI IDE Assistant: Only Java files are supported currently.'
                );
                return;
            }

            const position       = editor.selection.active;
            const codeBeforeCursor = editor.document.getText(
                new vscode.Range(new vscode.Position(0, 0), position)
            );

            if (!codeBeforeCursor.trim()) {
                vscode.window.showWarningMessage('AI IDE Assistant: No code found before cursor.');
                return;
            }

            await vscode.window.withProgress(
                {
                    location: vscode.ProgressLocation.Notification,
                    title: 'AI IDE Assistant: Fetching suggestion…',
                    cancellable: false,
                },
                async () => {
                    try {
                        const response = await fetch(BACKEND_URL, {
                            method : 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body   : JSON.stringify({ code: codeBeforeCursor }),
                        });

                        if (!response.ok) {
                            const err = await response.json() as { detail?: string };
                            vscode.window.showErrorMessage(
                                `AI IDE Assistant: Backend error — ${err.detail ?? response.statusText}`
                            );
                            return;
                        }

                        const data = await response.json() as { completion?: string };

                        if (data.completion) {
                            await editor.edit(eb => eb.insert(position, data.completion!));
                            vscode.window.showInformationMessage(
                                'AI IDE Assistant: Suggestion inserted ✅'
                            );
                        } else {
                            vscode.window.showWarningMessage(
                                'AI IDE Assistant: No suggestion returned from backend.'
                            );
                        }

                    } catch {
                        vscode.window.showErrorMessage(
                            'AI IDE Assistant: Cannot connect to backend. ' +
                            'Make sure the Python server is running on port 8000.'
                        );
                    }
                }
            );
        }
    );

    context.subscriptions.push(disposable);
}

export function deactivate() {
    console.log('AI IDE Assistant deactivated.');
}
