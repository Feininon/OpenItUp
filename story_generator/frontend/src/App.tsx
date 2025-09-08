import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import './App.css';

function App() {
    const [code, setCode] = useState<string>(`def find_max(numbers):
    max_val = float('-inf')
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val`);
    const [story, setStory] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const handleGenerateStory = async () => {
        setIsLoading(true);
        setStory('');
        try {
            const response = await axios.post('http://127.0.0.1:8000/generate-story', {
                code: code,
                style: "a dramatic pirate adventure" // You can make this a dropdown!
            });
            setStory(response.data.story);
        } catch (error) {
            console.error("Error generating story:", error);
            setStory('Failed to generate story. Is the backend server running?');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>📜 StoryCode</h1>
                <p>Turn your code into a character-driven narrative.</p>
            </header>
            <main className="App-main">
                <div className="editor-container">
                    <h3>Your Code Snippet (Python)</h3>
                    <Editor
                        height="300px"
                        language="python"
                        theme="vs-dark"
                        value={code}
                        onChange={(value) => setCode(value || '')}
                        options={{ minimap: { enabled: false } }}
                    />
                    <button onClick={handleGenerateStory} disabled={isLoading}>
                        {isLoading ? 'Weaving a Tale...' : '✨ Generate Story'}
                    </button>
                </div>
                <div className="story-container">
                    <h3>The Generated Story</h3>
                    <div className="story-output">
                        {isLoading ? <div className="spinner"></div> : <p>{story}</p>}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;